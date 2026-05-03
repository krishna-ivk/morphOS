# Playbook Outcome Recording Spec

## Purpose

This spec defines how the software factory captures the outcome of guided runs. It implements the discipline of "record the outcome exactly once per guided run" (inspired by ACE Platform) to turn execution history into reusable guidance and future learning.

## Core Principle

Every run that is guided by a **Playbook**, **Workflow Template**, or **Archetype Contract** should emit a structured **Playbook Outcome** record upon completion.

This record is NOT the same as:
- an execution receipt (which is low-level and command-focused)
- a validation report (which is objective and check-focused)
- an approval packet (which is decision-focused)

The **Playbook Outcome** is **guidance-focused**: it captures whether the provided instructions were effective and what was learned for future runs.

## Playbook Outcome Schema

A canonicalized `PlaybookOutcome` record (defined in `skyforce-core` contracts) should include:

- `outcome_id`: Unique record identifier.
- `run_id`: Reference to the `WorkflowRun`.
- `playbook_ref`: Reference to the primary `Playbook` or `WorkflowTemplate` that guided the run.
- `verdict`: `success` | `partial` | `failure` | `exception`.
- `confidence`: (Optional) How confident the agent/system is in the outcome classification.
- `summary`: A concise high-level summary of the result.
- `learnings`: Structured list of specific lessons (fixed patterns, anti-patterns, traps).
- `tradeoffs`: Mention of any specific tradeoffs made during the run.
- `playbook_effectiveness`: `accurate` | `vague` | `outdated` | `missing_steps`.
- `suggested_changes`: Specific recommendations for improving the guidance asset.
- `created_at`: ISODateTime.

## Recording Lifecycle

1. **Discovery**: Symphony selects and attaches a `PlaybookRef` to the `WorkflowRun` at intake.
2. **Execution**: Harness executes the work, guided by the playbook artifacts.
3. **Capture**: Upon run completion (success or failure), Symphony triggers the `outcome_capture` step.
4. **Synthesis**: The `operator_liaison` or `releaser` archetype synthesizes the outcome record from logs, receipts, and validation results.
5. **Persistence**: The record is stored in the `PlaybookOutcome` registry (likely part of the future learning subsystem).

## Feedback Loop (P2+)

In later milestones, these outcome records will be used for:

- **Exemplar Selection**: Future runs with similar goals will retrieve `PlaybookOutcome` records where `verdict == success` as positive exemplars.
- **Warning Injection**: Runs will retrieve `PlaybookOutcome` records where `verdict == failure` to inject warnings about known "traps" or "anti-patterns".
- **Guidance Evolution**: A gated process will use `suggested_changes` to automatically or semi-automatically update the source `Playbook` or `WorkflowTemplate`.

## Implementation Seams

- **`skyforce-core`**: Define `PlaybookOutcome` and `PlaybookRef` interfaces.
- **`skyforce-symphony`**: Add `attached_playbook_ref` to `WorkflowRun` and implement the completion-to-capture trigger.
- **`skyforce-harness`**: Ensure execution metadata includes enough context to satisfy the `PlaybookOutcome` synthesis.
- **`morphOS`**: Maintain the registry of canonical playbooks and post-run learning doctrine.
