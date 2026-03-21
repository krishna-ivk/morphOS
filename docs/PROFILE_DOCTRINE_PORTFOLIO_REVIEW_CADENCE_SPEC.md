# Profile Doctrine Portfolio Review Cadence Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio decision audit
- profile doctrine portfolio baseline, SLO, and escalation posture
- intervention, exit, and reentry behavior

What is still missing is the recurring operating rhythm for reviewing doctrine portfolio state and decisions on purpose instead of only in reaction to alerts or crises.

The platform still needs clear answers to these questions:

- when should doctrine portfolio health, watchpoints, and decisions be reviewed?
- what belongs in a daily, weekly, or wave-level doctrine review?
- how do we prevent doctrine review from being either constant noise or rare neglect?

This spec defines that portfolio review-cadence layer.

## Executive Summary

Doctrine portfolio governance should have a rhythm, not just a reaction pattern.

Review cadence should define the recurring checkpoints where operators examine:

- current portfolio health
- active watchpoints and alerts
- open escalations
- pending or recent decisions
- intervention and normalization posture

For `morphOS`, the correct posture is:

- use a small number of predictable review cadences
- assign each cadence a different scope and purpose
- keep urgent issues reactive, but keep important portfolio stewardship scheduled
- connect cadence outputs to triage, escalation, and learning

The goal is to make doctrine oversight continuous without making it chaotic.

## Core Design Goals

- define recurring review rhythms for doctrine portfolio operations
- separate lightweight review from deep review
- keep important portfolio signals from going stale between incidents
- connect review outputs to concrete next actions
- preserve a durable record of cadence-based oversight

## Cadence Principle

Healthy doctrine oversight should be both reactive and scheduled.

Review cadence should therefore:

- catch weak signals before they become urgent
- revisit important open decisions before they drift
- create predictable moments for escalation, correction, and learning

Good cadence reduces both panic and neglect.

## What This Spec Covers

The first useful review-cadence model should cover:

- review layers by frequency
- scope and purpose of each review
- expected participants or authority layers
- review outputs and artifacts
- relationship to intervention and learning

This is enough to make doctrine oversight operationally rhythmic.

## Canonical Cadence Objects

`morphOS` should support at least:

- `DoctrineReviewCadence`
- `DoctrineReviewSession`
- `DoctrineReviewAgenda`
- `DoctrineReviewOutcome`
- `DoctrineReviewRecord`

Suggested meanings:

- `DoctrineReviewCadence`
  - the declared recurring rhythm for a specific kind of doctrine portfolio review
- `DoctrineReviewSession`
  - one concrete execution of that review
- `DoctrineReviewAgenda`
  - the expected inputs and topics for that review
- `DoctrineReviewOutcome`
  - the actions, confirmations, or escalations produced
- `DoctrineReviewRecord`
  - durable history of cadence-based doctrine review

## First Useful Review Layers

The first useful review layers should include:

- `daily_watch_review`
- `weekly_portfolio_review`
- `wave_readiness_review`
- `post_wave_review`

Suggested meanings:

- `daily_watch_review`
  - short operational review of watchpoints, alerts, and urgent queue changes
- `weekly_portfolio_review`
  - broader stewardship review of health posture, load, aging work, and escalation pressure
- `wave_readiness_review`
  - targeted review of doctrine posture before meaningful release or freeze commitments
- `post_wave_review`
  - review of what the recent wave revealed about doctrine strength, drift, or decision quality

These layers give doctrine review both tempo and depth.

## Daily Watch Review

Use this cadence to examine:

- current alerts
- fast-aging watchpoints
- queue pressure and immediate deferrals
- current escalations or authority conflicts needing attention

The purpose is not deep theory.
It is keeping the portfolio from drifting unattended between bigger reviews.

## Weekly Portfolio Review

Use this cadence to examine:

- portfolio health trends
- capacity and load posture
- deferred work aging
- repeated escalations
- pending renewal or recovery priorities

This is the core steady-state stewardship rhythm.

## Wave Readiness Review

Use this cadence when:

- release planning depends on doctrine confidence
- freeze posture matters
- intervention or elevated-watch posture could affect commitments

This review should focus on whether doctrine posture is strong enough for the planned wave assumptions.

## Post-Wave Review

Use this cadence to examine:

- what the wave taught about doctrine quality
- which watchpoints intensified or resolved
- whether decisions held up well
- whether intervention or baseline assumptions need updating

This turns delivery experience back into doctrine improvement.

## Relationship To Alerts

Alerts should feed reviews, but not replace them.

Examples:

- urgent alerts may trigger immediate handling before the next scheduled review
- recurring alerts should be examined in weekly review to understand pattern, not just event noise
- a quiet period should still be reviewed to confirm health rather than assumed blindly

## Relationship To Decisions And Audit

Review cadence should use decision audit trails actively.

Examples:

- daily review checks unresolved high-consequence decisions
- weekly review checks repeated deferrals and reversals
- post-wave review checks whether authority and escalation decisions were well-judged

This keeps audit trails operational, not archival only.

## Relationship To Intervention

Cadence should also shape intervention posture.

Examples:

- weekly review may decide that baseline stewardship is no longer enough
- wave-readiness review may recommend intervention activation or tighter constraints
- post-wave review may confirm intervention exit, reentry progress, or regression concerns

This makes intervention part of a rhythm rather than only a panic move.

## Relationship To Governance

Not every cadence needs the same authority present.

Suggested posture:

- daily watch review can remain close to ordinary portfolio ownership
- weekly review may involve cross-area authority when signals are rising
- wave-readiness and post-wave reviews may involve workspace-admin or higher governance when consequence is broader

This keeps the cadence efficient and proportional.

## Operator Surface Requirements

Operator surfaces should be able to show:

- upcoming review sessions
- which review cadence produced a given outcome
- open items carried forward from one review to the next
- review-generated escalations, deferrals, or confirmations
- whether cadence reviews are being missed or delayed

This makes the rhythm visible and enforceable.

## Required Artifacts

The first useful review-cadence artifacts should include:

- `doctrine_review_calendar.json`
- `doctrine_review_agendas.md`
- `doctrine_review_outcomes.json`
- `doctrine_review_carryforwards.json`

Suggested contents:

- `doctrine_review_calendar.json`
  - machine-readable view of planned and completed doctrine review sessions
- `doctrine_review_agendas.md`
  - expected focus areas for each cadence type
- `doctrine_review_outcomes.json`
  - recorded results from cadence-based reviews
- `doctrine_review_carryforwards.json`
  - unresolved items intentionally carried into the next review cycle

## First Useful Outcomes

The first useful review-cadence outcomes should include:

- `confirm_current_posture`
- `reorder_priorities`
- `escalate_issue`
- `tighten_wave_assumptions`
- `schedule_deeper_review`

These outcomes connect recurring review to real operational change.

## Governance Expectations

Cadence should create discipline without bureaucracy.

Suggested posture:

- keep the number of cadence layers small
- make each review type answer a different question
- require that reviews produce either confirmation or action, not just conversation

## Non-Goals

This spec does not define:

- calendar tooling implementation
- every possible meeting or sync in the organization
- replacement of urgent incident response with scheduled reviews

It only defines the recurring review rhythm for healthy doctrine portfolio oversight.

## Bottom Line

`morphOS` should give doctrine portfolio oversight a real cadence.

Health, watchpoints, decisions, escalations, and intervention posture should be reviewed at predictable rhythms so the platform stays attentive without becoming reactive chaos.
