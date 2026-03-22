# Profile Doctrine Portfolio Intervention Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio health
- profile doctrine recovery, renewal, and trust-decay behavior
- wave, freeze, and governance posture at the doctrine level

What is still missing is the portfolio-level response model when the doctrine system as a whole starts showing concentrated weakness.

The platform still needs clear answers to these questions:

- what should happen when multiple doctrine areas are aging, recovering, or at risk at the same time?
- when should portfolio-level action be taken instead of only local doctrine action?
- how does the platform respond when doctrine weakness becomes strategic rather than isolated?

This spec defines that portfolio-intervention layer.

## Executive Summary

Portfolio health tells the platform what the doctrine system looks like.

Portfolio intervention should define what the platform does about it.

For `morphOS`, the correct posture is:

- intervene when doctrine weakness becomes concentrated or strategically important
- choose responses proportional to the scope and severity of the portfolio signal
- preserve local doctrine ownership while enabling broader portfolio correction
- connect intervention to planning, freeze posture, wave posture, and governance review

The goal is to stop portfolio-level weakness from being noticed but not acted on.

## Core Design Goals

- define when portfolio-level action is justified
- distinguish isolated doctrine maintenance from strategic intervention
- provide a graduated intervention ladder
- connect portfolio intervention to planning and governance
- preserve an auditable record of why broader action was taken

## Portfolio Intervention Principle

Not every weak doctrine area needs a portfolio response.

Portfolio intervention should begin only when:

- weakness is concentrated in an important area
- weakness is spreading
- weakness is blocking broader operational confidence

This keeps the response proportional.

Portfolio intervention should therefore:

- respect local doctrine handling when issues are isolated
- escalate when portfolio-level patterns threaten broader platform confidence
- favor correction and stabilization over symbolic central control

## What This Spec Covers

The first useful portfolio-intervention model should cover:

- intervention triggers
- intervention levels
- strategic response types
- operational effects on waves and freezes
- governance routing and artifacts

This is enough to make portfolio health actionable.

## Canonical Portfolio Intervention Objects

`morphOS` should support at least:

- `DoctrinePortfolioInterventionSignal`
- `DoctrinePortfolioInterventionPlan`
- `DoctrinePortfolioInterventionDecision`
- `DoctrinePortfolioInterventionAction`
- `DoctrinePortfolioInterventionRecord`

Suggested meanings:

- `DoctrinePortfolioInterventionSignal`
  - evidence that doctrine weakness has become strategically meaningful at the portfolio level
- `DoctrinePortfolioInterventionPlan`
  - the intended cross-portfolio response
- `DoctrinePortfolioInterventionDecision`
  - the approved intervention posture
- `DoctrinePortfolioInterventionAction`
  - concrete action taken to stabilize the portfolio
- `DoctrinePortfolioInterventionRecord`
  - durable history of the portfolio-level response

## Intervention Triggers

The first useful intervention triggers should include:

- multiple critical doctrine areas affecting active wave planning
- concentrated aging or renewal needs in a release-critical workflow family
- repeated doctrine recoveries in one strategic area without durable stabilization
- portfolio-wide decline in freshness or maturity support
- strategic planning blocked because doctrine confidence is too uneven

These triggers indicate that local doctrine management is no longer enough by itself.

## Intervention Levels

The first useful intervention levels should include:

- `watch`
- `targeted_intervention`
- `portfolio_stabilization`
- `strategic_pause`

Suggested meanings:

- `watch`
  - portfolio-level concern exists, but stronger coordination is not yet required
- `targeted_intervention`
  - a focused set of doctrine areas needs coordinated action
- `portfolio_stabilization`
  - broader cross-portfolio correction is needed before ordinary confidence returns
- `strategic_pause`
  - doctrine weakness is serious enough to constrain planned expansion, launches, or freezes until corrected

These levels keep the response proportional to strategic risk.

## Intervention Action Types

The first useful action types should include:

- `prioritize_renewal_wave`
- `prioritize_recovery_work`
- `narrow_wave_scope`
- `tighten_freeze_claims`
- `increase_governance_review`
- `launch_portfolio_audit`
- `pause_profile_expansion`

Examples:

- run a renewal wave when many doctrine areas are aging together
- narrow planned release scope when doctrine health is too uneven
- increase governance review when strategic doctrine families are unstable

## Relationship To Local Doctrine Ownership

Portfolio intervention should not erase doctrine-level ownership.

Suggested posture:

- local doctrine areas still keep their own evidence, decisions, and state transitions
- portfolio intervention coordinates priorities, constraints, and strategic response
- central intervention should amplify local clarity, not replace it with vague top-down control

## Relationship To Wave Planning

Portfolio intervention should influence wave planning directly.

Examples:

- high portfolio instability may shift the next wave toward renewal and stabilization
- concentrated doctrine weakness may justify narrower launch scope
- stable portfolio recovery may permit more confident future expansion

This keeps plans aligned with actual doctrine readiness.

## Relationship To Freeze Posture

Portfolio intervention should affect freeze confidence when necessary.

Examples:

- broad aging or recovery pressure may weaken freeze claims
- strategic pause may block broad freeze assertions until doctrine stabilizes
- targeted intervention may allow partial freeze confidence with clear caveats

## Relationship To Governance

Portfolio intervention should help governance focus at the right level.

Examples:

- isolated doctrine weakness may stay within workspace-level handling
- cross-workspace or strategic doctrine weakness may require broader governance coordination
- strategic pause should be explicitly governed, not implied informally

## Relationship To Change Management

Portfolio intervention should guide deeper change work when repeated doctrine weakness suggests structural problems.

Examples:

- repeated portfolio interventions in the same family may justify doctrine redesign
- portfolio audits may produce change requests affecting packs, profiles, or governance rules

This helps the platform fix recurring root causes instead of only reacting to symptoms.

## Operator Surface Requirements

Operator surfaces should be able to show:

- active intervention level
- why portfolio intervention was triggered
- affected doctrine areas and clusters
- active strategic constraints
- planned intervention actions
- exit criteria for returning to ordinary portfolio management

This gives operators a clear understanding of what is happening and why.

## Required Artifacts

The first useful portfolio-intervention artifacts should include:

- `portfolio_intervention_plan.md`
- `portfolio_intervention_decision.json`
- `portfolio_intervention_actions.json`
- `portfolio_intervention_summary.md`

Suggested contents:

- `portfolio_intervention_plan.md`
  - trigger analysis, affected areas, intended response, and exit criteria
- `portfolio_intervention_decision.json`
  - approved intervention level, scope, constraints, and governance record
- `portfolio_intervention_actions.json`
  - machine-readable list of coordinated actions and current status
- `portfolio_intervention_summary.md`
  - high-level explanation of the current intervention posture and expected operational effects

## Intervention Outcomes

The first useful portfolio intervention outcomes should include:

- `monitor_only`
- `targeted_correction_active`
- `portfolio_stabilization_active`
- `strategic_constraints_active`
- `intervention_resolved`

These outcomes make it clear whether the portfolio is merely being watched or is under active coordinated correction.

## Exit Criteria

Portfolio intervention should end only when:

- triggering clusters have stabilized, renewed, or recovered enough
- strategic planning confidence has improved materially
- intervention constraints are no longer necessary
- governance agrees the portfolio can return to ordinary posture

This prevents interventions from lingering without purpose.

## Governance Expectations

The broader the intervention, the stronger the expected governance.

Suggested posture:

- watch and narrow targeted interventions may be approved at the appropriate strategic workspace level
- portfolio stabilization should require stronger cross-area review
- strategic pause should require explicit higher-level approval and clear exit conditions

## Non-Goals

This spec does not define:

- the internal lifecycle of every local doctrine area
- a universal numeric portfolio score
- automatic replacement of governance judgment with aggregate metrics

It only defines how the platform responds when doctrine weakness becomes strategically meaningful across the portfolio.

## Bottom Line

`morphOS` should treat portfolio doctrine weakness as something that can require coordinated intervention, not just observation.

When multiple doctrine areas weaken together or threaten broader planning confidence, the platform should respond deliberately, proportionally, and visibly.
