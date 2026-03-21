# Profile Doctrine Recovery And Requalification Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine regression response
- profile doctrine maturity model
- profile doctrine maturity advancement playbook

What is still missing is the recovery path after regression.

The platform still needs clear answers to these questions:

- how does a doctrine area regain trust after regression?
- what evidence is enough to move from containment back to qualified use?
- when can maturity be restored, and when must doctrine remain constrained?

This spec defines that recovery and requalification layer.

## Executive Summary

Regression response protects the platform when confidence drops.

Recovery and requalification should define how confidence can be earned back.

For `morphOS`, the correct posture is:

- treat recovery as a governed proving process
- require fresh evidence instead of relying on old maturity status
- restore confidence in stages
- make requalification explicit before returning to broader wave use

The goal is to ensure that regained trust is deserved, visible, and durable.

## Core Design Goals

- define a clear path from regression to renewed trust
- prevent premature return to high-maturity assumptions
- require fresh evidence after doctrine repair or containment
- connect recovery to simulation, wave usage, and maturity reassessment
- preserve an auditable record of why confidence was restored

## Recovery Principle

Once doctrine has regressed, the old confidence should no longer be treated as active.

Recovery should therefore:

- start from current evidence, not historical prestige
- prove that the regression was understood and addressed
- rebuild trust in steps

Requalification is not automatic.
It is a new proof cycle.

## What This Spec Covers

The first useful recovery model should cover:

- recovery triggers
- staged requalification
- restored-use boundaries
- maturity restoration decisions
- required artifacts and governance

This is enough to make post-regression trust restoration disciplined instead of intuitive.

## Canonical Recovery Objects

`morphOS` should support at least:

- `DoctrineRecoveryPlan`
- `DoctrineRecoveryEvidence`
- `DoctrineRequalificationAssessment`
- `DoctrineRequalificationDecision`
- `DoctrineRecoveryRecord`

Suggested meanings:

- `DoctrineRecoveryPlan`
  - the intended path for addressing regression and gathering new proof
- `DoctrineRecoveryEvidence`
  - fresh simulations, reviews, wave results, and doctrine changes used to justify renewed trust
- `DoctrineRequalificationAssessment`
  - analysis of whether the doctrine has earned broader use again
- `DoctrineRequalificationDecision`
  - the official outcome for restored usage or maturity
- `DoctrineRecoveryRecord`
  - durable history of the recovery path and decision

## Recovery Entry Conditions

Recovery should begin only after at least one of these is true:

- containment actions are active
- the regression cause has been investigated enough to support a recovery plan
- doctrine changes, monitoring changes, or operational constraints are in place

The platform should not attempt requalification while the regression is still unmanaged.

## Recovery Phases

The first useful recovery phases should include:

- `contained`
- `repairing`
- `proving`
- `limited_reuse`
- `requalified`

Suggested meanings:

- `contained`
  - the regression has been acknowledged and risk is currently constrained
- `repairing`
  - doctrine, workflow, policy, or operational fixes are being prepared or applied
- `proving`
  - fresh evidence is being collected through simulation, review, and narrow usage
- `limited_reuse`
  - doctrine may be used again, but only with tighter controls
- `requalified`
  - the doctrine has met the current bar for restored trust at a defined scope

This helps operators separate recovery progress from restored confidence.

## Requalification Scope

Recovery should restore confidence by scope, not all at once.

The first useful scopes should include:

- `simulation_only`
- `single_workflow_family`
- `limited_wave`
- `broad_wave_use`
- `maturity_restoration`

Examples:

- allow simulation-only proving after a critical regression
- restore use for one workflow family before expanding to all profile areas
- allow one tightly monitored release wave before restoring broad confidence

## Evidence Requirements

The first useful requalification evidence should include:

- regression cause analysis
- documented remediation or doctrine changes
- successful simulation or sandbox runs
- validation and review outcomes after remediation
- wave-level evidence where the prior regression affected wave use
- absence of repeated critical regression signals during the proving window

Fresh evidence matters more than old maturity history.

## Requalification Levels

The first useful requalification levels should include:

- `operationally_contained`
- `narrowly_requalified`
- `wave_requalified`
- `maturity_requalified`

Suggested meanings:

- `operationally_contained`
  - recovery work is underway, but broader trust is not yet restored
- `narrowly_requalified`
  - doctrine may be used again only in limited, governed contexts
- `wave_requalified`
  - doctrine has earned controlled wave participation again
- `maturity_requalified`
  - doctrine has earned restoration of a formal maturity stage

These levels keep recovery proportional.

## Relationship To Maturity Restoration

Requalification and maturity restoration are related but not identical.

Suggested posture:

- doctrine may be requalified for limited use without fully restoring prior maturity
- maturity restoration should require stronger evidence than narrow reuse

This prevents the platform from overcorrecting upward too quickly.

## Relationship To Freeze And Launch

Recovery posture should affect freeze and launch decisions directly.

Examples:

- doctrine in `proving` should not be treated as freeze-stable
- doctrine in `limited_reuse` may be allowed in a constrained wave with stronger monitoring
- doctrine should regain ordinary launch assumptions only after requalification is explicit

## Relationship To Simulation

Simulation should be a primary proving surface during recovery.

Examples:

- run candidate profiles against past failure patterns
- compare pre-fix and post-fix doctrine posture
- require simulation before allowing limited wave use after serious regression

Simulation reduces the chance of mistaking optimism for recovery.

## Relationship To Multi-Wave Learning

Recovery should also be visible across multiple waves.

Examples:

- one clean wave may justify limited wave requalification
- multiple stable waves may justify maturity restoration
- recurring smaller failures may block advancement even if no new critical event occurs

This keeps recovery honest over time.

## Relationship To Change Management

If the recovery depends on doctrine or profile changes, those changes should remain governed.

Suggested posture:

- recovery evidence may justify a change request
- accepted changes may become part of the recovery plan
- requalification should reflect the currently active doctrine, not a proposed future state

## Operator Surface Requirements

Operator surfaces should be able to show:

- current recovery phase
- requalification scope
- active restrictions
- proving evidence collected so far
- remaining gates before broader reuse
- current maturity and whether restoration is pending or complete

This gives operators an honest picture of regained trust.

## Required Artifacts

The first useful recovery artifacts should include:

- `recovery_plan.md`
- `requalification_assessment.md`
- `recovery_evidence.json`
- `requalification_decision.json`

Suggested contents:

- `recovery_plan.md`
  - regression summary, constraints, repair actions, proving plan
- `requalification_assessment.md`
  - analysis of whether the current evidence supports broader reuse
- `recovery_evidence.json`
  - machine-readable summary of simulations, waves, findings, and outstanding risks
- `requalification_decision.json`
  - final scope, level, maturity effect, and approver record

## Decision Outcomes

The first useful recovery outcomes should include:

- `remain_contained`
- `limited_reuse_allowed`
- `wave_requalification_granted`
- `maturity_restoration_granted`
- `additional_proving_required`
- `recovery_failed_reopen_required`

These outcomes make recovery explicit instead of implied.

## Governance Expectations

Requalification should be governed proportionally to the scope being restored.

Suggested posture:

- narrow reuse may be approved by the appropriate workspace-level authority
- broader wave requalification may require stronger review
- maturity restoration after serious or critical regression may require higher-authority approval

## Non-Goals

This spec does not define:

- the detailed simulation engine
- the full maturity model itself
- generic validation unrelated to doctrine recovery

It only defines how doctrine trust is rebuilt after regression.

## Bottom Line

`morphOS` should treat doctrine recovery as a fresh proof cycle.

When confidence drops, the platform should not quietly resume old assumptions.
It should contain, repair, prove, requalify, and only then restore broader trust.
