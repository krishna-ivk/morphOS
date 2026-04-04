"""Native program step execution with timeout, contract validation, and policy integration."""

from __future__ import annotations

import json
import subprocess
import signal
import shlex
import time
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from dataclasses import dataclass


@dataclass
class ProgramExecutionResult:
    step_id: str
    command: str
    returncode: int
    stdout: str
    stderr: str
    duration_ms: float
    timed_out: bool
    policy_blocked: bool
    policy_reason: str | None
    contract_valid: bool
    contract_errors: list[str]
    output_files: list[str]
    started_at: str
    completed_at: str


class ProgramStepExecutor:
    """Executes program steps with timeout, policy checks, and contract validation."""

    def __init__(self, repo_root: Path, policy_engine=None):
        self.repo_root = Path(repo_root)
        self.policy_engine = policy_engine

    def execute(
        self,
        run_id: str,
        step_id: str,
        command: str,
        context: dict[str, Any],
        timeout: int = 300,
        workspace_path: str | None = None,
        allowed_commands: list[str] | None = None,
        blocked_patterns: list[str] | None = None,
    ) -> ProgramExecutionResult:
        expanded_command = self._expand_command(command, context)
        started_at = datetime.now(timezone.utc).isoformat()

        policy_blocked, policy_reason = self._check_policy(
            run_id, step_id, expanded_command, context
        )

        if policy_blocked:
            return ProgramExecutionResult(
                step_id=step_id,
                command=expanded_command,
                returncode=-1,
                stdout="",
                stderr="",
                duration_ms=0,
                timed_out=False,
                policy_blocked=True,
                policy_reason=policy_reason,
                contract_valid=False,
                contract_errors=["Policy blocked execution"],
                output_files=[],
                started_at=started_at,
                completed_at=datetime.now(timezone.utc).isoformat(),
            )

        command_blocked, command_reason = self._check_command_patterns(
            expanded_command, allowed_commands, blocked_patterns
        )
        if command_blocked:
            return ProgramExecutionResult(
                step_id=step_id,
                command=expanded_command,
                returncode=-1,
                stdout="",
                stderr="",
                duration_ms=0,
                timed_out=False,
                policy_blocked=True,
                policy_reason=command_reason,
                contract_valid=False,
                contract_errors=[f"Command pattern blocked: {command_reason}"],
                output_files=[],
                started_at=started_at,
                completed_at=datetime.now(timezone.utc).isoformat(),
            )

        cwd = workspace_path or str(self.repo_root)
        start_time = time.monotonic()
        timed_out = False

        try:
            process = subprocess.Popen(
                expanded_command,
                cwd=cwd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=lambda: signal.signal(signal.SIGTERM, signal.SIG_DFL),
            )

            try:
                stdout, stderr = process.communicate(timeout=timeout)
                returncode = process.returncode
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                returncode = -1
                timed_out = True

        except Exception as exc:
            stdout = ""
            stderr = str(exc)
            returncode = -1

        duration_ms = (time.monotonic() - start_time) * 1000
        completed_at = datetime.now(timezone.utc).isoformat()

        output_files = self._detect_output_files(cwd, started_at)
        contract_valid, contract_errors = self._validate_outputs(
            run_id, step_id, returncode, stdout, stderr, output_files
        )

        return ProgramExecutionResult(
            step_id=step_id,
            command=expanded_command,
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
            duration_ms=duration_ms,
            timed_out=timed_out,
            policy_blocked=False,
            policy_reason=None,
            contract_valid=contract_valid,
            contract_errors=contract_errors,
            output_files=output_files,
            started_at=started_at,
            completed_at=completed_at,
        )

    def _check_policy(
        self, run_id: str, step_id: str, command: str, context: dict[str, Any]
    ) -> tuple[bool, str | None]:
        if not self.policy_engine:
            return False, None

        try:
            decision = self.policy_engine.check_command(command, context)
            if not decision.allowed:
                return True, decision.reason
        except Exception:
            pass

        return False, None

    def _check_command_patterns(
        self,
        command: str,
        allowed_commands: list[str] | None,
        blocked_patterns: list[str] | None,
    ) -> tuple[bool, str | None]:
        default_blocked = [
            r"\brm\s+-rf\s+/",
            r"\bmkfs\b",
            r"\bdd\s+if=",
            r"\bchmod\s+[0-7]{3,4}\s+/",
            r"\bcurl.*\|\s*(bash|sh)\b",
            r"\bwget.*\|\s*(bash|sh)\b",
            r"\bnc\s+-",
            r"\bnetcat\b",
        ]

        patterns = blocked_patterns or default_blocked
        for pattern in patterns:
            if re.search(pattern, command):
                return True, f"Command matches blocked pattern: {pattern}"

        if allowed_commands:
            for allowed in allowed_commands:
                if re.search(allowed, command):
                    return False, None
            return True, f"Command not in allowed list"

        return False, None

    def _detect_output_files(self, cwd: str, since: str) -> list[str]:
        try:
            since_time = datetime.fromisoformat(since.replace("Z", "+00:00"))
            cwd_path = Path(cwd)
            files = []
            for path in cwd_path.rglob("*"):
                if path.is_file() and ".git" not in path.parts:
                    try:
                        mtime = datetime.fromtimestamp(
                            path.stat().st_mtime, tz=timezone.utc
                        )
                        if mtime >= since_time:
                            files.append(str(path.relative_to(cwd_path)))
                    except (OSError, ValueError):
                        pass
            return files[:100]
        except (OSError, PermissionError):
            return []

    def _validate_outputs(
        self,
        run_id: str,
        step_id: str,
        returncode: int,
        stdout: str,
        stderr: str,
        output_files: list[str],
    ) -> tuple[bool, list[str]]:
        errors = []

        if returncode != 0:
            errors.append(f"Non-zero exit code: {returncode}")

        validation_dir = self.repo_root / "artifacts" / "runs" / run_id / "validation"
        contract_path = validation_dir / f"{step_id}_program_contract.json"

        if contract_path.exists():
            try:
                contract = json.loads(contract_path.read_text(encoding="utf-8"))
                if "expected_files" in contract:
                    for expected in contract["expected_files"]:
                        if expected not in output_files:
                            errors.append(f"Expected file not found: {expected}")

                if "expected_output_pattern" in contract:
                    pattern = contract["expected_output_pattern"]
                    if not re.search(pattern, stdout):
                        errors.append(
                            f"Output does not match expected pattern: {pattern}"
                        )

                if "max_stderr_length" in contract:
                    if len(stderr) > contract["max_stderr_length"]:
                        errors.append(
                            f"Stderr exceeds max length: {len(stderr)} > {contract['max_stderr_length']}"
                        )
            except (json.JSONDecodeError, KeyError) as exc:
                errors.append(f"Contract validation error: {exc}")

        return len(errors) == 0, errors

    def _expand_command(self, command: str, context: dict[str, Any]) -> str:
        def replace(match: re.Match[str]) -> str:
            return shlex.quote(str(context.get(match.group(1), "")))

        return re.sub(r"\$\{([^}]+)\}", replace, command)

    def to_dict(self, result: ProgramExecutionResult) -> dict[str, Any]:
        return {
            "step_id": result.step_id,
            "command": result.command,
            "returncode": result.returncode,
            "stdout": result.stdout[:10000],
            "stderr": result.stderr[:10000],
            "duration_ms": round(result.duration_ms, 2),
            "timed_out": result.timed_out,
            "policy_blocked": result.policy_blocked,
            "policy_reason": result.policy_reason,
            "contract_valid": result.contract_valid,
            "contract_errors": result.contract_errors,
            "output_files": result.output_files,
            "started_at": result.started_at,
            "completed_at": result.completed_at,
        }
