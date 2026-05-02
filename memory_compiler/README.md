# Memory Compiler

`memory_compiler` turns raw memories, artifacts, and relations into a compact
Cognitive IR that can be injected into a model prompt or a local model KV cache.

## Pipeline

1. `retrieve_context` merges keyword, semantic, artifact, and relation results.
2. `cluster_context` groups related items by semantics, time, and entities.
3. `extract_primitives` asks a BYOK model provider for structured IR blocks.
4. `rank_blocks` scores blocks by relevance, confidence, recency, and impact.
5. `compress_blocks` deduplicates, preserves required diversity, and enforces limits.
6. `emit_ir` returns the final `cognitive_ir` payload.

## Minimal Usage

```python
from memory_compiler import AgentMemoryFlow, InjectionEngine, MemoryCompiler
from memory_compiler.tokenizer import SimpleTokenizer

tokenizer = SimpleTokenizer()
compiler = MemoryCompiler(
    retrieval_engine=retrieval_engine,
    artifact_store=artifact_store,
    relation_store=relation_store,
    model_provider=model_provider,
    tokenizer=tokenizer,
)

flow = AgentMemoryFlow(
    compiler=compiler,
    injection_engine=InjectionEngine(tokenizer),
    task_executor=task_executor,
    writeback_engine=writeback_engine,
)

result = flow.run_task(
    query="What context matters for this task?",
    user_id="user-123",
    session_id="session-456",
)
```

The flow enforces the integration rule that compiled IR must exist before task
execution. Remote providers receive text injection; local providers receive a KV
prefill payload with token IDs.

## Tests

Run from the workspace root in WSL:

```bash
python3 -m unittest discover -s tests -v
```
