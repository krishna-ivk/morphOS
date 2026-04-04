"""Git-based promotion: branch, commit, push, PR with pre-land invariants and rollback."""

from __future__ import annotations

import json
import subprocess
import shlex
import hashlib
import difflib
import fnmatch
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field


@dataclass
class PromotionCandidate:
    run_id: str
    step_id: str
    workspace_path: str
    source_repo_path: str
    branch_name: str
    file_statuses: list[dict[str, Any]]
    source_dirty: bool
    promotion_ready: bool
    pre_land_invariants: dict[str, bool] = field(default_factory=dict)


@dataclass
class PromotionReceipt:
    run_id: str
    step_id: str
    branch_name: str
    commit_sha: str
    files_promoted: list[str]
    checksums: list[dict[str, str]]
    pr_url: str | None = None
    promoted_at: str = ""
    rollback_branch: str | None = None


@dataclass
class PreLandInvariantResult:
    name: str
    passed: bool
    details: str = ""


class GitPromotionEngine:
    """Handles git-based promotion with pre-land invariants and rollback."""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def promote_with_git(
        self,
        run_id: str,
        handoff: dict[str, Any],
        apply: bool = False,
        only_files: list[str] | None = None,
        exclude_files: list[str] | None = None,
        remote: str = "origin",
        base_branch: str = "main",
        pr_title: str | None = None,
        pr_body: str | None = None,
    ) -> dict[str, Any]:
        workspace_path = Path(handoff["workspace_path"])
        source_repo_path = Path(handoff["source_repo_path"])
        step_id = handoff.get("step_id", "unknown")

        workspace_files = handoff.get("workspace_files", [])
        selected_files = self._select_files(workspace_files, only_files, exclude_files)

        file_statuses = self._compute_file_statuses(
            selected_files, workspace_path, source_repo_path
        )

        source_dirty = self._is_git_dirty(source_repo_path)
        branch_name = f"skyforce/{run_id}/{step_id}"
        rollback_branch = f"skyforce/rollback/{run_id}/{step_id}"

        invariants = self._check_pre_land_invariants(run_id, source_repo_path, handoff)

        candidate = PromotionCandidate(
            run_id=run_id,
            step_id=step_id,
            workspace_path=str(workspace_path),
            source_repo_path=str(source_repo_path),
            branch_name=branch_name,
            file_statuses=file_statuses,
            source_dirty=source_dirty,
            promotion_ready=all(v for v in invariants.values()) and not source_dirty,
            pre_land_invariants=invariants,
        )

        if not apply:
            return {
                "dry_run": True,
                "run_id": run_id,
                "step_id": step_id,
                "branch_name": branch_name,
                "rollback_branch": rollback_branch,
                "source_dirty": source_dirty,
                "changed_file_count": len(selected_files),
                "file_statuses": file_statuses,
                "pre_land_invariants": invariants,
                "promotion_ready": candidate.promotion_ready,
            }

        if source_dirty:
            return {
                "dry_run": False,
                "run_id": run_id,
                "step_id": step_id,
                "error": "source_repo_dirty",
                "message": "Source repository has uncommitted changes. Commit or stash before promoting.",
                "file_statuses": file_statuses,
            }

        if not candidate.promotion_ready:
            failed = [k for k, v in invariants.items() if not v]
            return {
                "dry_run": False,
                "run_id": run_id,
                "step_id": step_id,
                "error": "pre_land_invariants_failed",
                "failed_invariants": failed,
                "pre_land_invariants": invariants,
                "file_statuses": file_statuses,
            }

        return self._execute_git_promotion(
            run_id=run_id,
            step_id=step_id,
            branch_name=branch_name,
            rollback_branch=rollback_branch,
            selected_files=selected_files,
            file_statuses=file_statuses,
            workspace_path=workspace_path,
            source_repo_path=source_repo_path,
            remote=remote,
            base_branch=base_branch,
            pr_title=pr_title,
            pr_body=pr_body,
            handoff=handoff,
        )

    def _execute_git_promotion(
        self,
        run_id: str,
        step_id: str,
        branch_name: str,
        rollback_branch: str,
        selected_files: list[str],
        file_statuses: list[dict[str, Any]],
        workspace_path: Path,
        source_repo_path: Path,
        remote: str,
        base_branch: str,
        pr_title: str | None,
        pr_body: str | None,
        handoff: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            self._git(source_repo_path, ["fetch", remote, base_branch])

            self._git(
                source_repo_path,
                ["checkout", "-b", rollback_branch, f"{remote}/{base_branch}"],
                check=False,
            )

            self._git(
                source_repo_path,
                ["checkout", "-b", branch_name, f"{remote}/{base_branch}"],
                check=False,
            )
        except subprocess.CalledProcessError as exc:
            return {
                "dry_run": False,
                "run_id": run_id,
                "step_id": step_id,
                "error": "git_branch_creation_failed",
                "message": str(exc),
                "file_statuses": file_statuses,
            }

        promoted_files = []
        promoted_checksums = []
        for rel_path in selected_files:
            workspace_file = workspace_path / rel_path
            source_file = source_repo_path / rel_path
            if not workspace_file.exists():
                if source_file.exists():
                    source_file.unlink()
                    self._git(
                        source_repo_path, ["rm", "--cached", rel_path], check=False
                    )
                promoted_files.append(rel_path)
                promoted_checksums.append({"path": rel_path, "action": "deleted"})
                continue

            source_file.parent.mkdir(parents=True, exist_ok=True)
            content = workspace_file.read_text(encoding="utf-8")
            source_file.write_text(content, encoding="utf-8")
            promoted_files.append(rel_path)
            promoted_checksums.append(
                {
                    "path": rel_path,
                    "source_after": self._checksum_text(content),
                }
            )

        self._git(source_repo_path, ["add", "-A"])

        commit_msg = pr_title or f"skyforce: promote changes from {step_id} ({run_id})"
        self._git(source_repo_path, ["commit", "-m", commit_msg])

        try:
            result = self._git(source_repo_path, ["rev-parse", "HEAD"])
            commit_sha = result.stdout.strip()
        except subprocess.CalledProcessError:
            commit_sha = "unknown"

        try:
            self._git(source_repo_path, ["push", "-u", remote, branch_name])
        except subprocess.CalledProcessError as exc:
            return {
                "dry_run": False,
                "run_id": run_id,
                "step_id": step_id,
                "error": "git_push_failed",
                "message": str(exc),
                "branch_name": branch_name,
                "commit_sha": commit_sha,
                "files_promoted": promoted_files,
                "checksums": promoted_checksums,
                "rollback_branch": rollback_branch,
            }

        pr_url = self._try_create_pr(
            source_repo_path=source_repo_path,
            branch_name=branch_name,
            base_branch=base_branch,
            title=pr_title or f"[Skyforce] Promote {step_id} from {run_id}",
            body=pr_body
            or self._default_pr_body(run_id, step_id, promoted_files, handoff),
        )

        receipt = PromotionReceipt(
            run_id=run_id,
            step_id=step_id,
            branch_name=branch_name,
            commit_sha=commit_sha,
            files_promoted=promoted_files,
            checksums=promoted_checksums,
            pr_url=pr_url,
            promoted_at=datetime.now(timezone.utc).isoformat(),
            rollback_branch=rollback_branch,
        )

        promotions_dir = (
            self.repo_root / "artifacts" / "runs" / run_id / "artifacts" / "promotions"
        )
        promotions_dir.mkdir(parents=True, exist_ok=True)
        receipt_path = promotions_dir / f"{step_id}_promotion_receipt.json"
        receipt_path.write_text(
            json.dumps(self._receipt_to_dict(receipt), indent=2), encoding="utf-8"
        )

        return {
            "dry_run": False,
            "run_id": run_id,
            "step_id": step_id,
            "branch_name": branch_name,
            "commit_sha": commit_sha,
            "files_promoted": promoted_files,
            "checksums": promoted_checksums,
            "pr_url": pr_url,
            "rollback_branch": rollback_branch,
            "receipt_path": str(receipt_path),
            "file_statuses": file_statuses,
        }

    def rollback_promotion(
        self,
        run_id: str,
        step_id: str,
        remote: str = "origin",
        base_branch: str = "main",
    ) -> dict[str, Any]:
        receipt_path = (
            self.repo_root
            / "artifacts"
            / "runs"
            / run_id
            / "artifacts"
            / "promotions"
            / f"{step_id}_promotion_receipt.json"
        )
        if not receipt_path.exists():
            return {
                "error": "no_receipt",
                "message": f"No promotion receipt found for {step_id} in {run_id}",
            }

        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        rollback_branch = receipt.get("rollback_branch")
        source_repo_path = receipt.get("source_repo_path", str(self.repo_root))
        source_path = Path(source_repo_path)

        if not rollback_branch:
            return {
                "error": "no_rollback_branch",
                "message": "No rollback branch available for this promotion",
            }

        try:
            self._git(source_path, ["fetch", remote, base_branch])
            self._git(source_path, ["checkout", base_branch])
            self._git(source_path, ["reset", "--hard", f"{remote}/{base_branch}"])
            self._git(source_path, ["branch", "-D", rollback_branch], check=False)
        except subprocess.CalledProcessError as exc:
            return {
                "error": "rollback_failed",
                "message": str(exc),
            }

        receipt["rolled_back"] = True
        receipt["rolled_back_at"] = datetime.now(timezone.utc).isoformat()
        receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

        return {
            "run_id": run_id,
            "step_id": step_id,
            "rolled_back": True,
            "rolled_back_at": receipt["rolled_back_at"],
            "message": f"Successfully rolled back promotion for {step_id}",
        }

    def _check_pre_land_invariants(
        self, run_id: str, source_repo_path: Path, handoff: dict[str, Any]
    ) -> dict[str, bool]:
        invariants: dict[str, bool] = {}

        invariants["validation_green"] = self._check_validation_green(run_id)
        invariants["no_pending_approvals"] = self._check_no_pending_approvals(run_id)
        invariants["no_pending_directives"] = self._check_no_pending_directives(run_id)
        invariants["source_repo_clean"] = not self._is_git_dirty(source_repo_path)
        invariants["has_changed_files"] = len(handoff.get("workspace_files", [])) > 0

        return invariants

    def _check_validation_green(self, run_id: str) -> bool:
        validation_dir = self.repo_root / "artifacts" / "runs" / run_id / "validation"
        if not validation_dir.exists():
            return True
        for report_path in validation_dir.glob("*_contract_report.json"):
            try:
                report = json.loads(report_path.read_text(encoding="utf-8"))
                if report.get("overall_result") == "fail":
                    return False
            except (json.JSONDecodeError, KeyError):
                return False
        return True

    def _check_no_pending_approvals(self, run_id: str) -> bool:
        approval_path = (
            self.repo_root
            / "artifacts"
            / "runs"
            / run_id
            / "approvals"
            / "approval_packet.json"
        )
        if not approval_path.exists():
            return True
        try:
            packet = json.loads(approval_path.read_text(encoding="utf-8"))
            return packet.get("status") != "pending"
        except (json.JSONDecodeError, KeyError):
            return True

    def _check_no_pending_directives(self, run_id: str) -> bool:
        deferred_path = (
            self.repo_root
            / "artifacts"
            / "runs"
            / run_id
            / "artifacts"
            / "deferred_actions.json"
        )
        if not deferred_path.exists():
            return True
        try:
            actions = json.loads(deferred_path.read_text(encoding="utf-8"))
            return len(actions) == 0
        except (json.JSONDecodeError, KeyError):
            return True

    def _try_create_pr(
        self,
        source_repo_path: Path,
        branch_name: str,
        base_branch: str,
        title: str,
        body: str,
    ) -> str | None:
        try:
            result = subprocess.run(
                [
                    "gh",
                    "pr",
                    "create",
                    "--base",
                    base_branch,
                    "--head",
                    branch_name,
                    "--title",
                    title,
                    "--body",
                    body,
                ],
                cwd=source_repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            return result.stdout.strip()
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            return None

    def _default_pr_body(
        self, run_id: str, step_id: str, files: list[str], handoff: dict[str, Any]
    ) -> str:
        files_list = "\n".join(f"- `{f}`" for f in files[:20])
        return f"""## Skyforce Promotion

**Run:** `{run_id}`
**Step:** `{step_id}`
**Workflow:** `{handoff.get("workflow", "unknown")}`

### Files Changed ({len(files)})
{files_list}

### Evidence
- Run artifacts: `artifacts/runs/{run_id}/`
- Validation reports: `artifacts/runs/{run_id}/validation/`
- Checkpoint: `artifacts/runs/{run_id}/artifacts/checkpoint.json`

---
*Auto-generated by Skyforce morphOS*
"""

    def _select_files(
        self,
        workspace_files: list[str],
        only_files: list[str] | None,
        exclude_files: list[str] | None,
    ) -> list[str]:
        selected = list(workspace_files)
        if only_files:
            selected = [
                p
                for p in selected
                if any(fnmatch.fnmatch(p, pat) for pat in only_files)
            ]
        if exclude_files:
            selected = [
                p
                for p in selected
                if not any(fnmatch.fnmatch(p, pat) for pat in exclude_files)
            ]
        return selected

    def _compute_file_statuses(
        self,
        selected_files: list[str],
        workspace_path: Path,
        source_repo_path: Path,
    ) -> list[dict[str, Any]]:
        statuses = []
        for rel_path in selected_files:
            ws_file = workspace_path / rel_path
            src_file = source_repo_path / rel_path
            ws_text = ws_file.read_text(encoding="utf-8") if ws_file.exists() else ""
            src_text = src_file.read_text(encoding="utf-8") if src_file.exists() else ""

            if not src_file.exists():
                status = "create"
            elif src_text != ws_text:
                status = "modify"
            else:
                status = "unchanged"

            preview = ""
            if status != "unchanged":
                preview = "".join(
                    difflib.unified_diff(
                        src_text.splitlines(keepends=True),
                        ws_text.splitlines(keepends=True),
                        fromfile=f"a/{rel_path}",
                        tofile=f"b/{rel_path}",
                        n=2,
                    )
                )

            statuses.append(
                {
                    "path": rel_path,
                    "status": status,
                    "preview": preview,
                    "checksums": {
                        "path": rel_path,
                        "source": self._checksum_text(src_text)
                        if src_file.exists()
                        else None,
                        "workspace": self._checksum_text(ws_text)
                        if ws_file.exists()
                        else None,
                    },
                }
            )
        return statuses

    def _is_git_dirty(self, repo_path: Path) -> bool:
        git_dir = repo_path / ".git"
        if not git_dir.exists():
            return False
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        return bool(result.stdout.strip())

    def _git(
        self, repo_path: Path, args: list[str], check: bool = True, timeout: int = 30
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout,
        )

    def _checksum_text(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _receipt_to_dict(self, receipt: PromotionReceipt) -> dict[str, Any]:
        return {
            "run_id": receipt.run_id,
            "step_id": receipt.step_id,
            "branch_name": receipt.branch_name,
            "commit_sha": receipt.commit_sha,
            "files_promoted": receipt.files_promoted,
            "checksums": receipt.checksums,
            "pr_url": receipt.pr_url,
            "promoted_at": receipt.promoted_at,
            "rollback_branch": receipt.rollback_branch,
        }
