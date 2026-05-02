from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .interfaces import Tokenizer


class InjectionMode(str, Enum):
    TEXT = "text"
    KV_CACHE = "kv_cache"


@dataclass(slots=True)
class InjectionEngine:
    tokenizer: Tokenizer

    def choose_mode(self, model_provider_type: str) -> InjectionMode:
        if model_provider_type == "local":
            return InjectionMode.KV_CACHE
        return InjectionMode.TEXT

    def build_text_payload(self, cognitive_ir: dict[str, object], user_query: str) -> str:
        block_lines = []
        for block in cognitive_ir.get("context_blocks", []):
            if not isinstance(block, dict):
                continue
            block_lines.append(
                f"- [{block.get('type')}] {block.get('content')} "
                f"(confidence={block.get('confidence')})"
            )
        return (
            "### SYSTEM MEMORY (COMPILED)\n\n"
            + "\n".join(block_lines)
            + "\n\n### TASK\n"
            + user_query
        )

    def build_kv_payload(self, cognitive_ir: dict[str, object], user_query: str) -> dict[str, object]:
        text_payload = self.build_text_payload(cognitive_ir, user_query)
        return {
            "mode": InjectionMode.KV_CACHE.value,
            "prefill_text": text_payload,
            "token_ids": self.tokenizer.encode(text_payload),
        }

    def build_payload(
        self,
        cognitive_ir: dict[str, object],
        user_query: str,
        *,
        model_provider_type: str,
    ) -> dict[str, object]:
        mode = self.choose_mode(model_provider_type)
        if mode == InjectionMode.KV_CACHE:
            return self.build_kv_payload(cognitive_ir, user_query)
        return {
            "mode": InjectionMode.TEXT.value,
            "text": self.build_text_payload(cognitive_ir, user_query),
        }
