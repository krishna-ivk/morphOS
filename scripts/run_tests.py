from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from skyforce.runtime.models import ValidationCheck, ValidationReport


def parse_junit(path: Path) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    testcase_nodes = root.findall(".//testcase")
    tests = []
    passed = failed = skipped = 0
    for case in testcase_nodes:
        name = (
            f"{case.attrib.get('classname', '')}::{case.attrib.get('name', '')}".strip(
                ":"
            )
        )
        duration_ms = int(float(case.attrib.get("time", "0")) * 1000)
        failure = case.find("failure")
        error = case.find("error")
        skipped_node = case.find("skipped")
        if failure is not None:
            result = "fail"
            failed += 1
            error_message = (
                failure.attrib.get("message") or (failure.text or "").strip()
            )
            stack_trace = (failure.text or "").strip() or None
        elif error is not None:
            result = "error"
            failed += 1
            error_message = error.attrib.get("message") or (error.text or "").strip()
            stack_trace = (error.text or "").strip() or None
        elif skipped_node is not None:
            result = "skip"
            skipped += 1
            error_message = skipped_node.attrib.get("message") or None
            stack_trace = None
        else:
            result = "pass"
            passed += 1
            error_message = None
            stack_trace = None
        tests.append(
            {
                "name": name,
                "result": result,
                "duration_ms": duration_ms,
                "error_message": error_message,
                "stack_trace": stack_trace,
            }
        )
    total = len(tests)
    return {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
        },
        "overall_result": "fail" if failed else "pass",
        "tests": tests,
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    run_id = sys.argv[1] if len(sys.argv) > 1 else "local-run"
    validation_dir = repo_root / "artifacts" / "current"
    if len(sys.argv) > 2:
        validation_dir = Path(sys.argv[2])
    validation_dir.mkdir(parents=True, exist_ok=True)
    result_path = validation_dir / "test_results.json"
    validation_report_path = validation_dir / "validation_report.json"
    output_path = validation_dir / "test_results.txt"
    tests_dir = repo_root / "tests"
    if not tests_dir.exists():
        payload = {
            "run_id": run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {"total": 0, "passed": 0, "failed": 0, "skipped": 0},
            "overall_result": "pass",
            "tests": [],
        }
        result_path.write_text(json.dumps(payload, indent=2) + "\n")
        validation_report_path.write_text(
            ValidationReport(
                run_id=run_id,
                overall_result="pass",
                checks=[
                    ValidationCheck(
                        name="pytest",
                        result="skip",
                        details="No tests directory found.",
                    )
                ],
            ).model_dump_json(indent=2)
            + "\n"
        )
        output_path.write_text("No tests directory found.\n")
        return 0
    with tempfile.TemporaryDirectory() as temp_dir:
        junit_path = Path(temp_dir) / "pytest.xml"
        command = [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "tests",
            "--ignore=tests/test_runtime.py",
            "--ignore=tests/test_context_hub.py",
            f"--junitxml={junit_path}",
        ]
        completed = subprocess.run(
            command, cwd=repo_root, text=True, capture_output=True, check=False
        )
        output_path.write_text(completed.stdout + completed.stderr)
        payload = {
            "run_id": run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **parse_junit(junit_path),
        }
        result_path.write_text(json.dumps(payload, indent=2) + "\n")
        validation_report_path.write_text(
            ValidationReport(
                run_id=run_id,
                overall_result=payload["overall_result"],
                checks=[
                    ValidationCheck(
                        name="pytest",
                        result="pass"
                        if payload["overall_result"] == "pass"
                        else "fail",
                        evidence_ref=str(result_path),
                        details=f"Executed {payload['summary']['total']} tests.",
                    )
                ],
            ).model_dump_json(indent=2)
            + "\n"
        )
        return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
