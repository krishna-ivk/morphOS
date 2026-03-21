# Profile Doctrine Portfolio Scorecard Reconciliation Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio scorecard retention and history
- profile doctrine portfolio scorecard exception handling
- profile doctrine portfolio scorecard consumption policy

What is still missing is the reconciliation model for cases where multiple valid scorecard signals exist at once and the platform must decide which posture should govern a live decision.

The platform still needs clear answers to these questions:

- what happens when the current scorecard, a historical trend, an active dispute, and an exception all point in different directions?
- how should the platform reconcile competing scorecard views into one usable decision posture?
- how do we prevent consumers from cherry-picking whichever scorecard state is most convenient?

This spec defines that portfolio scorecard-reconciliation layer.

## Executive Summary

The scorecard system now includes:

- current authoritative posture
- historical snapshots
- calibration reviews
- disputes
- exceptions

That means the platform also needs a rule for reconciling these inputs when a real decision needs one coherent answer.

For `morphOS`, the correct posture is:

- treat the current authoritative scorecard as the starting point
- allow disputes, exceptions, and historical context to narrow or qualify its use
- prevent older or weaker scorecard signals from overriding stronger current truth without explicit governance
- make reconciliation explicit, auditable, and repeatable

The goal is to keep the scorecard system coherent when multiple scorecard truths are adjacent but not identical in operational meaning.

## Core Design Goals

- define how conflicting scorecard signals are reconciled
- prevent opportunistic or inconsistent scorecard interpretation
- preserve authority, freshness, and dispute posture during reconciliation
- support decision-ready scorecard posture without flattening away nuance
- preserve a durable record of reconciliation outcomes

## Reconciliation Principle

When multiple scorecard-related signals exist, the platform should reconcile them by trustworthiness, scope, freshness, and governing authority, not by convenience.

Reconciliation should therefore:

- start from the current authoritative scorecard
- narrow confidence when disputes or exceptions are active
- use history and trend only as contextual influence unless explicitly elevated

Reconciliation is not averaging.
It is deciding which scorecard posture is most appropriate for the present decision.

## What This Spec Covers

The first useful reconciliation model should cover:

- reconciliation inputs
- precedence rules
- confidence-narrowing behavior
- output posture classes
- required artifacts and operator visibility

This is enough to make scorecard conflict handling disciplined instead of improvised.

## Canonical Reconciliation Objects

`morphOS` should support at least:

- `DoctrineScorecardReconciliationInput`
- `DoctrineScorecardReconciliationRule`
- `DoctrineScorecardReconciledView`
- `DoctrineScorecardReconciliationDecision`
- `DoctrineScorecardReconciliationRecord`

Suggested meanings:

- `DoctrineScorecardReconciliationInput`
  - one relevant scorecard-related signal included in the decision
- `DoctrineScorecardReconciliationRule`
  - the rule for combining or constraining those signals
- `DoctrineScorecardReconciledView`
  - the resulting decision-ready scorecard posture
- `DoctrineScorecardReconciliationDecision`
  - the explicit outcome of the reconciliation step
- `DoctrineScorecardReconciliationRecord`
  - durable history of why one scorecard posture was used over others

## First Useful Reconciliation Inputs

The first useful reconciliation inputs should include:

- current authoritative scorecard
- recent historical trend view
- active calibration review or dispute
- active scorecard exception
- publication confidence and freshness label

These are the main signals most likely to conflict in real use.

## Precedence Rules

The first useful precedence rules should include:

- current authoritative scorecard outranks historical scorecards for present decisions
- active disputes and calibration review can narrow trust in the current scorecard
- scorecard exceptions can constrain or alter the usable view within their explicit scope
- historical trend can inform, but should not silently override current governed posture

These rules keep the scorecard system current, but not naive.

## Confidence Narrowing

Reconciliation should often narrow rather than replace.

Examples:

- if the current scorecard is `stable` but one dimension is disputed, the reconciled view may become `constrained`
- if history shows recent sharp decline, the reconciled view may require deeper validation even if the latest scorecard looks improved
- if an exception affects one publication view, only that scope should narrow

This keeps the result precise instead of dramatically binary.

## First Useful Reconciled View Classes

The first useful reconciled view classes should include:

- `current_authoritative`
- `current_with_constraints`
- `current_with_required_validation`
- `historically_informative_only`
- `temporarily_restricted_by_exception`

Suggested meanings:

- `current_authoritative`
  - the current scorecard may be used as published for this purpose
- `current_with_constraints`
  - the current scorecard is still primary, but caveats materially narrow its use
- `current_with_required_validation`
  - the scorecard may guide the decision only if deeper evidence is checked now
- `historically_informative_only`
  - history matters, but not as a governing current posture
- `temporarily_restricted_by_exception`
  - exception handling narrows or redirects how the scorecard may be used in this case

These classes help consumers know what kind of scorecard truth they are actually holding.

## Relationship To Consumption Policy

Reconciliation should feed consumption, not replace it.

Suggested posture:

- consumption policy says what kind of use is allowed
- reconciliation determines which scorecard posture is valid to consume in this case
- high-consequence uses should require reconciliation when multiple scorecard signals materially conflict

This keeps use policy and truth resolution aligned.

## Relationship To Publication

Published views may differ in detail but should reconcile back to one coherent decision posture.

Examples:

- a compact summary and governance-detail view may both exist, but the reconciled view should preserve the stronger caveat set
- stale publication should not outrank a fresher governance-detail view

This prevents audience-tailored publication from becoming contradictory truth.

## Relationship To Retention And History

History should matter, but within bounds.

Examples:

- recent trend may explain why confidence is narrowed
- old archived snapshots should not directly steer present operational decisions
- historical scorecards may matter more in retrospective or calibration contexts than in current gating contexts

This keeps history useful without letting it dominate current truth.

## Relationship To Disputes And Exceptions

Disputes and exceptions should remain visible during reconciliation.

Examples:

- a disputed dimension may force `current_with_required_validation`
- a publication exception may restrict which view is valid for a specific audience
- unresolved exception plus dispute may justify stronger narrowing than either alone

This makes uncertainty additive instead of ignorable.

## Operator Surface Requirements

Operator surfaces should be able to show:

- which scorecard inputs were reconciled
- which one governed the final posture
- what caveats narrowed confidence
- whether history, dispute, or exception changed the default current view
- whether deeper validation is now required

This makes reconciliation visible instead of hidden in human interpretation.

## Required Artifacts

The first useful reconciliation artifacts should include:

- `scorecard_reconciliation_inputs.json`
- `scorecard_reconciliation_decisions.json`
- `scorecard_reconciled_views.json`
- `scorecard_reconciliation_summary.md`

Suggested contents:

- `scorecard_reconciliation_inputs.json`
  - machine-readable list of scorecard-related inputs considered for the decision
- `scorecard_reconciliation_decisions.json`
  - explicit reconciliation outcomes and applied rules
- `scorecard_reconciled_views.json`
  - resulting decision-ready scorecard posture
- `scorecard_reconciliation_summary.md`
  - high-level explanation of why one scorecard view governed over the others

## First Useful Outcomes

The first useful reconciliation outcomes should include:

- `use_current_scorecard_as_is`
- `use_current_scorecard_with_constraints`
- `require_deeper_validation_before_use`
- `treat_history_as_context_only`
- `defer_due_to_unresolved_scorecard_conflict`

These outcomes make reconciliation concrete and reusable.

## Governance Expectations

Reconciliation should reduce ambiguity, not create another layer of interpretive theater.

Suggested posture:

- use reconciliation mainly when conflicting scorecard signals materially matter
- prefer current governed truth unless evidence requires narrowing
- preserve enough traceability that later review can confirm whether reconciliation was reasonable

## Non-Goals

This spec does not define:

- a universal mathematical merge function for all scorecard states
- replacement of judgment in complex governance disputes
- publication rendering logic in detail

It only defines how the platform should reconcile multiple scorecard-related signals into one coherent usable posture for present decisions.

## Bottom Line

`morphOS` should reconcile scorecard conflicts explicitly.

When current scorecard truth, historical trend, disputes, and exceptions all matter at once, the platform should decide which posture governs, how confidence narrows, and what further validation is required instead of leaving consumers to improvise.
