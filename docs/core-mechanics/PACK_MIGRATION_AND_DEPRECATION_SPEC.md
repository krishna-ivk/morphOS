# Pack Migration And Deprecation Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow packs and registries
- workflow profile compatibility
- semport adoption boundaries
- upstream drift monitoring

What is still missing is the transition model for reusable assets over time.

The platform still needs clear answers to these questions:

- how does a workflow pack move from one version to another?
- when is a pack deprecated rather than upgraded?
- how are attached profiles, tool expectations, and semported concepts migrated safely?

This spec defines that transition model.

## Executive Summary

Reusable packs should evolve through explicit migrations, not silent replacement.

For `morphOS`, the correct posture is:

- version packs deliberately
- declare migration paths explicitly
- separate upgrade, replacement, and deprecation
- assess compatibility before moving active workflows
- preserve evidence about why an old pack was retired

The goal is safe evolution without hidden runtime drift.

## Core Design Goals

- make pack evolution explicit and auditable
- prevent breaking changes from reaching active workflows silently
- support controlled replacement of outdated packs and profiles
- keep migration aligned with compatibility, governance, and drift posture
- preserve operator clarity during transition periods

## Transition Principle

Every reusable delivery asset should have a known lifecycle:

- introduced
- active
- migrating
- deprecated
- retired

The system should know which state a pack is in before selecting it for new work.

## What This Spec Covers

The first useful transition model should cover:

- workflow pack upgrades
- workflow template replacements
- acceptance profile migrations
- related tool-family expectation changes
- semported concept refresh or retirement

This is enough to make ecosystem change governable.

## Canonical Transition Objects

`morphOS` should support at least:

- `PackLifecycleRecord`
- `MigrationPlan`
- `MigrationAssessment`
- `MigrationVerdict`
- `DeprecationNotice`
- `RetirementRecord`

Suggested meanings:

- `PackLifecycleRecord`
  - current lifecycle state of a pack or related asset
- `MigrationPlan`
  - declared path from one version or asset to another
- `MigrationAssessment`
  - compatibility and risk analysis for that transition
- `MigrationVerdict`
  - approval to proceed, pause, or block
- `DeprecationNotice`
  - operator-visible warning that an asset should stop being selected
- `RetirementRecord`
  - evidence trail for final removal from active use

## Canonical Lifecycle States

The platform should support at least:

- `active`
- `migration_available`
- `migration_recommended`
- `migration_required`
- `deprecated`
- `retired`

Suggested meanings:

- `active`
  - normal selection allowed
- `migration_available`
  - a newer compatible path exists
- `migration_recommended`
  - newer path should be preferred for new work
- `migration_required`
  - continued use should be limited or blocked pending transition
- `deprecated`
  - existing runs may finish, but new selection should stop by default
- `retired`
  - no longer selectable for active use

## Upgrade Versus Replacement

The system should distinguish:

- `upgrade`
  - same pack lineage, newer compatible version
- `replacement`
  - different pack or template takes over the role
- `deprecation`
  - current asset is being phased out
- `retirement`
  - asset is no longer active in the ecosystem

Without this distinction, every change looks the same and migration logic becomes vague.

## Migration Triggers

Migration should be considered when one or more of these are true:

- a newer pack version is available
- compatibility rules changed
- upstream drift invalidates current assumptions
- semported concepts were refreshed significantly
- tool families or policy hooks changed
- governance posture changed enough that older workflows no longer fit

Migration is not only about new features.
It is also about preserving safe behavior.

## Compatibility-Gated Migration

No migration should proceed without compatibility assessment.

The migration check should compare at least:

- workflow template compatibility
- attached acceptance profiles
- required tool families
- execution-mode support
- policy-hook availability
- governance expectations

If migration breaks one of these, the move should be blocked or routed for review.

## Template And Profile Migration

Workflow template migration should evaluate the attached acceptance contract, not just the template file.

Examples:

- a new template version may require a stricter acceptance profile
- a deprecated profile may need replacement before the template can upgrade
- a pack replacement may preserve workflow purpose but change evidence families or eval categories

Migration should treat the workflow-plus-profile pair as a governed unit.

## Tool And Runtime Migration

Pack evolution may depend on tool and runtime changes.

Examples:

- a newer pack may require different tool families
- a new pack may assume digital twin validation exists
- a replacement workflow may require parallel-slice support

These conditions should be checked before migration is recommended for general use.

## Semport-Aware Migration

Some pack changes are really semport changes in disguise.

Examples:

- upstream orchestration concepts were reinterpreted locally
- policy meaning changed while upstream design intent stayed similar
- a pack’s behavior must be refreshed because a semported concept drifted

In those cases, migration should link back to the relevant semport packet and preserved invariants.

## Deprecation Rules

Deprecation should be explicit and operator-visible.

Deprecate when:

- a newer safer path exists
- compatibility drift makes continued default selection unsafe
- drift or governance posture weakens trust in the current pack
- the pack is being replaced by a clearer local or semported model

Deprecated packs may still support existing runs for a bounded period.
They should not remain the silent default.

## Retirement Rules

Retire when:

- migration paths are complete or sufficient
- active dependencies have been cleared or explicitly excepted
- operator notice and governance requirements were satisfied
- audit records for the transition exist

Retirement should remove the asset from normal workflow selection.

## Existing Run Handling

Migration policy should distinguish:

- new runs
- in-flight runs
- archived historical runs

Suggested posture:

- new runs should prefer non-deprecated packs
- in-flight runs may finish on the original pack when safe
- historical runs should keep their original pack references for audit and replay understanding

The platform should not rewrite history just because a new version exists.

## Exceptions And Grace Periods

Some migrations need a controlled grace period.

Examples:

- pack replacement is ready but operator training is incomplete
- one workspace depends on a deprecated profile temporarily
- a runtime feature rollout is still partial

These cases should use explicit migration exceptions with:

- scope
- rationale
- expiration
- approving authority
- linked compatibility evidence

## Operator Surface Requirements

Operator surfaces should be able to show:

- current pack version
- lifecycle state
- available migration target
- deprecation warnings
- compatibility blockers
- active migration exceptions

This helps teams understand whether a workflow is current, tolerated, or on borrowed time.

## Required Events And Artifacts

The first useful transition model should emit at least:

- `pack.migration_assessed`
- `pack.migration_recommended`
- `pack.migration_blocked`
- `pack.deprecated`
- `pack.retired`
- `pack.migration_exception_granted`

Useful artifacts include:

- `migration_plan.md`
- `migration_assessment.json`
- `deprecation_notice.md`
- `retirement_record.json`

## First Implementation Slice

The first implementation slice should stay intentionally narrow.

Start with:

- lifecycle state on workflow packs
- migration target metadata
- compatibility-gated migration assessment
- deprecation warnings for new workflow selection
- operator-visible migration and replacement notices

That is enough to make pack evolution safe before modeling full automated rollout across every asset family.

## Relationship To Other Specs

This spec depends on:

- `WORKFLOW_PACK_AND_REGISTRY_SPEC.md`
- `WORKFLOW_PROFILE_COMPATIBILITY_SPEC.md`
- `SEMPORT_ADOPTION_BOUNDARY_SPEC.md`
- `UPSTREAM_DRIFT_MONITORING_SPEC.md`
- `DRIFT_RESPONSE_PLAYBOOK_SPEC.md`

This spec should guide:

- pack versioning policy
- migration preflight checks
- deprecation messaging
- future workflow-pack rollout tooling
