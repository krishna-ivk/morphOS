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


VERDICT_ALLOW = "allow"
VERDICT_WARN = "warn"
VERDICT_BLOCK = "block"
VERDICT_REQUIRE_REVIEW = "require_review"
VERDICT_REQUIRE_APPROVAL = "require_approval"

ALL_VERDICTS = {
    VERDICT_ALLOW,
    VERDICT_WARN,
    VERDICT_BLOCK,
    VERDICT_REQUIRE_REVIEW,
    VERDICT_REQUIRE_APPROVAL,
}


@dataclass
class PolicyVerdict:
    """5-value verdict language for unified policy enforcement."""

    verdict: str
    decisions: list[PolicyDecision]
    warnings: list[str]
    blocked_by: str | None = None
    requires_review_reason: str | None = None
    requires_approval_reason: str | None = None

    @property
    def is_allowed(self) -> bool:
        return self.verdict == VERDICT_ALLOW

    @property
    def is_blocked(self) -> bool:
        return self.verdict in {VERDICT_BLOCK, VERDICT_REQUIRE_APPROVAL}

    @property
    def needs_human_action(self) -> bool:
        return self.verdict in {VERDICT_REQUIRE_REVIEW, VERDICT_REQUIRE_APPROVAL}


class PolicyEngine:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.policy_bundle = self._load_policy_bundle()
        self._command_rules = self._load_command_rules()
        self._intake_rules = self._load_intake_rules()

    def _load_policy_bundle(self) -> dict[str, dict[str, Any]]:
        bundle: dict[str, dict[str, Any]] = {}
        policies_dir = self.repo_root / "policies"
        if not policies_dir.exists():
            return bundle
        for path in sorted(policies_dir.glob("*.yaml")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not payload.get("enabled", False):
                continue
            for rule in payload.get("rules", []):
                bundle[rule["id"]] = rule
        return bundle

    def _load_command_rules(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "block_secret_in_code",
                "pattern": r"\bsk-[A-Za-z0-9]{20,}\b",
                "verdict": VERDICT_BLOCK,
                "reason": "secret-like token detected",
            },
            {
                "id": "block_rm_root",
                "pattern": r"\brm\s+-rf\s+/",
                "verdict": VERDICT_BLOCK,
                "reason": "destructive root directory removal",
            },
            {
                "id": "block_curl_pipe",
                "pattern": r"\b(curl|wget)\s+.*\|\s*(bash|sh)\b",
                "verdict": VERDICT_BLOCK,
                "reason": "remote code execution pattern",
            },
            {
                "id": "warn_large_output",
                "pattern": r".{100000,}",
                "verdict": VERDICT_WARN,
                "reason": "command output exceeds 100KB",
            },
        ]

    def _load_intake_rules(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "require_work_order",
                "field": "work_order",
                "verdict": VERDICT_REQUIRE_APPROVAL,
                "reason": "missing work_order",
            },
            {
                "id": "require_issue_ref",
                "field": "issue_identifier",
                "verdict": VERDICT_WARN,
                "reason": "missing issue reference",
            },
        ]

    def evaluate_verdict(
        self,
        run_id: str,
        step: dict[str, Any],
        context: dict[str, Any],
        command: str | None = None,
    ) -> PolicyVerdict:
        """Evaluate all applicable rules and return a unified 5-value verdict."""
        decisions: list[PolicyDecision] = []
        warnings: list[str] = []
        blocked_by: str | None = None
        review_reason: str | None = None
        approval_reason: str | None = None

        connectivity_decision = self._check_connectivity(step, context)
        if connectivity_decision:
            decisions.append(connectivity_decision)
            if not connectivity_decision.allowed:
                verdict = self._action_to_verdict(connectivity_decision.action)
                if verdict == VERDICT_BLOCK:
                    blocked_by = connectivity_decision.rule_id
                elif verdict == VERDICT_REQUIRE_REVIEW:
                    review_reason = connectivity_decision.reason
                elif verdict == VERDICT_REQUIRE_APPROVAL:
                    approval_reason = connectivity_decision.reason
                elif verdict == VERDICT_WARN:
                    warnings.append(connectivity_decision.reason or "")

        deployment_decision = self._check_deployment_gate(step, context)
        if deployment_decision:
            decisions.append(deployment_decision)
            if not deployment_decision.allowed:
                verdict = self._action_to_verdict(deployment_decision.action)
                if verdict == VERDICT_BLOCK and not blocked_by:
                    blocked_by = deployment_decision.rule_id
                elif verdict == VERDICT_REQUIRE_REVIEW and not review_reason:
                    review_reason = deployment_decision.reason
                elif verdict == VERDICT_REQUIRE_APPROVAL and not approval_reason:
                    approval_reason = deployment_decision.reason
                elif verdict == VERDICT_WARN:
                    warnings.append(deployment_decision.reason or "")

        if command:
            command_decision = self.check_command(command, context)
            decisions.append(command_decision)
            if not command_decision.allowed:
                verdict = self._action_to_verdict(command_decision.action)
                if verdict == VERDICT_BLOCK and not blocked_by:
                    blocked_by = command_decision.rule_id
                elif verdict == VERDICT_REQUIRE_REVIEW and not review_reason:
                    review_reason = command_decision.reason
                elif verdict == VERDICT_REQUIRE_APPROVAL and not approval_reason:
                    approval_reason = command_decision.reason
                elif verdict == VERDICT_WARN:
                    warnings.append(command_decision.reason or "")

        secret_decision = self._check_secrets(context)
        if secret_decision:
            decisions.append(secret_decision)
            if not secret_decision.allowed:
                verdict = self._action_to_verdict(secret_decision.action)
                if verdict == VERDICT_BLOCK and not blocked_by:
                    blocked_by = secret_decision.rule_id
                elif verdict == VERDICT_REQUIRE_REVIEW and not review_reason:
                    review_reason = secret_decision.reason
                elif verdict == VERDICT_REQUIRE_APPROVAL and not approval_reason:
                    approval_reason = secret_decision.reason
                elif verdict == VERDICT_WARN:
                    warnings.append(secret_decision.reason or "")

        if blocked_by:
            verdict = VERDICT_BLOCK
        elif approval_reason:
            verdict = VERDICT_REQUIRE_APPROVAL
        elif review_reason:
            verdict = VERDICT_REQUIRE_REVIEW
        elif warnings:
            verdict = VERDICT_WARN
        else:
            verdict = VERDICT_ALLOW

        return PolicyVerdict(
            verdict=verdict,
            decisions=decisions,
            warnings=warnings,
            blocked_by=blocked_by,
            requires_review_reason=review_reason,
            requires_approval_reason=approval_reason,
        )

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

    def check_command(self, command: str, context: dict[str, Any]) -> PolicyDecision:
        """Check a command against command evaluation rules."""
        for rule in self._command_rules:
            if re.search(rule["pattern"], command):
                verdict = rule["verdict"]
                action = self._verdict_to_action(verdict)
                return PolicyDecision(
                    allowed=verdict == VERDICT_ALLOW,
                    action=action,
                    rule_id=rule["id"],
                    reason=rule["reason"],
                )
        return PolicyDecision(allowed=True, action="allow")

    def check_intake(self, work_order: dict[str, Any]) -> PolicyVerdict:
        """Check work order intake rules."""
        decisions = []
        warnings = []
        approval_reason = None

        for rule in self._intake_rules:
            if not work_order.get(rule["field"]):
                verdict = rule["verdict"]
                action = self._verdict_to_action(verdict)
                decision = PolicyDecision(
                    allowed=verdict == VERDICT_ALLOW,
                    action=action,
                    rule_id=rule["id"],
                    reason=rule["reason"],
                )
                decisions.append(decision)
                if verdict == VERDICT_REQUIRE_APPROVAL:
                    approval_reason = rule["reason"]
                elif verdict == VERDICT_WARN:
                    warnings.append(rule["reason"])

        if approval_reason:
            verdict = VERDICT_REQUIRE_APPROVAL
        elif warnings:
            verdict = VERDICT_WARN
        else:
            verdict = VERDICT_ALLOW

        return PolicyVerdict(
            verdict=verdict,
            decisions=decisions,
            warnings=warnings,
            requires_approval_reason=approval_reason,
        )

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

    def _check_connectivity(
        self, step: dict[str, Any], context: dict[str, Any]
    ) -> PolicyDecision | None:
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
        return None

    def _check_deployment_gate(
        self, step: dict[str, Any], context: dict[str, Any]
    ) -> PolicyDecision | None:
        if step.get("step_type") == "deploy" and context.get("test_failure") is True:
            return PolicyDecision(
                allowed=False,
                action="block",
                rule_id="deployment_gate",
                reason="deployment blocked because validation failed",
            )
        return None

    def _check_secrets(self, context: dict[str, Any]) -> PolicyDecision | None:
        text = json.dumps(context, sort_keys=True)
        if re.search(r"\bsk-[A-Za-z0-9]{20,}\b", text):
            return PolicyDecision(
                allowed=False,
                action="reject",
                rule_id="block_secret_in_code",
                reason="secret-like token detected in context",
            )
        return None

    @staticmethod
    def _action_to_verdict(action: str) -> str:
        mapping = {
            "allow": VERDICT_ALLOW,
            "warn": VERDICT_WARN,
            "block": VERDICT_BLOCK,
            "defer": VERDICT_REQUIRE_REVIEW,
            "reject": VERDICT_REQUIRE_APPROVAL,
        }
        return mapping.get(action, VERDICT_ALLOW)

    @staticmethod
    def _verdict_to_action(verdict: str) -> str:
        mapping = {
            VERDICT_ALLOW: "allow",
            VERDICT_WARN: "warn",
            VERDICT_BLOCK: "block",
            VERDICT_REQUIRE_REVIEW: "defer",
            VERDICT_REQUIRE_APPROVAL: "reject",
        }
        return mapping.get(verdict, "allow")
