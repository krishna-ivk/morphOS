from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from .compiler import MemoryCompiler
from .injection import InjectionEngine
from .interfaces import TaskExecutor, WritebackEngine

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class AgentMemoryFlow:
    compiler: MemoryCompiler
    injection_engine: InjectionEngine
    task_executor: TaskExecutor
    writeback_engine: WritebackEngine

    def run_task(self, *, query: str, user_id: str, session_id: str) -> dict[str, Any]:
        compiled = self.compiler.compile(
            query=query,
            user_id=user_id,
            session_id=session_id,
        )
        cognitive_ir = compiled["cognitive_ir"]
        if not cognitive_ir.get("context_blocks"):
            raise ValueError("MemoryCompiler emitted no IR blocks; IR is required for task execution.")

        injected_payload = self.injection_engine.build_payload(
            cognitive_ir,
            query,
            model_provider_type=self.compiler.model_provider.type,
        )
        LOGGER.info("agent_memory_flow.inject mode=%s", injected_payload.get("mode"))

        task_result = self.task_executor.execute(query, injected_payload)
        self.writeback_engine.writeback(
            query=query,
            user_id=user_id,
            session_id=session_id,
            cognitive_ir=cognitive_ir,
            injected_payload=injected_payload,
            task_result=task_result,
        )

        return {
            "cognitive_ir": cognitive_ir,
            "injected_payload": injected_payload,
            "task_result": task_result,
        }
