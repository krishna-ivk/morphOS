# Profile Doctrine Portfolio Scorecard Consumption Policy Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio maturity scorecard
- profile doctrine portfolio scorecard publication
- profile doctrine portfolio scorecard retention and history

What is still missing is the policy for how different roles and surfaces are allowed to use the scorecard in actual doctrine, planning, and governance decisions.

The platform still needs clear answers to these questions:

- what decisions may rely on the doctrine scorecard directly?
- when is the scorecard only a navigation aid rather than decision-grade proof?
- how should roles consume scorecard views without overreading them or ignoring their caveats?

This spec defines that portfolio scorecard-consumption layer.

## Executive Summary

Publishing a scorecard is not enough.

The platform also needs clear rules for how that scorecard may and may not be used.

For `morphOS`, the correct posture is:

- let the scorecard guide attention and prioritization
- require deeper evidence for higher-consequence decisions
- preserve the meaning of confidence labels and caveats in every use
- prevent summary scorecards from being treated as full doctrine truth

The goal is to make the scorecard operationally useful without letting it become an oversimplified substitute for judgment.

## Core Design Goals

- define safe, role-aware use of doctrine maturity scorecards
- distinguish advisory use from decision-grade use
- prevent misuse of stale, disputed, or caveated scorecards
- connect scorecard consumption to authority and confidence posture
- preserve traceability when scorecards materially influence decisions

## Consumption Principle

A scorecard should influence decisions in proportion to how current, calibrated, and context-appropriate it is.

Consumption policy should therefore:

- treat the scorecard as a guided summary, not universal proof
- allow broader use when confidence is high and caveats are low
- require deeper evidence when the consequence of error is high

The scorecard should help focus judgment, not replace it.

## What This Spec Covers

The first useful scorecard-consumption model should cover:

- allowed use classes
- disallowed or constrained use cases
- role-specific expectations
- confidence-aware consumption rules
- required artifacts and operator visibility

This is enough to keep scorecard use helpful and disciplined.

## Canonical Consumption Objects

`morphOS` should support at least:

- `DoctrineScorecardUseClass`
- `DoctrineScorecardConsumptionRule`
- `DoctrineScorecardUseDecision`
- `DoctrineScorecardUseConstraint`
- `DoctrineScorecardConsumptionRecord`

Suggested meanings:

- `DoctrineScorecardUseClass`
  - the kind of decision or activity using the scorecard
- `DoctrineScorecardConsumptionRule`
  - the policy that governs that use
- `DoctrineScorecardUseDecision`
  - the explicit choice to use, supplement, or reject scorecard input for a given purpose
- `DoctrineScorecardUseConstraint`
  - the caveat or restriction attached to scorecard use
- `DoctrineScorecardConsumptionRecord`
  - durable history of scorecard use in material decisions

## First Useful Use Classes

The first useful scorecard use classes should include:

- `attention_guidance`
- `priority_guidance`
- `wave_readiness_input`
- `governance_supporting_input`
- `historical_learning`

Suggested meanings:

- `attention_guidance`
  - use the scorecard to decide where to look first
- `priority_guidance`
  - use the scorecard to help order improvement or review work
- `wave_readiness_input`
  - use the scorecard as one input into wave or freeze posture
- `governance_supporting_input`
  - use the scorecard as supporting context in governance review
- `historical_learning`
  - use scorecard history to interpret trend and institutional learning

These classes help keep uses explicit and bounded.

## First Useful Consumption Modes

The first useful consumption modes should include:

- `advisory_only`
- `supporting_evidence`
- `decision_gate_with_validation`

Suggested meanings:

- `advisory_only`
  - the scorecard may shape attention, but cannot by itself justify the decision
- `supporting_evidence`
  - the scorecard may support the decision when combined with other evidence
- `decision_gate_with_validation`
  - the scorecard may participate in a formal gate only if freshness, confidence, and caveat posture are all sufficient

These modes prevent all scorecard use from being treated as equally strong.

## Safe Uses

The first useful safe scorecard uses should include:

- identifying weak doctrine dimensions for review
- prioritizing where stewardship effort should focus next
- supporting weekly portfolio review discussion
- informing, but not replacing, wave-readiness analysis

These uses benefit from the scorecard’s compression without overclaiming its authority.

## Constrained Uses

The first useful constrained scorecard uses should include:

- broad planning confidence claims
- freeze-confidence claims
- intervention activation or exit decisions
- governance decisions with material trust or compliance consequence

Suggested posture:

- scorecard use here should require deeper evidence and current caveat review
- stale, disputed, or under-review scorecards should not be treated as settled truth in these contexts

This keeps high-consequence use proportionate.

## Disallowed Uses

The first useful disallowed scorecard uses should include:

- treating a summary view as full evidence
- using stale publications as current authority
- ignoring active dispute or calibration caveats
- substituting the scorecard for direct review where policy requires fuller evidence

These are the main ways scorecards become misleading.

## Role-Specific Expectations

The first useful role-specific expectations should include:

- operators may use scorecards primarily for attention and priority guidance
- portfolio authority may use them as supporting evidence in broader portfolio decisions
- workspace admins may rely on them only with visible caveats and linked underlying evidence
- summary audiences should treat them as directional, not as permission to compress away weak signals

This aligns scorecard consumption with role consequence.

## Relationship To Publication

Consumption policy should honor publication view boundaries.

Examples:

- compact summaries should not be consumed as if they carried governance-detail certainty
- governance-detail views may support stronger decisions when current and settled
- audience-specific omissions should remain visible so consumers know what they are not seeing

This prevents misuse caused by overtrust in compressed views.

## Relationship To Freshness And History

Scorecard consumption should be freshness-aware.

Examples:

- recent history may be used for learning and comparison
- current operational decisions should prefer the active current scorecard
- stale publications should be blocked or caveated for stronger decision use

This keeps old scorecards from masquerading as current posture.

## Relationship To Calibration And Disputes

Consumption should respond to scorecard uncertainty.

Examples:

- disputed dimensions should weaken decision-grade reliance
- under-review scorecards may still guide attention but should not anchor confident planning claims
- calibration changes should be visible before comparing old and new scorecards in decisions

This preserves the meaning of uncertainty.

## Relationship To Audit

Material scorecard use should itself be traceable.

Examples:

- if a scorecard materially influenced a governance decision, record that use
- if a wave-readiness decision depended on scorecard posture, preserve the linked scorecard and caveats
- if the scorecard was explicitly rejected as insufficient, that should also be recordable

This helps later review judge whether scorecard use was responsible.

## Operator Surface Requirements

Operator surfaces should be able to show:

- whether the current scorecard view is advisory or stronger
- what confidence and caveat posture applies
- whether the current use case is allowed, constrained, or disallowed
- links to deeper evidence where stronger use requires it

This helps people use the scorecard correctly instead of just conveniently.

## Required Artifacts

The first useful consumption-policy artifacts should include:

- `scorecard_consumption_rules.md`
- `scorecard_use_records.json`
- `scorecard_use_constraints.json`
- `scorecard_decision_links.json`

Suggested contents:

- `scorecard_consumption_rules.md`
  - allowed and constrained scorecard use by role and decision type
- `scorecard_use_records.json`
  - machine-readable record of material scorecard usage in portfolio decisions
- `scorecard_use_constraints.json`
  - current caveat and restriction posture affecting scorecard use
- `scorecard_decision_links.json`
  - links between material decisions and the scorecard versions they referenced

## First Useful Outcomes

The first useful consumption outcomes should include:

- `use_as_advisory_input`
- `use_with_supporting_evidence`
- `require_deeper_validation`
- `reject_as_insufficient_for_this_decision`
- `record_material_scorecard_use`

These outcomes make scorecard use explicit and reviewable.

## Governance Expectations

The scorecard should shape decisions without being allowed to oversimplify them.

Suggested posture:

- the higher the consequence, the lower the tolerance for scorecard-only reasoning
- consumers should be expected to honor caveats and freshness markers
- governance should be able to review not just the scorecard, but how it was used

## Non-Goals

This spec does not define:

- every possible UI presentation of the scorecard
- replacement of detailed doctrine evidence with summary scoring
- automatic decision-making based only on scorecard posture

It only defines how doctrine maturity scorecards may be consumed safely and responsibly across roles and decision contexts.

## Bottom Line

`morphOS` should govern how its doctrine scorecards are used, not just how they are created.

The scorecard should guide attention and support judgment, but higher-consequence decisions should still require the right depth of evidence, freshness, and caveat awareness before maturity claims are trusted operationally.
