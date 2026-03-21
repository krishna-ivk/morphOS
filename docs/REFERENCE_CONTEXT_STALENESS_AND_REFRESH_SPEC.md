# Reference Context Staleness And Refresh Spec

## Why This Spec Exists

`morphOS` already defines:

- Context Hub runtime integration
- upstream drift monitoring
- reference-context promotion
- memory governance and retention

What is still missing is the freshness model for reference context itself.

The platform still needs clear answers to these questions:

- when is reference context considered fresh enough to use?
- when should cached or attached context be refreshed?
- when should stale context stop influencing active runs?

This spec defines that freshness model.

## Executive Summary

Reference context is useful only if the platform can judge whether it is still current enough for the decision being made.

For `morphOS`, the correct posture is:

- label freshness explicitly
- refresh according to source type and risk
- degrade confidence before deleting useful references
- distinguish readable stale context from decision-grade fresh context
- tie refresh behavior back to drift, trust, and workflow risk

The goal is grounded execution without quietly reusing outdated guidance.

## Core Design Goals

- make reference freshness visible to runtimes and operators
- prevent stale context from silently driving high-risk actions
- support low-cost refresh for common cached references
- preserve provenance and version awareness across refresh cycles
- align refresh behavior with drift monitoring and memory governance

## Freshness Principle

Not all stale context is useless.
But not all readable context is safe to rely on for active decisions.

The platform should distinguish between:

- readable context
- recommended context
- decision-grade context

Freshness is what separates them.

## Canonical Freshness States

`morphOS` should support at least:

- `fresh`
- `aging`
- `stale`
- `refresh_required`
- `quarantined`

Suggested meanings:

- `fresh`
  - suitable for normal active use
- `aging`
  - still usable, but approaching refresh threshold
- `stale`
  - readable, but should not be trusted for high-risk or high-precision decisions by default
- `refresh_required`
  - must be refreshed before active decision use
- `quarantined`
  - source reliability or drift posture is bad enough that normal use should pause

## Freshness Objects

`morphOS` should support at least:

- `ReferenceFreshnessRecord`
- `RefreshAssessment`
- `RefreshDecision`
- `RefreshAttempt`
- `RefreshPolicy`

Suggested meanings:

- `ReferenceFreshnessRecord`
  - current freshness posture for a reference item
- `RefreshAssessment`
  - evaluation of age, drift, risk, and source characteristics
- `RefreshDecision`
  - whether to keep, refresh, downgrade, or quarantine
- `RefreshAttempt`
  - actual refresh execution and result
- `RefreshPolicy`
  - default rules for freshness windows by source class

## What Freshness Depends On

Freshness should be determined by a combination of:

- source type
- version specificity
- time since last verification
- observed upstream drift
- workflow risk class
- trust label
- whether the item was cached, attached, or operator-curated

Freshness should not be reduced to age alone.

## Source Classes And Refresh Pressure

Different source classes need different refresh posture.

### Official Versioned Docs

Typical posture:

- lower refresh pressure when version is pinned
- higher confidence if version and source remain stable

### Official Unversioned Docs

Typical posture:

- moderate refresh pressure
- more likely to age into `aging` or `stale`

### Changelogs And Release Notes

Typical posture:

- high refresh pressure
- often relevant only near active changes or migrations

### Cached Retrieval Bundles

Typical posture:

- short freshness window
- should refresh frequently when used in active delivery

### Human-Curated Reference Notes

Typical posture:

- may remain useful longer
- still require reevaluation when linked sources drift

## Risk-Aware Use Rules

Freshness requirements should tighten as workflow risk increases.

Examples:

- exploratory planning may allow `aging` references
- validation and policy-sensitive review may require `fresh` references
- live-action authorization may block on `refresh_required` or `quarantined` references

This prevents low-risk browsing rules from leaking into high-risk execution.

## When Context Should Refresh

Reference context should refresh when one or more of these are true:

- freshness window expired
- upstream drift signal is linked to the source
- workflow risk class requires stronger freshness
- the reference is about to influence validation, promotion, or live action
- the source is known to change frequently

Refresh should be demand-aware, not purely scheduled.

## Automatic Refresh Triggers

The first useful automatic triggers should include:

- cache age exceeds policy
- drift signal references the source
- version mismatch is detected
- a workflow requests decision-grade context and the item is only `aging` or `stale`
- operator explicitly requests a refresh

These triggers are enough to keep the first implementation practical.

## Refresh Outcomes

A refresh attempt should be able to produce at least:

- `unchanged`
- `updated`
- `version_shift_detected`
- `source_unavailable`
- `trust_degraded`
- `quarantined`

These outcomes should feed both runtime use decisions and operator surfaces.

## Stale But Readable Context

Some stale context should remain readable for:

- historical explanation
- low-risk exploration
- comparison against a refreshed source
- understanding why a past run behaved the way it did

But stale readability is not the same as active approval for current use.

## Decision-Grade Use Rules

When a reference is influencing an active decision, the platform should check whether it is decision-grade for that moment.

The first useful rule set is:

- `fresh`
  - normally decision-grade
- `aging`
  - decision-grade only for lower-risk use or when explicitly allowed by policy
- `stale`
  - not decision-grade by default
- `refresh_required`
  - must refresh before decision use
- `quarantined`
  - blocked from normal decision use

## Runtime Attachment Behavior

Attached `ContextRef` items should carry their freshness state with them.

That allows:

- planners to see freshness posture
- validators to reject stale citations
- summaries to disclose when context was aging or refreshed
- operators to inspect why the system trusted a source

Freshness should travel with the reference, not live only in a backend cache.

## Relationship To Drift

Upstream drift should immediately affect freshness posture when the source is linked.

Examples:

- a drift signal may move a reference from `fresh` to `aging`
- meaningful contract drift may move a reference straight to `refresh_required`
- trust drift may move a reference to `quarantined`

Freshness is one of the operational outputs of drift, not a separate concern.

## Relationship To Promotion

Reference-context promotion should consider freshness state.

Examples:

- `fresh` or well-governed `aging` references may support promotion assessment
- `stale` references may require refresh before promotion
- `quarantined` references should not support new promotion decisions

This keeps promoted memory from inheriting silent staleness.

## Relationship To Retention

Freshness and retention are related but different.

Examples:

- a reference may be stale but still retained for audit or history
- a fresh reference cache may still expire due to retention policy
- a quarantined record may be retained under hold but blocked from active use

Retention answers “do we keep this?”
Freshness answers “can we rely on this now?”

## Operator Surface Requirements

Operator surfaces should be able to show:

- freshness state
- last verified time
- linked source and version
- refresh reason
- whether the reference is decision-grade
- whether drift influenced the current state

This keeps context trust visible instead of implicit.

## Required Events And Artifacts

The first useful freshness model should emit at least:

- `reference.freshness_assessed`
- `reference.refresh_requested`
- `reference.refreshed`
- `reference.refresh_failed`
- `reference.quarantined`
- `reference.decision_use_blocked`

Useful artifacts include:

- `reference_freshness_record.json`
- `refresh_assessment.json`
- `refresh_attempt.json`
- `refresh_decision.json`

## First Implementation Slice

The first implementation slice should stay deliberately narrow.

Start with:

- freshness state on cached reference items
- policy windows by source class
- drift-triggered freshness downgrade
- refresh-before-use for validation and live-action paths
- operator-visible freshness and last-verified metadata

That is enough to make reference context safer before building fully automated refresh orchestration.

## Relationship To Other Specs

This spec depends on:

- `CONTEXT_HUB_RUNTIME_INTEGRATION_SPEC.md`
- `UPSTREAM_DRIFT_MONITORING_SPEC.md`
- `REFERENCE_CONTEXT_PROMOTION_SPEC.md`
- `MEMORY_GOVERNANCE_AND_RETENTION_SPEC.md`
- `DRIFT_RESPONSE_PLAYBOOK_SPEC.md`

This spec should guide:

- Context Hub caching behavior
- retrieval preflight checks
- validation citation rules
- future reference refresh jobs and dashboards
