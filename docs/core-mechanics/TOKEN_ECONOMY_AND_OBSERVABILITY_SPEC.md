# Token Economy And Observability Spec

## Why This Spec Exists

`morphOS` now defines:

- token and command mediation
- code intelligence retrieval
- policy-aware execution boundaries

What is still missing is the observability layer for efficiency itself.

This spec defines that layer.

## Executive Summary

Token economy is not just about reducing cost.
It is about making runtime attention legible and governable.

The platform should be able to answer questions like:

- why did this run consume so much context?
- which slice spent tokens without producing useful evidence?
- did retrieval narrow the problem or just churn?
- did command execution materially advance the run?

The right posture is:

- observe token and context use explicitly
- correlate usage with outputs and outcomes
- detect waste patterns early
- optimize for delivery value, not just low spend

## Core Design Goals

- make attention and execution costs visible
- tie spend to artifacts, outcomes, and phases
- distinguish healthy exploration from wasteful churn
- support budget-aware policy and mediation decisions
- help operators and builders improve system efficiency over time

## What The Token Economy Is

The token economy is the measurable flow of:

- context expansion
- retrieval activity
- summarization work
- command and tool proposals
- execution attempts
- validation runs

across a run or slice.

It is not only LLM token billing.
It is the broader economy of runtime attention and action.

## What It Is Not

This spec is not:

- a raw billing system
- a simplistic “use fewer tokens” doctrine
- a replacement for mediation or policy

It is the observability and governance layer around efficiency.

## Canonical Cost Dimensions

The platform should track at least these dimensions:

### 1. Context Cost

Examples:

- files opened
- retrieval expansions
- summary expansions
- graph traversals

### 2. Reasoning Cost

Examples:

- number of deliberation turns
- repeated reconsideration of the same question
- replan frequency

### 3. Command Cost

Examples:

- shell command count
- tool action count
- validation run count
- external call attempts

### 4. Waste Cost

Examples:

- duplicate searches
- stale retrieval use
- repeated command failures
- large context loads with no resulting action

### 5. Outcome Value

Examples:

- evidence produced
- blockers resolved
- review packet completed
- promotion posture advanced

Cost alone is not enough.
The system must compare cost to outcome value.

## Canonical Observability Questions

The system should be able to answer:

1. what did this run spend attention on?
2. what concrete outputs did that spend produce?
3. which steps were efficient?
4. which steps were noisy, repetitive, or low-yield?
5. was the current budget posture appropriate?

## Observability Units

The first useful units of measurement should be:

- per run
- per slice
- per phase
- per agent lane
- per tool or command family
- per retrieval query type

This makes analysis actionable instead of abstract.

## Suggested Metrics

The platform should track metrics such as:

- `context_units_loaded`
- `retrieval_queries_count`
- `retrieval_result_expansion_count`
- `summary_expansion_count`
- `commands_executed_count`
- `write_commands_count`
- `validation_runs_count`
- `duplicate_query_count`
- `repeated_failure_count`
- `artifact_outputs_count`
- `promotion_advancement_count`

These do not need to be perfect billing-grade units to be useful.

## Efficiency Ratios

The most useful signals are often ratios, not raw totals.

Examples:

- artifacts produced per command
- useful retrieval results per retrieval query
- validation findings resolved per retry
- summary reuse versus full re-expansion
- promotion advancement per total action count

These help distinguish productive effort from churn.

## Budget Posture Tracking

The budget postures already named in mediation should be observable:

- `minimal`
- `normal`
- `exploratory`
- `constrained`

The system should record:

- which posture was active
- why it was chosen
- whether the actual spend matched that posture

Example:

- a `minimal` posture with huge context expansion suggests mediation drift

## Phase-Aware Observability

Cost should be interpreted in the context of the current factory phase.

Examples:

- planning may justify more retrieval and less command execution
- execution may justify more write commands
- validation may justify more evidence-producing checks
- closeout should prefer summary reuse over large fresh exploration

Without phase awareness, the same behavior may be misclassified.

## Waste Pattern Detection

The platform should detect waste patterns explicitly.

Suggested initial waste classes:

- `duplicate_retrieval`
- `over_expansion`
- `retry_churn`
- `low_yield_command_fanout`
- `stale_context_use`
- `summary_bypass`

Examples:

- reopening many files after exact symbol location is already known
- repeating the same failed command path without new evidence
- reading full summaries when `status.txt` would suffice

## Helpful Versus Harmful Exploration

Not all high spend is bad.

Healthy exploration usually shows:

- narrowing scope over time
- better quality decisions
- artifact or evidence production
- reduced uncertainty

Harmful exploration usually shows:

- repeated similar searches
- wide fan-out with little synthesis
- rising cost with no posture advancement

Observability should distinguish these cases.

## Relationship To Policy

Policy may consume token-economy signals.

Examples:

- repeated low-yield retries can trigger constrained posture
- runaway exploration may trigger defer, replan, or kill behavior
- risky command fan-out may tighten policy posture

The token economy does not replace policy, but it gives policy a richer basis for intervention.

## Relationship To Review

Review surfaces should be able to see whether a run was:

- efficient and evidence-backed
- costly but justified
- noisy without meaningful progress

This is especially useful for:

- debugging automation quality
- deciding whether to trust an autonomous run
- improving workflow templates

## Relationship To Parallel Execution

Parallel slices should be compared independently before being aggregated.

Examples:

- one slice may be efficient and high-yield
- another may be noisy and conflict-heavy

Parent-run observability should preserve that distinction.

## Relationship To Persistent Memory

Persistent memory may later learn from economy signals.

Examples:

- which retrieval patterns were useful
- which command sequences were low-yield
- which workflows routinely burn effort without progress

But current-run observability should remain grounded in actual run artifacts first.

## Required Events

The event taxonomy should support at least:

- `economy.context_expanded`
- `economy.command_executed`
- `economy.waste_detected`
- `economy.budget_shifted`
- `economy.summary_reused`
- `economy.slice_profile_updated`

Each event should include:

- `run_id`
- optional `slice_id`
- phase
- budget posture
- measured dimension
- delta or aggregate value

## Required Artifacts

The observability layer should emit durable or inspectable artifacts.

Suggested baseline:

- `economy/run_profile.json`
- `economy/slice_profiles.json`
- `economy/waste_findings.json`
- `economy/budget_history.json`
- `economy/outcome_ratios.json`

These artifacts should help both operators and builders understand efficiency posture.

## Operator Surface Expectations

Operator views should make it easy to see:

- whether a run is efficient or noisy
- where spend concentrated
- whether the spend produced useful evidence
- whether constrained posture or replan is advisable

Avoid exposing raw numbers without interpretation.

Prefer:

- simple health summaries
- waste pattern flags
- efficiency trend indicators

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define economy events, waste classes, and profile artifacts
- `skyforce-symphony` should emit phase-aware efficiency signals and budget posture changes
- `skyforce-harness` should project command and validation outcomes into economy profiles
- `skyforce-command-centre` should show efficiency posture and waste findings in run and slice views

## Recommended First Implementation Slice

The first useful slice should be narrow and practical:

1. define run-level economy profile artifacts
2. track retrieval count, command count, validation count, and artifact outputs
3. detect simple duplicate retrieval and repeated failure patterns
4. surface budget posture and waste findings in operator views
5. keep the first pass descriptive before making it strongly prescriptive

That is enough to make efficiency visible before using it heavily for policy or automation changes.

## Recommended Next Specs

This spec should be followed by:

1. `CONTEXT_HUB_RUNTIME_INTEGRATION_SPEC.md`
2. `EVAL_DRIVEN_ACCEPTANCE_SPEC.md`
3. `UPSTREAM_DRIFT_MONITORING_SPEC.md`

Together, those continue the remaining context integration, evaluation, and drift-management work.
