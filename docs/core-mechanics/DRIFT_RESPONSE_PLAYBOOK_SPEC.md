# Drift Response Playbook Spec

## Why This Spec Exists

`morphOS` already defines:

- upstream drift monitoring
- semport adoption boundaries
- digital twin rollout
- eval-driven acceptance
- workspace admin governance

What is still missing is the operational answer to this question:

What should the platform and its operators do once drift is actually detected?

This spec defines that playbook.

## Executive Summary

Drift monitoring tells us that reality moved.
The response playbook tells us how to react without improvising every time.

For `morphOS`, the right posture is:

- detect drift and classify it
- contain trust where needed
- reevaluate impacted local assumptions
- remediate or refresh the affected layer
- accept, escalate, or deprecate with explicit evidence

The goal is not to panic on every change.
The goal is to make drift response predictable, proportional, and auditable.

## Core Design Goals

- convert drift signals into clear next actions
- contain trust before stale assumptions spread
- distinguish small reevaluations from major authority events
- keep semport, twin, policy, and acceptance posture aligned
- preserve operator visibility and evidence at each stage

## Drift Response Principle

When drift is detected, the system should first reduce misplaced confidence, then decide what must be refreshed.

That means:

- trust may narrow before functionality is restored
- acceptance may pause before new proof is gathered
- twins may be relabeled before they are rebuilt
- semports may be reevaluated before they are replaced

Containment before confidence is the core rule.

## Canonical Response Stages

`morphOS` should model drift response as six stages:

1. `observe`
2. `classify`
3. `contain`
4. `reevaluate`
5. `remediate`
6. `resolve`

## Stage Meanings

### 1. Observe

Purpose:

- register that a drift signal exists

Typical inputs:

- changelog updates
- shadow comparison mismatches
- failing contract evals
- manual operator reports

Required outputs:

- `DriftSignal`
- source references
- initial impact guess

### 2. Classify

Purpose:

- determine drift type, severity, and likely blast radius

Required questions:

- is this contract, behavior, documentation, trust, or twin drift?
- which local contracts or acceptance assumptions may be affected?
- does this only require observation, or immediate trust narrowing?

Required outputs:

- `DriftAssessment`
- severity
- impacted assets
- recommended containment posture

### 3. Contain

Purpose:

- reduce the chance that stale assumptions keep driving execution

Typical containment actions:

- mark a twin `drift_suspected`
- narrow accepted action sets
- downgrade a semport packet to `review_required`
- pause live authorization for a specific integration path
- force workflow acceptance back to governed review

Containment is reversible.
It is a trust posture change, not necessarily a permanent shutdown.

### 4. Reevaluate

Purpose:

- determine whether local assumptions still hold

Typical reevaluation actions:

- rerun contract evals
- perform shadow comparisons
- inspect upstream docs and release notes
- review semport packet intent versus current upstream behavior
- review affected workflow acceptance profiles

Required outputs:

- `ReevaluationRequest`
- refreshed evidence
- revised drift verdict

### 5. Remediate

Purpose:

- restore local correctness where drift proved material

Typical remediation actions:

- refresh a twin model
- update a semported contract
- revise validation requirements
- update reference-context annotations
- tighten policy hooks or approval categories

Remediation may be local, or it may require coordination across repos.

### 6. Resolve

Purpose:

- decide the durable ending posture for the incident

Canonical outcomes:

- `accepted_no_material_change`
- `accepted_with_refresh`
- `accepted_with_restrictions`
- `escalated_for_exception`
- `deprecated_until_rebuilt`

Resolution should always leave behind a clear evidence trail.

## Severity-Aware Response

Severity should change the speed and depth of response.

### Low

Typical posture:

- observe
- classify
- leave trust unchanged unless new evidence appears

Examples:

- wording-only documentation clarification
- minor non-breaking metadata changes

### Medium

Typical posture:

- classify
- contain narrowly
- reevaluate before the next high-risk usage

Examples:

- new optional fields in a contract
- documentation updates that may alter operator assumptions

### High

Typical posture:

- immediate containment
- mandatory reevaluation
- refresh acceptance posture before reuse

Examples:

- changed upstream behavior
- twin fidelity divergence on important actions
- semport assumptions no longer clearly valid

### Critical

Typical posture:

- contain immediately
- block or defer dependent live actions
- require governed review before trust is restored

Examples:

- major contract breakage
- trust posture collapse for a key upstream dependency
- live system behavior invalidates current twin or policy assumptions

## Response Lanes By Drift Type

Different drift types need different playbooks.

### Semport Drift Lane

Use when:

- a semported concept or local contract may no longer preserve upstream intent

Expected actions:

- inspect the semport packet
- compare preserved invariants to current upstream reality
- decide whether to refresh, narrow, or retire the semport

### Twin Drift Lane

Use when:

- the modeled system and live system no longer align well enough

Expected actions:

- mark the twin with degraded fidelity
- restrict the affected action set
- rerun shadow and replay validation
- relabel trust only after refreshed proof

### Reference and Documentation Drift Lane

Use when:

- reference context or annotations may now be stale

Expected actions:

- mark the relevant reference material stale or under review
- reevaluate promoted lessons that depended on it
- refresh citations, annotations, and summary wording

### Trust and Ownership Drift Lane

Use when:

- upstream support posture, ownership, or maintenance status changes

Expected actions:

- reevaluate trust level
- review whether adoption posture should change
- consider deprecation, wrapping, or additional approval requirements

## Containment Postures

Containment should be explicit and machine-readable.

Suggested postures:

- `monitor_only`
- `review_required`
- `restricted_use`
- `live_use_paused`
- `deprecated_pending_refresh`

These postures should be visible in operator surfaces and attached to impacted assets.

## Governance And Escalation

Not every drift case requires a `super_admin`.

Use this rule:

- workspace-scoped drift with local impact may stay with `workspace_admin`
- cross-workspace trust or policy posture changes escalate to `super_admin`

Escalation is especially appropriate when drift affects:

- global policy assumptions
- cross-workspace integrations
- shared twin trust
- semports used as shared contracts
- live-action authorization categories

## Acceptance Linkage

If drift affects a workflow acceptance profile or previously accepted evidence, acceptance posture should be reevaluated explicitly.

Examples:

- a once-accepted twin may now require fresh proof
- a promotion-ready workflow may return to review-required
- previously promoted reference context may need demotion or annotation refresh

Acceptance should never silently remain green if its assumptions have become stale.

## Required Events And Artifacts

The first useful response playbook should emit at least:

- `drift.observed`
- `drift.classified`
- `drift.contained`
- `drift.reevaluation_requested`
- `drift.remediation_started`
- `drift.resolved`
- `drift.escalated`

Useful artifacts include:

- `drift_signal.json`
- `drift_assessment.json`
- `containment_record.json`
- `reevaluation_packet.md`
- `remediation_plan.md`
- `drift_resolution.md`

## Command Centre And Runtime Responsibilities

### Runtime Responsibilities

- apply automatic containment rules
- narrow trust posture during execution
- block or defer now-illegal transitions
- request reevaluation when policy or acceptance requires it

### Command Centre Responsibilities

- show current drift posture
- surface impacted assets and workflows
- route review and escalation
- display evidence and current response stage

## First Implementation Slice

The first implementation slice should be intentionally small.

Start with:

- drift severity classification
- explicit containment posture on semports and twins
- reevaluation packet generation
- governed escalation for high and critical drift
- operator-visible drift resolution records

That is enough to make drift operational before the entire platform automates every response lane.

## Relationship To Other Specs

This spec depends on:

- `UPSTREAM_DRIFT_MONITORING_SPEC.md`
- `SEMPORT_ADOPTION_BOUNDARY_SPEC.md`
- `DIGITAL_TWIN_UNIVERSE_ROLLOUT_SPEC.md`
- `EVAL_DRIVEN_ACCEPTANCE_SPEC.md`
- `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`

This spec should guide:

- semport refresh flows
- twin fidelity refresh flows
- acceptance reevaluation
- operator escalation behavior
- future deprecation and retirement policies
