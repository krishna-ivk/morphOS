from __future__ import annotations

import re

from ..interfaces import Tokenizer
from ..models import IRBlock

_TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)
_REQUIRED_TYPES = ["FACT", "CAUSE", "DECISION", "RISK"]


def _similarity(left: IRBlock, right: IRBlock) -> float:
    if left.block_type != right.block_type:
        return 0.0
    left_tokens = {token.lower() for token in _TOKEN_PATTERN.findall(left.content)}
    right_tokens = {token.lower() for token in _TOKEN_PATTERN.findall(right.content)}
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def _trim_to_token_limit(block: IRBlock, max_tokens: int, tokenizer: Tokenizer) -> IRBlock:
    if tokenizer.count_tokens(block.content) <= max_tokens:
        return block

    words = block.content.split()
    trimmed = []
    for word in words:
        candidate = " ".join(trimmed + [word])
        if tokenizer.count_tokens(candidate) > max_tokens:
            break
        trimmed.append(word)
    block.content = " ".join(trimmed).strip()
    return block


def _serialized_block_tokens(block: IRBlock, tokenizer: Tokenizer) -> int:
    metadata_text = " ".join(
        value
        for value in [block.rationale or "", block.outcome or "", " ".join(block.chain)]
        if value
    )
    return tokenizer.count_tokens(f"{block.block_type} {block.content} {metadata_text}".strip())


def compress_blocks(
    ranked_blocks: list[IRBlock],
    tokenizer: Tokenizer,
    *,
    min_confidence: float = 0.6,
    max_blocks: int = 20,
    max_tokens: int = 2000,
    diversity_required: bool = True,
) -> list[IRBlock]:
    filtered = [block for block in ranked_blocks if block.confidence >= min_confidence]

    deduplicated: list[IRBlock] = []
    for block in filtered:
        if any(_similarity(block, existing) >= 0.85 for existing in deduplicated):
            continue
        deduplicated.append(block)

    per_type: dict[str, list[IRBlock]] = {}
    for block in deduplicated:
        per_type.setdefault(block.block_type, []).append(block)

    merged: list[IRBlock] = []
    for block_type, group in per_type.items():
        group = sorted(group, key=lambda value: value.score, reverse=True)
        primary = group[0]
        if len(group) > 1:
            additions = []
            for sibling in group[1:]:
                if _similarity(primary, sibling) >= 0.45:
                    additions.append(sibling.content)
            if additions:
                primary.content = f"{primary.content} {' '.join(additions)}".strip()
        merged.append(primary)

    merged.sort(key=lambda value: value.score, reverse=True)
    selected: list[IRBlock] = []

    if diversity_required:
        for required_type in _REQUIRED_TYPES:
            candidate = next((block for block in merged if block.block_type == required_type), None)
            if candidate and candidate not in selected:
                selected.append(candidate)

    for block in merged:
        if len(selected) >= max_blocks:
            break
        if block not in selected:
            selected.append(block)

    selected = selected[:max_blocks]

    final_blocks: list[IRBlock] = []
    used_tokens = 0

    required_candidates = [block for block in selected if block.block_type in _REQUIRED_TYPES]
    optional_candidates = [block for block in selected if block.block_type not in _REQUIRED_TYPES]

    for index, block in enumerate(required_candidates):
        remaining_required = len(required_candidates) - index
        block_budget = max(1, (max_tokens - used_tokens) // remaining_required)
        trimmed = _trim_to_token_limit(block, block_budget, tokenizer)
        serialized_tokens = _serialized_block_tokens(trimmed, tokenizer)
        if serialized_tokens == 0 or serialized_tokens > (max_tokens - used_tokens):
            continue
        final_blocks.append(trimmed)
        used_tokens += serialized_tokens

    for block in optional_candidates:
        block_budget = max_tokens - used_tokens
        if block_budget <= 0:
            break
        trimmed = _trim_to_token_limit(block, block_budget, tokenizer)
        serialized_tokens = _serialized_block_tokens(trimmed, tokenizer)
        if serialized_tokens == 0 or serialized_tokens > block_budget:
            continue
        final_blocks.append(trimmed)
        used_tokens += serialized_tokens

    return final_blocks
