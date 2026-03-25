from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class PolicyDecision:
    allowed: bool
    action: str
    rule_id: str | None = None
    reason: str | None = None


class PolicyEngine:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.policy_bundle = self._load_policy_bundle()

    def _load_policy_bundle(self) -> dict[str, dict[str, Any]]:
        bundle: dict[str, dict[str, Any]] = {}
        for path in sorted((self.repo_root / "policies").glob("*.yaml")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not payload.get("enabled", False):
                continue
            for rule in payload.get("rules", []):
                bundle[rule["id"]] = rule
        return bundle

    def check_output_for_secrets(
        self, run_id: str, agent: str, payload: dict[str, Any]
    ) -> PolicyDecision:
        text = json.dumps(payload, sort_keys=True)
        if re.search(r"\bsk-[A-Za-z0-9]{20,}\b", text):
            return PolicyDecision(
                allowed=False,
                action="reject",
                rule_id="block_secret_in_code",
                reason="secret-like token detected in output",
            )
        return PolicyDecision(allowed=True, action="allow")

    def check_step_start(
        self,
        runs_root: Path,
        run_id: str,
        step: dict[str, Any],
        context: dict[str, Any],
    ) -> PolicyDecision:
        required = step.get("requires_connectivity")
        current = context.get("connectivity_mode", "offline")
        if required == "online_read" and current == "offline":
            return PolicyDecision(
                allowed=False,
                action="defer",
                rule_id="network_write_gate",
                reason="connectivity requirement not satisfied",
            )
        if required == "deploy_enabled" and current != "deploy_enabled":
            return PolicyDecision(
                allowed=False,
                action="defer",
                rule_id="network_write_gate",
                reason="deploy connectivity requirement not satisfied",
            )
        if step.get("step_type") == "deploy" and context.get("test_failure") is True:
            return PolicyDecision(
                allowed=False,
                action="block",
                rule_id="deployment_gate",
                reason="deployment blocked because validation failed",
            )
        return PolicyDecision(allowed=True, action="allow")
