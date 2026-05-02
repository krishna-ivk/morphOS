from __future__ import annotations

from typing import Any, Protocol


class RetrievalEngine(Protocol):
    def keyword_search(self, query: str, *, top_k: int) -> list[dict[str, Any]]:
        ...

    def semantic_search(self, query: str, *, top_k: int) -> list[dict[str, Any]]:
        ...


class ArtifactStore(Protocol):
    def fetch_related_artifacts(
        self, query: str, user_id: str, *, top_k: int
    ) -> list[dict[str, Any]]:
        ...


class RelationStore(Protocol):
    def fetch_relations(
        self, query: str, user_id: str, *, top_k: int
    ) -> list[dict[str, Any]]:
        ...


class ModelProvider(Protocol):
    type: str

    def complete_json(self, prompt: str) -> dict[str, Any]:
        ...


class Tokenizer(Protocol):
    def count_tokens(self, text: str) -> int:
        ...

    def encode(self, text: str) -> list[int]:
        ...


class TaskExecutor(Protocol):
    def execute(self, query: str, injected_payload: dict[str, Any]) -> dict[str, Any]:
        ...


class WritebackEngine(Protocol):
    def writeback(
        self,
        *,
        query: str,
        user_id: str,
        session_id: str,
        cognitive_ir: dict[str, Any],
        injected_payload: dict[str, Any],
        task_result: dict[str, Any],
    ) -> None:
        ...
