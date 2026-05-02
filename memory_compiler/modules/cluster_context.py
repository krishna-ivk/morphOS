from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from datetime import timedelta

from ..models import Cluster, ContextItem

_TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)
_EMBEDDING_DIMENSIONS = 16


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in _TOKEN_PATTERN.findall(text)}


def _embedding(text: str) -> list[float]:
    vector = [0.0] * _EMBEDDING_DIMENSIONS
    token_counts = Counter(_TOKEN_PATTERN.findall(text.lower()))
    for token, count in token_counts.items():
        digest = hashlib.md5(token.encode("utf-8")).digest()
        slot = digest[0] % _EMBEDDING_DIMENSIONS
        vector[slot] += float(count)

    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def _average_embedding(items: list[ContextItem]) -> list[float]:
    if not items:
        return [0.0] * _EMBEDDING_DIMENSIONS
    vectors = [_embedding(item.content) for item in items]
    return [sum(values) / len(values) for values in zip(*vectors, strict=True)]


def _temporal_proximity(left: ContextItem, right: ContextItem) -> bool:
    if not left.timestamp or not right.timestamp:
        return False
    return abs(left.timestamp - right.timestamp) <= timedelta(days=7)


def _shared_entities(left: ContextItem, right: ContextItem) -> bool:
    return bool(set(left.entities).intersection(right.entities))


def _semantic_similarity(left: ContextItem, right: ContextItem) -> float:
    left_tokens = _tokens(left.content)
    right_tokens = _tokens(right.content)
    if not left_tokens or not right_tokens:
        return 0.0
    union = left_tokens | right_tokens
    return len(left_tokens & right_tokens) / len(union)


def cluster_context(
    context_items: list[ContextItem],
    *,
    cluster_method: str = "hierarchical",
) -> list[Cluster]:
    if cluster_method not in {"hierarchical", "kmeans"}:
        raise ValueError(f"Unsupported cluster method: {cluster_method}")

    clusters: list[list[ContextItem]] = []
    for item in sorted(context_items, key=lambda value: value.score, reverse=True):
        assigned = False
        for cluster in clusters:
            similarity = max(_semantic_similarity(item, candidate) for candidate in cluster)
            if similarity >= 0.25 or any(_shared_entities(item, candidate) for candidate in cluster):
                cluster.append(item)
                assigned = True
                break
            if any(_temporal_proximity(item, candidate) for candidate in cluster) and similarity >= 0.15:
                cluster.append(item)
                assigned = True
                break
        if not assigned:
            clusters.append([item])

    return [
        Cluster(
            cluster_id=f"cluster-{index + 1}",
            items=items,
            centroid_embedding=_average_embedding(items),
        )
        for index, items in enumerate(clusters)
    ]
