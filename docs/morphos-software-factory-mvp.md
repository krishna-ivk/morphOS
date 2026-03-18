# morphOS Software Factory MVP

Canonical priority note: for the authoritative feature order and repo ownership, see [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md).

## Goal

Make `morphOS` useful first as a software factory operating model.

That means the MVP should help Skyforce reliably do this loop:

1. accept a seed
2. choose a workflow
3. execute work in a bounded workspace
4. validate the result with objective checks
5. summarize outcomes for a human
6. require approval where risk is real
7. feed artifacts back into future runs

The MVP should not turn `morphOS` into a second runtime.

`morphOS` should define the model.
Skyforce should run the model.

## Product Thesis

For the MVP, `morphOS` should be the source of truth for:

- software-factory workflow definitions
- agent archetypes and roles
- artifact schemas
- approval and escalation points
- summary and feedback conventions
- filesystem-based memory conventions

The runtime behavior should stay in:

- `skyforce-symphony` for orchestration
- `skyforce-harness` for bounded execution and checks
- `sky-force-command-centre-live` for human control and visibility
- `skyforce-core` for contracts and shared CLI or validation surfaces

## What To Incorporate Now

These are the strongest ideas to pull into the MVP immediately.

### 1. StrongDM: Shift Work

Use two explicit modes:

- interactive mode
  - human intent is still forming
  - ask, clarify, reshape, approve
- factory mode
  - intent is complete enough to execute
  - run without repeated human interruption until a gate is hit

This should become a first-class `morphOS` concept.

### 2. StrongDM: The Filesystem

Use the filesystem as inspectable shared state for runs.

Each run should have durable folders for:

- seed
- plan
- working notes
- artifacts
- validation evidence
- summaries
- approval packets

This is the cheapest practical memory layer for the MVP.

### 3. StrongDM: Pyramid Summaries

Require multiple summary levels for every run:

- one-line status
- short operator summary
- detailed run summary
- artifact-level evidence

This improves both operator UX and model context reuse.

### 4. Symphony

Use `Symphony` as the orchestration spine.

It already fits the MVP by handling:

- work polling and dispatch
- isolated workspaces
- agent execution loops
- workflow progression
- operator-visible state

### 5. openai/skills

Treat reusable skills as the practical embodiment of agent archetypes.

For the MVP, archetypes do not need to be fully abstract.
They can be defined as:

- role
- capabilities
- allowed tools
- required artifacts
- preferred skills

### 6. Harness Engineering

Every workflow must end in deterministic checks where possible.

The MVP should prefer:

- lint
- tests
- schema checks
- smoke checks
- repo-shape checks
- receipt generation

### 7. Gene Transfusion

When one repo solves something well, make it easy to transplant the pattern into another repo.

For the MVP, this means:

- exemplar-based implementation prompts
- pattern libraries in `morphOS`
- validation after transfer

## What To Defer

These are valuable, but should not be in the first MVP.

- full Digital Twin Universe for all integrations
- autonomous self-modification
- unconstrained learning loops
- full semantic memory platform
- broad multi-company control plane
- generalized Semport as a platform feature
- rich economic optimization loops

## MVP Capabilities

## 1. Seed Intake

The MVP should accept these seed types:

- issue or ticket
- spec or PRD
- bug report
- screenshot or mock
- existing codebase task

Each seed should normalize into one `work order` schema.

## 2. Workflow Selection

`morphOS` should define a small software-factory workflow set.

Recommended MVP workflows:

- feature delivery
- bug fix
- repo evaluation
- release preparation
- incident triage

Each workflow should define:

- required inputs
- step types
- validation expectations
- approval points
- outputs

## 3. Archetypes

Recommended MVP archetypes:

- planner
- coder
- reviewer
- validator
- releaser
- operator liaison

Each archetype should specify:

- responsibilities
- tool permissions
- expected artifacts
- failure escalation conditions

## 4. Artifact Contracts

The MVP should standardize a few critical artifacts:

- work order
- run plan
- execution receipt
- validation report
- summary pyramid
- approval packet
- run memory index

## 5. Approval Model

The MVP should have explicit approval gates for:

- production-impacting changes
- release actions
- publish actions
- unresolved validation failures
- policy exceptions

Approvals should produce a structured artifact, not just a button click.

## 6. Filesystem Memory

Each run should have a standard directory layout like:

```text
run/
  seed/
  plan/
  work/
  artifacts/
  validation/
  summaries/
  approvals/
  memory/
```

This gives the model and the human the same inspectable state.

## 7. Summary Pyramid

Every run should emit:

- `status.txt`
- `summary_short.md`
- `summary_full.md`
- `evidence.json`

That gives both machine-friendly and human-friendly visibility.

## 8. Feedback Loop

The MVP feedback loop should be simple and governed:

- keep successful artifacts
- keep failed validation evidence
- keep human approval or rejection reasons
- attach these to future similar runs

This should be retrieval and exemplar driven, not self-modifying.

## Repo Responsibilities For The MVP

## morphOS

Own:

- workflow specs
- archetype specs
- artifact schemas
- run directory conventions
- summary pyramid conventions
- approval and escalation semantics

Do not own:

- active orchestration runtime
- direct execution engine
- primary operator UI

## skyforce-symphony

Implement:

- workflow loading
- workflow execution
- shift-work mode handling
- step progression
- run directory creation
- summary artifact collection
- approval pause and resume

## skyforce-harness

Implement:

- bounded command execution
- validation checks
- receipts
- evidence packaging

## sky-force-command-centre-live

Implement:

- work queue and run visibility
- summary pyramid display
- validation evidence display
- approval actions
- operator notes and rejection reasons

## skyforce-core

Implement:

- shared schemas
- CLI inspection tools
- validation helpers
- artifact contract enforcement

## The MVP User Journey

1. A human submits a seed.
2. `morphOS` workflow selection chooses a factory workflow.
3. `Symphony` creates a workspace and assigns archetypes.
4. Agents work inside a standard filesystem layout.
5. `Harness` runs objective validation checks.
6. The system emits summary pyramid artifacts.
7. `Command Centre` shows results and requests approval if needed.
8. Approval or rejection is stored as a structured artifact.
9. The next similar run can reuse these artifacts as exemplars.

## Recommended First Deliverables

If we want a real MVP quickly, I would build these first:

1. `work_order` schema
2. `summary_pyramid` schema
3. standard run directory layout
4. feature delivery workflow spec
5. bug fix workflow spec
6. approval packet schema
7. Symphony support for `program` and `approval` step execution
8. Harness receipt and validation report format
9. Command Centre views for summaries, evidence, and approvals

## Suggested Priorities

### Priority A: Must Have

- shift-work distinction
- workflow specs
- archetypes
- validation contracts
- approval gates
- filesystem memory layout
- summary pyramid

### Priority B: Strong Next Step

- exemplar retrieval for similar tasks
- reusable skills mapped to archetypes
- transfer patterns between repos
- replayable integration fixtures

### Priority C: Later

- richer learning layer
- semport automation
- broad digital twin universe
- budget optimization and economic routing

## MVP Definition Of Done

The MVP is done when a human can:

1. submit a software task as a seed
2. watch the system choose and run a workflow
3. inspect validation evidence
4. approve or reject at a clear gate
5. see compact and detailed summaries
6. rerun similar work with useful prior artifacts available

If those six things work reliably, `morphOS` is functioning as a software factory operating model.

## Current Implementation Status

Status snapshot date:

- `2026-03-18`

Current milestone estimates:

- local software-factory MVP: `80%`
- workflow orchestration and task routing: `85%`
- validation and approval loop: `80%`
- real feature implementation into source code: `45%`
- full Skyforce multi-repo production path: `55%`

### What Is Already Working

The local `morphOS` MVP runtime is now beyond pure planning and documentation.

The current repository includes:

- a runnable local orchestrator
- a CLI for workflow execution and inspection
- a workflow library for feature delivery, bug fix, release, incident triage, repo evaluation, and smoke runs
- run directory creation with stored artifacts and summaries
- contract validation and evidence generation
- approval pause and resume behavior
- connectivity-aware pause and replay behavior
- retrieval context attached to runs

Representative working paths:

- `codex_smoke` completes end to end
- `feature_pipeline` completes end to end
- `release_pipeline` pauses correctly at approval gates and resumes after approval
- local validation and policy tests are passing

### What This Means

`morphOS` now has a real software-factory execution loop for the local MVP:

1. a seed is accepted
2. a workflow is selected
3. a workspace is created
4. steps execute through programs and agents
5. validation artifacts are generated
6. summaries are emitted
7. approvals can pause and resume the run

This means the software-factory model is no longer only conceptual.

### What Is Still Thin

The current local MVP should still be treated as an early execution layer rather than a production-grade autonomous factory.

Important gaps remain:

- the default local `coding_agent` is still a bounded worker and not yet a strong general-purpose feature builder
- workspace-to-source promotion is not yet the normal end state of every feature workflow
- deployment is still simulated in the local MVP
- local validation is real, but still scoped around the MVP runtime and its test harness
- multi-repo operator integration is not yet the default path for all runs

### Practical Interpretation

Today, `morphOS` can credibly claim:

- a working local software-factory MVP
- working workflow execution semantics
- working validation and approval gates
- working run artifacts and summary outputs

Today, `morphOS` cannot yet claim:

- dependable direct feature delivery into real product repos as the default mode
- a full production-ready Skyforce factory across `Symphony`, `Harness`, `Core`, and Command Centre
- a mature autonomous coding backend with reliable merge-ready output

### Next Milestone To Unlock

The next major milestone is to move from:

- `workflow executes successfully`

to:

- `workflow produces trustworthy source changes that can be promoted, reviewed, and landed`

That requires:

- a stronger coding backend by default
- first-class workspace promotion
- tighter integration with Skyforce operator surfaces
- preservation of approval and validation gates as merge and release controls
