from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import read_json, write_json


def vision_agent(repo_root: Path, run_dir: Path, seed_path: str | None = None) -> dict[str, Any]:
    plan = {
        "project_name": "Skyforce Project",
        "features": [
            {
                "name": "Execution Planning",
                "description": "Create a concrete execution plan",
                "priority": "high",
                "acceptance_criteria": ["Plan exists"],
                "dependencies": [],
            },
            {
                "name": "Validation Loop",
                "description": "Run tests and validate results",
                "priority": "high",
                "acceptance_criteria": ["Validation results captured"],
                "dependencies": ["Execution Planning"],
            },
        ],
    }
    path = run_dir / "artifacts" / "feature_plan.json"
    write_json(path, plan)
    return {"feature_plan_path": str(path), "backend": "local"}


def planning_agent(repo_root: Path, run_dir: Path) -> dict[str, Any]:
    feature_plan = read_json(run_dir / "artifacts" / "feature_plan.json", {"features": []})
    retrieval = read_json(run_dir / "artifacts" / "retrieval_context.json", {})
    tasks = []
    feature_to_id: dict[str, str] = {}
    for index, feature in enumerate(feature_plan.get("features", []), start=1):
        task_id = f"TASK-{index:03d}"
        feature_to_id[feature["name"]] = task_id
        tasks.append(
            {
                "id": task_id,
                "task": feature["name"],
                "description": feature["description"],
                "status": "pending",
                "assigned_agent": "coding_agent",
                "feature_ref": feature["name"],
                "depends_on": [],
            }
        )
    for task, feature in zip(tasks, feature_plan.get("features", []), strict=True):
        task["depends_on"] = [
            feature_to_id[name]
            for name in feature.get("dependencies", [])
            if name in feature_to_id
        ]
    write_json(run_dir / "artifacts" / "tasks.json", tasks)
    write_json(
        run_dir / "artifacts" / "execution_plan.json",
        {
            "task_count": len(tasks),
            "task_ids": [task["id"] for task in tasks],
            "reference_context": retrieval.get("reference_context", []),
            "reference_context_count": retrieval.get("reference_context_count", 0),
        },
    )
    return {"tasks_path": str(run_dir / "artifacts" / "tasks.json"), "backend": "local"}


def reviewer_agent(repo_root: Path, run_dir: Path) -> dict[str, Any]:
    retrieval = read_json(run_dir / "artifacts" / "retrieval_context.json", {})
    review = {
        "approved": True,
        "comments": ["Plan looks good"],
        "cited_reference_context": retrieval.get("reference_context", [])[:3],
    }
    path = run_dir / "artifacts" / "plan_review.json"
    write_json(path, review)
    return {"plan_review_path": str(path), "backend": "local"}


def debugging_agent(run_dir: Path) -> dict[str, Any]:
    results = read_json(run_dir / "validation" / "test_results.json", {"tests": []})
    tasks = []
    for index, item in enumerate(results.get("tests", []), start=1):
        if item.get("result") not in {"fail", "error"}:
            continue
        repair = {
            "id": f"REPAIR-{index:03d}",
            "task": f"Repair {item.get('name', f'failure-{index}')}",
            "description": item.get("error_message") or "Investigate failure",
            "status": "pending",
            "assigned_agent": "coding_agent",
            "feature_ref": item.get("name", "failure"),
            "depends_on": [],
        }
        message = item.get("error_message") or ""
        directives = []
        for line in [part.strip() for part in message.splitlines() if part.strip()]:
            if line.startswith("AUTO_FIX|"):
                _, target_file, search_text, replace_text = line.split("|", 3)
                directives.append(
                    {
                        "action": "replace",
                        "target_file": target_file,
                        "search_text": search_text,
                        "replace_text": replace_text,
                    }
                )
            elif line.startswith("AUTO_FIX_APPEND|"):
                _, target_file, append_text = line.split("|", 2)
                directives.append(
                    {
                        "action": "append",
                        "target_file": target_file,
                        "append_text": append_text,
                    }
                )
            elif line.startswith("AUTO_FIX_CREATE|"):
                _, target_file, file_content = line.split("|", 2)
                directives.append(
                    {
                        "action": "create",
                        "target_file": target_file,
                        "file_content": file_content,
                    }
                )
        if len(directives) == 1 and directives[0]["action"] == "replace":
            repair.update(
                {
                    "target_file": directives[0]["target_file"],
                    "search_text": directives[0]["search_text"],
                    "replace_text": directives[0]["replace_text"],
                }
            )
        if directives:
            repair["fix_directives"] = directives
        tasks.append(repair)
    path = run_dir / "artifacts" / "repair_tasks.json"
    write_json(path, tasks)
    return {"count": len(tasks), "repair_tasks_path": str(path), "backend": "local"}


def coding_agent(
    repo_root: Path,
    run_dir: Path,
    task: dict[str, Any],
    workspace_path: str | None = None,
    retrieval: dict[str, Any] | None = None,
) -> dict[str, Any]:
    workspace = Path(workspace_path or (run_dir / "workspace"))
    workspace.mkdir(parents=True, exist_ok=True)
    files_written: list[str] = []
    patch_lines: list[str] = []
    cited_reference_context = (retrieval or {}).get("reference_context", [])[:3]

    directives = task.get("fix_directives") or []
    if not directives and task.get("target_file") and task.get("search_text") is not None:
        directives = [
            {
                "action": "replace",
                "target_file": task.get("target_file"),
                "search_text": task.get("search_text"),
                "replace_text": task.get("replace_text", ""),
            }
        ]

    for directive in directives:
        action = directive.get("action", "replace")
        target_file = directive.get("target_file")
        if not target_file:
            continue
        target_path = workspace / target_file
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if action == "replace":
            original = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
            updated = original.replace(directive.get("search_text", ""), directive.get("replace_text", ""))
            target_path.write_text(updated, encoding="utf-8")
            patch_lines.append(f"replace:{target_file}")
        elif action == "append":
            original = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
            append_text = directive.get("append_text", "")
            updated = original if append_text in original else f"{original}{append_text}"
            target_path.write_text(updated, encoding="utf-8")
            patch_lines.append(f"append:{target_file}")
        elif action == "create":
            target_path.write_text(directive.get("file_content", ""), encoding="utf-8")
            patch_lines.append(f"create:{target_file}")
        if target_file not in files_written:
            files_written.append(target_file)

    work_dir = run_dir / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    note_path = work_dir / f"{task.get('id', 'TASK')}.md"
    lines = [f"# {task.get('id', 'TASK')}", "", task.get("description", "No description")]
    if retrieval and retrieval.get("exemplars"):
        lines.extend(["", "Retrieved lessons:"])
        for item in retrieval["exemplars"][:3]:
            lines.append(f"- {item.get('run_id')}: {item.get('workflow')}")
    if cited_reference_context:
        lines.extend(["", "Reference context:"])
        for item in cited_reference_context:
            lines.append(f"- {item.get('title')} ({item.get('context_id')})")
    note_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    patch_path = None
    if patch_lines:
        patch_path = run_dir / "artifacts" / f"{task.get('id', 'TASK')}_patch.txt"
        patch_path.write_text("\n".join(patch_lines) + "\n", encoding="utf-8")

    return {
        "task_id": task.get("id", "TASK"),
        "status": "completed",
        "files_written": files_written,
        "tests_written": [],
        "patch_path": str(patch_path) if patch_path else None,
        "error": None,
        "partial_output_ref": None,
        "cited_reference_context": cited_reference_context,
        "backend": "local",
    }


def architecture_agent(repo_root: Path, run_dir: Path) -> dict[str, Any]:
    path = run_dir / "artifacts" / "architecture_report.json"
    write_json(
        path,
        {"repo_path": str(repo_root), "overall_health": "healthy", "findings": []},
    )
    return {"architecture_report_path": str(path), "backend": "local"}


def learning_agent(repo_root: Path, run_dir: Path) -> dict[str, Any]:
    path = run_dir / "summaries" / "lessons.json"
    write_json(path, {"summary": "Run completed", "run_dir": str(run_dir)})
    return {"lessons_path": str(path), "backend": "local"}
