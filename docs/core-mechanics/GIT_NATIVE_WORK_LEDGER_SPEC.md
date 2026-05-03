# Git Native Work Ledger Spec

This document defines a git-native work ledger for `morphOS`.

It is the second follow-on specification from the starred repo
gene-transfusion backlog and is primarily informed by:

- `jallum/beadwork`
- StrongDM `The Filesystem`
- the existing morphOS summary, receipt, and promotion artifacts

The goal is to make work history:

- durable
- inspectable
- branch-safe
- agent-readable
- human-auditable

without polluting the source tree with uncontrolled planning and run-state
files.

## Why This Spec Exists

Skyforce already believes in filesystem-first state.

That is visible in:

- run artifacts
- receipts
- evidence files
- summaries
- approvals

What is still under-specified is where durable work history should live when it
needs to outlast a single process but should not clutter the product codebase.

Without a work ledger:

- plans, progress notes, and decisions drift into ad hoc files
- different runs leave state in inconsistent places
- agents lose a durable shared history surface
- promotion and review reasoning become hard to audit
- repos accumulate “agent cruft” in the working tree

This spec exists to solve that.

## Executive Summary

The correct model is:

- source code stays in the normal repository history
- operational work history is persisted in a git-native ledger surface
- the ledger records plans, decisions, progress, approvals, evidence, and
  promotion posture
- the ledger is readable by both humans and agents
- the ledger should be separable from product commits

The preferred v0 shape is:

- file-backed ledger records
- git-managed history
- isolated from the main implementation branch
- correlated by `run_id`, `task_execution_id`, `issue_identifier`, and
  `workspace_id`

## What The Ledger Is For

The work ledger should capture:

- work intake
- planning
- action assignment
- progress checkpoints
- decisions
- validation posture
- approval posture
- promotion readiness
- final closeout state

It is not meant to replace:

- source code history
- binary artifact storage
- high-volume raw event streaming

## What The Ledger Is Not

The ledger is not:

- the main event bus
- the canonical source code branch
- a dumping ground for every transient log line
- a substitute for structured runtime contracts

It is a durable operational history surface.

## Core Design Rule

Every durable item in the ledger must answer:

- what run or issue it belongs to
- what happened
- when it happened
- who or what produced it
- what it points to next

If a file cannot answer those questions, it does not belong in the ledger.

## Why Git-Native

Git gives the ledger several useful properties immediately:

- appendable history
- diffability
- branch isolation
- offline-friendly durability
- auditability
- low-friction transport between nodes

This is especially aligned with morphOS because the platform already prefers:

- filesystem-backed state
- inspectability
- replayable evidence
- repo-local durability when possible

## Separation Rule

The ledger must remain separate from the product source tree’s normal change
history.

Preferred options, in descending order:

1. orphan ledger branch
2. dedicated git worktree bound to a ledger branch
3. clearly isolated ledger directory with strict ignore and projection rules

### v0 Recommendation

Use a dedicated ledger branch or worktree when possible.

Reason:

- source commits stay clean
- agent work history is still versioned
- operational state can evolve without rewriting product history

## Minimum Ledger Objects

The v0 ledger should persist these object families.

## 1. Intake Record

Purpose:

- record how a run began

Minimum fields:

- `run_id`
- `issue_identifier`
- `workflow_template_id`
- `execution_mode`
- `workspace_id`
- `created_at`
- `input_refs`

## 2. Plan Record

Purpose:

- record the accepted action plan for the run

Minimum fields:

- `run_id`
- `plan_id`
- `generated_by`
- `task_refs`
- `context_refs`
- `created_at`
- `supersedes_plan_id`

## 3. Assignment Record

Purpose:

- record which agent was assigned which action

Minimum fields:

- `assignment_id`
- `run_id`
- `task_execution_id`
- `agent_id`
- `action_type`
- `requested_at`
- `status`

## 4. Checkpoint Record

Purpose:

- capture durable progress milestones at the ledger level

Minimum fields:

- `ledger_checkpoint_id`
- `run_id`
- `task_execution_id`
- `status`
- `summary`
- `artifact_refs`
- `created_at`

### Note

This is not the same thing as Durable’s kernel-owned `ExecutionCheckpoint`.

Use this ledger checkpoint for human and operational traceability.
Use Durable checkpoints for resumability truth.

## 5. Decision Record

Purpose:

- persist meaningful human or machine decisions

Examples:

- replan accepted
- validation failed but retry approved
- promotion deferred
- workspace admin approved release

Minimum fields:

- `decision_id`
- `run_id`
- `decision_type`
- `decided_by`
- `decider_role`
- `summary`
- `supporting_artifact_refs`
- `created_at`

## 6. Validation Record

Purpose:

- persist validation posture and references

Minimum fields:

- `run_id`
- `validation_record_id`
- `overall_result`
- `artifact_refs`
- `created_at`

## 7. Promotion Record

Purpose:

- persist promotion readiness and final promotion outcome

Minimum fields:

- `promotion_record_id`
- `run_id`
- `promotion_readiness`
- `proposed_branch`
- `approval_decision_ref`
- `summary_refs`
- `evidence_ref`
- `created_at`

## File Layout

The v0 ledger layout should prefer stable, predictable paths.

Recommended shape:

```text
ledger/
  runs/
    <run_id>/
      intake.json
      plan.json
      assignments/
        <assignment_id>.json
      checkpoints/
        <ledger_checkpoint_id>.json
      decisions/
        <decision_id>.json
      validation/
        validation.json
      promotion/
        promotion.json
      summaries/
        status.txt
        summary_short.md
        summary_full.md
        evidence.json
      index.json
  issues/
    <issue_identifier>/
      latest_run.txt
      run_refs.json
  workspaces/
    <workspace_id>/
      active_runs.json
      recent_decisions.json
```

## Indexing Rule

Every run ledger directory should include an `index.json` file that lets an
agent or operator quickly discover:

- the current posture
- the latest checkpoint
- the latest decision
- the validation posture
- the promotion posture
- the key artifact refs

That prevents consumers from scanning every file blindly.

## Relationship To Existing Artifacts

The ledger should not rename already frozen summary and approval artifacts.

It should incorporate and point to them.

That means the following remain stable:

- `summaries/status.txt`
- `summaries/summary_short.md`
- `summaries/summary_full.md`
- `summaries/evidence.json`
- `approvals/approval_packet.json`

### Rule

The ledger may mirror or reference these files.
It must not redefine their names in v0.

## Write Rules

The ledger should use append-or-supersede behavior, not silent mutation.

Preferred rules:

- create new checkpoint records instead of rewriting prior checkpoints
- create new decision records instead of overwriting old reasoning
- allow `latest` pointers in index files
- allow supersession fields where a new plan replaces an old one

This preserves auditability without making lookup too expensive.

## Human And Agent Access Model

### Humans should be able to:

- inspect the latest plan
- understand why a run is blocked
- see validation posture
- see approval posture
- see promotion readiness

### Agents should be able to:

- reopen the current run state quickly
- reuse prior plans and decisions
- find the latest evidence and summary refs
- avoid duplicating already completed work

## Sync And Portability

Because the ledger is git-native, it should support:

- offline capture
- later sync
- cross-node portability
- branch-safe review of operational history

### v0 Constraint

Do not depend on immediate multi-writer conflict resolution.

Prefer:

- one active writer per run
- one orchestrator-authoritative ledger update path
- append-friendly files with narrow scope

## Relationship To Operational Context And Persistent Memory

The ledger belongs primarily to operational context, not full long-term memory.

It may later feed persistent memory extraction, but it is not itself the final
memory system.

That means:

- it should capture run truth
- it may seed lessons later
- it should not act like an unconstrained memory graph

## Ownership

### `morphOS` owns

- the ledger doctrine
- layout semantics
- object meanings

### `skyforce-core` owns

- shared ledger contracts
- CLI and helper access paths

### `skyforce-symphony` owns

- authoritative ledger updates tied to workflow progression

### `skyforce-harness` owns

- execution receipts and evidence that feed ledger records

### `skyforce-command-centre-live` observes

- ledger projections for operator visibility

### `skyforce-api-gateway` owns

- normalized operator-facing ledger projections for HTTP clients

## What To Build After This Spec

Once this model is accepted, the next useful follow-on specs are:

1. `FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md`
2. `TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md`
3. `SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md`

## Bottom Line

The correct morphOS work ledger is:

- filesystem-backed
- git-native
- separate from normal product history
- append-friendly
- keyed by stable run and task identities
- readable by both agents and humans

It should become the durable operational memory surface for software-factory
work, without turning the product branch into a notebook.
