# Context Hub Integration Plan

This document defines the practical integration plan for bringing
`andrewyng/context-hub` ideas into the `morphOS` and Skyforce stack.

It focuses on three slices:

1. reference context retrieval
2. persistent annotation model
3. access labels and trust boundaries

This should be read alongside:

- `docs/CONTEXT_ARCHITECTURE.md`
- `docs/CONTEXT_HUB_EVALUATION.md`
- `docs/MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md`
- `docs/MORPHOS_V0_UPSTREAM_FEATURE_BACKLOG.md`

## Goal

Adopt the strongest parts of `context-hub` without collapsing three different
things into one vague "context system":

- reference context
- operational context
- persistent memory

The plan here is intentionally narrower than a full memory subsystem.

`context-hub` should first become the reference-context and annotation layer.

## Non-Goals

This plan does not make `context-hub` responsible for:

- live workflow state
- directives and approvals
- execution receipts
- durable checkpoints
- full episodic or semantic memory
- distributed node synchronization

Those remain outside the first Context Hub integration slice.

## Integration Principle

The right first move is:

- wrap `context-hub`
- semport the contracts we need
- keep Skyforce authoritative over operational state and trust policy

That means:

- `context-hub` should be a subsystem, not the whole context architecture
- `skyforce-core` should own shared context contracts
- a future context-core layer should own runtime integration

## Slice 1: Reference Context Retrieval

### Purpose

Give agents and operator tools a reliable way to retrieve curated external or
project-authored references.

Examples:

- framework documentation
- package and SDK references
- API docs
- deployment and infrastructure runbooks
- repo-local technical guides
- version-specific migration notes

### First Consumers

- Hermes-style implementation agents
- review and validation agents
- operator issue summaries
- future context-aware CLI retrieval

### What We Should Build First

1. A local reference-context contract in `skyforce-core`
2. A context provider adapter boundary in a future context-core subsystem
3. A retrieval path that can answer:
   - query
   - repo
   - scope
   - source
   - trust label

### Minimum Contract

The first shared contract should support:

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
- `annotation_count`

### First Milestone

Support read-only retrieval for:

- curated repo docs
- selected external references
- operator-visible source attribution

That is enough to make the feature useful without yet solving memory.

## Slice 2: Persistent Annotation Model

### Purpose

Allow humans and agents to attach durable notes to reference material without
turning annotations into runtime state.

Examples:

- "This API changed in v3"
- "Use this migration path, not the older doc example"
- "This provider rejects this payload under org policy"
- "This guide is safe for staging but not production"

### Design Rule

Annotations should be first-class, attributable, and provenance-aware.

Every annotation should distinguish:

- who wrote it
- whether it is human-authored or machine-derived
- what source item it is attached to
- how trustworthy it is

### Minimum Annotation Contract

- `annotation_id`
- `context_id`
- `author_kind`
- `author_id`
- `content`
- `confidence`
- `trust_label`
- `access_label`
- `created_at`
- `updated_at`
- `supersedes_annotation_id`

### First Milestone

Enable:

- human-authored annotations
- readback of annotations during retrieval
- lightweight annotation display in operator surfaces

### Second Milestone

Enable:

- machine-proposed annotations
- human approval or promotion of machine annotations
- stale or superseded annotation tracking

## Slice 3: Access Labels and Trust Boundaries

### Purpose

Prevent context access from becoming an ungoverned free-for-all.

This is the part that keeps reference context safe enough to use inside a real
operator and multi-agent system.

### Core Rule

Every retrieved or annotated context item should carry both:

- `access_label`
- `trust_label`

These are different.

### Access Labels

Access labels describe who is allowed to read or write the item.

Initial label set:

- `public`
- `workspace`
- `trusted-agent`
- `operator-only`
- `local-only`

### Trust Labels

Trust labels describe how much the system should rely on the item.

Initial label set:

- `verified`
- `curated`
- `annotated`
- `unverified`
- `machine-derived`

### Enforcement Goals

The first enforcement layer should answer:

- can this agent read this context?
- can this agent propose an annotation?
- can this annotation be used in operator-facing summaries?
- does this context require attribution when surfaced?

### First Milestone

Implement labels in contracts and retrieval responses before deep policy
enforcement.

That means the system can:

- classify context
- display trust/access clearly
- avoid losing policy metadata

### Second Milestone

Use labels in runtime decisions:

- hide restricted context from some agents
- require approval for some annotation writes
- prevent local-only context from syncing outward

## Target Repo Ownership

### `morphOS`

Owns:

- the architecture
- the policy model
- the meaning of access and trust labels

### `skyforce-core`

Owns:

- shared contracts for reference context and annotations
- CLI-visible projection rules

### Future context-core subsystem

Owns:

- provider adapters
- retrieval orchestration
- annotation storage integration
- query normalization

### `skyforce-command-centre` and `skyforce-command-centre-live`

Own:

- operator views of retrieved context
- annotation visibility and later annotation actions

They should not own the core retrieval semantics.

## Phased Delivery

### Phase 0: Contract and Boundary Definition

- define shared contracts in `skyforce-core`
- define provider adapter boundary
- define initial access/trust label sets

Status:

- planned

### Phase 1: Read-Only Retrieval

- retrieve curated reference context
- expose it in CLI and operator surfaces
- keep source attribution visible

Status:

- planned

### Phase 2: Human Annotation Support

- store and retrieve persistent annotations
- show them alongside reference context
- preserve provenance and labels

Status:

- planned

### Phase 3: Policy-Aware Annotation and Retrieval

- enforce access labels
- gate machine-written annotations
- suppress unsafe or low-trust context from some lanes

Status:

- planned

## Recommended Immediate Next Steps

1. Add shared contracts in `skyforce-core` for:
   - reference context item
   - context annotation
   - access label
   - trust label

2. Define a context provider adapter interface:
   - `search`
   - `get_context`
   - `list_annotations`
   - `create_annotation`

3. Pick one small retrieval pilot:
   - repo-local docs first
   - not external APIs yet

4. Surface retrieval in one operator path first:
   - CLI before dashboard

5. Only after that:
   - add annotation write paths

## Bottom Line

The correct first Context Hub integration is not "build memory."

It is:

- retrieve trustworthy reference context
- allow durable annotations on that context
- preserve access and trust labels from the beginning

That gives `morphOS` and Skyforce a usable context layer without confusing
reference retrieval with operational state or long-term memory.
