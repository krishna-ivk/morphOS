from __future__ import annotations

import json
import sys
from pathlib import Path


IGNORED = {
    ".git",
    "Archive",
    "job-search",
    "artifacts",
    "logs",
    "__pycache__",
    ".pytest_cache",
}


def main() -> int:
    repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    out_dir = (
        Path(sys.argv[2]).resolve()
        if len(sys.argv) > 2
        else Path.cwd() / "artifacts" / "current"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    files = []
    language_counts: dict[str, int] = {}
    for path in repo.rglob("*"):
        if any(part in IGNORED for part in path.parts):
            continue
        if path.is_file():
            rel = path.relative_to(repo)
            files.append(str(rel))
            suffix = path.suffix.lower() or "[no_ext]"
            language_counts[suffix] = language_counts.get(suffix, 0) + 1
    payload = {
        "repo_path": str(repo),
        "file_count": len(files),
        "top_files": files[:200],
        "extension_counts": language_counts,
    }
    (out_dir / "repo_scan.json").write_text(json.dumps(payload, indent=2) + "\n")
    (out_dir / "repo_tree.txt").write_text("\n".join(files[:500]) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
