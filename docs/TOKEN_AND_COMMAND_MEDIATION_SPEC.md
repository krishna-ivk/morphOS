# Token And Command Mediation Spec

## Why This Spec Exists

`morphOS` already defines:

- tool registry and action discovery
- code intelligence retrieval
- software-factory control flow

What is still missing is the runtime discipline between intention and execution:

- when should an agent retrieve more context?
- when should it run a command?
- when should it summarize instead of expand?
- when should it defer, ask for approval, or stop?

This spec defines that mediation layer.

## Executive Summary

Token and command mediation is the layer that decides how the system spends attention and action budget.

Its job is to prevent two common failures:

- wasteful over-exploration
- unsafe or noisy command execution

The correct posture is:

- retrieve only enough context to make the next step credible
- run only the commands that materially advance the flow
- summarize aggressively when detail is not needed
- escalate when more action would be risky, redundant, or low-confidence

This makes the runtime more efficient without making it reckless.

## Core Design Goals

- reduce token waste and duplicate exploration
- keep command execution purposeful and traceable
- make mediation decisions visible enough to debug
- align execution with policy, approval, and run mode
- keep agents from using brute-force context loading as a default strategy

## What Mediation Is

Mediation sits between:

- a semantic action request
- the retrieval and tool systems

It decides how much context to load, which command path to take, and whether execution is justified at all.

In practical terms, it answers:

- do we need more context or enough already exists?
- is a read command enough or is a write command justified?
- should we run one precise command or many broad ones?
- should we summarize existing evidence instead of collecting more?

## What It Is Not

Mediation is not:

- policy itself
- orchestration meaning
- tool discovery itself
- a generic rate limiter with no semantic awareness

It is the runtime judgment layer between planning and concrete execution.

## The Two Budgets

The mediation layer should manage two related budgets:

### 1. Context Budget

How much context may be loaded or expanded before the next decision?

Examples:

- files opened
- symbols expanded
- retrieval results loaded
- summaries expanded into full detail

### 2. Action Budget

How much concrete execution may be attempted before re-evaluation?

Examples:

- shell commands
- tool actions
- validation runs
- external writes

These budgets are different.
Large context use does not automatically justify large action use.

## Canonical Mediation Questions

Before loading more context:

- is the next action blocked by missing information?
- can retrieval narrow the scope first?
- would summary-level context be enough?

Before running a command:

- what decision or artifact will this command advance?
- is there a lower-risk read-only alternative?
- is this command allowed in the current mode and policy posture?

Before expanding further:

- are we learning something new or just confirming what we already know?

## Mediation Decision Types

The runtime should support at least these mediation decisions:

- `load_context`
- `summarize_context`
- `run_read_command`
- `run_write_command`
- `run_validation_command`
- `defer_action`
- `request_review`
- `request_approval`
- `stop_and_replan`

These are not raw tool calls.
They are mediation outcomes that then map into retrieval or tool actions.

## Context Loading Rules

### Rule 1: Narrow Before Expanding

Prefer:

- symbol lookup before broad semantic search
- targeted file reads before loading many files
- short summary before full narrative

### Rule 2: Reuse Existing Evidence

If the needed evidence already exists in:

- receipts
- summaries
- validation artifacts
- prior retrieval results

prefer using it instead of reloading large context.

### Rule 3: Prefer Structural Certainty Over Semantic Breadth

When exact structure is available, use it first.

Examples:

- exact file path
- symbol definition
- direct contract mapping

This reduces token waste and ambiguity.

## Command Selection Rules

### Rule 1: Read Before Write

Prefer read-only commands when the system is still establishing what is true.

### Rule 2: One Material Step At A Time

A command should materially advance:

- implementation
- validation
- evidence
- summary
- promotion posture

If it does not, it is probably noise.

### Rule 3: Bound Command Fan-Out

Do not execute many similar commands when one precise command or retrieval query would do.

### Rule 4: Prefer Artifact-Producing Commands

When possible, choose commands that leave useful receipts, artifacts, or structured outputs.

## Mode-Aware Mediation

### Interactive Mode

Prefer:

- smaller context expansions
- earlier summary handoffs
- more explicit re-evaluation before risky commands

### Factory Mode

Prefer:

- bounded autonomous progress
- narrow but decisive retrieval
- deterministic command sequences where the path is already known

The mediation layer should adapt to mode without changing the underlying policy rules.

## Policy And Approval Interaction

Mediation should consult policy posture before escalating to concrete execution.

Examples:

- a risky write command may become `request_approval`
- a live external action may become `defer_action` pending twin validation
- a blocked command path may become `stop_and_replan`

Mediation is not policy, but it should avoid proposing obviously illegal actions as the next step.

## Retrieval Interaction

Mediation should treat retrieval as a cheaper alternative to blind command execution when the problem is still informational.

Examples:

- use contract mapping before grepping the entire repo
- use symbol lookup before recursively opening many files
- use retrieval evidence before rerunning broad scans

This is where code intelligence retrieval pays off directly.

## Summary Interaction

Mediation should decide when summary is enough.

Examples:

- use `status.txt` or short summary for posture checks
- use full summary only when review or recovery requires it
- avoid expanding every artifact when the next step only needs current posture

Summary is part of the budget strategy, not just a reporting layer.

## Parallel Execution Interaction

Parallel slices should each have their own mediation posture.

Examples:

- one slice may need high retrieval budget but low action budget
- another slice may already be implementation-ready and need low retrieval but higher action budget

This helps avoid duplicated repo exploration across slices.

## Canonical Mediation Objects

`morphOS` should support at least:

- `MediationContext`
- `MediationDecision`
- `MediationReason`
- `BudgetPosture`
- `CommandProposal`

Suggested meanings:

- `MediationContext`
  - current run mode, scope, policy posture, and known evidence
- `MediationDecision`
  - what kind of next move is allowed or preferred
- `MediationReason`
  - why that move was chosen
- `BudgetPosture`
  - current context and action budget stance
- `CommandProposal`
  - a proposed command path before tool execution

## Suggested Budget Postures

The first useful budget postures should be:

- `minimal`
- `normal`
- `exploratory`
- `constrained`

Examples:

- `minimal`
  - use only the smallest context or command needed
- `normal`
  - standard bounded work
- `exploratory`
  - broader search allowed because the problem is still under-defined
- `constrained`
  - reduce activity because of risk, failure history, or approval posture

## Required Mediation Evidence

Mediation decisions should be inspectable.

Suggested fields:

- `decision_type`
- `budget_posture`
- `trigger`
- `reason`
- `inputs_used`
- `commands_considered`
- `commands_selected`
- `commands_rejected`

This keeps the layer debuggable instead of magical.

## Anti-Patterns

The mediation layer should actively discourage:

- opening many files without narrowing first
- repeating similar searches after clear results already exist
- running write commands before establishing current truth
- using large context expansion to compensate for weak planning
- executing broad validation when a focused check would answer the question

## Relationship To The Software Factory

Mediation should be aware of phase.

Examples:

- planning phase prefers retrieval and summarization
- execution phase prefers targeted write commands
- validation phase prefers evidence-producing checks
- closeout phase prefers summary generation and artifact completion

This keeps command behavior aligned with the delivery loop.

## Required Artifacts

The mediation layer should emit durable or inspectable artifacts when needed.

Suggested baseline:

- `mediation/context.json`
- `mediation/decision.json`
- `mediation/command_proposals.json`
- `mediation/evidence.json`

These are especially useful for:

- debugging agent efficiency
- explaining paused or deferred work
- analyzing token waste patterns

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define mediation decision and budget-posture contracts
- `skyforce-symphony` should use mediation before broad retrieval or tool fan-out
- `skyforce-harness` should surface command outcomes in a form the mediation layer can learn from
- `skyforce-command-centre` may show why the system chose to pause, summarize, or limit execution

## Recommended First Implementation Slice

The first useful slice should be narrow and practical:

1. define mediation decision and budget-posture contracts
2. mediate between targeted retrieval and command execution
3. prefer read-before-write and narrow-before-expand defaults
4. emit mediation evidence for blocked or deferred command paths
5. make mediation mode-aware for `interactive` and `factory`

That is enough to improve efficiency and traceability without building a full optimizer first.

## Recommended Next Specs

This spec should be followed by:

1. `DIGITAL_TWIN_UNIVERSE_ROLLOUT_SPEC.md`
2. `REVIEW_LOOP_AUTOMATION_SPEC.md`
3. `TOKEN_ECONOMY_AND_OBSERVABILITY_SPEC.md`

Together, those continue the remaining twin-expansion, review-automation, and efficiency-observability work.
