# Parallel Workspace Execution Spec

## Why This Spec Exists

`morphOS` already defines:

- a software-factory control flow
- a git-native work ledger
- workspace and global governance
- approval and policy boundaries

What is still missing is a concrete runtime model for safe parallel work.

This spec defines that model.

## Executive Summary

Parallel execution should be a first-class capability, not an accident of launching multiple agents.

For `morphOS`, safe parallel execution means:

- multiple agents may work concurrently
- each concurrent slice has a clear ownership boundary
- ledger, workspace, and branch state remain auditable
- conflicts are surfaced early
- merges and promotions remain governed

The goal is faster delivery without turning the platform into a race-condition factory.

## Core Design Goals

- allow useful concurrency without shared-state chaos
- make ownership of parallel slices explicit
- preserve deterministic run history and approval posture
- minimize duplicate work and token waste
- keep parallel execution compatible with review, validation, and promotion flows

## What A Parallel Slice Is

A `Parallel Slice` is a bounded unit of work that may run concurrently with other slices under one larger delivery objective.

Each slice should have:

- a parent run or delivery objective
- a slice id
- a clear owned scope
- a workspace or worktree boundary
- an assigned agent or agent lane
- declared inputs and expected outputs
- explicit merge or reintegration rules

Parallel work should not begin without this shape.

## Parallelism Is About Scope, Not Just Count

The number of agents matters less than the quality of the boundaries between them.

Parallel work is safe only when slices are:

- disjoint enough to avoid constant conflict
- meaningful enough to justify coordination cost
- traceable enough to reintegrate later

Launching many agents against the same unclear area is not parallelism.
It is duplication.

## Canonical Parallelization Levels

`morphOS` should support at least these levels:

### 1. Research Parallelism

Multiple agents gather non-overlapping information in parallel.

Examples:

- one agent maps policy effects
- one agent inspects runtime contracts
- one agent inventories UI states

### 2. Implementation Parallelism

Multiple agents modify different parts of a system in parallel.

Examples:

- one slice owns Symphony orchestration changes
- one slice owns Harness execution changes
- one slice owns operator surface rendering

### 3. Validation Parallelism

Validation tasks run concurrently with ongoing work where safe.

Examples:

- twin validation running while documentation or closeout is assembled
- review packet generation while final deterministic checks complete

### 4. Workspace Parallelism

Independent workspaces or worktrees are used to isolate concurrent slices.

Examples:

- separate worktree per implementation slice
- isolated workspace per risky experiment

## Required Slice Packet

Each parallel slice should begin with a `Slice Packet`.

Minimum fields:

- `slice_id`
- `parent_run_id`
- `issue_identifier`
- `workspace_id`
- `owned_scope`
- `forbidden_scope`
- `agent_lane`
- `input_refs`
- `expected_outputs`
- `merge_strategy`

Without this packet, ownership and reintegration become ambiguous.

## Ownership Rules

Every slice must have one clear mutation owner for each write surface.

Typical write surfaces:

- contracts
- orchestration logic
- execution adapters
- operator UI
- ledger records
- promotion artifacts

The core rule is:

- one active writer per write surface at a time

Read access may be broader.
Mutation ownership should remain narrow.

## Workspace And Worktree Isolation

Parallel execution should prefer isolated workspaces or worktrees for implementation slices.

Recommended order:

1. dedicated worktree per slice
2. dedicated workspace directory per slice
3. shared workspace only for read-mostly or tightly coordinated work

Why:

- reduces accidental file collisions
- makes cleanup easier
- keeps partial work inspectable
- supports safer promotion and merge review

## Ledger Rules For Parallel Runs

The work ledger must remain coherent even when multiple slices are active.

Required rules:

- each slice must write under a stable slice-aware path or record identity
- parent run state must not be silently overwritten by child slices
- reintegration decisions must be recorded explicitly
- final parent posture should cite which slices merged, failed, or were abandoned

Suggested ledger shape:

- `ledger/runs/<run_id>/slices/<slice_id>/...`

This keeps parallel traces separate while preserving shared lineage.

## Conflict Classes

Parallel execution should treat conflicts as a normal managed case.

Suggested conflict classes:

- `write_conflict`
- `contract_conflict`
- `semantic_conflict`
- `validation_conflict`
- `approval_conflict`
- `merge_conflict`

Examples:

- two slices edit the same contract file
- two slices preserve incompatible workflow semantics
- one slice passes validation while another invalidates the assumptions

## Conflict Handling Rules

When a conflict appears:

1. classify it
2. record it in the ledger
3. decide whether one slice must yield, merge, rebase, or escalate
4. route governance or review if the conflict changes risk posture

Conflicts should never be resolved only through hidden local edits.

## Merge And Reintegration

Parallel work is not complete when the slices finish independently.
It is complete when their outputs are safely reintegrated.

Each slice should declare one of these merge strategies:

- `direct_merge`
- `review_before_merge`
- `rebase_then_merge`
- `artifact_only`
- `abandon_if_conflicted`

Recommended meanings:

- `direct_merge`
  - safe to merge automatically when all checks pass
- `review_before_merge`
  - requires human review before reintegration
- `rebase_then_merge`
  - must reconcile with updated base before merge
- `artifact_only`
  - emits artifacts or findings but no source merge
- `abandon_if_conflicted`
  - lower-priority exploratory slice may be dropped if conflict cost is too high

## Parent Run Authority

The parent run remains the authority for:

- overall delivery posture
- promotion readiness
- final summary posture
- governance and escalation context

Parallel slices should feed the parent run.
They should not each declare their own final delivery truth independently.

## Approval Semantics In Parallel Work

Approvals should not become ambiguous because multiple slices are active.

Rules:

- approvals may be slice-specific or parent-run-wide
- the approval packet must say which scope it applies to
- a slice-local approval does not automatically authorize sibling slices
- parent-run promotion requires that all required slice-level approvals are resolved

## Policy Semantics In Parallel Work

Policy should be evaluated both:

- at the slice boundary
- at reintegration time

Examples:

- one slice may be allowed to experiment in isolation
- reintegration may still be blocked by policy if the merged result changes risk posture

This prevents local success from bypassing global safety.

## Validation Semantics In Parallel Work

Each slice should validate its own owned outputs.
The parent run should also validate the reintegrated result.

That means parallel execution needs two validation layers:

1. slice-local validation
2. reintegration validation

Without the second layer, individually passing slices can still fail when combined.

## Execution Mode And Parallelism

### Interactive Mode

Parallelism should be used more conservatively.

Good uses:

- parallel research
- narrow non-overlapping implementation slices

Avoid:

- broad autonomous fan-out while the user is still shaping core intent

### Factory Mode

Parallelism is more natural when:

- scope is stable
- slice boundaries are clear
- merge strategy is known
- policy and approval paths are predeclared

Factory mode should still avoid unconstrained fan-out.

## Parallelism Budget

The platform should not assume “more agents is always better.”

Recommended first-order rule:

- prefer a small number of well-bounded concurrent slices over many loosely bounded ones

Good signals for more parallelism:

- disjoint file or module ownership
- clear reintegration plan
- low coordination overhead

Bad signals:

- unclear ownership
- shared contract edits still in flux
- strong semantic coupling
- no reintegration owner

## Required Events

The event taxonomy should support at least:

- `task.slice_created`
- `task.slice_started`
- `task.slice_blocked`
- `task.slice_completed`
- `task.slice_abandoned`
- `task.slice_merged`
- `task.slice_conflicted`

Each event should include:

- `run_id`
- `slice_id`
- `owned_scope`
- current slice posture
- parent run relation

## Required Artifacts

Parallel execution should emit durable artifacts.

Suggested baseline:

- `slices/<slice_id>/packet.json`
- `slices/<slice_id>/status.json`
- `slices/<slice_id>/validation.json`
- `slices/<slice_id>/merge_notes.md`
- `slices/<slice_id>/conflicts.json`

These artifacts should feed:

- parent-run summaries
- reintegration review
- promotion readiness
- audit history

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define slice packet, conflict class, and merge strategy contracts
- `skyforce-symphony` should coordinate slice creation, ownership, and reintegration
- `skyforce-harness` should preserve slice-aware receipts and artifacts
- `skyforce-command-centre-live` should show parent-run and slice-level status distinctly
- `skyforce-api-gateway` should normalize parent-run and slice projections for operator clients

## Recommended First Implementation Slice

The first useful slice should be narrow and practical:

1. define `Slice Packet` and slice lifecycle events
2. support one parent run with multiple implementation slices
3. isolate slices via worktree or workspace path
4. require reintegration validation before parent-run promotion
5. render slice conflict and merge posture in operator views

That is enough to make safe parallel delivery real without overbuilding swarm mechanics.

## Recommended Next Specs

This spec should be followed by:

1. `SEMPORT_ADOPTION_BOUNDARY_SPEC.md`
2. `CODE_INTELLIGENCE_RETRIEVAL_SPEC.md`
3. `TOKEN_AND_COMMAND_MEDIATION_SPEC.md`

Together, those would continue the remaining upstream-porting, retrieval, and execution-efficiency work.
