from __future__ import annotations

import json
from typing import Any

from ..interfaces import ModelProvider
from ..models import Cluster, IRBlock

PROMPT_TEMPLATE = """You are a memory compiler.

Given the following context cluster, extract:

- FACT (objective truths)
- CAUSE (causal chains)
- DECISION (with rationale + outcome)
- RISK (with severity)
- DEPENDENCY (relationships)
- OPEN_QUESTION (unknowns)

Rules:
- Maximize signal, remove redundancy
- Be concise and precise
- Output JSON only

Context:
{cluster_content}
"""

VALID_BLOCK_TYPES = {
    "FACT",
    "CAUSE",
    "DECISION",
    "RISK",
    "DEPENDENCY",
    "OPEN_QUESTION",
}


def _cluster_content(cluster: Cluster) -> str:
    rendered_items = []
    for item in cluster.items:
        rendered_items.append(
            json.dumps(
                {
                    "id": item.item_id,
                    "type": item.item_type,
                    "content": item.content,
                    "entities": item.entities,
                    "created_at": item.created_at,
                },
                sort_keys=True,
            )
        )
    return "\n".join(rendered_items)


def _normalize_block(raw_block: dict[str, Any], cluster: Cluster) -> IRBlock | None:
    block_type = str(raw_block.get("type", "")).upper()
    content = str(raw_block.get("content", "")).strip()
    confidence = float(raw_block.get("confidence", 0.0))
    if block_type not in VALID_BLOCK_TYPES or not content:
        return None

    sources = [str(value) for value in raw_block.get("sources", [])] or [item.item_id for item in cluster.items]
    return IRBlock(
        block_type=block_type,
        content=content,
        confidence=max(0.0, min(confidence, 1.0)),
        sources=sources,
        chain=[str(value) for value in raw_block.get("chain", [])],
        rationale=raw_block.get("rationale"),
        outcome=raw_block.get("outcome"),
        severity=raw_block.get("severity"),
        metadata={"cluster_id": cluster.cluster_id},
    )


def extract_primitives(cluster: Cluster, model_provider: ModelProvider) -> list[IRBlock]:
    prompt = PROMPT_TEMPLATE.format(cluster_content=_cluster_content(cluster))
    response = model_provider.complete_json(prompt)
    blocks = response.get("blocks", [])
    extracted: list[IRBlock] = []
    for raw_block in blocks:
        if not isinstance(raw_block, dict):
            continue
        normalized = _normalize_block(raw_block, cluster)
        if normalized is not None:
            extracted.append(normalized)
    return extracted
