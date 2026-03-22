# P0 Factory Spine Recovery Plan

## Purpose

This document resets near-term execution around the minimum viable AI software factory transaction:

`Intake -> Plan -> Code -> Harness Test -> Human Approval -> Git Merge`

The goal is to stop expanding doctrine faster than the factory proves itself in practice.

## Decision

For the next execution wave, the platform should prioritize one complete, successful, automated delivery spine over additional doctrine expansion.

This means:

- freeze most new doctrine/spec writing
- protect only MVP-blocking contract work
- focus implementation on one real end-to-end transaction

## Why

The current stack is strong on:

- control-flow doctrine
- artifact discipline
- governance concepts
- filesystem-first inspectability

But it is still weak on:

- a proven end-to-end factory run
- self-repair after failed validation
- safe sandboxed execution
- context retrieval at runtime
- real-time observability

The system now needs proof more than additional theory.

## P0 Outcome

Success for this phase is:

1. a seed becomes a normalized `work_order`
2. a planner produces a usable plan
3. a coder changes a real repo
4. `skyforce-harness` runs validation
5. failure returns a structured receipt and retry path
6. success produces an approval packet
7. a human approves
8. the change merges cleanly

Until this works, broader doctrine remains secondary.

## Scope In

This phase includes:

- `work_order` creation and consumption
- planner-to-coder handoff
- coder-to-harness execution
- harness receipt production
- minimal retry / self-healing loop
- approval packet generation
- merge-ready closeout
- minimal run telemetry

## Scope Out

This phase excludes new work on:

- profile doctrine expansion
- portfolio scorecards
- maturity ladders
- multi-wave doctrine systems
- advanced super-admin governance
- nonessential semport refinement

These are deferred unless they directly block the P0 spine.

## Hard Priorities

### `P0.1` Golden Path

Build one tiny feature or bug-fix path that completes end to end.

Target:

- one repo
- one small change
- one merge

### `P0.2` Self-Repair Loop

If validation fails, the system should not immediately fall back to human intervention.

Minimum requirement:

- one or two bounded retry rounds
- receipt-aware replan or patch step
- escalation only after bounded retries fail

### `P0.3` Safe Execution Boundary

The coder/harness path must not rely on unrestricted host execution as the long-term default.

Minimum requirement:

- define and enforce one real sandbox boundary
- container, jailed workspace, or equivalent bounded executor

### `P0.4` Runtime Context Injection

The planner and coder need targeted context, not just filesystem presence.

Minimum requirement:

- relevant files
- tests
- contract refs
- changed-surface context

### `P0.5` Minimal Telemetry

Filesystem artifacts stay, but the system also needs lightweight live visibility.

Minimum requirement:

- event stream or run timeline
- failure counters
- current run state visibility

## Implementation Sequence

1. choose one golden-path task
2. normalize it into `work_order`
3. drive planner output into coder execution
4. connect coder output to harness validation
5. emit execution receipt
6. add bounded failure retry loop
7. emit approval packet
8. complete human approval and merge
9. record what broke
10. repeat once more before widening scope

## Repo Focus

Primary repos for this phase:

- [morphOS](/home/vashista/skyforce/morphOS)
  - source of doctrine and MVP contracts only
- [skyforce-symphony](/home/vashista/skyforce/skyforce-symphony)
  - orchestration and planning loop
- [skyforce-harness](/home/vashista/skyforce/skyforce-harness)
  - execution and receipt loop
- [skyforce-command-centre](/home/vashista/skyforce/skyforce-command-centre)
  - approval and operator surface
- [skyforce-core](/home/vashista/skyforce/skyforce-core)
  - shared contracts and sync helpers

## Freeze Rule

New specification work is paused unless it meets one of these tests:

- directly unblocks the P0 spine
- defines a missing MVP contract required by code
- clarifies behavior that is causing current implementation ambiguity

If not, it waits.

## Allowed Spec Work

Still allowed during this phase:

- corrections to MVP contract docs
- implementation-aligned updates to:
  - [WORK_ORDER_SCHEMA_SPEC.md](../../core-mechanics/WORK_ORDER_SCHEMA_SPEC.md)
  - [AGENT_ARCHETYPES_SPEC.md](../../architecture/AGENT_ARCHETYPES_SPEC.md)
  - [APPROVAL_PACKET_SCHEMA_SPEC.md](../../core-mechanics/APPROVAL_PACKET_SCHEMA_SPEC.md)
  - [EXECUTION_RECEIPT_SCHEMA_SPEC.md](../../core-mechanics/EXECUTION_RECEIPT_SCHEMA_SPEC.md)
  - [MVP_WORKFLOW_BEHAVIOR_SPEC.md](../../core-mechanics/MVP_WORKFLOW_BEHAVIOR_SPEC.md)

## Exit Criteria

This recovery phase ends only when:

- one full golden-path run merges successfully
- one failure path retries before escalating
- one approval packet is used for a real decision
- one sandboxed execution path is real, not aspirational
- one second run succeeds without redesigning the whole system

## Anti-Patterns

Avoid these failures:

- writing more doctrine instead of debugging the spine
- declaring success after a partial dry run
- using manual heroics and calling it automation
- bypassing validation or approval to make the demo pass
- widening scope after one lucky run

## Summary

The factory now needs proof of production, not more administrative doctrine.

This recovery plan narrows the mission to one complete delivery spine, one bounded self-repair loop, one safe execution boundary, one minimal context path, and one minimal telemetry path. Everything else waits until the line produces real output.
