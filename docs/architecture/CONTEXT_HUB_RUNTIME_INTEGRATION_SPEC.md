# Context Hub Runtime Integration Spec

## Why This Spec Exists

`morphOS` already defines:

- the three-layer context architecture
- the role of Context Hub as a reference-context subsystem
- an initial integration plan for retrieval, annotations, and labels

What is still missing is the runtime integration boundary:

- how reference retrieval enters actual run execution
- how retrieval requests are shaped
- how trust and access labels affect runtime behavior
- how retrieved context appears in artifacts and operator surfaces

This spec defines that boundary.

## Executive Summary

Context Hub should plug into Skyforce as a reference-context runtime service, not as the owner of workflow state or memory as a whole.

The correct runtime posture is:

- Symphony or other runtime layers request reference context through a local adapter boundary
- retrieved context is attached to runs as references, not copied blindly into operational state
- access and trust labels remain visible throughout the flow
- annotations enrich reference context without becoming workflow truth

The goal is grounded execution without collapsing reference retrieval into runtime state.

## Core Design Goals

- make reference retrieval available during real execution
- preserve the separation between reference context and operational context
- ensure trust and access labels survive end to end
- keep retrieval attributable and inspectable
- let operators see what reference material influenced important work

## Integration Boundary

The integration boundary should sit between:

- runtime consumers that need grounded reference material
- a reference-context provider layer that can search, fetch, and annotate curated sources

The runtime should never talk directly to arbitrary retrieval implementations.
It should go through a stable local boundary.

## Canonical Runtime Flow

The healthy flow should be:

1. a run or slice needs reference grounding
2. the runtime creates a scoped retrieval request
3. the Context Hub adapter resolves matching reference items
4. the runtime receives `ContextRef` results with trust and access labels
5. the selected context refs are attached to the run or action as references
6. summaries and review packets may later cite those refs

The key rule is:

- retrieved context is referenced into the run
- it is not silently converted into operational truth

## Canonical Runtime Consumers

The first useful consumers should be:

### Hermes-Style Implementation Agents

Needs:

- framework and SDK docs
- API reference grounding
- version-aware technical references

### Validation Agents

Needs:

- source-of-truth docs
- contract references
- provider behavior references

### Architect Or Planning Agents

Needs:

- broader curated docs
- infrastructure or provider guidance
- migration references

### Operator Surfaces

Needs:

- source attribution
- retrieved context snippets or references for review and inspection

## What The Runtime May Request

The runtime should support scoped reference-context requests such as:

- `reference_lookup`
- `versioned_reference_lookup`
- `repo_doc_lookup`
- `annotation_lookup`
- `context_bundle_lookup`

These are runtime use cases, not raw provider commands.

## Canonical Request Object

The runtime should support a stable request shape such as:

- `query`
- `scope`
- `repo_context`
- `workspace_id`
- `run_id`
- `consumer_lane`
- `preferred_sources`
- `required_trust_labels`
- `max_results`

This keeps runtime retrieval explicit and governable.

## Canonical Response Object

The runtime should receive structured response items such as:

- `context_id`
- `title`
- `summary`
- `uri`
- `version_label`
- `trust_label`
- `access_label`
- `source`
- `annotation_refs`
- `retrieval_reason`

This should be enough for both agents and operator surfaces to understand why the context was returned.

## Attachment Rule

Retrieved reference context should be attached to runtime work through references, not wholesale copying.

Good attachment examples:

- a `ContextRef` attached to a planning record
- a context ref listed in a validation packet
- a context ref cited in summary evidence

Bad attachment examples:

- dumping full external docs into operational state
- treating retrieved notes as workflow truth
- storing the whole retrieval response as durable memory by default

## Trust And Access Enforcement

Runtime integration must preserve:

- `trust_label`
- `access_label`

These labels should influence:

- whether an agent may see a context item
- whether the item may be used in operator-visible summaries
- whether annotations may be proposed or read
- whether the item may be cached outside a local boundary

The runtime should not strip this metadata away after retrieval.

## Caching Rules

Reference context is cacheable, but caching should remain policy-aware.

Recommended rules:

- cache by source and version where possible
- preserve trust and access labels in cache entries
- allow local caching for read-mostly reference context
- avoid treating cache as the source of authority when freshness is critical

Caching should improve performance, not obscure provenance.

## Freshness And Version Awareness

Runtime integration should prefer version-aware retrieval when applicable.

Examples:

- framework version in a repo
- SDK version tied to a workspace
- migration guidance for a specific release line

Each retrieval result should remain attributable to:

- a source
- a version label when known
- a retrieval timestamp or cached-at time

## Annotation Integration

Annotations should appear as enrichments to reference items.

The runtime should be able to:

- read annotations alongside references
- show annotation provenance
- distinguish human-authored from machine-derived notes

The runtime should not:

- treat annotations as operational state
- silently elevate machine-derived notes to trusted truth

## Runtime Surfaces That Should Cite Context

Context should show up in runtime outputs where it materially influenced the work.

Good candidates:

- planning records
- validation records
- review packets
- summary evidence
- operator inspection views

This improves auditability and reduces hallucinated “I used docs” claims without evidence.

## Relationship To Operational Context

Operational context should store:

- that reference context was used
- which refs were attached
- how it influenced the run

Operational context should not become the full reference store.

This preserves the architecture split:

- Context Hub owns reference retrieval and annotations
- runtime repos own run state and decisions

## Relationship To Persistent Memory

Persistent memory may later promote lessons derived from repeated use of reference material.

Examples:

- repeated annotation themes
- trusted usage notes
- stable subsystem guidance

But promotion to persistent memory must be deliberate.
Runtime retrieval alone should not automatically create memory records.

## Relationship To Retrieval And Mediation

Code intelligence retrieval and Context Hub retrieval should cooperate but remain distinct.

Useful split:

- code intelligence retrieval answers repo-code questions
- Context Hub answers external or curated reference questions

Mediation should choose between them based on the problem:

- code structure issue -> code retrieval first
- framework or provider behavior issue -> Context Hub retrieval first

## Runtime Failure Modes

The integration should handle:

- no relevant context found
- low-trust results only
- access denied by label
- stale cached reference
- provider unavailable

The runtime should degrade gracefully:

- proceed without reference context when safe
- route to review when grounding is required but unavailable
- record retrieval failure explicitly when it matters

## Required Events

The event taxonomy should support at least:

- `context.reference_requested`
- `context.reference_attached`
- `context.reference_denied`
- `context.reference_unavailable`
- `context.annotation_attached`

Each event should include:

- `run_id`
- consumer lane
- retrieval scope
- resulting trust posture

## Required Artifacts

The runtime integration should emit durable or inspectable artifacts when needed.

Suggested baseline:

- `context/reference_requests.json`
- `context/reference_refs.json`
- `context/annotation_refs.json`
- `context/retrieval_failures.json`

These artifacts are especially useful for:

- review
- debugging grounding failures
- operator inspection
- audit trails

## Operator Surface Expectations

Operator views should be able to show:

- which reference sources were used
- what trust posture applied
- whether the context was annotated
- whether the source was repo-local, curated, or external

The goal is not to drown operators in docs.
The goal is to make grounding visible when it matters.

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define reference-request, reference-result, and annotation-ref contracts
- a future context-core subsystem should implement the provider adapter boundary
- `skyforce-symphony` should request and attach scoped reference context during planning, execution, and validation where relevant
- `skyforce-command-centre-live` should show operator-visible reference grounding with trust and access cues
- `skyforce-api-gateway` should preserve and normalize reference grounding metadata for operator clients

## Recommended First Implementation Slice

The first useful slice should be narrow and practical:

1. implement a local adapter boundary for reference lookup
2. support repo-local docs and curated reference retrieval first
3. attach `ContextRef` objects to runs and validation packets
4. preserve trust and access labels through CLI and operator views
5. defer annotation write paths until read-only retrieval is stable

That is enough to make Context Hub runtime-relevant without confusing it with the full memory system.

## Recommended Next Specs

This spec should be followed by:

1. `EVAL_DRIVEN_ACCEPTANCE_SPEC.md`
2. `UPSTREAM_DRIFT_MONITORING_SPEC.md`
3. `REFERENCE_CONTEXT_PROMOTION_SPEC.md`

Together, those continue evaluation surfaces, upstream drift management, and the promotion path from repeated reference use into governed memory.
