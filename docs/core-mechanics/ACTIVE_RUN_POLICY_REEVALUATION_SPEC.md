# Active Run Policy Reevaluation Spec

## Why This Spec Exists

`morphOS` already defines:

- policy hooks at workflow boundaries
- drift response behavior
- pack migration and deprecation
- reference-context freshness rules

What is still missing is the rule set for active runs after conditions change mid-execution.

The platform still needs clear answers to these questions:

- what happens when an in-flight run becomes riskier than it was at start?
- when should a run continue, pause, replan, or stop?
- how do policy, drift, migration, and freshness changes affect already-running work?

This spec defines that reevaluation model.

## Executive Summary

A run should not keep executing under stale assumptions just because it already started.

For `morphOS`, the correct posture is:

- reevaluate active runs when meaningful posture changes occur
- separate safe continuation from unsafe continuation
- pause or narrow trust before allowing risky progress
- require explicit reapproval when authority or evidence posture changes materially
- preserve a clear audit trail for all mid-run posture shifts

The goal is active execution that stays legal and trustworthy as conditions evolve.

## Core Design Goals

- make mid-run reevaluation explicit instead of ad hoc
- stop risky continuation under changed conditions
- support targeted replanning rather than needless full restart
- keep policy, governance, and acceptance posture aligned during long runs
- surface operator-visible reasons for pauses, resumes, and run termination

## Reevaluation Principle

Every active run is executing under a posture:

- policy posture
- trust posture
- workflow compatibility posture
- acceptance posture

If one of those changes materially, the run should be reevaluated before crossing the next meaningful boundary.

## What Triggers Reevaluation

The first useful triggers should include:

- new policy verdict or rule change
- upstream drift affecting linked assumptions
- freshness downgrade on required reference context
- workflow pack deprecation or migration-required state
- governance scope change
- tool-family availability or permission change
- repeated execution failure that changes risk posture

Not every event requires immediate stop.
But every meaningful posture change should create a reevaluation check.

## Canonical Reevaluation Objects

`morphOS` should support at least:

- `ActiveRunPosture`
- `ReevaluationTrigger`
- `ReevaluationAssessment`
- `RunContinuationVerdict`
- `RunInterventionRecord`

Suggested meanings:

- `ActiveRunPosture`
  - current policy, trust, compatibility, and acceptance posture for the run
- `ReevaluationTrigger`
  - the event that forces reassessment
- `ReevaluationAssessment`
  - structured analysis of whether continuation remains valid
- `RunContinuationVerdict`
  - the decision on what the run may do next
- `RunInterventionRecord`
  - the emitted record of a mid-run pause, replan, resume, or stop

## Continuation Verdicts

The platform should converge on a small shared set of continuation verdicts:

- `continue`
- `continue_with_restrictions`
- `pause_for_review`
- `pause_for_approval`
- `replan_required`
- `restart_required`
- `terminate`

Suggested meanings:

- `continue`
  - current posture remains acceptable
- `continue_with_restrictions`
  - work may proceed, but only with narrowed authority or scope
- `pause_for_review`
  - human or governed review is required before more progress
- `pause_for_approval`
  - formal approval is required because authority posture changed
- `replan_required`
  - the run may continue only after an updated plan is accepted
- `restart_required`
  - current execution context is too stale to continue safely
- `terminate`
  - the active run should stop and not resume under current conditions

## Reevaluation Lanes

Different triggers should follow different reevaluation lanes.

### Policy Change Lane

Use when:

- a new policy finding or rule makes the current path less safe

Typical outcomes:

- continue with restrictions
- pause for approval
- terminate if the path is now forbidden

### Drift Lane

Use when:

- upstream drift affects linked assumptions, contracts, or twin trust

Typical outcomes:

- pause for review
- replan required
- continue only after narrowed trust posture

### Freshness Lane

Use when:

- reference context used by the run becomes stale or requires refresh

Typical outcomes:

- refresh-before-next-boundary
- continue for low-risk work only
- pause if the next step needs decision-grade references

### Migration Lane

Use when:

- the selected workflow pack or profile becomes migration-required or deprecated during execution

Typical outcomes:

- let the current run finish on existing posture
- require compatibility review before next major phase
- restart only if the current pack is no longer safe for continuation

### Governance Lane

Use when:

- approval scope, workspace boundary, or authority category changes

Typical outcomes:

- pause for approval
- escalate to `super_admin`
- terminate if the required authority path is unavailable

## Boundary-Aware Reevaluation

Reevaluation should happen at meaningful workflow boundaries whenever possible.

Good reevaluation points include:

- before entering validation
- before entering review
- before promotion
- before any live action
- after repeated failure loops

The system should avoid random interruption in the middle of safe local work unless the trigger is severe.

## Severity And Timing

Severity should influence timing.

Suggested posture:

- low severity
  - reevaluate at the next planned boundary
- medium severity
  - reevaluate before the next risky action
- high severity
  - pause before further material progress
- critical severity
  - stop or quarantine the run immediately

This keeps the system proportional without being lax.

## Continuation With Restrictions

Many active runs should not need a full stop.

Useful restriction examples:

- allow reads and local analysis, but block writes
- allow replanning, but block promotion
- allow validation-only steps, but block live actions
- allow artifact assembly, but block new tool use

This gives the runtime a safe middle path between “ignore” and “kill.”

## Replanning Rules

Replanning is appropriate when:

- the original plan assumed capabilities that no longer exist
- required references changed materially
- migration or compatibility posture invalidates the planned path
- policy now requires a different sequence or approval route

Replanning should preserve the run history rather than pretending the original plan never existed.

## Restart Rules

Restart is stronger than replanning.

Use restart when:

- too much of the current execution context depends on invalid assumptions
- pack or profile compatibility changed fundamentally
- active run state cannot be trusted after the posture shift
- operator governance requires a clean restart under new rules

The old run should remain auditable even if a successor run takes over.

## Termination Rules

Terminate when:

- policy now forbids the path entirely
- governance required for continuation is unavailable or denied
- trust posture collapsed for the critical dependency set
- continuing would produce misleading or unsafe results

Termination should be explicit, visible, and justified.

## Relationship To Acceptance

Active-run reevaluation should feed directly into acceptance posture.

Examples:

- a run once headed toward promotion may drop back to review-required
- a previously acceptable validation packet may need refreshed evidence
- a run may lose eligibility for automatic closeout after posture changes

Acceptance should remain dynamic while the run is alive.

## Relationship To Durable Execution

Durable state should preserve:

- the trigger that caused reevaluation
- the current continuation verdict
- any narrowed restrictions
- the evidence needed to resume or terminate

This allows paused runs to be resumed or audited without guessing what happened.

## Operator Surface Requirements

Operator surfaces should be able to show:

- why reevaluation happened
- current continuation verdict
- what is blocked
- what is still allowed
- whether replanning or approval is required
- whether a successor run replaced the original

This keeps mid-run interventions understandable instead of mysterious.

## Required Events And Artifacts

The first useful reevaluation model should emit at least:

- `run.reevaluation_triggered`
- `run.reevaluation_assessed`
- `run.continuation_restricted`
- `run.paused_for_review`
- `run.paused_for_approval`
- `run.replan_required`
- `run.restarted`
- `run.terminated`

Useful artifacts include:

- `reevaluation_trigger.json`
- `reevaluation_assessment.json`
- `continuation_verdict.json`
- `run_intervention_record.json`

## First Implementation Slice

The first implementation slice should stay narrow and practical.

Start with:

- reevaluation trigger objects for policy, drift, freshness, and migration
- continuation verdicts at validation, review, promotion, and live-action boundaries
- pause and restriction handling in durable run state
- operator-visible reason codes for paused or terminated runs

That is enough to make active runs safe under changing conditions before modeling every possible mid-step edge case.

## Relationship To Other Specs

This spec depends on:

- `POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md`
- `DRIFT_RESPONSE_PLAYBOOK_SPEC.md`
- `REFERENCE_CONTEXT_STALENESS_AND_REFRESH_SPEC.md`
- `PACK_MIGRATION_AND_DEPRECATION_SPEC.md`
- `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`

This spec should guide:

- active run pause and resume behavior
- mid-run approval routing
- future durable-state reevaluation features
- operator incident handling for in-flight workflows
