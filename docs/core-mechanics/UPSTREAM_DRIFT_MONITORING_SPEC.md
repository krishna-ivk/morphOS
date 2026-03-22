# Upstream Drift Monitoring Spec

## Why This Spec Exists

`morphOS` already defines:

- semport adoption boundaries
- digital twin rollout and fidelity
- eval-driven acceptance

What is still missing is the system that notices when upstream reality has moved.

This spec defines that system.

## Executive Summary

Upstream drift is the gap between:

- the upstream behavior, contract, or concept we originally relied on
- the current upstream reality

If we do not monitor that gap, several things degrade quietly:

- semported contracts
- wrapped integrations
- digital twin fidelity
- acceptance assumptions
- operator trust

The right posture is:

- monitor upstream sources deliberately
- classify drift by severity and type
- route the right drift cases into review, twin refresh, or contract reevaluation

## Core Design Goals

- detect meaningful upstream change before it becomes production confusion
- separate harmless upstream movement from dangerous contract drift
- tie drift signals back to semport packets, twins, and local contracts
- make reevaluation explicit and auditable
- avoid treating upstream drift as an occasional manual surprise

## What Counts As Upstream Drift

Upstream drift occurs when a tracked upstream source changes in a way that may invalidate local assumptions.

Examples:

- API shape changes
- behavioral changes in orchestration or durable semantics
- changed provider docs that contradict current annotations
- upstream repo lifecycle or ownership changes
- changed integration behavior that makes a twin stale

Drift is not only code changes.
It includes documentation, contract, behavior, and trust posture changes.

## Drift Domains

The platform should monitor at least these domains:

### 1. Contract Drift

Examples:

- payload shape changes
- renamed fields
- changed event semantics

### 2. Behavioral Drift

Examples:

- an upstream workflow runtime behaves differently
- a provider API changes side effects or edge cases

### 3. Documentation Drift

Examples:

- new official guidance contradicts current reference context
- version-specific docs change meaningfully

### 4. Trust Drift

Examples:

- repo ownership or support posture changes
- an upstream project becomes unmaintained
- official guidance is replaced or deprecated

### 5. Twin Fidelity Drift

Examples:

- a live system’s current behavior diverges from its twin
- shadow comparison reveals new unsupported states

## Canonical Drift Objects

`morphOS` should support at least:

- `UpstreamSourceRef`
- `DriftSignal`
- `DriftAssessment`
- `DriftVerdict`
- `ReevaluationRequest`

Suggested meanings:

- `UpstreamSourceRef`
  - the tracked upstream source or concept
- `DriftSignal`
  - a raw indication that something changed
- `DriftAssessment`
  - the structured analysis of that change
- `DriftVerdict`
  - the current conclusion about impact
- `ReevaluationRequest`
  - the follow-up required to restore trust

## Canonical Drift Verdicts

The system should support at least:

- `no_material_drift`
- `drift_observed`
- `drift_detected`
- `drift_affects_local_contracts`
- `drift_requires_twin_refresh`
- `drift_requires_governed_review`

Suggested meanings:

- `no_material_drift`
  - change exists but does not meaningfully affect local reliance
- `drift_observed`
  - change noticed, impact still low or unclear
- `drift_detected`
  - meaningful divergence exists
- `drift_affects_local_contracts`
  - shared contracts or semports may now be stale
- `drift_requires_twin_refresh`
  - digital twin fidelity is materially impacted
- `drift_requires_governed_review`
  - human or governed acceptance is required before continuing normal trust

## Drift Sources

The first useful drift sources should be:

- official upstream docs
- official changelogs
- tagged releases or version metadata
- shadow comparison from twin systems
- failing contract or behavior evals
- explicit manual reports from operators

This keeps drift detection grounded in primary sources and real runtime signals.

## Semport Linkage

Every semport packet should record its upstream source references.

That allows drift monitoring to ask:

- which local contracts depend on this upstream concept?
- which operator surfaces might now be misleading?
- which runtime adapters should be rechecked?

Without linkage, drift signals become hard to route usefully.

## Twin Linkage

Every digital twin should record:

- the upstream system it models
- the action set it covers
- the last known fidelity basis

That allows drift monitoring to determine:

- whether the twin is still trustworthy
- whether it should be relabeled `drift_suspected`
- whether validation should narrow or pause trust in the twin

## Acceptance Linkage

Acceptance decisions that depend on upstream assumptions should be traceable back to those assumptions.

This is especially important for:

- semported contracts
- integration behavior
- high-fidelity twin trust
- reference-context-backed policy or validation claims

If drift is detected, the system should know which acceptance surfaces may need reevaluation.

## Drift Severity

The platform should classify drift severity explicitly.

Suggested levels:

- `low`
- `medium`
- `high`
- `critical`

Examples:

- low
  - wording change in docs with no behavioral impact
- medium
  - non-breaking but meaningful contract addition
- high
  - changed behavior affecting semport assumptions or twin accuracy
- critical
  - local contracts or trust posture are no longer reliable

## Reevaluation Triggers

Drift should trigger reevaluation when it affects:

- shared contracts
- operator-facing trust or wording
- digital twin fidelity
- acceptance criteria
- policy assumptions

The system should not treat every drift signal as immediate emergency, but it should always classify whether reevaluation is required.

## Monitoring Cadence

Different upstream sources may need different cadence.

Examples:

- official docs or versions: periodic polling or refresh
- twin shadow comparison: event-driven and scheduled
- operator-reported drift: immediate assessment

Cadence should match risk and update volatility.

## Required Artifacts

Drift monitoring should emit durable artifacts.

Suggested baseline:

- `drift/sources.json`
- `drift/signals.json`
- `drift/assessments.json`
- `drift/verdicts.json`
- `drift/reevaluation_requests.json`

These artifacts should feed:

- review automation
- operator alerts
- twin fidelity management
- semport reevaluation

## Required Events

The event taxonomy should support at least:

- `drift.signal_detected`
- `drift.assessed`
- `drift.verdict_changed`
- `drift.reevaluation_requested`
- `drift.twin_fidelity_changed`

Each event should include:

- upstream source ref
- affected local surface
- severity
- current verdict

## Operator Surface Expectations

Operator views should be able to show:

- what upstream source drifted
- what local surfaces may be affected
- whether the impact is contract, twin, or trust related
- whether immediate action is required

The goal is informed trust, not noisy alert spam.

## Relationship To Context Hub

Reference-context drift matters too.

Examples:

- curated docs may become stale
- annotations may contradict updated official guidance
- version labels may no longer match runtime reality

Drift monitoring should therefore cover:

- reference context freshness
- annotation staleness
- trust-label reevaluation when source credibility changes

## Relationship To Review Automation

Review automation should consume drift verdicts when relevant.

Examples:

- route drift-sensitive items to review
- refresh review packets when upstream assumptions changed
- surface drift warnings on approval or promotion paths

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define upstream source refs, drift verdicts, and reevaluation request contracts
- `skyforce-symphony` should route drift-affected runs into review or constrained posture when needed
- `skyforce-command-centre` should surface drift posture and affected local surfaces
- twin adapters and semport boundaries should record enough lineage to support drift linkage

## Recommended First Implementation Slice

The first useful slice should be narrow and high-value:

1. define `UpstreamSourceRef`, `DriftSignal`, and `DriftVerdict`
2. link semport packets and twin artifacts back to upstream sources
3. support simple drift assessment for official docs, versions, and twin shadow signals
4. emit reevaluation requests when drift affects local contracts or twin trust
5. surface drift posture in operator inspection views

That is enough to make upstream change visible before building a full drift-management platform.

## Recommended Next Specs

This spec should be followed by:

1. `REFERENCE_CONTEXT_PROMOTION_SPEC.md`
2. `WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md`
3. `DRIFT_RESPONSE_PLAYBOOK_SPEC.md`

Together, those continue memory promotion, reusable acceptance profiles, and operational response patterns.
