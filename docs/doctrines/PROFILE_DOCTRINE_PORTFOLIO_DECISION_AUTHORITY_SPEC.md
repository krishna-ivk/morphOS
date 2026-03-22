# Profile Doctrine Portfolio Decision Authority Spec

## Why This Spec Exists

`morphOS` already defines:

- profile doctrine portfolio escalation policy
- profile doctrine portfolio intervention and governance posture
- workspace-admin governance and profile override governance

What is still missing is the authority model for who actually owns doctrine portfolio decisions once issues rise above ordinary queue management.

The platform still needs clear answers to these questions:

- who decides which kinds of doctrine portfolio issues?
- what decisions stay local, and what decisions require broader portfolio or governance authority?
- how do operators know which authority is allowed to approve, defer, constrain, or escalate doctrine work?

This spec defines that portfolio decision-authority layer.

## Executive Summary

Escalation is only useful if the platform knows who may decide next.

Decision authority should define the portfolio-level ownership boundaries for:

- routine stewardship decisions
- triage and deferral decisions
- escalation routing
- intervention decisions
- governance-sensitive doctrine decisions

For `morphOS`, the correct posture is:

- make doctrine authority explicit by decision type and scope
- keep local ownership where possible
- escalate only when the consequence exceeds local decision rights
- preserve a durable record of who decided what and why

The goal is to remove ambiguity from doctrine portfolio decision making.

## Core Design Goals

- define decision rights by doctrine scope and consequence
- distinguish local stewardship from portfolio authority and higher governance
- support fast routing during escalation
- prevent accidental overreach or under-escalation
- preserve auditable decision ownership

## Authority Principle

Doctrine decisions should be made at the lowest level that can responsibly absorb the consequence.

Authority should therefore:

- stay local for ordinary stewardship where possible
- widen when the impact becomes cross-area, strategic, or governance-sensitive
- be explicit enough that operators do not need to guess who may decide

Authority is not about status.
It is about owning the consequence of the decision.

## What This Spec Covers

The first useful decision-authority model should cover:

- authority layers
- decision classes
- routing rules
- reserved decisions
- required artifacts and operator visibility

This is enough to make doctrine portfolio decisions governable and legible.

## Canonical Authority Objects

`morphOS` should support at least:

- `DoctrineDecisionClass`
- `DoctrineAuthorityLayer`
- `DoctrineDecisionRoute`
- `DoctrineAuthorityGrant`
- `DoctrineDecisionAuthorityRecord`

Suggested meanings:

- `DoctrineDecisionClass`
  - the type of doctrine decision being made
- `DoctrineAuthorityLayer`
  - the level of authority allowed to make that decision
- `DoctrineDecisionRoute`
  - the path from issue type to authorized decider
- `DoctrineAuthorityGrant`
  - the allowed scope of authority for a role or control point
- `DoctrineDecisionAuthorityRecord`
  - durable history of decision ownership and exercise

## First Useful Authority Layers

The first useful authority layers should include:

- `local_portfolio_owner`
- `cross_area_portfolio_authority`
- `workspace_admin`
- `super_admin`

Suggested meanings:

- `local_portfolio_owner`
  - owns ordinary doctrine stewardship within a bounded area
- `cross_area_portfolio_authority`
  - owns decisions spanning multiple doctrine families or workflow areas
- `workspace_admin`
  - owns broader workspace-level governance and risk-sensitive doctrine decisions
- `super_admin`
  - owns globally exceptional or platform-wide doctrine decisions that exceed normal workspace authority

These layers align portfolio authority with consequence and scope.

## First Useful Decision Classes

The first useful decision classes should include:

- `routine_stewardship`
- `triage_and_deferral`
- `portfolio_priority_conflict`
- `intervention_activation`
- `intervention_exit_or_reentry`
- `governance_sensitive_exception`
- `platform_wide_doctrine_exception`

Suggested meanings:

- `routine_stewardship`
  - ordinary maintenance and healthy-state portfolio handling
- `triage_and_deferral`
  - ordering and postponement decisions inside normal stewardship
- `portfolio_priority_conflict`
  - tradeoff decisions affecting multiple areas or shared capacity
- `intervention_activation`
  - formal decision to enter strategic intervention posture
- `intervention_exit_or_reentry`
  - decision to step down, close, or normalize portfolio posture
- `governance_sensitive_exception`
  - decisions where compliance, policy, or approval integrity materially matters
- `platform_wide_doctrine_exception`
  - exceptional decisions affecting multiple workspaces or the platform baseline itself

These classes give authority routing a stable vocabulary.

## Local Authority Boundary

The first useful local authority boundary should include:

- routine stewardship
- ordinary watchpoint handling
- normal planned work ordering
- safe deferral with visible watchpoints

Local authority should not extend to:

- cross-area strategic tradeoffs
- formal intervention activation
- governance-sensitive exceptions with broader workspace consequence

This keeps the lowest level empowered without hiding bigger risk.

## Cross-Area Authority Boundary

Cross-area portfolio authority should handle:

- portfolio priority conflicts
- load-driven tradeoffs across multiple doctrine families
- coordinated action before intervention becomes necessary
- escalations that exceed one local owner but not yet broader governance

This layer helps avoid premature jumps to heavy governance.

## Workspace Admin Boundary

Workspace-admin authority should handle:

- intervention activation with workspace-level impact
- intervention exit or reentry with material planning consequence
- governance-sensitive doctrine exceptions inside workspace scope
- doctrine decisions that materially alter workspace trust posture

This aligns with the broader workspace governance model already present in `morphOS`.

## Super-Admin Boundary

Super-admin authority should be reserved for:

- platform-wide doctrine exceptions
- authority conflicts that cannot be resolved within normal workspace governance
- exceptional doctrine decisions with multi-workspace or baseline-contract consequence

This keeps the highest authority rare and meaningful.

## Relationship To Escalation Policy

Escalation policy should feed directly into authority routing.

Examples:

- a persistent deferral escalation may route to cross-area portfolio authority
- a governance-sensitive escalation may route to workspace admin
- a platform-wide doctrine exception may route to super-admin

This keeps escalation from producing ownership ambiguity.

## Relationship To Intervention

Decision authority should also clarify intervention ownership.

Examples:

- activation of targeted intervention may require workspace-admin approval
- coordinated pre-intervention tradeoffs may remain with cross-area portfolio authority
- exit and reentry decisions should be owned according to their planning and trust consequence

This makes intervention lifecycle control explicit.

## Relationship To Governance

Decision authority should work with governance, not duplicate it.

Suggested posture:

- governance defines the allowed authority layers and exceptions
- authority routing applies those rules to current doctrine decisions
- decisions outside granted scope should not be accepted as valid

This helps prevent informal authority drift.

## Authority Conflicts

The first useful authority-conflict cases should include:

- multiple authorities claiming the same decision
- local owners attempting decisions beyond scope
- governance-sensitive issues being held at too low a level
- lack of clear owner for a cross-area doctrine issue

The platform should prefer explicit escalation over silent confusion.

## Operator Surface Requirements

Operator surfaces should be able to show:

- current decision class
- current authorized authority layer
- why the decision routed there
- whether the current user or agent has authority to decide
- where the issue must go next if current authority is insufficient

This makes portfolio decisions operationally clear.

## Required Artifacts

The first useful authority artifacts should include:

- `doctrine_decision_routes.json`
- `doctrine_authority_grants.json`
- `doctrine_decision_authority_log.json`
- `authority_conflicts.json`

Suggested contents:

- `doctrine_decision_routes.json`
  - machine-readable mapping from decision classes to authority layers
- `doctrine_authority_grants.json`
  - current scope of allowed authority by role or layer
- `doctrine_decision_authority_log.json`
  - durable record of who decided what under which authority
- `authority_conflicts.json`
  - unresolved or recent authority-boundary conflicts

## First Useful Outcomes

The first useful authority outcomes should include:

- `decide_locally`
- `route_to_cross_area_authority`
- `route_to_workspace_admin`
- `route_to_super_admin`
- `reject_out_of_scope_decision`

These outcomes make authority handling precise and enforceable.

## Governance Expectations

Authority models should support clarity, not bureaucracy for its own sake.

Suggested posture:

- most ordinary doctrine decisions should remain low in the stack
- higher authority should appear mainly when consequence truly widens
- authority routing should be understandable enough to use quickly during live portfolio pressure

## Non-Goals

This spec does not define:

- the full identity and permissions system
- product-wide RBAC outside doctrine governance
- replacement of human judgment with rigid authority automation

It only defines how doctrine portfolio decisions map to the right level of authority once consequence and scope are understood.

## Bottom Line

`morphOS` should make doctrine portfolio authority explicit.

When a doctrine issue needs a decision, the platform should know whether that decision belongs to local stewardship, cross-area portfolio authority, workspace admin, or super-admin, and it should route accordingly.
