# Profile Doctrine Trust Decay Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine regression response
- profile doctrine recovery and requalification
- profile doctrine reentry and expansion

What is still missing is the quiet failure mode where trust becomes stale even without an obvious incident.

The platform still needs clear answers to these questions:

- what happens when a doctrine area stops receiving fresh validating evidence?
- how should confidence narrow when maturity is old but not actively disproven?
- when should the platform require renewed proving rather than relying on aged trust?

This spec defines that trust-decay layer.

## Executive Summary

Not every loss of confidence begins with a dramatic regression.

Sometimes doctrine simply becomes less trustworthy because:

- its evidence is old
- its operating environment changed
- its success history is no longer recent enough to justify the same confidence

For `morphOS`, the correct posture is:

- treat trust as something that can decay over time
- narrow confidence when evidence freshness weakens
- require renewed proving before stale trust is used for strong claims
- keep decay distinct from explicit regression, while allowing the two to interact

The goal is to stop old confidence from silently pretending to still be current.

## Core Design Goals

- define how doctrine trust weakens in the absence of fresh evidence
- separate quiet trust aging from explicit regression events
- connect evidence freshness to wave use, freeze posture, and maturity claims
- require proportional renewal before strong trust assumptions are reused
- preserve an auditable record of why confidence narrowed

## Trust Decay Principle

Confidence that is not refreshed should gradually narrow.

This does not mean the doctrine is broken.
It means the platform should be more careful about what claims it makes on the basis of old evidence.

Trust decay should therefore:

- reduce confidence gradually
- affect scope and posture before declaring outright failure
- encourage renewal through proving, observation, and current evidence

## What This Spec Covers

The first useful trust-decay model should cover:

- confidence aging
- freshness-linked narrowing of doctrine posture
- renewal triggers
- interaction with maturity and reentry
- required artifacts and operator visibility

This is enough to keep mature doctrine honest when time passes faster than proof.

## Canonical Trust Decay Objects

`morphOS` should support at least:

- `DoctrineTrustWindow`
- `DoctrineTrustDecaySignal`
- `DoctrineTrustRefreshAssessment`
- `DoctrineTrustDecayDecision`
- `DoctrineTrustDecayRecord`

Suggested meanings:

- `DoctrineTrustWindow`
  - the expected period during which current evidence may support a given confidence claim
- `DoctrineTrustDecaySignal`
  - evidence that trust freshness is weakening or has expired
- `DoctrineTrustRefreshAssessment`
  - analysis of whether the doctrine requires renewed proving
- `DoctrineTrustDecayDecision`
  - the official narrowing or refresh posture chosen
- `DoctrineTrustDecayRecord`
  - durable history of the decay and refresh process

## Decay States

The first useful decay states should include:

- `fresh`
- `aging`
- `stale`
- `refresh_required`

Suggested meanings:

- `fresh`
  - current evidence is recent enough for ordinary confidence claims
- `aging`
  - evidence is still useful, but stronger claims should start narrowing
- `stale`
  - doctrine may still be usable, but should not be treated as recently proven
- `refresh_required`
  - continued strong trust claims require new evidence before expansion or broad reliance

These states allow confidence to narrow before trust becomes misleading.

## Trust Windows

Trust windows should be defined relative to context, not as one universal duration.

Examples:

- fast-moving workflow doctrine may age quickly
- more stable, low-change doctrine may retain usefulness longer
- doctrine touching external systems or policy-sensitive flows may decay faster than internal static conventions

The important thing is not the exact clock.
It is the governed relationship between time, change, and confidence.

## Decay Signals

The first useful trust-decay signals should include:

- long periods without recent wave evidence
- lack of recent simulation or monitored use
- major environment or dependency changes since the last proving cycle
- repeated small exceptions that do not yet rise to regression severity
- mismatch between old doctrine assumptions and current operator behavior

These signals indicate that trust may be outliving its evidence.

## Relationship To Regression

Trust decay is not the same as regression.

Suggested posture:

- use decay when confidence is aging without decisive failure
- use regression when evidence shows the doctrine is actively underperforming or unsafe
- allow prolonged decay plus new failures to become a regression pathway when warranted

This keeps the model truthful without being alarmist.

## Relationship To Maturity

Maturity should depend not only on historical success, but on the freshness of that success.

Suggested posture:

- maturity claims may narrow when trust reaches `stale`
- doctrine in `refresh_required` should not be treated as fully current even if its last mature phase was strong
- maturity restoration and maintenance should both depend on recent proof

This prevents maturity from becoming a permanent title.

## Relationship To Reentry And Expansion

Recovered doctrine that reenters normal use should still be subject to trust decay later.

Examples:

- successful reentry does not grant indefinite freshness
- expanded doctrine without recent monitored use may need renewed proof before broader future claims

This keeps recovery and long-term trust connected.

## Relationship To Freeze And Wave Launch

Decay posture should affect operational claims.

Examples:

- doctrine in `aging` may still participate in waves, but with narrower assumptions
- doctrine in `stale` should not automatically support broad freeze confidence
- doctrine in `refresh_required` may need proving before being used as a strong dependency in launch planning

## Refresh Triggers

The first useful triggers for renewing trust should include:

- entering `refresh_required`
- planned use in a broader scope than current freshness supports
- major environment changes
- repeated operator exceptions suggesting old doctrine is drifting from real practice

These triggers should drive proving rather than passive waiting.

## Refresh Paths

The first useful trust-refresh paths should include:

- targeted simulation
- monitored limited use
- wave-level observation
- profile or doctrine review with current evidence

The right path depends on what confidence needs to be renewed.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current trust-decay state
- freshness window or freshness posture
- last meaningful proving activity
- refresh triggers currently active
- how decay affects current wave, freeze, or maturity claims

This gives operators a more honest picture than just showing maturity labels.

## Required Artifacts

The first useful trust-decay artifacts should include:

- `trust_decay_assessment.md`
- `trust_refresh_plan.md`
- `trust_freshness.json`
- `trust_decay_decision.json`

Suggested contents:

- `trust_decay_assessment.md`
  - why trust is narrowing and what operational claims are affected
- `trust_refresh_plan.md`
  - how freshness will be renewed and at what scope
- `trust_freshness.json`
  - machine-readable freshness state, dates, windows, and active triggers
- `trust_decay_decision.json`
  - official narrowing, restrictions, and refresh requirements

## Decision Outcomes

The first useful trust-decay outcomes should include:

- `no_change`
- `narrow_confidence`
- `restrict_scope_until_refresh`
- `refresh_required_before_broader_use`
- `escalate_to_regression_assessment`

These outcomes keep decay actionable without turning every stale signal into crisis.

## Governance Expectations

Trust-decay handling should be governed in proportion to what is being narrowed or restored.

Suggested posture:

- ordinary refresh requirements may be handled by the appropriate workspace authority
- narrowing that materially affects wave or freeze posture may require stronger review
- escalation from quiet decay into formal regression should be explicitly governed

## Non-Goals

This spec does not define:

- the full regression-response process
- the full maturity model
- exact universal timing constants for every doctrine area

It only defines how trust should narrow when evidence freshness weakens.

## Bottom Line

`morphOS` should treat doctrine trust as something that can quietly decay.

When evidence gets old, the platform should narrow confidence, refresh proof where needed, and avoid acting as if yesterday's trust automatically still applies today.
