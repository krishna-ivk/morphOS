from __future__ import annotations

import unittest

from memory_compiler.compiler import MemoryCompiler
from memory_compiler.evaluation import evaluate_run
from memory_compiler.flow import AgentMemoryFlow
from memory_compiler.injection import InjectionEngine, InjectionMode
from memory_compiler.modules.cluster_context import cluster_context
from memory_compiler.modules.compress_blocks import compress_blocks
from memory_compiler.modules.rank_blocks import rank_blocks
from memory_compiler.modules.retrieve_context import retrieve_context
from memory_compiler.models import IRBlock
from memory_compiler.tokenizer import SimpleTokenizer


class FakeRetrievalEngine:
    def keyword_search(self, query: str, *, top_k: int) -> list[dict[str, object]]:
        return [
            {
                "id": "mem-1",
                "content": "Switched vector index from flat to HNSW for faster memory retrieval.",
                "keyword_match": 0.9,
                "created_at": "2026-04-25T10:00:00+00:00",
                "entities": ["vector-index", "retrieval"],
            },
            {
                "id": "mem-2",
                "content": "Latency spiked after the shard rebalance finished.",
                "keyword_match": 0.8,
                "created_at": "2026-04-26T10:00:00+00:00",
                "entities": ["latency", "shard"],
            },
        ]

    def semantic_search(self, query: str, *, top_k: int) -> list[dict[str, object]]:
        return [
            {
                "id": "mem-1",
                "content": "Switched vector index from flat to HNSW for faster memory retrieval.",
                "semantic_similarity": 0.95,
                "created_at": "2026-04-25T10:00:00+00:00",
                "entities": ["vector-index", "retrieval"],
            },
            {
                "id": "mem-3",
                "content": "Decision: keep the compiler deterministic and prefer a cheap extraction model.",
                "semantic_similarity": 0.9,
                "created_at": "2026-04-27T10:00:00+00:00",
                "entities": ["compiler", "model"],
            },
        ]


class FakeArtifactStore:
    def fetch_related_artifacts(
        self, query: str, user_id: str, *, top_k: int
    ) -> list[dict[str, object]]:
        return [
            {
                "id": "art-1",
                "content": "Runbook notes dependency on tokenizer alignment for KV cache injection.",
                "semantic_similarity": 0.6,
                "created_at": "2026-04-24T10:00:00+00:00",
                "entities": ["tokenizer", "kv-cache"],
            }
        ]


class FakeRelationStore:
    def fetch_relations(
        self, query: str, user_id: str, *, top_k: int
    ) -> list[dict[str, object]]:
        return [
            {
                "id": "rel-1",
                "content": "Shard rebalance caused indexing pressure which increased latency.",
                "semantic_similarity": 0.85,
                "created_at": "2026-04-26T11:00:00+00:00",
                "entities": ["latency", "shard"],
                "related_ids": ["mem-2"],
            }
        ]


class FakeModelProvider:
    type = "remote"

    def complete_json(self, prompt: str) -> dict[str, object]:
        if "HNSW" in prompt:
            return {
                "blocks": [
                    {
                        "type": "FACT",
                        "content": "The retrieval stack now uses an HNSW vector index.",
                        "confidence": 0.94,
                        "sources": ["mem-1"],
                    },
                    {
                        "type": "DECISION",
                        "content": "The team chose a deterministic compiler with a cheap extraction model.",
                        "confidence": 0.91,
                        "sources": ["mem-3"],
                        "rationale": "Control cost and keep outputs stable.",
                        "outcome": "Predictable IR generation.",
                    },
                ]
            }
        return {
            "blocks": [
                {
                    "type": "CAUSE",
                    "content": "Shard rebalance increased indexing pressure, which then raised latency.",
                    "confidence": 0.88,
                    "sources": ["mem-2", "rel-1"],
                    "chain": ["rebalance", "indexing pressure", "latency"],
                },
                {
                    "type": "RISK",
                    "content": "KV cache injection can break if tokenizer alignment drifts.",
                    "confidence": 0.86,
                    "sources": ["art-1"],
                    "severity": "high",
                },
                {
                    "type": "OPEN_QUESTION",
                    "content": "How should session persistence be managed for KV cache reuse?",
                    "confidence": 0.72,
                    "sources": ["art-1"],
                },
            ]
        }


class FakeTaskExecutor:
    def __init__(self) -> None:
        self.payloads: list[dict[str, object]] = []

    def execute(self, query: str, injected_payload: dict[str, object]) -> dict[str, object]:
        self.payloads.append(injected_payload)
        return {
            "answer": "Shard rebalance raised latency, and tokenizer alignment matters for KV cache injection.",
            "used_ir": "SYSTEM MEMORY" in str(injected_payload),
        }


class FakeWritebackEngine:
    def __init__(self) -> None:
        self.records: list[dict[str, object]] = []

    def writeback(self, **kwargs: object) -> None:
        self.records.append(dict(kwargs))


class MemoryCompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tokenizer = SimpleTokenizer()
        self.retrieval_engine = FakeRetrievalEngine()
        self.artifact_store = FakeArtifactStore()
        self.relation_store = FakeRelationStore()
        self.model_provider = FakeModelProvider()

    def test_retrieve_context_deduplicates_and_scores(self) -> None:
        items = retrieve_context(
            "memory compiler latency",
            "user-1",
            self.retrieval_engine,
            self.artifact_store,
            self.relation_store,
        )
        self.assertEqual([item.item_id for item in items[:2]], ["mem-1", "mem-3"])
        self.assertEqual(len([item for item in items if item.item_id == "mem-1"]), 1)

    def test_cluster_context_groups_related_items(self) -> None:
        items = retrieve_context(
            "latency after shard rebalance",
            "user-1",
            self.retrieval_engine,
            self.artifact_store,
            self.relation_store,
        )
        clusters = cluster_context(items)
        latency_cluster = next(cluster for cluster in clusters if any(item.item_id == "mem-2" for item in cluster.items))
        self.assertTrue(any(item.item_id == "rel-1" for item in latency_cluster.items))

    def test_rank_and_compress_blocks_enforce_diversity_and_limit(self) -> None:
        blocks = [
            IRBlock("FACT", "Compiler uses HNSW.", 0.95, ["mem-1"]),
            IRBlock("CAUSE", "Rebalance led to latency.", 0.9, ["mem-2"]),
            IRBlock("DECISION", "Use cheap model.", 0.92, ["mem-3"]),
            IRBlock("RISK", "Tokenizer drift breaks KV cache.", 0.93, ["art-1"], severity="high"),
            IRBlock("FACT", "Compiler uses HNSW index.", 0.91, ["mem-1"]),
        ]
        items = retrieve_context(
            "compiler kv cache latency",
            "user-1",
            self.retrieval_engine,
            self.artifact_store,
            self.relation_store,
        )
        ranked = rank_blocks(blocks, "compiler kv cache latency", items)
        compressed = compress_blocks(ranked, self.tokenizer, max_tokens=20)
        self.assertEqual({block.block_type for block in compressed[:4]}, {"FACT", "CAUSE", "DECISION", "RISK"})
        total_tokens = sum(self.tokenizer.count_tokens(block.content) for block in compressed)
        self.assertLessEqual(total_tokens, 20)

    def test_compile_returns_cognitive_ir(self) -> None:
        compiler = MemoryCompiler(
            retrieval_engine=self.retrieval_engine,
            artifact_store=self.artifact_store,
            relation_store=self.relation_store,
            model_provider=self.model_provider,
            tokenizer=self.tokenizer,
        )
        result = compiler.compile(
            query="Why did latency rise and what matters for KV cache injection?",
            user_id="user-1",
            session_id="session-1",
        )
        blocks = result["cognitive_ir"]["context_blocks"]
        self.assertGreaterEqual(len(blocks), 4)
        self.assertTrue(any(block["type"] == "RISK" for block in blocks))
        self.assertTrue(any(block["type"] == "DECISION" for block in blocks))

    def test_injection_uses_required_ir(self) -> None:
        payload = {
            "ir_version": "0.1",
            "context_blocks": [
                {"type": "FACT", "content": "Compiler uses HNSW.", "confidence": 0.9},
            ],
        }
        engine = InjectionEngine(self.tokenizer)
        text = engine.build_payload(payload, "Answer the user", model_provider_type="remote")
        kv = engine.build_payload(payload, "Answer the user", model_provider_type="local")
        self.assertEqual(text["mode"], InjectionMode.TEXT.value)
        self.assertIn("SYSTEM MEMORY", text["text"])
        self.assertEqual(kv["mode"], InjectionMode.KV_CACHE.value)
        self.assertTrue(kv["token_ids"])

    def test_agent_memory_flow_compiles_injects_executes_and_writes_back(self) -> None:
        compiler = MemoryCompiler(
            retrieval_engine=self.retrieval_engine,
            artifact_store=self.artifact_store,
            relation_store=self.relation_store,
            model_provider=self.model_provider,
            tokenizer=self.tokenizer,
        )
        executor = FakeTaskExecutor()
        writeback = FakeWritebackEngine()
        flow = AgentMemoryFlow(
            compiler=compiler,
            injection_engine=InjectionEngine(self.tokenizer),
            task_executor=executor,
            writeback_engine=writeback,
        )
        result = flow.run_task(
            query="Why did latency rise?",
            user_id="user-1",
            session_id="session-1",
        )
        self.assertTrue(result["cognitive_ir"]["context_blocks"])
        self.assertEqual(len(executor.payloads), 1)
        self.assertEqual(len(writeback.records), 1)
        self.assertEqual(writeback.records[0]["task_result"], result["task_result"])

    def test_evaluate_run_computes_spec_metrics(self) -> None:
        cognitive_ir = {
            "context_blocks": [
                {
                    "type": "CAUSE",
                    "content": "Shard rebalance increased latency.",
                    "confidence": 0.9,
                },
                {
                    "type": "RISK",
                    "content": "Tokenizer alignment can break KV cache injection.",
                    "confidence": 0.9,
                },
            ]
        }
        metrics = evaluate_run(
            tokens_used=100,
            accuracy=0.8,
            baseline_tool_calls=10,
            actual_tool_calls=4,
            cognitive_ir=cognitive_ir,
            output="The shard rebalance increased latency. Tokenizer alignment matters for KV cache injection.",
            baseline_hallucination_rate=0.2,
            actual_hallucination_rate=0.05,
        )
        self.assertEqual(metrics.reasoning_efficiency, 125)
        self.assertEqual(metrics.retrieval_reduction, 0.6)
        self.assertEqual(metrics.ir_utilization, 1.0)
        self.assertAlmostEqual(metrics.hallucination_rate_delta or 0, 0.15)


if __name__ == "__main__":
    unittest.main()
