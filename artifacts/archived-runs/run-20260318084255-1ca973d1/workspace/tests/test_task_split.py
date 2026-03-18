import json
import subprocess
import sys


def test_task_split_emits_schema_valid_tasks(tmp_path):
    feature_plan = {
        "project_name": "Demo",
        "features": [
            {
                "name": "Feature A",
                "description": "Do A",
                "priority": "critical",
                "acceptance_criteria": ["A works"],
                "dependencies": [],
            },
            {
                "name": "Feature B",
                "description": "Do B",
                "priority": "high",
                "acceptance_criteria": ["B works"],
                "dependencies": ["Feature A"],
            },
        ],
    }
    feature_plan_path = tmp_path / "feature_plan.json"
    tasks_path = tmp_path / "tasks.json"
    feature_plan_path.write_text(json.dumps(feature_plan))
    subprocess.run(
        [
            sys.executable,
            "scripts/task_split.py",
            str(feature_plan_path),
            str(tasks_path),
        ],
        check=True,
    )
    tasks = json.loads(tasks_path.read_text())
    assert tasks[0]["id"] == "TASK-001"
    assert tasks[0]["assigned_agent"] == "coding_agent"
    assert tasks[1]["depends_on"] == ["TASK-001"]
