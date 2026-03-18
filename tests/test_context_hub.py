import json
from pathlib import Path

from skyforce.runtime.context_hub import ContextHub
from skyforce.runtime.orchestrator import Orchestrator
from skyforce.runtime.retrieval import build_retrieval_context
from skyforce.runtime.io import write_json


def _make_context_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    (repo_root / "docs").mkdir(parents=True, exist_ok=True)
    (repo_root / "artifacts" / "runs").mkdir(parents=True, exist_ok=True)
    (repo_root / "README.md").write_text(
        "# Repo Home\n\nContext Hub overview and integration guidance.\n"
    )
    (repo_root / "docs" / "guide.md").write_text(
        "# Context Hub Guide\n\nUse annotations and trust labels for grounded retrieval.\n"
    )
    (repo_root / "memory").mkdir(parents=True, exist_ok=True)
    (repo_root / "memory" / "capability_store.json").write_text(
        json.dumps({"patterns": [], "bug_fixes": [], "architecture_lessons": []})
    )
    return repo_root


def test_context_hub_search_returns_repo_docs_with_source_attribution(tmp_path):
    repo_root = _make_context_repo(tmp_path)
    hub = ContextHub(repo_root)
    result = hub.search("Context Hub", consumer="operator", limit=5)
    assert result["matched"] >= 1
    first = result["results"][0]
    assert first["source"] == "repo-local-docs"
    assert first["trust_label"] == "curated"
    assert first["access_label"] == "public"
    assert first["uri"].endswith("guide.md") or first["uri"].endswith("README.md")


def test_context_hub_human_annotation_is_returned_in_context_reads(tmp_path):
    repo_root = _make_context_repo(tmp_path)
    hub = ContextHub(repo_root)
    context_id = hub.search("Context Hub", consumer="operator", limit=1)["results"][0][
        "context_id"
    ]
    created = hub.create_annotation(
        context_id,
        consumer="operator",
        author_kind="human",
        author_id="alice",
        content="Prefer this guide for local pilots.",
        trust_label="annotated",
        access_label="public",
    )
    assert created["status"] == "active"
    fetched = hub.get_context(context_id, consumer="coding_agent")
    assert fetched["annotation_count"] == 1
    assert fetched["annotations"][0]["content"] == "Prefer this guide for local pilots."


def test_context_hub_machine_annotation_requires_promotion(tmp_path):
    repo_root = _make_context_repo(tmp_path)
    hub = ContextHub(repo_root)
    context_id = hub.search("Context Hub", consumer="operator", limit=1)["results"][0][
        "context_id"
    ]
    created = hub.create_annotation(
        context_id,
        consumer="coding_agent",
        author_kind="machine",
        author_id="coding_agent",
        content="This seems relevant for coding tasks.",
        access_label="trusted-agent",
    )
    assert created["status"] == "pending_review"
    hidden = hub.list_annotations(context_id, consumer="operator")
    assert hidden == []
    promoted = hub.promote_annotation(created["annotation_id"], approver="operator")
    assert promoted["status"] == "active"
    visible = hub.list_annotations(context_id, consumer="operator")
    assert visible[0]["annotation_id"] == created["annotation_id"]


def test_build_retrieval_context_includes_reference_context(tmp_path):
    repo_root = _make_context_repo(tmp_path)
    retrieval = build_retrieval_context(
        repo_root,
        workflow="feature_pipeline",
        current_run_id="run-current",
        query="Context Hub",
        consumer="coding_agent",
    )
    assert retrieval["reference_context_count"] >= 1
    assert retrieval["reference_context"][0]["source"] == "repo-local-docs"


def test_promote_workspace_changes_previews_and_applies(tmp_path):
    repo_root = _make_context_repo(tmp_path)
    orchestrator = Orchestrator(repo_root)
    run_dir = repo_root / "artifacts" / "runs" / "run-123"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    source_repo = tmp_path / "source"
    workspace = run_dir / "workspace"
    source_repo.mkdir(parents=True, exist_ok=True)
    workspace.mkdir(parents=True, exist_ok=True)
    (source_repo / "sample.txt").write_text("old")
    (workspace / "sample.txt").write_text("new")
    write_json(
        run_dir / "artifacts" / "implement_features_source_handoff.json",
        {
            "step_id": "implement_features",
            "workspace_path": str(workspace),
            "source_repo_path": str(source_repo),
            "workspace_files": ["sample.txt"],
            "combined_patch_path": None,
            "promotion_ready": True,
        },
    )
    preview = orchestrator.promote_workspace_changes("run-123")
    assert preview["dry_run"] is True
    assert preview["matched"] == 1
    candidate = preview["candidates"][0]
    assert candidate["changed_file_count"] == 1
    assert candidate["file_statuses"][0]["status"] == "overwrite"
    applied = orchestrator.promote_workspace_changes("run-123", apply=True)
    assert applied["dry_run"] is False
    assert applied["promoted"][0]["files_promoted"] == ["sample.txt"]
    assert applied["promoted"][0]["checksums"][0]["source_after"]
    assert (source_repo / "sample.txt").read_text() == "new"


def test_workflow_summary_captures_reference_context_evidence(repo_root):
    orchestrator = Orchestrator(repo_root)
    state = orchestrator.run_workflow(
        "feature_pipeline", mode="factory", seed_path=None, repo_path=str(repo_root)
    )
    summary = orchestrator.run_summary(state.run_id)
    assert summary["evidence"]["retrieval"]["reference_context_count"] >= 1
    assert summary["evidence"]["retrieval"]["reference_context_titles"]
    run_dir = repo_root / "artifacts" / "runs" / state.run_id
    execution_plan = json.loads(
        (run_dir / "artifacts" / "execution_plan.json").read_text()
    )
    review = json.loads((run_dir / "artifacts" / "plan_review.json").read_text())
    delivery = json.loads(
        (run_dir / "artifacts" / "implement_features_delivery.json").read_text()
    )
    assert execution_plan["reference_context"]
    assert review["cited_reference_context"]
    assert delivery["cited_reference_context"]
    assert len(delivery["cited_reference_context"]) <= 3
