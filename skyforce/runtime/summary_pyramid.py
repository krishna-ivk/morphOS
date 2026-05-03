"""Summary Pyramid: generates status.txt, summary_short.md, summary_full.md from run evidence."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SummaryPyramidGenerator:
    """Generates the three layers of the summary pyramid for operator inspectability."""

    def __init__(self, run_dir: Path):
        self.run_dir = Path(run_dir)

    def generate_all(self, state: dict[str, Any]) -> dict[str, str]:
        status_txt = self.generate_status_txt(state)
        summary_short = self.generate_summary_short(state)
        summary_full = self.generate_summary_full(state)
        return {
            "status_txt": status_txt,
            "summary_short": summary_short,
            "summary_full": summary_full,
        }

    def generate_status_txt(self, state: dict[str, Any]) -> str:
        status = state.get("status", "unknown").upper()
        workflow = state.get("workflow", "unknown")
        run_id = state.get("run_id", "unknown")
        steps = state.get("steps", [])
        completed = sum(1 for s in steps if s.get("status") == "completed")
        total = len(steps)
        return f"[{status}] {workflow} ({run_id}): {completed}/{total} steps completed"

    def generate_summary_short(self, state: dict[str, Any]) -> str:
        status = state.get("status", "unknown")
        workflow = state.get("workflow", "unknown")
        run_id = state.get("run_id", "unknown")
        steps = state.get("steps", [])
        completed = sum(1 for s in steps if s.get("status") == "completed")
        total = len(steps)
        pause_reason = state.get("pause_reason")
        mode = state.get("mode", "factory")

        lines = [
            f"## {workflow.capitalize()} Run: `{run_id}`",
            f"",
            f"**Status:** {status.upper()} ({completed}/{total} steps)",
            f"**Mode:** {mode}",
        ]

        if pause_reason:
            lines.append(f"**Paused:** {pause_reason}")

        if status == "failed":
            failed_step = next((s for s in steps if s.get("status") == "failed"), None)
            if failed_step:
                lines.append(
                    f"**Failed at:** `{failed_step.get('step_id', 'unknown')}`"
                )

        if status == "completed":
            lines.append(f"**Result:** All {total} steps completed successfully")

        return "\n".join(lines) + "\n"

    def generate_summary_full(self, state: dict[str, Any]) -> str:
        status = state.get("status", "unknown")
        workflow = state.get("workflow", "unknown")
        run_id = state.get("run_id", "unknown")
        steps = state.get("steps", [])
        context = state.get("context", {})
        started_at = state.get("started_at", "")
        ended_at = state.get("ended_at", "")
        mode = state.get("mode", "factory")
        pause_reason = state.get("pause_reason")

        lines = [
            f"# Run Summary: `{run_id}`",
            f"",
            f"## Overview",
            f"",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Workflow | `{workflow}` |",
            f"| Run ID | `{run_id}` |",
            f"| Status | **{status.upper()}** |",
            f"| Mode | `{mode}` |",
            f"| Started | `{started_at}` |",
            f"| Ended | `{ended_at or 'N/A'}` |",
        ]

        if pause_reason:
            lines.append(f"| Pause Reason | `{pause_reason}` |")

        connectivity = context.get("connectivity_mode", "unknown")
        lines.append(f"| Connectivity | `{connectivity}` |")

        completed = sum(1 for s in steps if s.get("status") == "completed")
        failed = sum(1 for s in steps if s.get("status") == "failed")
        deferred = sum(1 for s in steps if s.get("status") == "deferred")
        skipped = sum(1 for s in steps if s.get("status") == "skipped")

        lines.extend(
            [
                f"",
                f"## Step Progress",
                f"",
                f"- **Completed:** {completed}",
                f"- **Failed:** {failed}",
                f"- **Deferred:** {deferred}",
                f"- **Skipped:** {skipped}",
                f"- **Total:** {len(steps)}",
                f"",
                f"## Steps",
                f"",
            ]
        )

        for i, step in enumerate(steps, 1):
            step_id = step.get("step_id", "unknown")
            step_status = step.get("status", "unknown")
            status_icon = {
                "completed": "✅",
                "failed": "❌",
                "deferred": "⏸️",
                "skipped": "⏭️",
                "pending": "⬜",
            }.get(step_status, "❓")
            lines.append(f"{i}. {status_icon} `{step_id}` — {step_status}")
            if step.get("details"):
                details = step["details"]
                if isinstance(details, dict):
                    if "returncode" in details:
                        lines.append(f"   - Exit code: {details['returncode']}")
                    if "duration_ms" in details:
                        lines.append(f"   - Duration: {details['duration_ms']:.0f}ms")
                    if "policy_blocked" in details and details["policy_blocked"]:
                        lines.append(
                            f"   - Policy blocked: {details.get('policy_reason', 'unknown')}"
                        )

        lines.extend(
            [
                f"",
                f"## Artifacts",
                f"",
            ]
        )

        artifacts_dir = self.run_dir / "artifacts"
        if artifacts_dir.exists():
            for item in sorted(artifacts_dir.rglob("*")):
                if item.is_file() and item.suffix in (".json", ".md", ".txt", ".patch"):
                    rel = item.relative_to(self.run_dir)
                    lines.append(f"- `{rel}`")

        lines.extend(
            [
                f"",
                f"---",
                f"*Generated by morphOS Summary Pyramid at {datetime.now(timezone.utc).isoformat()}*",
            ]
        )

        return "\n".join(lines) + "\n"

    def write_summaries(self, state: dict[str, Any]) -> dict[str, str]:
        summaries_dir = self.run_dir / "summaries"
        summaries_dir.mkdir(parents=True, exist_ok=True)

        results = self.generate_all(state)

        (summaries_dir / "status.txt").write_text(
            results["status_txt"], encoding="utf-8"
        )
        (summaries_dir / "summary_short.md").write_text(
            results["summary_short"], encoding="utf-8"
        )
        (summaries_dir / "summary_full.md").write_text(
            results["summary_full"], encoding="utf-8"
        )

        return {
            "status_txt": str(summaries_dir / "status.txt"),
            "summary_short": str(summaries_dir / "summary_short.md"),
            "summary_full": str(summaries_dir / "summary_full.md"),
        }
