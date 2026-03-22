# Profile Doctrine Reentry And Expansion Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine regression response
- profile doctrine recovery and requalification
- profile doctrine wave launch

What is still missing is the operational path from narrow requalification back to broader use.

The platform still needs clear answers to these questions:

- how should a recovered doctrine area reenter normal usage?
- when is it safe to expand from limited reuse to broader wave participation?
- how do we prevent recovery success from becoming overconfidence?

This spec defines that reentry and expansion layer.

## Executive Summary

Recovery proves that a doctrine area may be trusted again at some scope.

Reentry and expansion should define how that restored trust grows safely.

For `morphOS`, the correct posture is:

- treat reentry as staged expansion
- preserve tighter monitoring while scope increases
- require evidence at each expansion boundary
- allow retreat if the recovered doctrine shows renewed instability

The goal is to move from narrow trust to broader trust without skipping the proving steps in between.

## Core Design Goals

- define a controlled path from limited reuse to broader operational use
- prevent abrupt return to full trust after initial recovery
- require evidence at each expansion boundary
- connect reentry to wave launch, freeze posture, and maturity restoration
- make rollback from failed reentry explicit

## Reentry Principle

A recovered doctrine area should not immediately regain its maximum prior scope.

Instead, reentry should:

- begin from the narrowest justified scope
- expand only after successful observed use
- preserve the ability to halt or narrow again quickly

Recovery answers, "can we use this again?"
Reentry answers, "how do we safely use it more broadly?"

## What This Spec Covers

The first useful reentry model should cover:

- staged expansion
- expansion gates
- monitoring requirements during expansion
- rollback handling during reentry
- relationship to restored maturity and wave posture

This is enough to make post-recovery growth disciplined instead of optimistic.

## Canonical Reentry Objects

`morphOS` should support at least:

- `DoctrineReentryPlan`
- `DoctrineExpansionStage`
- `DoctrineExpansionAssessment`
- `DoctrineExpansionDecision`
- `DoctrineReentryRecord`

Suggested meanings:

- `DoctrineReentryPlan`
  - the intended staged path from limited reuse toward broader use
- `DoctrineExpansionStage`
  - the current scope and monitoring posture for recovered doctrine
- `DoctrineExpansionAssessment`
  - analysis of whether the doctrine has earned the next expansion step
- `DoctrineExpansionDecision`
  - approval or denial of broader usage scope
- `DoctrineReentryRecord`
  - durable history of expansion attempts, results, and setbacks

## Reentry Preconditions

Reentry should begin only when:

- recovery has produced an explicit requalification decision
- the allowed starting scope is clear
- monitoring and rollback rules are already defined

The platform should not expand usage based on vague confidence.

## Expansion Stages

The first useful expansion stages should include:

- `limited_reuse`
- `controlled_wave_use`
- `multi_wave_monitored_use`
- `broad_normal_use`

Suggested meanings:

- `limited_reuse`
  - doctrine is permitted only in narrow governed situations
- `controlled_wave_use`
  - doctrine may participate in selected waves with added monitoring and constraints
- `multi_wave_monitored_use`
  - doctrine has passed more than one wave but still carries explicit observation posture
- `broad_normal_use`
  - doctrine is broadly trusted at its current maturity and no longer needs exceptional expansion handling

These stages separate "usable again" from "operationally normal again."

## Expansion Gates

The first useful expansion gates should include:

- successful use at the current stage
- no repeated serious regression signals in the expansion window
- acceptable override and conflict pressure
- acceptable validation and review posture
- required simulation for the next broader scope where needed

Each gate should answer whether the next stage is justified now.

## Expansion Evidence

The first useful evidence for advancing expansion should include:

- monitored run outcomes
- wave-level evidence where applicable
- review and validation results
- operator observations and exceptions raised
- trend comparison against the original regression pattern

Fresh operational evidence matters more than intent.

## Relationship To Freeze

Expansion posture should influence freeze eligibility.

Examples:

- doctrine in `controlled_wave_use` may be excluded from broad freeze assumptions
- doctrine in `multi_wave_monitored_use` may support narrower freeze claims than fully stable doctrine
- only doctrine in `broad_normal_use` should be treated as ordinarily stable without caveat

## Relationship To Wave Launch

Reentry should be visible in launch planning.

Examples:

- mark recovered doctrine explicitly in launch packets
- require extra monitoring in waves using recovered doctrine
- define stop conditions specific to reentry scope

This prevents recovered doctrine from being mistaken for unremarkable doctrine too early.

## Relationship To Maturity

Expansion and maturity restoration should move together, but not always at the same speed.

Suggested posture:

- a doctrine area may reach `controlled_wave_use` before regaining its prior maturity stage
- maturity restoration should generally follow demonstrated expansion success, not precede it

This keeps the maturity model tied to earned trust.

## Relationship To Rollback

Expansion must allow explicit retreat.

If renewed instability appears during reentry, the platform should be able to:

- pause expansion
- remain at the current stage
- narrow scope again
- reopen recovery or regression handling

This makes expansion reversible rather than ceremonial.

## Expansion Failure Signals

The first useful signals that expansion is failing should include:

- repeated exceptions at the current expansion stage
- wave-specific instability tied to the recovered doctrine
- rising override pressure
- reappearance of the original failure pattern
- new serious review or policy defects tied to the doctrine area

These signals should influence whether the doctrine advances, holds, or retreats.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current expansion stage
- current scope and restrictions
- next eligible expansion step
- evidence collected for expansion
- remaining gates
- rollback triggers and current monitoring posture

This gives operators an honest view of how recovery is progressing in practice.

## Required Artifacts

The first useful reentry artifacts should include:

- `reentry_plan.md`
- `expansion_assessment.md`
- `expansion_evidence.json`
- `expansion_decision.json`

Suggested contents:

- `reentry_plan.md`
  - current requalification level, intended stages, monitoring posture, rollback rules
- `expansion_assessment.md`
  - whether the current stage has earned the next scope
- `expansion_evidence.json`
  - machine-readable summary of outcomes, exceptions, signals, and unresolved risk
- `expansion_decision.json`
  - approved stage, restrictions, required monitoring, and approver record

## Decision Outcomes

The first useful reentry outcomes should include:

- `stay_at_current_stage`
- `expand_scope`
- `expand_with_restrictions`
- `pause_expansion`
- `narrow_scope`
- `return_to_recovery`

These outcomes make expansion posture explicit.

## Governance Expectations

Broader expansion should require stronger authority than narrow continued use.

Suggested posture:

- small scope increases may be handled at the appropriate workspace level
- broader wave expansion may require stronger review
- return to `broad_normal_use` after serious regression should require explicit governed approval

## Non-Goals

This spec does not define:

- the full recovery model
- the maturity model itself
- generic release-wave policy unrelated to recovered doctrine

It only defines how recovered doctrine safely expands back into broader use.

## Bottom Line

`morphOS` should treat doctrine reentry as staged expansion.

After recovery, the platform should not jump from limited trust to ordinary trust in one move.
It should expand, observe, decide, and only then normalize broader use.
