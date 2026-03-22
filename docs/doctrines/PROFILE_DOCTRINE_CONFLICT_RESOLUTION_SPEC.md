# Profile Doctrine Conflict Resolution Spec

## Why This Spec Exists

`morphOS` already defines:

- workflow profile recommendation
- workflow profile resolution
- workflow profile override governance

What is still missing is the doctrine-level arbitration model for when those inputs disagree.

The platform still needs clear answers to these questions:

- what wins when compatibility says one thing and operator preference says another?
- how should recommendations be handled when governance is more conservative?
- how do we adjudicate conflicts between observed fit and declared doctrine?

This spec defines that conflict-resolution layer.

## Executive Summary

Profile doctrine will eventually face competing signals.

For `morphOS`, the correct posture is:

- treat conflict resolution as an explicit governed process
- define a stable order of authority among signals
- preserve hard boundaries around compatibility and governance
- allow recommendations and operator input to influence outcomes only within those bounds

The goal is consistent arbitration instead of case-by-case improvisation.

## Core Design Goals

- make profile disputes predictable and explainable
- prevent soft signals from overriding hard safety boundaries
- let useful operational feedback influence doctrine without destabilizing it
- keep conflict resolution auditable and reviewable
- reduce hidden tension between default doctrine and real usage

## Conflict Principle

Not all signals have the same authority.

Some inputs are advisory:

- recommendations
- operator preference
- observed fit correlations

Some inputs are boundary-defining:

- compatibility constraints
- governance constraints
- hard policy posture

Conflict resolution should respect that difference.

## What This Spec Covers

The first useful conflict model should cover disputes between:

- compatibility results and operator preference
- governance requirements and recommendation signals
- declared defaults and repeated override behavior
- observed fit and current profile doctrine
- workspace-local needs and global platform policy

This is enough to handle the most common doctrine tensions.

## Canonical Conflict Objects

`morphOS` should support at least:

- `ProfileDoctrineConflict`
- `ConflictAssessment`
- `ConflictVerdict`
- `ConflictRationale`
- `ConflictDisposition`

Suggested meanings:

- `ProfileDoctrineConflict`
  - the identified disagreement between doctrine-relevant inputs
- `ConflictAssessment`
  - structured analysis of the conflict
- `ConflictVerdict`
  - the chosen resolution outcome
- `ConflictRationale`
  - why that outcome won
- `ConflictDisposition`
  - what happened after review or escalation

## Conflict Sources

Useful conflict sources include:

- resolution requested one profile, recommendation suggests another
- operator explicitly prefers a profile the system would not normally choose
- repeated overrides suggest doctrine mismatch
- compatibility allows multiple choices but governance prefers a stricter posture
- workspace evidence conflicts with global defaults

Conflict should be modeled as normal system behavior, not as an exceptional embarrassment.

## Authority Order

The first useful authority order should be:

1. hard compatibility constraints
2. hard governance and policy boundaries
3. resolved workflow contract logic
4. approved override rules
5. recommendations and observed-fit signals
6. operator preference where allowed

This means:

- soft signals can influence selection only after hard boundaries are satisfied
- recommendations can guide, but not overrule, the core safety model

## Conflict Verdicts

The platform should converge on a small shared set of verdicts:

- `default_doctrine_upheld`
- `override_allowed`
- `workspace_exception_allowed`
- `change_request_recommended`
- `escalation_required`
- `request_denied`

Suggested meanings:

- `default_doctrine_upheld`
  - the existing resolved posture remains correct
- `override_allowed`
  - a narrow governed exception may proceed
- `workspace_exception_allowed`
  - a local bounded deviation is acceptable
- `change_request_recommended`
  - the conflict suggests doctrine should evolve
- `escalation_required`
  - conflict crosses authority boundaries and needs higher review
- `request_denied`
  - the requested deviation should not proceed

## Compatibility Versus Preference

If compatibility and preference disagree:

- compatibility wins
- preference may still become a change request or simulation candidate
- the platform should explain why preference could not be honored

This prevents “I wanted it” from becoming a stealth compatibility override.

## Governance Versus Recommendation

If governance and recommendation disagree:

- governance wins in the current run
- recommendation may still be preserved as evidence for future change review

This keeps recommendations useful without letting them soften authority boundaries by accident.

## Doctrine Versus Repeated Overrides

Repeated overrides are not automatic proof that doctrine is wrong.

The correct response is:

- detect the pattern
- assess whether the overrides are healthy and repeatable
- decide whether the result is:
  - keep doctrine as-is
  - allow a bounded workspace exception
  - create a profile change request

This turns conflict into structured learning rather than direct mutation.

## Local Versus Global Conflict

Some conflicts are local, some are platform-wide.

Suggested posture:

- workspace-local needs may justify bounded local exceptions
- cross-workspace or shared-policy conflicts should usually escalate
- global doctrine should not shift based on one local convenience case alone

This keeps the blast radius proportional.

## Recommendation And Simulation Linkage

When conflicts are ambiguous, simulation should often be the next step.

Examples:

- recommendation suggests a different profile but governance is cautious
- repeated overrides imply better fit, but evidence is incomplete
- operator preference conflicts with current defaults and wants proof

Simulation can help convert opinion conflict into evidence-backed review.

## Relationship To Change Management

Some conflicts should terminate in a profile change request rather than an override.

Good signals include:

- same conflict recurring across multiple workspaces
- same recommendation repeatedly accepted for review
- same override pattern showing strong evidence in simulation

This keeps doctrine improvement tied to repeated evidence instead of ad hoc pressure.

## Relationship To Active Runs

If a conflict appears during an active run:

- the active-run reevaluation model should decide immediate continuation posture
- doctrine conflict resolution should decide whether the issue is local, temporary, or doctrine-level

This preserves the distinction between operational safety and longer-term doctrine arbitration.

## Operator Surface Requirements

Operator surfaces should be able to show:

- conflicting inputs
- which authority rule decided the outcome
- whether the result was a denial, override, escalation, or change request
- whether simulation or further evidence was requested

This makes profile disputes legible instead of political.

## Required Events And Artifacts

The first useful conflict-resolution model should emit at least:

- `profile_doctrine_conflict.detected`
- `profile_doctrine_conflict.assessed`
- `profile_doctrine_conflict.escalated`
- `profile_doctrine_conflict.resolved`
- `profile_doctrine_conflict.change_request_recommended`

Useful artifacts include:

- `profile_doctrine_conflict.json`
- `conflict_assessment.json`
- `conflict_rationale.md`
- `conflict_disposition.json`

## First Implementation Slice

The first implementation slice should stay intentionally narrow.

Start with:

- conflict detection between operator preference, recommendation, and resolved profile
- stable authority order application
- operator-visible rationale for upheld defaults or denied requests
- conversion path from repeated doctrine conflicts into change requests

That is enough to make profile arbitration explicit before building richer conflict taxonomies and cross-workspace governance analytics.

## Relationship To Other Specs

This spec depends on:

- `WORKFLOW_PROFILE_RECOMMENDATION_SPEC.md`
- `WORKFLOW_PROFILE_RESOLUTION_SPEC.md`
- `WORKFLOW_PROFILE_OVERRIDE_GOVERNANCE_SPEC.md`
- `WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md`
- `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`

This spec should guide:

- doctrine dispute handling
- operator-facing arbitration UX
- future conflict analytics
- escalation from repeated local disagreement into governed platform updates
