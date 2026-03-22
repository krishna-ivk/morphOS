from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .io import read_json, write_json


def _context_id_for(path: Path) -> str:
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:12]
    return f"ctx-{digest}"


class ContextHub:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.annotations_path = self.repo_root / "artifacts" / "context_hub" / "annotations.json"

    def _doc_paths(self) -> list[Path]:
        docs: list[Path] = []
        for pattern in ("README.md", "docs/**/*.md"):
            docs.extend(self.repo_root.glob(pattern))
        return sorted({path for path in docs if path.is_file()})

    def _context_record(self, path: Path) -> dict[str, Any]:
        rel = path.relative_to(self.repo_root)
        title = path.stem.replace("_", " ").replace("-", " ").title()
        if path.name.lower() == "readme.md":
            title = "Repo Home"
        return {
            "context_id": _context_id_for(rel),
            "title": title,
            "uri": str(rel),
            "path": str(path),
            "source": "repo-local-docs",
            "trust_label": "curated",
            "access_label": "public",
            "summary": path.read_text(encoding="utf-8")[:240].strip(),
        }

    def _all_annotations(self) -> list[dict[str, Any]]:
        return read_json(self.annotations_path, [])

    def _write_annotations(self, items: list[dict[str, Any]]) -> None:
        write_json(self.annotations_path, items)

    def search(self, query: str, consumer: str, limit: int = 8) -> dict[str, Any]:
        q = query.lower()
        matches = []
        for path in self._doc_paths():
            text = path.read_text(encoding="utf-8")
            if q in text.lower() or q in path.name.lower():
                matches.append(self._context_record(path))
        return {"matched": len(matches), "results": matches[:limit], "consumer": consumer}

    def list_annotations(self, context_id: str, consumer: str) -> list[dict[str, Any]]:
        annotations = []
        for item in self._all_annotations():
            if item.get("context_id") != context_id:
                continue
            if item.get("status") != "active":
                continue
            annotations.append(item)
        return annotations

    def get_context(self, context_id: str, consumer: str) -> dict[str, Any]:
        for path in self._doc_paths():
            record = self._context_record(path)
            if record["context_id"] != context_id:
                continue
            annotations = self.list_annotations(context_id, consumer)
            return {
                **record,
                "annotation_count": len(annotations),
                "annotations": annotations,
            }
        raise FileNotFoundError(f"context not found: {context_id}")

    def create_annotation(
        self,
        context_id: str,
        consumer: str,
        author_kind: str,
        author_id: str,
        content: str,
        trust_label: str | None = None,
        access_label: str | None = None,
    ) -> dict[str, Any]:
        items = self._all_annotations()
        annotation = {
            "annotation_id": f"ann-{len(items) + 1:04d}",
            "context_id": context_id,
            "consumer": consumer,
            "author_kind": author_kind,
            "author_id": author_id,
            "content": content,
            "trust_label": trust_label or "annotated",
            "access_label": access_label or "public",
            "status": "active" if author_kind == "human" else "pending_review",
        }
        items.append(annotation)
        self._write_annotations(items)
        return annotation

    def promote_annotation(self, annotation_id: str, approver: str) -> dict[str, Any]:
        items = self._all_annotations()
        for item in items:
            if item.get("annotation_id") != annotation_id:
                continue
            item["status"] = "active"
            item["approved_by"] = approver
            self._write_annotations(items)
            return item
        raise FileNotFoundError(f"annotation not found: {annotation_id}")
