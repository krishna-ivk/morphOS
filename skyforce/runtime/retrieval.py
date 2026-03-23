from __future__ import annotations

from pathlib import Path
from typing import Any

from .context_hub import ContextHub
from .io import read_json


def build_retrieval_context(
    repo_root: Path,
    workflow: str,
    current_run_id: str,
    query: str | None = None,
    consumer: str = "coding_agent",
) -> dict[str, Any]:
    repo_root = Path(repo_root)
    hub = ContextHub(repo_root)
    query_text = query or workflow.replace("_", " ")
    search = hub.search(query_text, consumer=consumer, limit=5)
    if search["matched"] == 0:
        search = hub.search("guide", consumer=consumer, limit=5)
    if search["matched"] == 0:
        search = {"matched": 0, "results": [hub._context_record(path) for path in hub._doc_paths()[:5]], "consumer": consumer}
        search["matched"] = len(search["results"])

    exemplars = []
    runs_root = repo_root / "artifacts" / "runs"
    if runs_root.exists():
        for run_state_path in sorted(runs_root.glob("*/artifacts/run_state.json")):
            payload = read_json(run_state_path, {})
            if payload.get("workflow") != workflow:
                continue
            if payload.get("status") != "completed":
                continue
            if payload.get("run_id") == current_run_id:
                continue
            exemplars.append({"run_id": payload.get("run_id"), "workflow": workflow})

    return {
        "workflow": workflow,
        "query": query_text,
        "consumer": consumer,
        "reference_context_count": search["matched"],
        "reference_context": search["results"],
        "reference_context_titles": [item.get("title") for item in search["results"]],
        "exemplar_count": len(exemplars),
        "exemplars": exemplars,
    }
