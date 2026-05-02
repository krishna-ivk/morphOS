from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None

    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


@dataclass(slots=True)
class ContextItem:
    item_id: str
    item_type: str
    content: str
    created_at: str | None = None
    semantic_similarity: float = 0.0
    keyword_match: float = 0.0
    recency_score: float = 0.0
    score: float = 0.0
    entities: list[str] = field(default_factory=list)
    related_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def timestamp(self) -> datetime | None:
        return parse_timestamp(self.created_at)


@dataclass(slots=True)
class Cluster:
    cluster_id: str
    items: list[ContextItem]
    centroid_embedding: list[float]


@dataclass(slots=True)
class IRBlock:
    block_type: str
    content: str
    confidence: float
    sources: list[str]
    chain: list[str] = field(default_factory=list)
    rationale: str | None = None
    outcome: str | None = None
    severity: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    score: float = 0.0

    def as_ir_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "type": self.block_type,
            "content": self.content,
            "confidence": round(self.confidence, 4),
            "metadata": {"sources": self.sources, **self.metadata},
        }
        if self.chain:
            payload["metadata"]["chain"] = self.chain
        if self.rationale:
            payload["metadata"]["rationale"] = self.rationale
        if self.outcome:
            payload["metadata"]["outcome"] = self.outcome
        if self.severity:
            payload["metadata"]["severity"] = self.severity
        if self.score:
            payload["metadata"]["score"] = round(self.score, 4)
        return payload
