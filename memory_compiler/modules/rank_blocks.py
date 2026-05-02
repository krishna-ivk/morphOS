from __future__ import annotations

import re
from datetime import datetime, timezone

from ..models import ContextItem, IRBlock, parse_timestamp

_TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)
_SEVERITY_SCORES = {"low": 0.4, "medium": 0.7, "high": 1.0}
_TYPE_IMPACT = {
    "FACT": 0.6,
    "CAUSE": 0.75,
    "DECISION": 0.9,
    "RISK": 1.0,
    "DEPENDENCY": 0.65,
    "OPEN_QUESTION": 0.5,
}


def _tokenize(text: str) -> set[str]:
    return {token.lower() for token in _TOKEN_PATTERN.findall(text)}


def _compute_relevance(query: str, block: IRBlock) -> float:
    query_tokens = _tokenize(query)
    block_tokens = _tokenize(block.content)
    if not query_tokens or not block_tokens:
        return 0.0
    return len(query_tokens & block_tokens) / len(query_tokens)


def _compute_recency(block: IRBlock, context_items: dict[str, ContextItem], now: datetime) -> float:
    timestamps = [
        parse_timestamp(context_items[source].created_at)
        for source in block.sources
        if source in context_items and context_items[source].created_at
    ]
    timestamps = [timestamp for timestamp in timestamps if timestamp]
    if not timestamps:
        return 0.0
    newest = max(timestamps)
    age_days = max((now - newest.astimezone(timezone.utc)).days, 0)
    return max(0.0, 1.0 - (age_days / 30.0))


def _estimate_impact(block: IRBlock) -> float:
    if block.block_type == "RISK":
        return _SEVERITY_SCORES.get((block.severity or "").lower(), 0.5)
    return _TYPE_IMPACT.get(block.block_type, 0.5)


def rank_blocks(
    blocks: list[IRBlock],
    query: str,
    context_items: list[ContextItem],
    *,
    now: datetime | None = None,
) -> list[IRBlock]:
    current_time = now or datetime.now(timezone.utc)
    item_index = {item.item_id: item for item in context_items}
    ranked: list[IRBlock] = []

    for block in blocks:
        relevance = _compute_relevance(query, block)
        recency = _compute_recency(block, item_index, current_time)
        impact = _estimate_impact(block)
        block.score = (
            relevance * 0.4
            + block.confidence * 0.2
            + recency * 0.2
            + impact * 0.2
        )
        ranked.append(block)

    return sorted(ranked, key=lambda value: value.score, reverse=True)
