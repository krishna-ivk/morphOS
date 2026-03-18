# Context Architecture

This document defines the context architecture for `morphOS` and its relationship to the Skyforce runtime.

The purpose is to separate three problems that are often collapsed into one vague idea of "context":

1. reference context
2. operational context
3. persistent memory

If we do not separate them, the system will drift into an unclear mix of:

- documentation retrieval
- runtime state storage
- long-term learning

Those are different concerns and should be designed as different layers.

## Executive Summary

The context architecture for the platform should be:

- `Reference Context`
  - external and curated knowledge used to ground agents
- `Operational Context`
  - live and near-live workflow/run/task state needed for execution
- `Persistent Memory`
  - long-lived lessons, patterns, and reusable knowledge extracted from completed work

Each layer has different:

- read/write patterns
- trust and privacy requirements
- storage models
- synchronization behavior
- policy boundaries

## Why This Separation Matters

Without this separation:

- external docs get mixed with internal run state
- agent notes get treated like production memory
- workflow receipts become pseudo-memory
- policy boundaries become unclear
- operators cannot tell what is ephemeral versus durable

For Skyforce, that would quickly create confusion across:

- Symphony
- Harness
- Command Centre
- CLI
- OpenClaw
- future mobile and distributed nodes

## Layer 1: Reference Context

### Purpose

Reference context is read-mostly material used to ground agents in accurate external or curated information.

Examples:

- framework documentation
- SDK references
- API documentation
- cloud provider setup guides
- deployment notes
- version-specific technical references
- curated annotations on those references

### Primary Use Cases

- Hermes needs exact library or framework behavior
- Architect needs provider or infrastructure references
- OpenClaw needs grounded technical context when drafting summaries
- validation agents need source-of-truth docs during checks

### Characteristics

- mostly read-only
- relatively stable
- can be versioned
- can be cached locally
- should be attributable to a source
- should support annotations

### Good Storage Model

- external retrieval and caching layer
- curated document index
- annotation store

### Good Fit

- `andrewyng/context-hub`

### Not For

- live workflow state
- execution receipts
- directive state
- approval logs
- agent health state

## Layer 2: Operational Context

### Purpose

Operational context is the state required to run, observe, and control the current system.

Examples:

- active issue context
- workflow progress
- execution envelopes
- execution receipts
- validation summaries
- directives and approvals
- node status
- event stream
- artifact references
- run checkpoints

### Primary Use Cases

- Symphony needs it for orchestration
- Harness needs it for execution pickup and receipts
- Command Centre needs it for operator visibility
- CLI needs it for inspection and summaries
- validation agents need it for merge-readiness decisions

### Characteristics

- read and write heavy
- highly dynamic
- often issue-scoped or run-scoped
- must support correlation across artifacts
- may need replay
- must support policy and approval checks

### Good Storage Model

- runtime state stores
- artifact directories
- event logs
- issue workspace state
- API-backed state exposure

### Good Fit

- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-command-centre`
- `skyforce-core` contracts

### Not For

- long-term semantic memory
- broad external doc retrieval
- speculative learning archives

## Layer 3: Persistent Memory

### Purpose

Persistent memory is the long-lived knowledge the system should retain beyond a single run or issue.

Examples:

- known good fix patterns
- architecture lessons
- policy violation patterns
- repo-specific practices
- deployment lessons
- reusable workflow heuristics
- operator preferences
- communication patterns for OpenClaw

### Primary Use Cases

- learning from repeated incidents
- reducing repeated mistakes
- improving future planning and implementation
- preserving knowledge across runs, repos, and devices

### Characteristics

- durable
- slower-moving than operational context
- must be curated or gated
- should support confidence and provenance
- should distinguish human-authored from machine-derived knowledge

### Good Storage Model

- structured memory store
- indexed knowledge base
- memory graph or document index
- provenance-aware artifact store

### Good Fit

- future dedicated memory subsystem
- likely separate from the main runtime repos

### Not For

- transient run state
- immediate execution control
- one-off external lookups

## Context Access Rules

Different agent lanes should have different context access profiles.

### Hermes

Needs:

- reference context
- issue-scoped operational context
- limited persistent memory relevant to implementation and fixes

Should not automatically get:

- broad privileged operational history
- unrestricted global memory write access

### Architect

Needs:

- reference context
- broad operational context
- architecture and policy memory

May need wider read access than Hermes, but still should not bypass policy.

### OpenClaw

Needs:

- reference context
- summary-oriented operational context
- communication and operator memory

Should usually avoid direct write access to low-level runtime state.

### Validation Agent

Needs:

- issue-scoped operational context
- validation-related reference context
- limited access to historical validation and policy memory

Should remain narrow and evidence-driven.

## Privacy and Trust Boundaries

The system should eventually support trust-aware context access.

Examples:

- some context is public to all agents
- some context is lane-restricted
- some context is node-local only
- some context requires human approval to expose

Recommended future access labels:

- `public`
- `workspace`
- `trusted-runtime`
- `operator-only`
- `sensitive`

These labels should apply to both operational context and persistent memory.

## Synchronization Model

Because Skyforce is hybrid, context cannot assume one always-on server.

### Reference Context

- cacheable across nodes
- sync on demand
- safe to replicate selectively

### Operational Context

- authoritative source should be clear per context family
- some state is local-first
- some state is orchestrator-first
- some state is artifact-derived

### Persistent Memory

- sync should be deliberate
- conflicts need provenance-aware merge rules
- some memory should remain local-only

## Relationship To `morphOS`

`morphOS` should define:

- layer boundaries
- context contracts
- access rules
- policy expectations
- memory taxonomy

It should not implement the main operational context runtime.

That belongs in Skyforce.

## Relationship To Skyforce

### `skyforce-core`

Should own shared contracts for:

- `ContextRef`
- `ArtifactRef`
- `MemoryRecord`
- `ContextAccessLabel`
- `OperationalContextSummary`

### `skyforce-symphony`

Should own:

- workflow and run context
- checkpoints
- directives
- event-based operational state

### `skyforce-harness`

Should own:

- execution receipts
- node-local execution context
- adapter result context

### `skyforce-command-centre`

Should own:

- human presentation of operational context
- approval and control views
- summarized context for intervention

### Future Context or Memory Repo

Should own:

- persistent memory services
- memory indexing
- long-term retrieval
- confidence and provenance scoring

## Recommended Build Order

1. Formalize shared contracts for context and memory references in `skyforce-core`.
2. Standardize operational context families already present in Skyforce.
3. Introduce trust labels for context access.
4. Define persistent memory record types.
5. Decide whether the memory subsystem deserves its own repo.

## What Not To Do

Do not:

- treat reference retrieval as the whole context system
- use execution receipts as long-term memory
- let every agent write global memory freely
- blur operational context and persistent memory
- make `morphOS` itself the operational runtime store

## Final Recommendation

The platform should use a three-layer context model:

- reference context
- operational context
- persistent memory

This is the cleanest way to make `morphOS` architecturally strong while keeping Skyforce practical and buildable.
