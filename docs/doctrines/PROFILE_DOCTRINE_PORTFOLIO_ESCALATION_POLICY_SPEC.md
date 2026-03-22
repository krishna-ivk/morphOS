# Profile Doctrine Portfolio Escalation Policy Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio triage policy
- profile doctrine portfolio capacity and load
- profile doctrine portfolio intervention and governance posture

What is still missing is the formal handoff rule for when doctrine work should stop being managed as ordinary queueing and start being treated as a portfolio-level escalation.

The platform still needs clear answers to these questions:

- when should a doctrine issue stop being “just another queued item”?
- what kinds of repeated deferral or overload should trigger broader attention?
- how does the platform move from local prioritization into explicit portfolio-level decision making?

This spec defines that portfolio-escalation layer.

## Executive Summary

Triage is not enough when doctrine pressure becomes strategically important.

Escalation policy should define when the platform must stop merely reordering work and instead raise the issue into a broader portfolio decision.

For `morphOS`, the correct posture is:

- escalate when consequence, repetition, or persistence makes ordinary handling insufficient
- distinguish operational inconvenience from strategic doctrine risk
- preserve clear ownership of who must decide next
- make the boundary between queue management and escalation explicit and auditable

The goal is to prevent important doctrine risks from staying trapped in “we’ll get to it” mode.

## Core Design Goals

- define clear triggers for portfolio-level escalation
- separate triage from formal strategic review
- route escalations according to severity and scope
- preserve visible rationale for why escalation happened
- keep escalation proportional instead of reflexive

## Escalation Principle

Escalation should happen when ordinary stewardship is no longer enough to manage the consequence of delay or uncertainty.

Escalation should therefore:

- look at strategic impact, not only queue age
- treat repetition and persistence as important signals
- route decisions to the right scope of authority

Escalation is not failure.
It is the moment the platform acknowledges that a larger decision is now required.

## What This Spec Covers

The first useful escalation model should cover:

- escalation triggers
- escalation classes
- decision-routing rules
- interaction with triage and intervention
- required artifacts and operator visibility

This is enough to make escalation explicit and governable.

## Canonical Escalation Objects

`morphOS` should support at least:

- `DoctrinePortfolioEscalationSignal`
- `DoctrinePortfolioEscalationClass`
- `DoctrinePortfolioEscalationDecision`
- `DoctrinePortfolioEscalationRoute`
- `DoctrinePortfolioEscalationRecord`

Suggested meanings:

- `DoctrinePortfolioEscalationSignal`
  - evidence that a doctrine issue now requires portfolio-level attention
- `DoctrinePortfolioEscalationClass`
  - the type and seriousness of the escalation
- `DoctrinePortfolioEscalationDecision`
  - the official decision to escalate and how it should be handled
- `DoctrinePortfolioEscalationRoute`
  - the target authority or process that now owns the next decision
- `DoctrinePortfolioEscalationRecord`
  - durable history of the escalation and its outcome

## First Useful Escalation Classes

The first useful escalation classes should include:

- `priority_conflict`
- `persistent_deferral`
- `capacity_pressure`
- `strategic_risk`
- `governance_sensitive`

Suggested meanings:

- `priority_conflict`
  - competing doctrine items now require a broader decision about tradeoffs
- `persistent_deferral`
  - an item has been deferred enough times that ordinary triage is no longer credible
- `capacity_pressure`
  - doctrine load is too high for healthy stewardship and ordinary prioritization is no longer enough
- `strategic_risk`
  - doctrine weakness is now materially affecting planning, freeze confidence, or release posture
- `governance_sensitive`
  - delay or ambiguity now requires higher-confidence governance review

These classes help separate “busy queue” problems from strategic doctrine decisions.

## Escalation Triggers

The first useful escalation triggers should include:

- repeated deferral of the same strategically meaningful item
- sustained overload without visible backlog relief
- multiple high-priority items competing for the same narrow window
- doctrine issues now weakening active planning or freeze confidence
- unresolved governance-sensitive doctrine decisions aging beyond ordinary stewardship tolerance

These signals indicate that the queue is no longer the right container.

## Relationship To Triage

Triage should feed escalation, not compete with it.

Suggested posture:

- triage decides work ordering while ordinary stewardship remains sufficient
- escalation begins when ordering alone no longer resolves the real risk
- escalation should record what triage already tried before broader review was triggered

This keeps the handoff from feeling arbitrary.

## Relationship To Capacity And Load

Capacity pressure is one of the strongest escalation pathways.

Examples:

- overload with strategic doctrine work slipping should escalate
- persistent strain plus growing backlog may require portfolio review
- high queue pressure without consequence may remain triage, not escalation

This makes escalation consequence-aware, not queue-size-driven alone.

## Relationship To Baseline And Intervention

Escalation should act as the bridge between baseline stewardship and intervention.

Examples:

- some escalations may resolve through portfolio review without full intervention
- repeated or unresolved escalations may support intervention decisions
- intervention should not start without a visible escalation path unless the situation is already plainly critical

This keeps the operating model coherent.

## Relationship To Governance

Escalation should route to governance only when the consequence truly warrants it.

Suggested posture:

- not every escalation requires the highest authority
- governance-sensitive or strategic-risk escalations may need broader review quickly
- escalation routing should be explicit so ownership is never ambiguous

## Escalation Routing

The first useful routes should include:

- `portfolio_owner_review`
- `cross_area_review`
- `governance_review`
- `intervention_decision_review`

Suggested meanings:

- `portfolio_owner_review`
  - broader portfolio ownership decides the next action
- `cross_area_review`
  - multiple affected areas need coordinated decision making
- `governance_review`
  - approval, compliance, or policy-sensitive review is required
- `intervention_decision_review`
  - the issue now warrants explicit consideration of portfolio intervention

These routes keep escalation tied to actual decision-making surfaces.

## Operator Surface Requirements

Operator surfaces should be able to show:

- active escalations
- escalation class and route
- why ordinary triage was no longer sufficient
- current owner of the next decision
- whether the escalation is trending toward intervention

This makes escalation transparent instead of social or implicit.

## Required Artifacts

The first useful escalation artifacts should include:

- `portfolio_escalations.json`
- `portfolio_escalation_summary.md`
- `escalation_routing_log.json`
- `persistent_deferrals.json`

Suggested contents:

- `portfolio_escalations.json`
  - machine-readable list of active escalations and their classes
- `portfolio_escalation_summary.md`
  - high-level explanation of why escalations are active and what they mean
- `escalation_routing_log.json`
  - route history, decision owners, and escalation transitions
- `persistent_deferrals.json`
  - deferred items whose age or repetition now threatens credibility

## First Useful Outcomes

The first useful escalation outcomes should include:

- `resolve_within_triage`
- `raise_to_portfolio_review`
- `raise_to_governance_review`
- `raise_to_intervention_decision`
- `maintain_under_observation`

These outcomes make escalation decisive instead of theatrical.

## Governance Expectations

Escalation policy should help governance see the right problems at the right time.

Suggested posture:

- operators should not have to guess whether something is “big enough” to raise
- governance should see persistent or strategically meaningful doctrine issues before they become silent liabilities
- escalation should preserve enough context that higher-level review is fast and grounded

## Non-Goals

This spec does not define:

- every detail of the intervention lifecycle
- automatic portfolio intervention with no human or governed review
- replacement of local ownership with constant top-down oversight

It only defines when doctrine work should move from queue management into formal portfolio-level escalation.

## Bottom Line

`morphOS` should treat escalation as a clear operating boundary.

When doctrine work can no longer be managed responsibly through ordinary prioritization alone, the platform should raise it explicitly, route it clearly, and make the next decision visible.
