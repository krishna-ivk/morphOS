# Universal Delivery Terminology

## Purpose

This document defines a universal, adoption-friendly vocabulary for `morphOS` and the Skyforce group of repos.

The goal is to make the system understandable to software teams on first read while preserving enough precision for operators, agents, and runtime contracts.

This terminology is intended for:

- dashboard labels
- workflow specs
- docs and guides
- run artifacts
- operator actions
- future API naming guidance

This terminology is not intended to force immediate backend renames. The preferred rollout is:

1. UI language first
2. docs and onboarding language second
3. contracts and API aliases later, only when needed

## Design Goals

The vocabulary should be:

- universal across product, engineering, QA, and operations
- understandable in an Agile or software-delivery context
- neutral across Jira-style, GitHub-style, and internal workflow tools
- compatible with agent orchestration without sounding overly internal
- stable enough to survive repo and architecture changes

## Naming Principles

### 1. Prefer delivery language over system-internal language

Use terms that describe work in progress, review, validation, release, and status.

Prefer:

- `ticket`
- `work item`
- `active work`
- `review queue`
- `quality checks`
- `delivery status`

Avoid exposing internal-only terms as primary UI language:

- `directive`
- `summary sync`
- `execution target`
- `operator readiness`
- `publish posture`

### 2. Prefer terms that map to existing software team mental models

The first read should feel familiar to someone used to Agile, Kanban, Jira, GitHub Issues, release ops, or engineering management.

### 3. Prefer one canonical user-facing word per concept

Examples:

- use `ticket` as the default user-facing term
- do not mix `issue`, `ticket`, `task`, and `job` for the same concept on the same screen

### 4. Separate user-facing language from internal model names

Internal structures may continue using terms like `workflow`, `directive`, or `validation artifact`, but the UI should translate them into simpler delivery language where possible.

### 5. Prefer durable nouns over implementation-specific nouns

Use terms tied to the work lifecycle rather than the current implementation.

Prefer:

- `published update`
- `quality check`
- `active run`

Over:

- `summary sync`
- `validation summary`
- `durable execution`

## Canonical Vocabulary

### Primary work object

- Canonical term: `Ticket`
- Acceptable secondary term: `Work Item`
- Internal legacy terms: `Issue`

Why:

- `ticket` is broadly understood in Agile and operational workflows
- it fits software delivery better than `job`
- it is more concrete for operators than `issue`

### Work in progress

- Canonical term: `Active Work`
- Acceptable secondary terms: `In Progress`, `Work In Flight`
- Internal legacy terms: `Execution Targets`

Why:

- emphasizes active delivery
- easier to scan than `execution targets`

### Human decision queue

- Canonical term: `Review Queue`
- Acceptable secondary terms: `Approval Queue`, `Needs Review`
- Internal legacy terms: `Pending Approvals`

Why:

- `review` is familiar to engineering teams
- still covers explicit approvals
- feels less bureaucratic than approval-only phrasing

### Validation surface

- Canonical term: `Quality Checks`
- Acceptable secondary terms: `Checks`, `Validation Results`, `Test Results`
- Internal legacy terms: `Validation Summaries`

Why:

- `quality checks` is broad enough to include tests, lint, policy, and review evidence
- avoids exposing artifact-specific naming

### Published operator output

- Canonical term: `Published Updates`
- Acceptable secondary terms: `Release Updates`, `Posted Updates`
- Internal legacy terms: `Summary Sync`

Why:

- describes the operator-visible outcome instead of the synchronization mechanism
- works whether the system posts a summary, report, or release note

### Status of delivery

- Canonical term: `Delivery Status`
- Acceptable secondary terms: `Status`, `Release Status`
- Internal legacy terms: `Readiness`

Why:

- teams understand `status` quickly
- `delivery status` keeps the focus on shipping work

### Approval object

- Canonical term: `Review Request`
- Acceptable secondary terms: `Approval Request`
- Internal legacy terms: `Directive`

Why:

- `directive` is too system-internal for most users
- `review request` is immediately understandable

### Long-running execution

- Canonical term: `Active Run`
- Acceptable secondary terms: `Run State`, `Run Session`
- Internal legacy terms: `Durable Execution`

Why:

- `durable` is meaningful to engineers but unclear to operators
- `active run` communicates the state directly

### Intermediate state marker

- Canonical term: `Progress Checkpoint`
- Acceptable secondary terms: `Run Checkpoint`
- Internal legacy terms: `Execution Checkpoint`

Why:

- clearer connection to delivery progress

### Agent capacity surface

- Canonical term: `Agent Capacity`
- Acceptable secondary terms: `Team Capacity`, `Agent Fleet`
- Internal legacy terms: `Fleet Health`

Why:

- makes it clear that this panel is about available execution capacity
- `fleet health` sounds infrastructure-heavy on first read

## Recommended UI Mappings

### Dashboard panels

| Current term | Recommended term | Notes |
| --- | --- | --- |
| Fleet Health | Agent Capacity | Best default for software-factory usage |
| Execution Targets | Active Work | Best first-read improvement |
| Pending Approvals | Review Queue | Keeps approval semantics but reads more naturally |
| Validation Summaries | Quality Checks | Broad and easy to understand |
| Summary Sync | Published Updates | Outcome-focused naming |
| Issue Inspector | Ticket Detail | Clear and familiar |
| Focused Issue | Selected Ticket | More direct |

### Detail labels

| Current term | Recommended term | Notes |
| --- | --- | --- |
| Issue | Ticket | Canonical work object |
| Directive | Review Request | User-facing phrasing |
| Readiness | Delivery Status | Can be shortened to `Status` in dense layouts |
| Published Readiness | Published Status | Keeps comparison readable |
| Current Readiness | Current Status | Better side-by-side comparison |
| Summary Sync | Update Status | For smaller cards |
| Durable Execution | Active Run | Better operator comprehension |
| Execution Checkpoint | Progress Checkpoint | Better workflow meaning |
| Publish State | Update State | Keeps action family consistent |

### Action labels

| Current term | Recommended term | Notes |
| --- | --- | --- |
| Inspect | Open Ticket | More explicit |
| Dry Run Summary | Preview Update | Better operator phrasing |
| Publish Summary | Post Update | Short and understandable |
| Dry Run Validation | Preview Check Results | More explicit but longer |
| Publish Validation | Post Check Results | Best direct translation |
| Copy Publish Hint | Copy Update Command | For operator-heavy views |
| Approve | Approve | Keep as-is |
| Reject | Reject | Keep as-is |
| Refresh Durable | Refresh Run | Reduce internal jargon |
| Resume Durable | Resume Run | Reduce internal jargon |
| Cancel Durable | Cancel Run | Reduce internal jargon |

## Universal Term Families

To keep the system coherent, preferred words should cluster by family.

### Work family

- ticket
- active work
- selected ticket
- ticket detail

### Review family

- review queue
- review request
- approve
- reject

### Quality family

- quality checks
- check results
- blocked
- passed

### Release family

- published updates
- preview update
- post update
- update state

### Run family

- active run
- progress checkpoint
- refresh run
- resume run
- cancel run

## Terms To Avoid As Primary UI Language

These can still exist in implementation or docs, but should not be the first words a new operator sees.

- directive
- execution target
- summary sync
- publish posture
- operator readiness
- durable execution
- artifact refs

## When To Use Alternative Terms

### Use `Work Item` instead of `Ticket` when:

- the audience is broader than engineering
- the object may represent non-bug, non-feature work
- the product wants a more neutral business-facing term

### Use `Agent Fleet` instead of `Agent Capacity` when:

- the panel is mostly infrastructure and worker-node state
- the user is expected to think about machines first, work second

### Use `Approval Queue` instead of `Review Queue` when:

- the panel is only about formal approvals
- there is a strong governance requirement

### Use `Release Updates` instead of `Published Updates` when:

- the output is tightly tied to release operations
- the primary audience is release management

## Adoption Guidance

### Phase 1: UI translation layer

Apply the canonical terms to:

- dashboard panel titles
- button labels
- empty states
- help text
- detail labels

Do not change:

- API field names
- internal module names
- persisted artifact schemas

### Phase 2: docs and onboarding alignment

Update:

- README guides
- screenshots
- user guides
- operator runbooks

Use the canonical term first, with the legacy term in parentheses when needed.

Example:

`Review Queue (formerly Pending Approvals)`

### Phase 3: contract aliases

Only if helpful, add translation or aliasing at the contract layer.

Examples:

- display `ticket` while preserving internal `issue_identifier`
- display `review_request_id` while preserving internal `directive_id`

## Compatibility With morphOS

This terminology is compatible with `morphOS` because it:

- preserves the operating-model/runtime split
- makes workflows easier to understand
- supports a software-factory-first MVP
- avoids coupling user understanding to one runtime implementation

## Compatibility With Skyforce

This terminology is compatible with Skyforce because it:

- keeps existing backend concepts intact
- mainly requires a UI translation layer first
- fits orchestration, approval, validation, and publishing surfaces
- improves operator clarity without forcing a rewrite

## Recommended Default Set For Immediate Adoption

If we want a single universal set to start with, use:

- `Ticket`
- `Active Work`
- `Review Queue`
- `Quality Checks`
- `Published Updates`
- `Delivery Status`
- `Review Request`
- `Active Run`
- `Progress Checkpoint`
- `Agent Capacity`

## Example First-Pass Dashboard Rewrite

Suggested panel set:

- `Agent Capacity`
- `Active Work`
- `Review Queue`
- `Quality Checks`
- `Published Updates`
- `Ticket Detail`

Suggested action set:

- `Open Ticket`
- `Preview Update`
- `Post Update`
- `Preview Check Results`
- `Post Check Results`
- `Approve`
- `Reject`

## Decision

For universal adoption across `morphOS` and Skyforce, the default naming style should be:

- Agile-friendly
- software-delivery-oriented
- operator-readable
- implementation-neutral

The preferred canonical work noun is `Ticket`.
The preferred canonical status noun is `Delivery Status`.
The preferred canonical release noun is `Published Update`.
