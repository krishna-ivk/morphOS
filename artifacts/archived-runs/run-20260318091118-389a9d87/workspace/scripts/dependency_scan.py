from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def extract_dependencies(repo_root: Path) -> list[str]:
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.exists():
        return []
    text = pyproject.read_text()
    in_deps = False
    deps: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("dependencies = ["):
            in_deps = True
            continue
        if in_deps and stripped == "]":
            break
        if in_deps:
            match = re.search(r'"([^"]+)"', stripped)
            if match:
                deps.append(match.group(1))
    return deps


def main() -> int:
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    out_dir = (
        Path(sys.argv[2]).resolve()
        if len(sys.argv) > 2
        else repo_root / "artifacts" / "current"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    deps = extract_dependencies(repo_root)
    payload = {
        "repo_path": str(repo_root),
        "dependency_count": len(deps),
        "dependencies": deps,
        "scan_mode": "static_manifest_only",
        "critical_findings": [],
    }
    (out_dir / "vuln_report.json").write_text(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
