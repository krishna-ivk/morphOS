# Memory Governance And Retention Spec

## Why This Spec Exists

`morphOS` already defines:

- a filesystem memory topology
- reference-context runtime integration
- reference-context promotion into persistent memory
- upstream drift monitoring and response

What is still missing is the lifecycle policy for stored knowledge:

- what should be retained?
- what should expire?
- what should be demoted or deleted?
- who is allowed to make those decisions?

This spec defines that lifecycle.

## Executive Summary

Memory should not grow forever just because storage is cheap.

For `morphOS`, the correct posture is:

- retain information according to its purpose
- govern retention by trust, reuse, and scope
- degrade stale confidence before deleting useful records
- separate archival, demotion, expiration, and deletion
- keep governance and audit trails attached to lifecycle decisions

The goal is memory that stays useful, legible, and trustworthy.

## Core Design Goals

- prevent persistent memory from becoming an unbounded junk drawer
- preserve high-value lessons while letting transient state age out
- align retention with trust, drift, access, and governance posture
- make memory lifecycle actions explicit and reviewable
- keep reference context, operational context, and persistent memory distinct over time

## Governance Principle

Retention should follow purpose.

That means:

- operational context is often short-lived
- reference context may be cached and refreshed, but not treated as permanent memory
- persistent memory should keep only reusable knowledge worth carrying forward

The system should prefer confidence reduction, archival, or demotion before destructive deletion when the record may still matter.

## Canonical Lifecycle States

`morphOS` should support at least:

- `active`
- `cooling`
- `stale`
- `archived`
- `demoted`
- `expired`
- `deleted`
- `legal_hold`

Suggested meanings:

- `active`
  - current and trusted enough for normal use
- `cooling`
  - still retained, but recent reuse has dropped
- `stale`
  - retained with freshness concerns or unresolved drift
- `archived`
  - preserved for history or audit, not preferred for active reuse
- `demoted`
  - moved to a lower-trust or less-reusable layer
- `expired`
  - retention window ended and the record is no longer operationally needed
- `deleted`
  - removed according to policy
- `legal_hold`
  - protected from deletion or compaction until explicitly released

## Lifecycle Actions

The platform should support explicit lifecycle actions:

- `retain`
- `refresh`
- `downgrade_confidence`
- `demote`
- `archive`
- `expire`
- `delete`
- `hold`
- `restore`

These should be first-class actions, not implied side effects.

## Retention Lanes By Memory Layer

Different layers need different retention behavior.

### Reference Context

Default posture:

- cache and refresh
- keep provenance and version linkage
- expire local copies when freshness or access rules require it

Reference context should usually be removed by cache and access policy, not promoted into permanence by accident.

### Operational Context

Default posture:

- short retention
- aggressive compaction where safe
- preserve audit-critical artifacts longer than ephemeral execution details

Examples of shorter-lived items:

- temporary retrieval bundles
- transient directives
- in-progress planner scratch state

Examples of longer-lived operational records:

- approvals
- validation packets
- promotion decisions
- durable ledger checkpoints

### Persistent Memory

Default posture:

- retain reusable lessons and patterns longer
- reevaluate when drift or low reuse appears
- demote or archive when trust or relevance falls

Persistent memory should not be immortal.
It should remain governed.

## Retention Drivers

Retention decisions should consider at least:

- reuse frequency
- recency of use
- trust label
- access label
- drift posture
- governance requirements
- audit or compliance importance
- workflow criticality

No single driver should control everything by itself.

## Reuse And Decay

The platform should track whether a memory record is still being used meaningfully.

Useful signals include:

- attached across successful runs
- cited in validation or review packets
- selected by retrieval and accepted by agents or operators
- referenced by active workflow acceptance profiles

When reuse drops, the record should not disappear immediately.
It should move through a decay path such as:

`active -> cooling -> stale -> archived or expired`

## Trust-Aware Retention

Trust posture should influence how long records remain active.

Suggested rules:

- high-trust curated records may stay active longer
- machine-derived records should cool faster unless reinforced by review
- stale or drift-affected records should lose active status early
- unresolved trust issues may force demotion or hold further promotion

Retention should preserve trust semantics rather than flatten them.

## Drift-Aware Retention

When upstream drift appears, affected memory should not keep pretending to be fresh.

Expected behaviors:

- downgrade confidence on linked memory
- mark records `stale` or `review_required`
- reevaluate promoted lessons whose source assumptions changed
- archive or demote records that can no longer be defended

Drift should usually change active usability before it changes physical existence.

## Demotion Rules

Demotion is different from deletion.

Examples:

- promoted persistent memory becomes reference-linked archival knowledge
- active memory becomes stale archival memory
- a reusable lesson becomes a historical note with warnings attached

Demotion is useful when a record still has historical or audit value but should no longer guide current runs by default.

## Archival Rules

Archive when:

- the record still matters for audit, history, or explanation
- active reuse has dropped
- the record should remain available but not preferred

Archived records should keep:

- provenance
- access labels
- lifecycle history
- links to drift and acceptance decisions when relevant

## Expiration And Deletion Rules

Expire when:

- the retention window ended
- the record has no active governance hold
- no audit or policy rule requires longer retention

Delete when:

- expiration policy allows it
- access or legal requirements demand removal
- the record is not protected by hold or audit requirements

Deletion should be explicit and auditable for governed layers.

## Hold And Preservation Rules

Some records must not be deleted even if they are stale.

Examples:

- approval records under review
- evidence linked to incidents
- records affected by governance disputes
- compliance-sensitive operational artifacts

Use `legal_hold` or an equivalent protected state for these cases.

## Access And Scope Rules

Retention actions must respect access scope.

Examples:

- restricted workspace memory should not be archived into a broader shared scope
- public reference caches may expire quickly, but operator-only audit artifacts may require longer retention
- deletion authority may differ between workspace-scoped and global records

Scope must be preserved across the lifecycle.

## Governance And Authority

Not every lifecycle action needs the same authority.

Default posture:

- routine expiration and compaction may be automated by policy
- workspace-scoped retention exceptions may be handled by `workspace_admin`
- global retention exceptions, deletion overrides, or cross-workspace preservation rules escalate to `super_admin`

Destructive actions should never become invisible automation.

## Acceptance And Workflow Linkage

Memory records that support acceptance or workflow policy should be handled carefully.

Examples:

- a workflow acceptance profile may depend on a retained lesson
- a validation rule may cite a persistent caution
- a promotion record may rely on historical evidence

Before demotion or deletion, the system should check whether active workflows still depend on the record.

## Canonical Lifecycle Objects

`morphOS` should support at least:

- `MemoryRecord`
- `RetentionPolicy`
- `LifecycleAssessment`
- `LifecycleDecision`
- `RetentionException`
- `DeletionRecord`

Suggested meanings:

- `MemoryRecord`
  - the governed record being evaluated
- `RetentionPolicy`
  - the normal lifecycle rule for that class of record
- `LifecycleAssessment`
  - current reuse, trust, drift, and scope posture
- `LifecycleDecision`
  - the chosen action and rationale
- `RetentionException`
  - an override, hold, or non-default retention rule
- `DeletionRecord`
  - the evidence trail for destructive removal

## Required Events And Artifacts

The first useful retention model should emit at least:

- `memory.retained`
- `memory.refreshed`
- `memory.demoted`
- `memory.archived`
- `memory.expired`
- `memory.deleted`
- `memory.held`
- `memory.restored`

Useful artifacts include:

- `lifecycle_assessment.json`
- `retention_decision.json`
- `retention_exception.json`
- `deletion_record.json`

## First Implementation Slice

The first implementation slice should stay small and practical.

Start with:

- lifecycle state on persistent memory records
- decay from `active` to `stale`
- drift-triggered confidence downgrade
- archive versus delete distinction
- hold support for governed records
- workspace versus super-admin routing for destructive exceptions

That is enough to make memory lifecycle governable before building advanced compaction and automated pruning.

## Relationship To Other Specs

This spec depends on:

- `FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md`
- `REFERENCE_CONTEXT_PROMOTION_SPEC.md`
- `CONTEXT_HUB_RUNTIME_INTEGRATION_SPEC.md`
- `UPSTREAM_DRIFT_MONITORING_SPEC.md`
- `DRIFT_RESPONSE_PLAYBOOK_SPEC.md`
- `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`

This spec should guide:

- memory cleanup jobs
- promotion reevaluation
- archival and audit behavior
- future memory indexing and compaction strategies
