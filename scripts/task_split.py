from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pydantic import TypeAdapter

from skyforce.runtime.models import FeaturePlan, TaskItem


def main() -> int:
    feature_plan_path = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path("feature_plan.json")
    )
    tasks_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("tasks.json")
    data = FeaturePlan.model_validate(json.loads(feature_plan_path.read_text()))
    tasks = []
    feature_to_id: dict[str, str] = {}
    for index, feature in enumerate(data.features, start=1):
        task_id = f"TASK-{index:03d}"
        feature_to_id[feature.name] = task_id
        tasks.append(
            {
                "id": task_id,
                "task": feature.name,
                "description": feature.description,
                "status": "pending",
                "assigned_agent": "coding_agent",
                "feature_ref": feature.name,
                "depends_on": [],
            }
        )
    for task, feature in zip(tasks, data.features, strict=True):
        task["depends_on"] = [
            feature_to_id[name]
            for name in feature.dependencies
            if name in feature_to_id
        ]
    validated_tasks = TypeAdapter(list[TaskItem]).validate_python(tasks)
    tasks_path.write_text(
        json.dumps([item.model_dump(mode="json") for item in validated_tasks], indent=2)
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
