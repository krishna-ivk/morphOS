from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .agents import coding_agent
from .io import write_json
from .models import AgentInvocation, CodingTaskReceipt


class AgentBackend:
    def execute(self, invocation: AgentInvocation) -> dict[str, object]:
        raise NotImplementedError


class AgentRegistry:
    def __init__(self) -> None:
        self.backends: dict[str, AgentBackend] = {}

    def register(self, agent: str, backend: AgentBackend) -> None:
        self.backends[agent] = backend

    def get(self, agent: str) -> AgentBackend | None:
        return self.backends.get(agent)


class ModelWorkerBackend(AgentBackend):
    def __init__(self, mode_override: str | None = None):
        self.mode_override = mode_override

    def execute(self, invocation: AgentInvocation) -> dict[str, object]:
        mode = self.mode_override or os.getenv(
            f"SKYFORCE_{invocation.agent.upper()}_BACKEND", "codex"
        )
        if mode not in {"codex", "opencode"}:
            return self._fallback(invocation, reason=f"unsupported backend: {mode}")
        binary = shutil.which(mode)
        if not binary:
            return self._fallback(invocation, reason=f"missing backend binary: {mode}")

        response_path = invocation.run_dir / "artifacts" / f"{invocation.payload.get('id', invocation.agent)}_model_output.json"
        response_path.parent.mkdir(parents=True, exist_ok=True)
        schema = {
            "type": "object",
            "required": ["task_id", "status", "files_written", "tests_written", "patch_path"],
        }
        command = [
            binary,
            "exec",
            "--output-schema",
            json.dumps(schema),
            "--output-last-message",
            str(response_path),
        ]
        if not (Path(invocation.repo_root) / ".git").exists():
            command.append("--skip-git-repo-check")
        command.append("-")
        prompt = self._build_prompt(invocation)
        completed = subprocess.run(
            command,
            cwd=invocation.repo_root,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
        if completed.returncode != 0 or not response_path.exists():
            return self._fallback(
                invocation,
                reason=completed.stderr.strip() or f"{mode} returned {completed.returncode}",
            )

        raw = response_path.read_text(encoding="utf-8").strip()
        parsed = self._parse_json(raw)
        if not parsed:
            return self._fallback(invocation, reason="model output was not valid JSON")
        parsed.setdefault("backend", mode)
        if parsed.get("task_id") != invocation.payload.get("id"):
            return self._fallback(invocation, reason="model output task_id did not match invocation")
        try:
            validated = CodingTaskReceipt.model_validate(parsed)
        except Exception as exc:
            return self._fallback(invocation, reason=f"model output failed schema validation: {exc}")
        return validated.model_dump(mode="json")

    def _build_prompt(self, invocation: AgentInvocation) -> str:
        return json.dumps(
            {
                "agent": invocation.agent,
                "task": invocation.payload,
                "context": {
                    "repo_root": str(invocation.repo_root),
                    "run_dir": str(invocation.run_dir),
                    "retrieval": invocation.context.get("retrieval"),
                },
            },
            indent=2,
        )

    def _parse_json(self, raw: str) -> dict[str, Any] | None:
        fenced = re.search(r"```json\s*(\{.*\})\s*```", raw, re.DOTALL)
        if fenced:
            raw = fenced.group(1)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def _fallback(self, invocation: AgentInvocation, reason: str) -> dict[str, object]:
        error_path = invocation.run_dir / "artifacts" / f"{invocation.payload.get('id', invocation.agent)}_model_worker_error.json"
        write_json(
            error_path,
            {
                "agent": invocation.agent,
                "task_id": invocation.payload.get("id"),
                "reason": reason,
            },
        )
        result = coding_agent(
            Path(invocation.repo_root),
            Path(invocation.run_dir),
            invocation.payload,
            workspace_path=invocation.context.get("workspace_path"),
            retrieval=invocation.context.get("retrieval"),
        )
        result["backend"] = "local_fallback"
        result["model_worker_error_path"] = str(error_path)
        return result


def build_default_agent_registry() -> AgentRegistry:
    registry = AgentRegistry()
    configured = os.getenv("SKYFORCE_CODING_AGENT_BACKEND")
    if configured:
        registry.register("coding_agent", ModelWorkerBackend())
    return registry
