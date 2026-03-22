# Profile Doctrine Portfolio SLO And Alerting Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio baseline
- profile doctrine portfolio health, intervention, exit, and reentry
- doctrine-level recovery, renewal, and trust-decay behavior

What is still missing is the operational measurement layer that makes portfolio health observable through concrete expectations and alerts.

The platform still needs clear answers to these questions:

- what portfolio conditions should be considered healthy enough by default?
- when should watchpoints become alerts?
- how do operators know when baseline stewardship is slipping toward intervention territory?

This spec defines that portfolio SLO and alerting layer.

## Executive Summary

Portfolio doctrine management should not rely only on human intuition.

It should also use a small set of operational expectations and alerting rules that turn doctrine posture into something measurable and actionable.

For `morphOS`, the correct posture is:

- define a narrow set of meaningful portfolio SLOs
- translate repeated weak signals into alertable conditions
- support early action before doctrine weakness becomes strategic
- keep alerts tied to planning, freeze, and governance impact rather than vanity metrics

The goal is to make portfolio doctrine health operationally visible without reducing it to shallow scorekeeping.

## Core Design Goals

- define measurable steady-state expectations for doctrine portfolio health
- connect watchpoints, alerts, and intervention thresholds
- distinguish informational signals from actionable alerts
- align alerting with planning and governance impact
- preserve an auditable record of portfolio reliability expectations

## SLO Principle

Portfolio SLOs should express the minimum level of doctrine health and responsiveness the platform expects to maintain during normal operations.

They should therefore:

- focus on operationally meaningful outcomes
- help detect degradation early
- avoid creating noise from low-value metrics

An SLO is not a vanity target.
It is a practical promise about healthy portfolio stewardship.

## What This Spec Covers

The first useful portfolio SLO model should cover:

- baseline health expectations
- alert thresholds and severities
- watchpoint-to-alert escalation
- operator routing
- required artifacts and surfaces

This is enough to make doctrine portfolio operations measurable and governable.

## Canonical SLO Objects

`morphOS` should support at least:

- `DoctrinePortfolioSLO`
- `DoctrinePortfolioSLI`
- `DoctrinePortfolioAlertRule`
- `DoctrinePortfolioAlertEvent`
- `DoctrinePortfolioSLORecord`

Suggested meanings:

- `DoctrinePortfolioSLO`
  - a declared operational expectation for doctrine portfolio health
- `DoctrinePortfolioSLI`
  - the measured indicator used to evaluate the SLO
- `DoctrinePortfolioAlertRule`
  - the rule that turns SLO degradation or repeated watchpoints into an alert
- `DoctrinePortfolioAlertEvent`
  - a concrete alert triggered by current portfolio conditions
- `DoctrinePortfolioSLORecord`
  - durable history of SLO state, alerting, and response

## First Useful Portfolio SLO Families

The first useful portfolio SLO families should include:

- freshness coverage
- unresolved critical doctrine count
- intervention frequency
- watchpoint aging
- doctrine maintenance responsiveness

Suggested meanings:

- `freshness coverage`
  - how much of the portfolio remains within acceptable freshness posture
- `unresolved critical doctrine count`
  - how much strategic doctrine weakness remains unresolved at once
- `intervention frequency`
  - how often the portfolio falls out of baseline management into strategic intervention
- `watchpoint aging`
  - how long meaningful watchpoints remain open without ordinary resolution
- `doctrine maintenance responsiveness`
  - how quickly routine stewardship addresses known ordinary maintenance work

These are more useful than generic counts because they connect to actual portfolio operability.

## Alert Severity Levels

The first useful alert severities should include:

- `info`
- `warning`
- `high`
- `critical`

Suggested meanings:

- `info`
  - notable portfolio movement that should remain visible but does not require immediate action
- `warning`
  - baseline stewardship should react soon to avoid drift into intervention posture
- `high`
  - the portfolio is materially degrading and needs active operational attention
- `critical`
  - portfolio posture now threatens planning confidence, freeze confidence, or governance expectations

These severities help keep attention proportional.

## Watchpoint To Alert Escalation

Not every watchpoint should page or interrupt operators.

Suggested posture:

- isolated watchpoints remain visible but non-alerting
- repeated or aging watchpoints can escalate to `warning`
- clustered watchpoints in strategic areas can escalate faster
- alerting should consider spread, severity, and persistence together

This keeps the signal useful without creating portfolio-noise fatigue.

## Relationship To Baseline

Portfolio SLOs should primarily describe whether baseline stewardship is holding.

Examples:

- baseline is healthy if freshness coverage remains above the ordinary threshold
- elevated watch may be triggered when watchpoint aging exceeds expectations
- repeated misses may support a recommendation for portfolio intervention

This helps baseline management stay operationally grounded.

## Relationship To Intervention

Alerting should also support intervention decisions.

Examples:

- repeated `high` alerts in the same doctrine family may justify targeted intervention
- a `critical` portfolio alert may support strategic pause review
- intervention exit can be informed by alert quieting and SLO recovery

This makes the alert model useful across the full portfolio lifecycle.

## Relationship To Planning And Freeze

SLO breaches should matter because they affect planning confidence.

Examples:

- degraded freshness coverage may narrow planning assumptions
- persistent `high` alerts may weaken freeze confidence
- repeated critical doctrine alerts should be visible in release planning

This keeps the measurement model tied to operational reality.

## Relationship To Governance

Governance should see the alerts that matter, but not be flooded by noise.

Suggested posture:

- `info` and routine `warning` signals can stay within ordinary portfolio ownership
- persistent `high` alerts should become visible to broader governance
- `critical` alerts should be routed as explicit strategic concerns

This supports calm escalation.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current portfolio SLO status
- active alerts by severity
- breached SLO families
- whether breaches are isolated, clustered, or systemic
- current routing and acknowledgment posture

This should support both scanning and investigation.

## Required Artifacts

The first useful SLO artifacts should include:

- `portfolio_slo_status.json`
- `portfolio_alerts.json`
- `portfolio_slo_summary.md`
- `portfolio_alert_history.json`

Suggested contents:

- `portfolio_slo_status.json`
  - machine-readable view of current SLO state and breach posture
- `portfolio_alerts.json`
  - active alert events and routing details
- `portfolio_slo_summary.md`
  - high-level explanation of current portfolio reliability posture
- `portfolio_alert_history.json`
  - durable record of alert events, acknowledgments, and resolution

## First Useful Outcomes

The first useful SLO and alerting outcomes should include:

- `within_slo`
- `watch_closely`
- `requires_baseline_action`
- `escalate_to_portfolio_review`
- `escalate_to_intervention_decision`

These outcomes connect measurement to action.

## Governance Expectations

SLOs and alerts should support judgment, not replace it.

Suggested posture:

- operators may handle routine warning conditions through ordinary stewardship
- stronger governance should see persistent or strategic alerts
- no alert should automatically declare doctrine intervention without human or governed review

## Non-Goals

This spec does not define:

- a universal numerical scoring formula for all doctrine health
- product-facing uptime style SLAs
- replacement of portfolio judgment with pure thresholds

It only defines the operational expectation and alerting layer for doctrine portfolio management.

## Bottom Line

`morphOS` should make doctrine portfolio health measurable enough to operate.

Baseline stewardship, rising risk, and intervention pressure should be visible through a small, meaningful set of SLOs and alerts so operators can act before doctrine weakness becomes strategically expensive.
