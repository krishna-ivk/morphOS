from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from math import exp
from typing import Any

from ..interfaces import ArtifactStore, RelationStore, RetrievalEngine
from ..models import ContextItem


def _normalize_item(payload: dict[str, Any], item_type: str) -> ContextItem:
    return ContextItem(
        item_id=str(payload.get("id") or payload.get("item_id") or payload.get("source_id")),
        item_type=str(payload.get("item_type") or item_type),
        content=str(payload.get("content", "")).strip(),
        created_at=payload.get("created_at"),
        semantic_similarity=float(payload.get("semantic_similarity", 0.0)),
        keyword_match=float(payload.get("keyword_match", 0.0)),
        entities=[str(entity) for entity in payload.get("entities", [])],
        related_ids=[str(value) for value in payload.get("related_ids", [])],
        metadata=dict(payload.get("metadata", {})),
    )


def _compute_recency_score(created_at: str | None, now: datetime) -> float:
    if not created_at:
        return 0.0
    try:
        timestamp = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError:
        return 0.0
    age_days = max((now - timestamp.astimezone(timezone.utc)).days, 0)
    return exp(-age_days / 30.0)


def retrieve_context(
    query: str,
    user_id: str,
    retrieval_engine: RetrievalEngine,
    artifact_store: ArtifactStore,
    relation_store: RelationStore,
    *,
    now: datetime | None = None,
) -> list[ContextItem]:
    current_time = now or datetime.now(timezone.utc)
    sources: list[tuple[str, list[dict[str, Any]]]] = [
        ("memory", retrieval_engine.keyword_search(query, top_k=50)),
        ("memory", retrieval_engine.semantic_search(query, top_k=30)),
        ("artifact", artifact_store.fetch_related_artifacts(query, user_id, top_k=20)),
        ("relation", relation_store.fetch_relations(query, user_id, top_k=20)),
    ]

    merged: dict[str, ContextItem] = {}
    for item_type, result_set in sources:
        for payload in result_set:
            normalized = _normalize_item(payload, item_type)
            if not normalized.item_id or not normalized.content:
                continue
            normalized.recency_score = _compute_recency_score(normalized.created_at, current_time)
            normalized.score = (
                normalized.semantic_similarity * 0.5
                + normalized.keyword_match * 0.3
                + normalized.recency_score * 0.2
            )

            if normalized.item_id not in merged:
                merged[normalized.item_id] = normalized
                continue

            existing = merged[normalized.item_id]
            merged[normalized.item_id] = replace(
                existing,
                semantic_similarity=max(existing.semantic_similarity, normalized.semantic_similarity),
                keyword_match=max(existing.keyword_match, normalized.keyword_match),
                recency_score=max(existing.recency_score, normalized.recency_score),
                score=max(existing.score, normalized.score),
                entities=sorted(set(existing.entities + normalized.entities)),
                related_ids=sorted(set(existing.related_ids + normalized.related_ids)),
                metadata={**existing.metadata, **normalized.metadata},
            )

    return sorted(merged.values(), key=lambda item: item.score, reverse=True)
