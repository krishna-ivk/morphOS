# Profile Doctrine Portfolio Decision Audit Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio decision authority
- profile doctrine portfolio escalation policy
- portfolio intervention, exit, and reentry behavior

What is still missing is the audit model for recording, reviewing, and later explaining doctrine portfolio decisions across the full decision lifecycle.

The platform still needs clear answers to these questions:

- how are doctrine portfolio decisions recorded in a durable and reviewable way?
- what evidence should be preserved when authority is exercised?
- how can operators later explain why a doctrine decision was made, deferred, escalated, or reversed?

This spec defines that portfolio decision-audit layer.

## Executive Summary

Clear authority is necessary, but not sufficient.

The platform also needs a durable audit trail that explains:

- what decision was made
- who made it
- under what authority
- based on what evidence
- with what consequences and follow-up

For `morphOS`, the correct posture is:

- treat doctrine decisions as auditable operational events
- preserve both the decision outcome and the reasoning context
- support later review across triage, escalation, intervention, and normalization
- make audit records useful for accountability, learning, and replay

The goal is to make doctrine portfolio decisions explainable long after the moment has passed.

## Core Design Goals

- define a durable audit model for doctrine portfolio decisions
- preserve decision context, not only outcomes
- support review of authority use, escalation, and reversal
- connect audit records to governance, retrospectives, and learning
- keep audit trails useful without becoming noisy or ceremonial

## Audit Principle

Important doctrine portfolio decisions should be explainable after the fact without relying on memory or informal chat history.

Decision audit should therefore:

- preserve who decided, why, and under what authority
- record the evidence and constraints present at decision time
- capture reversals, overrides, and follow-up obligations

An audit record is not just a receipt.
It is the minimum truth needed to reconstruct responsible decision-making.

## What This Spec Covers

The first useful decision-audit model should cover:

- audited decision types
- minimum audit fields
- evidence linkage
- review and replay posture
- required artifacts and surfaces

This is enough to make doctrine portfolio decisions durable and reviewable.

## Canonical Audit Objects

`morphOS` should support at least:

- `DoctrineDecisionAuditRecord`
- `DoctrineDecisionEvidenceLink`
- `DoctrineDecisionOutcome`
- `DoctrineDecisionReversalRecord`
- `DoctrineDecisionAuditTrail`

Suggested meanings:

- `DoctrineDecisionAuditRecord`
  - one durable record of a doctrine portfolio decision
- `DoctrineDecisionEvidenceLink`
  - pointers to the evidence used at decision time
- `DoctrineDecisionOutcome`
  - the action, deferral, escalation, or approval result produced
- `DoctrineDecisionReversalRecord`
  - durable record of later reversal, override, or superseding decision
- `DoctrineDecisionAuditTrail`
  - the linked history of decisions affecting the same doctrine issue or portfolio path

## First Useful Audited Decision Types

The first useful audited decision types should include:

- triage decisions
- deferral decisions
- escalation decisions
- intervention activation or step-down decisions
- authority-routing decisions
- exception approvals
- reversal or override decisions

These are the decisions most likely to matter later for trust, governance, or learning.

## Minimum Audit Fields

The first useful minimum audit fields should include:

- decision id
- decision class
- authority layer
- decider identity
- timestamp
- affected doctrine scope
- evidence summary
- decision outcome
- stated rationale
- follow-up obligations

These fields should make the decision independently legible later.

## Evidence Linkage

Audit records should not duplicate every artifact, but they should point to the evidence that mattered.

The first useful evidence links should include:

- health snapshots
- alert events
- capacity and load snapshots
- triage queue state
- escalation records
- governance review notes

This keeps the audit trail grounded in the actual state of the platform at decision time.

## Relationship To Authority

Decision audit should verify authority use, not just record that “someone decided.”

Suggested posture:

- each record should include the authority layer used
- out-of-scope decisions should be visible as authority-boundary problems
- later review should be able to confirm whether the right level decided

This helps authority remain enforceable in practice.

## Relationship To Escalation

Escalations should be auditable as transitions, not only as destinations.

Examples:

- record why ordinary triage was judged insufficient
- record what route was selected and by whom
- record whether escalation later resolved, intensified, or reversed

This makes escalation reviewable instead of anecdotal.

## Relationship To Intervention

Intervention decisions should carry especially strong audit context.

Examples:

- activation should record strategic triggers and expected scope
- exit should record why extraordinary handling was no longer needed
- reentry should record what transitional watchpoints remained

This helps future operators understand not only what happened, but why intervention posture changed.

## Relationship To Governance

Governance should be able to use audit trails without drowning in raw event noise.

Suggested posture:

- ordinary routine decisions may be summarized unless later review is needed
- governance-sensitive and strategic decisions should retain full audit posture
- audit trails should support spot review, exception review, and retrospective sampling

## Relationship To Learning

Decision audits should also support learning and doctrine improvement.

Examples:

- repeated reversals may indicate weak authority routing or weak evidence quality
- repeated deferral patterns may reveal unhealthy triage defaults
- intervention audit trails may inform future baseline and escalation criteria

This turns audit into improvement material, not only compliance material.

## Reversals And Overrides

The audit model should make decision changes explicit.

The first useful reversal data should include:

- what prior decision was superseded
- who reversed or overrode it
- under what authority the change happened
- what new evidence or changed condition justified the reversal

This prevents the trail from becoming misleading after the fact.

## Operator Surface Requirements

Operator surfaces should be able to show:

- the current decision and its authority
- linked prior decisions affecting the same issue
- evidence snapshots relevant to the decision
- whether the decision has been challenged, reversed, or completed
- follow-up obligations still open

This gives operators a usable history, not just a log dump.

## Required Artifacts

The first useful decision-audit artifacts should include:

- `doctrine_decision_audit_log.json`
- `doctrine_decision_audit_summary.md`
- `decision_reversals.json`
- `decision_followups.json`

Suggested contents:

- `doctrine_decision_audit_log.json`
  - machine-readable sequence of audited doctrine portfolio decisions
- `doctrine_decision_audit_summary.md`
  - high-level review of notable decisions, authority use, and unresolved follow-ups
- `decision_reversals.json`
  - reversals, overrides, and superseded decision links
- `decision_followups.json`
  - obligations created by decisions and their current closure state

## First Useful Outcomes

The first useful decision-audit outcomes should include:

- `audit_record_created`
- `audit_record_linked_to_authority`
- `audit_record_flagged_for_review`
- `audit_record_superseded`
- `audit_record_closed`

These outcomes make audit trail state visible and queryable.

## Governance Expectations

Audit should support real accountability without forcing every doctrine action into heavyweight ceremony.

Suggested posture:

- strategic and governance-sensitive decisions should be fully auditable
- routine decisions may use lighter audit posture if later drill-down remains possible
- higher-risk decisions should remain easy to reconstruct during review or incident analysis

## Non-Goals

This spec does not define:

- a full enterprise compliance framework
- immutable storage implementation details
- replacement of good decision-making with paperwork

It only defines how doctrine portfolio decisions should be durably recorded, linked, and later explained.

## Bottom Line

`morphOS` should treat doctrine portfolio decisions as auditable events.

When doctrine work is prioritized, deferred, escalated, approved, reversed, or normalized, the platform should preserve enough truth to explain who decided, why they decided, what evidence mattered, and what happened next.
