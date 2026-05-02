from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .interfaces import ArtifactStore, ModelProvider, RelationStore, RetrievalEngine, Tokenizer
from .models import IRBlock
from .modules.cluster_context import cluster_context
from .modules.compress_blocks import compress_blocks
from .modules.emit_ir import emit_ir
from .modules.extract_primitives import extract_primitives
from .modules.rank_blocks import rank_blocks
from .modules.retrieve_context import retrieve_context
from .tokenizer import SimpleTokenizer

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class MemoryCompilerConfig:
    context_limit_tokens: int = 8000
    max_blocks: int = 20
    min_confidence: float = 0.6
    max_tokens: int = 2000
    diversity_required: bool = True
    cluster_method: str = "hierarchical"


@dataclass(slots=True)
class MemoryCompiler:
    retrieval_engine: RetrievalEngine
    artifact_store: ArtifactStore
    relation_store: RelationStore
    model_provider: ModelProvider
    tokenizer: Tokenizer = field(default_factory=SimpleTokenizer)
    config: MemoryCompilerConfig = field(default_factory=MemoryCompilerConfig)

    def compile(
        self,
        *,
        query: str,
        user_id: str,
        session_id: str,
        context_limit_tokens: int | None = None,
    ) -> dict[str, Any]:
        current_time = datetime.now(timezone.utc)
        effective_limit = context_limit_tokens or self.config.context_limit_tokens
        LOGGER.info("memory_compiler.start session_id=%s user_id=%s", session_id, user_id)

        context_items = retrieve_context(
            query,
            user_id,
            self.retrieval_engine,
            self.artifact_store,
            self.relation_store,
            now=current_time,
        )
        LOGGER.info("memory_compiler.retrieve_context count=%s", len(context_items))

        trimmed_context = self._enforce_context_limit(context_items, effective_limit)
        LOGGER.info("memory_compiler.context_limit count=%s", len(trimmed_context))

        clusters = cluster_context(trimmed_context, cluster_method=self.config.cluster_method)
        LOGGER.info("memory_compiler.cluster_context count=%s", len(clusters))

        extracted_blocks: list[IRBlock] = []
        for cluster in clusters:
            cluster_blocks = extract_primitives(cluster, self.model_provider)
            extracted_blocks.extend(cluster_blocks)
            LOGGER.info(
                "memory_compiler.extract_primitives cluster_id=%s blocks=%s",
                cluster.cluster_id,
                len(cluster_blocks),
            )

        ranked_blocks = rank_blocks(extracted_blocks, query, trimmed_context, now=current_time)
        LOGGER.info("memory_compiler.rank_blocks count=%s", len(ranked_blocks))

        compressed_blocks = compress_blocks(
            ranked_blocks,
            self.tokenizer,
            min_confidence=self.config.min_confidence,
            max_blocks=self.config.max_blocks,
            max_tokens=self.config.max_tokens,
            diversity_required=self.config.diversity_required,
        )
        LOGGER.info("memory_compiler.compress_blocks count=%s", len(compressed_blocks))

        cognitive_ir = emit_ir(compressed_blocks)
        LOGGER.info("memory_compiler.emit_ir count=%s", len(cognitive_ir["context_blocks"]))

        return {"cognitive_ir": cognitive_ir}

    def _enforce_context_limit(
        self, context_items: list[Any], context_limit_tokens: int
    ) -> list[Any]:
        selected = []
        used_tokens = 0
        for item in context_items:
            token_count = self.tokenizer.count_tokens(item.content)
            if used_tokens + token_count > context_limit_tokens:
                continue
            selected.append(item)
            used_tokens += token_count
        return selected
