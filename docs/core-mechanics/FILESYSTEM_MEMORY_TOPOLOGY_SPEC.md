# Filesystem Memory Topology Spec

This document defines how `morphOS` should lay out memory-like data on the
filesystem.

It is the third follow-on specification from the starred repo
gene-transfusion backlog and is primarily informed by:

- `volcengine/OpenViking`
- StrongDM `The Filesystem`
- the morphOS context architecture
- the git-native work ledger spec

The goal is to make filesystem-backed memory:

- inspectable
- classifiable
- policy-aware
- composable across agents
- safe to sync selectively

without collapsing all stored knowledge into one vague “memory folder.”

## Why This Spec Exists

The current morphOS docs already separate:

1. reference context
2. operational context
3. persistent memory

What is still missing is the filesystem topology that makes that separation
real.

Without a concrete topology:

- reference docs get mixed with live run state
- receipts and summaries get mistaken for memory
- durable operational history becomes hard to search
- memory sync rules stay vague
- trust and access labels become hard to enforce

This spec exists to prevent that drift.

## Executive Summary

The correct filesystem memory topology for morphOS is:

- `reference-context/`
  - curated, attributable grounding material
- `operational-context/`
  - active and recent run state needed for execution
- `persistent-memory/`
  - durable lessons, patterns, and promoted knowledge

These layers may point to each other.
They must not become the same thing.

The key rule is:

- operational truth is for running the system now
- persistent memory is for helping future runs
- reference context is for grounding against external or curated knowledge

## Top-Level Layout

Recommended v0 layout:

```text
memory/
  reference-context/
    sources/
    annotations/
    indexes/
  operational-context/
    runs/
    issues/
    workspaces/
    nodes/
    indexes/
  persistent-memory/
    patterns/
    lessons/
    policies/
    workflows/
    preferences/
    indexes/
```

## Layer 1: Reference Context

### Purpose

Reference context stores material used to ground agents against external or
curated truth.

Examples:

- framework docs
- API references
- deployment runbooks
- repo-authored guides
- curated notes on those sources

### Filesystem Shape

Recommended layout:

```text
memory/reference-context/
  sources/
    <context_id>.json
  annotations/
    <context_id>/
      <annotation_id>.json
  indexes/
    by_source.json
    by_repo.json
    by_trust_label.json
```

### Reference Context Record

Minimum fields:

- `context_id`
- `kind`
- `source`
- `title`
- `summary`
- `uri`
- `version_label`
- `trust_label`
- `access_label`
- `updated_at`

### Rules

- reference context is mostly read-only
- it must remain attributable to a source
- annotations may extend it, but should not replace the source record
- reference context should be safe to cache and re-index

## Layer 2: Operational Context

### Purpose

Operational context stores the state required to execute, inspect, and control
current work.

Examples:

- active run posture
- receipts
- summaries
- directives
- approval packets
- event projections
- work ledger entries

### Filesystem Shape

Recommended layout:

```text
memory/operational-context/
  runs/
    <run_id>/
      index.json
      workflow_run.json
      task_executions/
      directives/
      approvals/
      receipts/
      summaries/
      evidence/
      ledger_ref.json
  issues/
    <issue_identifier>/
      active_run.txt
      run_refs.json
  workspaces/
    <workspace_id>/
      active_runs.json
      approval_queue.json
  nodes/
    <node_id>.json
  indexes/
    active_runs.json
    blocked_runs.json
    pending_approvals.json
```

### Rules

- operational context should support fast current-state lookup
- it may be high-churn
- it should prefer stable ids over free-text-only indexing
- it may expire or compact over time
- it should remain clearly distinct from long-term memory

### Relationship To The Work Ledger

The work ledger is an operational memory surface with durable history.

That means:

- ledger data belongs conceptually under operational context
- it may live on a separate git-native branch or worktree
- operational context should point to ledger records rather than duplicate them
  unnecessarily

## Layer 3: Persistent Memory

### Purpose

Persistent memory stores knowledge promoted beyond a single run.

Examples:

- known good remediation patterns
- architecture lessons
- reusable deployment cautions
- workflow heuristics
- validated operator preferences

### Filesystem Shape

Recommended layout:

```text
memory/persistent-memory/
  patterns/
    <memory_id>.json
  lessons/
    <memory_id>.json
  policies/
    <memory_id>.json
  workflows/
    <memory_id>.json
  preferences/
    <memory_id>.json
  indexes/
    by_kind.json
    by_repo.json
    by_confidence.json
    by_authority.json
```

### Persistent Memory Record

Minimum fields:

- `memory_id`
- `kind`
- `title`
- `summary`
- `derived_from_refs`
- `confidence`
- `trust_label`
- `access_label`
- `author_kind`
- `author_id`
- `promoted_at`
- `last_reviewed_at`

### Rules

- persistent memory should be promoted, not casually dumped
- machine-derived memory should not become trusted automatically
- every record should preserve provenance
- persistent memory should support later revalidation or demotion

## Access And Trust Labels

Every stored object across all three layers should carry:

- `access_label`
- `trust_label`

These labels should not be bolted on later.
They are part of the topology itself.

### Initial Access Labels

- `public`
- `workspace`
- `trusted-agent`
- `operator-only`
- `local-only`

### Initial Trust Labels

- `verified`
- `curated`
- `annotated`
- `unverified`
- `machine-derived`

## Promotion Paths Between Layers

The topology should support controlled movement between layers.

### Reference Context -> Persistent Memory

Example:

- a repeated annotation on a trusted deployment guide becomes a promoted lesson

### Operational Context -> Persistent Memory

Example:

- repeated fix patterns from multiple runs become a reusable remediation pattern

### Operational Context -> Reference Context

Usually not allowed directly.

Reason:

- run state should not silently rewrite source-of-truth references

## Indexing Strategy

Every layer should have its own indexes.

### Why

- lookup patterns differ by layer
- trust rules differ by layer
- retention rules differ by layer

### Minimum indexing axes

- by stable id
- by repo or workspace
- by issue or run where relevant
- by trust label
- by access label
- by updated time

## Retention Rules

### Reference Context

- retain until source invalidation or curation change

### Operational Context

- keep active runs hot
- compact or archive older runs
- preserve durable evidence refs

### Persistent Memory

- retain until superseded, demoted, or explicitly removed by policy

## Sync Rules

Different layers should sync differently.

### Reference Context

- safe to cache and distribute selectively

### Operational Context

- sync only when needed for execution, audit, or operator visibility
- avoid broad uncontrolled replication

### Persistent Memory

- sync more conservatively than reference context
- require label-aware filtering

## Agent Access Model

### Hermes-style implementation agent

Default access:

- reference context: scoped read
- operational context: issue-scoped read, limited write through runtime
- persistent memory: limited read, no direct trusted write

### Architect-style planning agent

Default access:

- reference context: broader read
- operational context: broader read
- persistent memory: broader read, proposed write only

### Support-oriented communication agent

Default access:

- reference context: read
- operational context: summary-oriented read
- persistent memory: communication and operator preference read

### Validation agent

Default access:

- reference context: validation-scoped read
- operational context: issue-scoped read
- persistent memory: narrow read to policy and historical validation patterns

## Relationship To Contracts

This topology should later project into shared contracts, not replace them.

At minimum it should reinforce:

- `ContextRef`
- `MemoryRecord`
- `ArtifactRef`
- `WorkflowRun`
- `TaskExecution`

The filesystem layout is the storage topology.
The contracts remain the interoperability language.

## Ownership

### `morphOS` owns

- the topology doctrine
- layer meanings
- promotion rules between layers

### `skyforce-core` owns

- shared contracts
- indexing helpers
- CLI projection rules

### `skyforce-symphony` owns

- operational-context projections tied to workflow state

### `skyforce-harness` owns

- receipt and evidence surfaces feeding operational context

### future context subsystem owns

- reference-context retrieval integration
- annotation surfaces
- memory promotion tooling

## What To Build After This Spec

Once this model is accepted, the next useful follow-on specs are:

1. `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`
2. `SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md`
3. `WORKFLOW_PACK_AND_REGISTRY_SPEC.md`

## Bottom Line

The correct morphOS filesystem memory topology is:

- three-layered
- label-aware
- promotion-aware
- agent-readable
- separate from raw source history

It should make memory visible and governable without turning every stored file
into the same kind of thing.
