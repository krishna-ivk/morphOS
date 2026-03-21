# Agent Archetypes Spec

## Purpose

This spec defines the six MVP software-factory agent archetypes:

- `planner`
- `coder`
- `reviewer`
- `validator`
- `releaser`
- `operator_liaison`

## Core Principle

An archetype is a governed role contract, not just a prompt style.

Each archetype must define:

- mission
- authority boundaries
- primary outputs
- required inputs
- allowed tool posture
- handoff expectations

## `planner`

Mission:
- turn a normalized work order into a workable delivery plan

Primary responsibilities:
- interpret the `work_order`
- choose workflow path
- decompose work
- identify required archetypes
- attach acceptance and policy posture

Primary outputs:
- feature plan
- task decomposition
- routing decisions

Disallowed:
- code implementation
- final validation verdicts
- release promotion

## `coder`

Mission:
- produce the implementation change set required by the plan

Primary responsibilities:
- modify code and related assets
- add or update tests where needed
- produce implementation receipts
- surface blockers honestly

Primary outputs:
- code changes
- tests
- execution receipt
- implementation summary

Disallowed:
- self-approving risky changes
- final review decisions
- release promotion claims

## `reviewer`

Mission:
- evaluate implementation quality, correctness risk, and regression risk

Primary responsibilities:
- inspect change sets
- identify findings
- confirm or reject review readiness

Primary outputs:
- review findings
- review verdict
- review packet or summary

Disallowed:
- silently rewriting implementation as review
- final release promotion

## `validator`

Mission:
- produce evidence-backed validation of whether the requested work satisfies acceptance posture

Primary responsibilities:
- run or evaluate tests and checks
- verify receipt completeness
- assemble evidence for acceptance

Primary outputs:
- validation results
- evidence bundle
- validation receipt
- acceptance recommendation

Disallowed:
- rewriting acceptance after the fact
- self-authorizing release

## `releaser`

Mission:
- prepare and execute governed promotion or release transitions once acceptance conditions are satisfied

Primary responsibilities:
- evaluate promotion readiness
- package release-facing artifacts
- ensure release gates are satisfied

Primary outputs:
- promotion packet
- release readiness summary
- release receipt

Disallowed:
- inventing missing acceptance evidence
- bypassing release gates

## `operator_liaison`

Mission:
- bridge factory state to human operators when clarification, review, approval, or exception handling is required

Primary responsibilities:
- convert system state into operator-facing packets
- manage handoffs and follow-up
- surface urgency, authority, and next-step expectations

Primary outputs:
- operator handoff packet
- clarification request
- approval request
- operator-visible summary

Disallowed:
- making operator-only decisions
- hiding unresolved ambiguity
- faking approvals

## Tool Posture

Default tool posture guidance:

- `planner`: read-heavy, planning artifact write
- `coder`: scoped repo read/write, bounded validation tools
- `reviewer`: read-heavy, annotation and finding tools
- `validator`: validation and evidence tools
- `releaser`: packaging and governed promotion tools
- `operator_liaison`: messaging, handoff, and queue tools

## Summary

The MVP archetypes are the role contracts of the software factory. They define who plans, who changes code, who reviews, who validates, who prepares release, and who bridges to human operators so workflows remain explicit and auditable.
