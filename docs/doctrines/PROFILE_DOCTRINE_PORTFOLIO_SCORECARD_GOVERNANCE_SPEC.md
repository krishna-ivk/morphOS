# Profile Doctrine Portfolio Scorecard Governance Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio maturity scorecard
- profile doctrine portfolio scorecard calibration
- profile doctrine portfolio decision authority and audit posture

What is still missing is the governance model for who owns the scorecard itself, who may change it, and how disputes about scorecard posture are resolved in practice.

The platform still needs clear answers to these questions:

- who is responsible for maintaining the doctrine portfolio scorecard?
- who may approve scorecard changes, challenge scorecard ratings, or close scorecard disputes?
- how do we keep the scorecard governed instead of informally edited?

This spec defines that portfolio scorecard-governance layer.

## Executive Summary

Calibration rules are not enough if scorecard ownership is vague.

Scorecard governance should define:

- who owns scorecard stewardship
- who may approve or reject changes
- who may challenge ratings
- how disputes and overrides are handled

For `morphOS`, the correct posture is:

- give the scorecard explicit ownership
- require governed changes for material scorecard movement
- make disputes visible and resolvable
- preserve auditability for all scorecard decisions

The goal is to make the scorecard a real governance instrument rather than a soft narrative artifact.

## Core Design Goals

- define clear ownership of the doctrine maturity scorecard
- establish approval and challenge rights for scorecard changes
- prevent quiet, unreviewed scorecard drift
- connect scorecard governance to existing authority and audit models
- preserve trust that the scorecard is managed deliberately

## Governance Principle

If the scorecard influences attention, planning, or confidence, then it should itself be governed with explicit ownership and authority.

Scorecard governance should therefore:

- assign clear stewards
- distinguish routine maintenance from material change
- make disputes and overrides visible

The scorecard should not be editable by vague consensus.

## What This Spec Covers

The first useful scorecard-governance model should cover:

- scorecard ownership layers
- change classes
- approval routes
- dispute and override handling
- required artifacts and operator visibility

This is enough to make the scorecard governable in day-to-day practice.

## Canonical Governance Objects

`morphOS` should support at least:

- `DoctrineScorecardOwner`
- `DoctrineScorecardChangeClass`
- `DoctrineScorecardApprovalRoute`
- `DoctrineScorecardDispute`
- `DoctrineScorecardGovernanceRecord`

Suggested meanings:

- `DoctrineScorecardOwner`
  - the role or layer currently responsible for scorecard stewardship
- `DoctrineScorecardChangeClass`
  - the kind of scorecard modification being proposed or applied
- `DoctrineScorecardApprovalRoute`
  - the authority path required for that change
- `DoctrineScorecardDispute`
  - a challenge to a scorecard rating, interpretation, or decision
- `DoctrineScorecardGovernanceRecord`
  - durable history of scorecard governance actions

## First Useful Ownership Layers

The first useful ownership layers should include:

- `scorecard_steward`
- `portfolio_authority`
- `workspace_admin`
- `super_admin`

Suggested meanings:

- `scorecard_steward`
  - maintains the scorecard operationally and prepares evidence-backed updates
- `portfolio_authority`
  - approves ordinary material changes within portfolio scope
- `workspace_admin`
  - approves higher-consequence scorecard changes or resolves significant disputes
- `super_admin`
  - handles platform-wide or baseline-contract scorecard exceptions

These layers align scorecard ownership with consequence and scope.

## First Useful Change Classes

The first useful scorecard change classes should include:

- `routine_refresh`
- `material_rating_change`
- `calibration_rule_change`
- `dispute_resolution`
- `exceptional_override`

Suggested meanings:

- `routine_refresh`
  - evidence update that does not materially alter overall interpretation
- `material_rating_change`
  - a change that meaningfully affects one or more maturity dimensions or the rollup
- `calibration_rule_change`
  - a change to the logic or anchors behind scorecard ratings
- `dispute_resolution`
  - a governed decision resolving a challenge to current scorecard posture
- `exceptional_override`
  - a rare change made outside the ordinary path due to unusual governance need

These classes help keep scorecard governance proportional.

## Routine Stewardship Boundary

Routine scorecard stewardship should include:

- collecting current evidence
- preparing ordinary refreshes
- surfacing likely rating changes
- recording unresolved disputes

Routine stewardship should not by itself finalize:

- major rating upgrades with strategic consequence
- calibration rule changes
- exceptional overrides

This keeps stewardship active without making it unilateral.

## Approval Routes

The first useful approval routes should include:

- `steward_prepares_authority_confirms`
- `portfolio_authority_approves`
- `workspace_admin_approves`
- `super_admin_exception_route`

Suggested posture:

- ordinary refreshes may complete through steward preparation plus routine authority confirmation
- material rating changes should go through portfolio authority
- calibration rule changes or major disputes should route higher
- exceptional overrides should remain rare and explicit

This keeps the scorecard stable without making every update heavy.

## Relationship To Calibration

Scorecard governance should enforce calibration, not bypass it.

Suggested posture:

- no material scorecard claim should bypass calibration evidence
- governance may request recalibration review, but should not silently replace it
- calibration disputes should route through the scorecard governance model

This preserves trust in the rating system.

## Relationship To Authority And Audit

Scorecard governance should plug directly into the broader doctrine authority and audit model.

Examples:

- authority layer used for scorecard decisions should be explicit
- all material scorecard changes should create governance records
- out-of-scope scorecard edits should be visible as governance violations or disputes

This keeps the scorecard inside the same control system as other doctrine decisions.

## Relationship To Review Cadence

Scorecard governance should operate on recurring rhythm, not only on demand.

Examples:

- weekly review may confirm no material change
- post-wave review may trigger material rating updates
- dispute review may happen on its own cadence when active

This keeps the scorecard both current and governed.

## Disputes And Overrides

The scorecard should support challenge without becoming unstable.

Suggested posture:

- any material challenge should be recorded as a dispute
- disputes should be resolved by the appropriate authority layer
- overrides should remain explicit, temporary where possible, and heavily auditable

This helps preserve both flexibility and trust.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current scorecard owner
- pending scorecard changes
- active disputes
- approval route for the current change
- whether a rating is settled, contested, or under review

This makes scorecard governance visible instead of hidden in process lore.

## Required Artifacts

The first useful scorecard-governance artifacts should include:

- `scorecard_governance_roles.json`
- `scorecard_change_requests.json`
- `scorecard_disputes.json`
- `scorecard_governance_log.json`

Suggested contents:

- `scorecard_governance_roles.json`
  - current scorecard stewardship and approval ownership
- `scorecard_change_requests.json`
  - proposed and in-flight scorecard changes
- `scorecard_disputes.json`
  - open and resolved scorecard disputes
- `scorecard_governance_log.json`
  - durable history of approvals, rejections, overrides, and dispute resolutions

## First Useful Outcomes

The first useful scorecard-governance outcomes should include:

- `change_approved`
- `change_rejected`
- `dispute_opened`
- `dispute_resolved`
- `override_recorded`

These outcomes make scorecard governance explicit and inspectable.

## Governance Expectations

The scorecard should be governed seriously enough to be trusted, but lightly enough to stay current.

Suggested posture:

- routine upkeep should be easy
- material claims should require real review
- no one should need to guess whether a scorecard change was official

## Non-Goals

This spec does not define:

- broad enterprise governance beyond doctrine scorecards
- a permanent committee structure for every scorecard update
- replacement of evidence-based calibration with governance politics

It only defines how the doctrine portfolio maturity scorecard is owned, changed, challenged, and approved.

## Bottom Line

`morphOS` should govern its doctrine portfolio scorecard explicitly.

If the scorecard is used to shape attention and confidence, then its ownership, changes, disputes, and approvals should be visible, authority-bound, and auditable instead of informal.
