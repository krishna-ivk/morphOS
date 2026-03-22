# P1 Summary Pyramid Spec

## Origin & Influence
- **Source Influence**: StrongDM `Pyramid Summaries`
- **Local Owner(s)**: `morphOS`, `skyforce-core`, `skyforce-symphony`, `sky-force-command-centre-live`

## Core Concept
Operators and agents need drastically different granularities of information when viewing a workflow execution. A 5,000-line durably executed trace of an agent writing tests is useless to a Workspace Admin trying to click "Approve". 

The Summary Pyramid defines how execution state is continuously synthesized into hierarchical abstractions.

This is the intended `P1` summary contract, not a claim that every current `P0` proving run already emits the full pyramid. The local `P0` demo may still produce receipt, evidence, sync-update, and sync-intent artifacts first while the full summary layer is being formalized.

## Implementation (The Pyramid Levels)
1. **The Headline (`sky-force-command-centre-live`)**: 
   - A deterministic 1-line string classifying the current state (e.g., `Blocked: Tests Failed`).
   - Sourced from `skyforce-symphony` emitting explicit `run.status` events.
2. **The TL;DR (`sky-force-command-centre-live`)**: 
   - A 1-paragraph synthesis of what the agent just attempted and why it needs human review. 
   - Usually LLM-generated locally by an evaluation agent wrapping the dense payload.
3. **The Evidence (`skyforce-harness`)**: 
   - The absolute, unredacted truth. For `Harness`, this is the direct JSON projection of `ExecutionReceipt` containing exact `exitCode`, `stdout`, and `stderr` buffers. 
   - Stored persistently in filesystem artifacts first, with richer indexing added later if needed.

## Multi-Repo Responsibilities
- `skyforce-harness` is ONLY responsible for Level 3 (Evidence). It must never attempt to summarize its own failures using an LLM. 
- `skyforce-symphony` is responsible for Level 1 (Headline) state transitions.
- `sky-force-command-centre-live` orchestrates Level 2 (TL;DR) on the client side or via a dedicated GraphQL resolver to keep the core orchestration bus lightweight.

### `skyforce-symphony`

Supplies the run-level orchestration truth.

### `skyforce-command-centre`

Chooses the right summary layer for the operator surface.

### `morphOS`

Defines the relationship between the layers.

## P1 Success Condition

This spec is successful when:

1. the `P0` golden path can be understood from a short summary
2. operators do not need raw logs for routine interpretation
3. the short and full summaries both point back to the same evidence

## Bottom Line

The summary pyramid is how the factory stays inspectable at human speed without hiding the underlying truth.
