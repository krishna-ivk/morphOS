from __future__ import annotations

import re
from dataclasses import dataclass

_TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)


@dataclass(frozen=True, slots=True)
class EvaluationMetrics:
    reasoning_efficiency: float
    retrieval_reduction: float
    ir_utilization: float
    hallucination_rate_delta: float | None = None


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in _TOKEN_PATTERN.findall(text)}


def _referenced_blocks(cognitive_ir: dict[str, object], output: str) -> int:
    output_tokens = _tokens(output)
    referenced = 0
    for block in cognitive_ir.get("context_blocks", []):
        if not isinstance(block, dict):
            continue
        content_tokens = _tokens(str(block.get("content", "")))
        if content_tokens and len(content_tokens & output_tokens) / len(content_tokens) >= 0.25:
            referenced += 1
    return referenced


def evaluate_run(
    *,
    tokens_used: int,
    accuracy: float,
    baseline_tool_calls: int,
    actual_tool_calls: int,
    cognitive_ir: dict[str, object],
    output: str,
    baseline_hallucination_rate: float | None = None,
    actual_hallucination_rate: float | None = None,
) -> EvaluationMetrics:
    bounded_accuracy = max(min(accuracy, 1.0), 0.0)
    reasoning_efficiency = float("inf") if bounded_accuracy == 0 else tokens_used / bounded_accuracy

    if baseline_tool_calls <= 0:
        retrieval_reduction = 0.0
    else:
        retrieval_reduction = (baseline_tool_calls - actual_tool_calls) / baseline_tool_calls

    blocks = cognitive_ir.get("context_blocks", [])
    total_blocks = len(blocks) if isinstance(blocks, list) else 0
    ir_utilization = 0.0 if total_blocks == 0 else _referenced_blocks(cognitive_ir, output) / total_blocks

    hallucination_rate_delta = None
    if baseline_hallucination_rate is not None and actual_hallucination_rate is not None:
        hallucination_rate_delta = baseline_hallucination_rate - actual_hallucination_rate

    return EvaluationMetrics(
        reasoning_efficiency=reasoning_efficiency,
        retrieval_reduction=retrieval_reduction,
        ir_utilization=ir_utilization,
        hallucination_rate_delta=hallucination_rate_delta,
    )
