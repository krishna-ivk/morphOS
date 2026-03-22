# Shift Work Execution Semantics Spec

## Why This Spec Exists

`morphOS` already freezes two execution modes:

- `interactive`
- `factory`

It also already states the high-level intent:

- `interactive` means the intent may still evolve
- `factory` means the runtime may continue until a real gate stops it

What is still missing is the operational meaning of that distinction across the full delivery loop.

This spec defines those semantics.

## Executive Summary

Shift Work is the rule that `interactive` and `factory` are not cosmetic labels.
They are different operating modes with different expectations for:

- planning completeness
- interruption behavior
- retry policy
- validation posture
- approval routing
- summary style
- operator involvement

The system should use the same core workflow phases in both modes.
What changes is how much ambiguity is tolerated before the runtime pauses and asks for help.

## Core Design Goals

- make execution mode behavior predictable to humans and agents
- allow autonomous factory execution without hiding meaningful risk
- prevent interactive runs from behaving like silent batch jobs
- ensure policy, validation, and approval still work in both modes
- keep mode behavior stable across CLI, dashboard, and orchestration surfaces

## The Two Modes

### Interactive Mode

Meaning:

- the intent is still being shaped
- the operator may revise scope or direction during the run
- the runtime should prefer surfacing ambiguity early

Default posture:

- collaborate
- confirm
- clarify
- pause sooner

### Factory Mode

Meaning:

- the intent is sufficiently specified for end-to-end execution
- the runtime should continue through deterministic work until a real gate stops it
- interruptions should be minimized

Default posture:

- continue
- validate
- retry within bounds
- escalate only at named gates

## Mode Declaration

Each run should have:

- `execution_mode`
- `execution_mode_source`
- `execution_mode_locked`

Recommended meanings:

- `execution_mode`
  - current mode in force
- `execution_mode_source`
  - whether the mode was declared or inferred
- `execution_mode_locked`
  - whether the runtime may still change the mode

Mode changes should be explicit.
The runtime should not quietly drift from `interactive` to `factory` or back without emitting a visible event.

## Canonical Mode Events

The runtime should support at least:

- `run.mode_declared`
- `run.mode_inferred`
- `run.mode_changed`
- `run.mode_locked`

Each event should include:

- `run_id`
- prior mode when relevant
- new mode
- reason or source

## Phase Semantics By Mode

### 1. Intake

In `interactive` mode:

- incomplete intent is acceptable
- the system may enter planning with open questions
- the operator may still reshape the request materially

In `factory` mode:

- intake should produce a sufficiently bounded objective
- missing core scope, workspace, or target details should block progression

### 2. Planning

In `interactive` mode:

- planning may be iterative
- partial plans are acceptable if the next move is clear
- the operator may reframe goals without treating the run as failed

In `factory` mode:

- planning should produce an executable path with defined outputs
- ambiguous plans should block or revert to review before execution

### 3. Assignment

In `interactive` mode:

- the system may present alternative agent or tool paths
- the operator may choose among options

In `factory` mode:

- assignment should pick a valid route and proceed
- lack of a safe route should block instead of asking speculative questions

### 4. Execution

In `interactive` mode:

- the runtime should surface uncertainty, tradeoffs, and conflicts earlier
- operators may redirect, replan, or revise scope mid-run

In `factory` mode:

- the runtime should continue through bounded deterministic steps
- human interruption should happen only at policy, validation, approval, or unrecoverable failure gates

### 5. Validation

In `interactive` mode:

- findings may be surfaced earlier and more conversationally
- exploratory outputs can still be useful even if not promotion-ready

In `factory` mode:

- validation should prefer deterministic pass, fail, retry, or escalate outcomes
- promotion claims must be evidence-backed

### 6. Review

In `interactive` mode:

- review may be part of ongoing shaping
- a reviewer can redirect the objective itself

In `factory` mode:

- review should mostly focus on acceptance, risk, and exceptions
- rework should re-enter the flow cleanly instead of reopening all prior choices

### 7. Promotion

In `interactive` mode:

- promotion is usually deferred until the run becomes sufficiently stable

In `factory` mode:

- promotion should proceed once validation, approval, and policy conditions are satisfied

### 8. Closeout

In `interactive` mode:

- closeout may emphasize current posture and next action more than terminal readiness

In `factory` mode:

- closeout should emphasize completeness, evidence, and promotion posture

## Interruption Strategy

This is the most important practical difference between modes.

### Interactive Interruption Rule

Interrupt early when:

- scope is unclear
- multiple non-obvious paths exist
- tradeoffs are meaningful
- operator preference changes the right answer

### Factory Interruption Rule

Do not interrupt for ordinary deterministic work.
Interrupt only when:

- policy blocks the next step
- approval is required
- validation cannot clear the work
- retry budget is exhausted
- an unrecoverable failure occurs

## Retry Semantics

### Interactive Mode

- retry budgets should be conservative
- repeated failure should surface quickly
- the operator may decide whether to keep pushing

### Factory Mode

- bounded automated retries are expected
- retries should be visible but not noisy
- exhaustion of retry budget should route to review, approval, or blocked state

## Replanning Semantics

### Interactive Mode

- replanning is normal
- changing the plan does not imply the prior run was wrong

### Factory Mode

- replanning should be exceptional and evidence-triggered
- repeated replanning suggests the run was not actually factory-ready

If this happens, the system should consider mode change or explicit review.

## Validation Semantics

Interactive and factory modes both use the same validation layers.
What changes is what happens after a finding.

### Interactive Mode

- findings may route back to discussion or scope adjustment
- non-blocking findings may still allow the run to continue as exploration

### Factory Mode

- findings should lead to deterministic rework, review, approval, or block decisions
- validation should avoid conversational ambiguity

## Approval Semantics

### Interactive Mode

- approval may appear earlier as a shaping or permission checkpoint

### Factory Mode

- approval should appear only when a named policy or governance boundary requires it
- once approval is granted or denied, the flow should resume deterministically

## Policy Semantics

The same policy hooks should exist in both modes.
The difference is how close to the boundary the system waits before surfacing the issue.

### Interactive Mode

- may surface warnings and review needs earlier

### Factory Mode

- should continue until a real policy gate is reached, then stop decisively

## Summary Semantics

The summary pyramid should render the current mode explicitly when it affects interpretation.

### Interactive Summary Bias

Prefer:

- current posture
- ambiguity or decisions pending
- next discussion point

### Factory Summary Bias

Prefer:

- current control state
- validation posture
- approval state
- readiness or blocked boundary

## Suggested Mode Heuristics

The runtime may infer mode when it is not declared, but the heuristics should be visible.

Possible signals for `interactive`:

- open-ended request wording
- unresolved scope questions
- active human steering
- exploratory or comparative workflow archetype

Possible signals for `factory`:

- bounded scope
- known workspace and target
- explicit requested outputs
- stable workflow template
- acceptable risk posture for autonomous progression

Inference should never be silent.

## Mode Misfit Signals

The runtime should detect when the selected mode appears wrong.

Common signs that a run labeled `factory` is actually `interactive`:

- repeated replanning
- frequent clarification needs
- unresolved scope changes
- operator redirection of core goals

Common signs that a run labeled `interactive` is ready for `factory`:

- stable scope
- repeated deterministic loops
- no meaningful clarifications needed
- bounded outputs and acceptance conditions

These signals should trigger review or explicit mode change, not silent reinterpretation.

## Relationship To Durable Execution

Execution mode affects orchestration behavior, not durable truth ownership.

That means:

- Symphony decides how mode changes workflow progression
- Durable still owns paused, blocked, retried, and resumable execution state

Mode should influence how the runtime uses the durable layer, not who owns it.

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define mode-related enums, events, and summary fields
- `skyforce-symphony` should vary interruption, retry, and replanning behavior by mode
- `skyforce-harness` should project mode-aware receipts when execution context matters
- `skyforce-command-centre` should show why a run paused and whether that pause was mode-expected

## Recommended First Implementation Slice

The first useful slice should be narrow and visible:

1. surface execution mode on all run views
2. vary interruption behavior between `interactive` and `factory`
3. add retry-budget differences by mode
4. emit `run.mode_changed` when the runtime explicitly switches modes
5. include mode in status and summary rendering

That is enough to make the mode meaningful before deeper optimization.

## Recommended Next Specs

This spec should be followed by:

1. `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`
2. `PARALLEL_WORKSPACE_EXECUTION_SPEC.md`
3. `SEMPORT_ADOPTION_BOUNDARY_SPEC.md`

Together, those would close more of the remaining governance, multi-agent, and upstream-porting gaps.
