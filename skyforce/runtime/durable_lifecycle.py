"""Durable lifecycle management: checkpoint, resume, cancel, retry with backoff."""

from __future__ import annotations

import json
import signal
import subprocess
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field


@dataclass
class RetryConfig:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    backoff_factor: float = 2.0


@dataclass
class RetryState:
    attempt: int = 0
    last_error: str = ""
    next_retry_at: str | None = None
    delays: list[float] = field(default_factory=list)


@dataclass
class SubprocessHandle:
    pid: int
    process: subprocess.Popen
    started_at: str
    cancelled: bool = False


class DurableLifecycleManager:
    """Manages run lifecycle with checkpoint, resume, cancel, and retry."""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self._active_processes: dict[str, SubprocessHandle] = {}

    def create_checkpoint(
        self,
        run_id: str,
        step_id: str,
        step_index: int,
        state: dict[str, Any],
        reason: str = "checkpoint",
    ) -> dict[str, Any]:
        checkpoint = {
            "checkpoint_id": f"cp-{run_id}-{step_index}",
            "run_id": run_id,
            "step_id": step_id,
            "step_index": step_index,
            "reason": reason,
            "state_snapshot": state,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "retry_state": None,
        }
        self._write_checkpoint(run_id, checkpoint)
        return checkpoint

    def resume_from_checkpoint(self, run_id: str) -> dict[str, Any] | None:
        checkpoint = self._load_checkpoint(run_id)
        if not checkpoint:
            return None

        retry_state = checkpoint.get("retry_state")
        if retry_state:
            next_at = retry_state.get("next_retry_at")
            if next_at:
                next_time = datetime.fromisoformat(next_at)
                if datetime.now(timezone.utc) < next_time:
                    return {
                        "checkpoint": checkpoint,
                        "status": "retry_pending",
                        "next_retry_at": next_at,
                        "attempt": retry_state.get("attempt", 0),
                    }

        return {
            "checkpoint": checkpoint,
            "status": "ready_to_resume",
            "step_index": checkpoint.get("step_index"),
            "state_snapshot": checkpoint.get("state_snapshot"),
        }

    def cancel_run(self, run_id: str, reason: str = "user_requested") -> dict[str, Any]:
        handle = self._active_processes.pop(run_id, None)
        if handle and not handle.cancelled:
            self._terminate_process(handle)
            handle.cancelled = True

        checkpoint = self._load_checkpoint(run_id)
        if checkpoint:
            checkpoint["cancelled"] = True
            checkpoint["cancel_reason"] = reason
            checkpoint["cancelled_at"] = datetime.now(timezone.utc).isoformat()
            self._write_checkpoint(run_id, checkpoint)

        run_state_path = (
            self.repo_root
            / "artifacts"
            / "runs"
            / run_id
            / "artifacts"
            / "run_state.json"
        )
        if run_state_path.exists():
            state = json.loads(run_state_path.read_text(encoding="utf-8"))
            state["status"] = "cancelled"
            state["pause_reason"] = reason
            state["ended_at"] = datetime.now(timezone.utc).isoformat()
            run_state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

        return {
            "run_id": run_id,
            "status": "cancelled",
            "reason": reason,
            "cancelled_at": datetime.now(timezone.utc).isoformat(),
            "process_terminated": handle is not None,
        }

    def retry_with_backoff(
        self,
        run_id: str,
        step_id: str,
        step_index: int,
        state: dict[str, Any],
        error: str,
        config: RetryConfig | None = None,
    ) -> dict[str, Any]:
        config = config or RetryConfig()
        checkpoint = self._load_checkpoint(run_id) or {}
        retry_state = checkpoint.get("retry_state") or {}

        attempt = retry_state.get("attempt", 0) + 1

        if attempt > config.max_retries:
            return {
                "run_id": run_id,
                "status": "retry_exhausted",
                "attempt": attempt,
                "max_retries": config.max_retries,
                "last_error": error,
            }

        delay = min(
            config.base_delay * (config.backoff_factor ** (attempt - 1)),
            config.max_delay,
        )
        next_retry_at = (
            datetime.now(timezone.utc) + timedelta(seconds=delay)
        ).isoformat()

        retry_state = {
            "attempt": attempt,
            "last_error": error,
            "next_retry_at": next_retry_at,
            "delays": retry_state.get("delays", []) + [delay],
        }

        checkpoint.update(
            {
                "checkpoint_id": f"cp-{run_id}-{step_index}-retry-{attempt}",
                "run_id": run_id,
                "step_id": step_id,
                "step_index": step_index,
                "reason": f"retry-{attempt}",
                "state_snapshot": state,
                "retry_state": retry_state,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        self._write_checkpoint(run_id, checkpoint)

        return {
            "run_id": run_id,
            "status": "retry_scheduled",
            "attempt": attempt,
            "max_retries": config.max_retries,
            "next_retry_at": next_retry_at,
            "delay_seconds": delay,
            "last_error": error,
        }

    def run_with_retry(
        self,
        run_id: str,
        command: list[str],
        cwd: str | None = None,
        config: RetryConfig | None = None,
        timeout: int = 300,
    ) -> dict[str, Any]:
        config = config or RetryConfig()

        for attempt in range(1, config.max_retries + 1):
            if attempt > 1:
                delay = min(
                    config.base_delay * (config.backoff_factor ** (attempt - 1)),
                    config.max_delay,
                )
                time.sleep(delay)

            result = self._run_subprocess(run_id, command, cwd, timeout)

            if result["returncode"] == 0:
                result["attempt"] = attempt
                result["retries"] = attempt - 1
                return result

            if attempt < config.max_retries:
                self.retry_with_backoff(
                    run_id=run_id,
                    step_id=run_id,
                    step_index=0,
                    state={"command": command},
                    error=result.get("stderr", "unknown error"),
                    config=config,
                )

        result["retry_exhausted"] = True
        result["max_retries"] = config.max_retries
        return result

    def recover_from_reboot(self) -> dict[str, Any]:
        runs_dir = self.repo_root / "artifacts" / "runs"
        if not runs_dir.exists():
            return {"recovered": [], "message": "No runs found"}

        recovered = []
        for run_dir in runs_dir.iterdir():
            if not run_dir.is_dir():
                continue

            run_state_path = run_dir / "artifacts" / "run_state.json"
            if not run_state_path.exists():
                continue

            state = json.loads(run_state_path.read_text(encoding="utf-8"))
            if state.get("status") == "running":
                state["status"] = "paused"
                state["pause_reason"] = "system_reboot"
                state["recovered_at"] = datetime.now(timezone.utc).isoformat()
                run_state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

                checkpoint = self._load_checkpoint(state["run_id"])
                recovered.append(
                    {
                        "run_id": state["run_id"],
                        "workflow": state.get("workflow"),
                        "previous_status": "running",
                        "new_status": "paused",
                        "checkpoint_step_index": checkpoint.get("step_index")
                        if checkpoint
                        else None,
                    }
                )

        return {
            "recovered": recovered,
            "count": len(recovered),
            "message": f"Recovered {len(recovered)} running runs to paused state",
        }

    def register_process(
        self, run_id: str, process: subprocess.Popen
    ) -> SubprocessHandle:
        handle = SubprocessHandle(
            pid=process.pid,
            process=process,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self._active_processes[run_id] = handle
        return handle

    def _terminate_process(self, handle: SubprocessHandle) -> None:
        try:
            handle.process.terminate()
            try:
                handle.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                handle.process.kill()
                handle.process.wait(timeout=5)
        except (ProcessLookupError, OSError):
            pass

    def _run_subprocess(
        self,
        run_id: str,
        command: list[str],
        cwd: str | None,
        timeout: int,
    ) -> dict[str, Any]:
        try:
            process = subprocess.Popen(
                command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=lambda: signal.signal(signal.SIGTERM, signal.SIG_DFL),
            )
            self.register_process(run_id, process)

            try:
                stdout, stderr = process.communicate(timeout=timeout)
                return {
                    "returncode": process.returncode,
                    "stdout": stdout,
                    "stderr": stderr,
                    "pid": process.pid,
                    "timeout": False,
                }
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                return {
                    "returncode": -1,
                    "stdout": stdout or "",
                    "stderr": stderr or "",
                    "pid": process.pid,
                    "timeout": True,
                    "error": f"Process timed out after {timeout}s",
                }
        finally:
            self._active_processes.pop(run_id, None)

    def _write_checkpoint(self, run_id: str, checkpoint: dict[str, Any]) -> None:
        checkpoint_dir = self.repo_root / "artifacts" / "runs" / run_id / "artifacts"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        path = checkpoint_dir / "checkpoint.json"
        path.write_text(json.dumps(checkpoint, indent=2), encoding="utf-8")

        checkpoints_dir = checkpoint_dir / "checkpoints"
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        cp_path = checkpoints_dir / f"{checkpoint['checkpoint_id']}.json"
        cp_path.write_text(json.dumps(checkpoint, indent=2), encoding="utf-8")

    def _load_checkpoint(self, run_id: str) -> dict[str, Any] | None:
        path = (
            self.repo_root
            / "artifacts"
            / "runs"
            / run_id
            / "artifacts"
            / "checkpoint.json"
        )
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, KeyError):
            return None
