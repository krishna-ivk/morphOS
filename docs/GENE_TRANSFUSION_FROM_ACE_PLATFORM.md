# Gene Transfusion From ACE Platform

## Source

- Upstream repo: <https://github.com/DannyMac180/ace-platform>
- Primary references reviewed:
  - `README.md`
  - `AGENTS.md`
  - `docs/`

## Why This Repo Matters

`ace-platform` is not a strong template for the full Skyforce runtime.
It is a strong template for one narrower but important concern:

- how instructions become reusable playbooks
- how agents discover those playbooks before acting
- how outcomes from real runs are fed back into better future guidance

This makes `ace-platform` a good gene-transfusion candidate for **playbook learning** and **MCP-facing agent ergonomics**, not for the full software-factory control plane.

## High-Level Fit

### Strong Fit

- playbooks as living operational assets
- outcome recording after real work
- MCP-friendly tool and client posture
- using execution history to improve future guidance

### Partial Fit

- hosted versus OSS product boundary
- shared team collaboration around evolving instructions

### Weak Fit

- using ACE itself as the main runtime architecture for Skyforce
- replacing hard factory gates with playbook evolution
- treating playbook logic as a substitute for approvals, promotion, and policy hooks

## What To Adopt

### 1. Playbook Discovery Before Execution

Skyforce should adopt the ACE idea that each new task should first search for a relevant reusable playbook or workflow guide before acting.

What to borrow:

- summarize the task in a compact form
- search for the best matching playbook
- load one primary playbook before execution
- allow supporting playbooks as secondary context only

Why it matters:

- reduces prompt drift
- keeps successful tactics reusable
- gives future runs a better first pass

Where it should land:

- `morphOS`: doctrine for playbook discovery and attachment
- `skyforce-core`: shared playbook reference contracts
- `skyforce-symphony`: run-time playbook selection/attachment

### 2. Record Outcome Exactly Once Per Guided Run

ACE has a practical discipline in `AGENTS.md`: record the outcome once after the task completes.

Skyforce should adopt a similar loop for any run that was meaningfully guided by a workflow template, playbook, or archetype contract.

What to borrow:

- one primary guidance source per run
- one final outcome record per run or per major slice
- notes on what worked, failed, and why
- concise reasoning and tradeoff summary

Why it matters:

- gives gene transfusion and workflow improvement better raw material
- avoids losing lessons in chat history
- provides a clean bridge into future self-improvement loops

Where it should land:

- `morphOS`: doctrine for post-run learning packets
- `skyforce-harness`: artifact emission
- `skyforce-core`: shared outcome schema
- `skyforce-symphony`: orchestration timing for when outcome capture happens

### 3. MCP-Portable Guidance Layer

ACE is intentionally tool-agnostic and MCP-friendly.
Skyforce should preserve this idea.

What to borrow:

- playbooks should not be bound to one assistant surface only
- guidance assets should be attachable to Codex, Claude Code, and other MCP-capable clients
- tool integration should stay contract-driven rather than prompt-only

Why it matters:

- keeps Skyforce adaptable across interfaces
- prevents overfitting the instruction model to one client
- makes future tool registry work more durable

Where it should land:

- `morphOS`: doctrine
- `skyforce-core`: contracts and registries
- `skyforce-command-centre`: operator projection where relevant

### 4. Execution History As Improvement Fuel

ACE’s core promise is that real work should make future work better.
Skyforce should adopt that at the workflow/playbook level.

What to borrow:

- successful runs become exemplars
- failed runs become anti-patterns or warning material
- instruction assets evolve from real evidence, not only theory

Why it matters:

- aligns directly with your gene transfusion direction
- makes the factory smarter without weakening runtime control
- turns receipts and postmortems into reusable capability

Where it should land:

- `morphOS`: gene transfusion doctrine
- `skyforce-core`: exemplar/outcome contracts
- future learning subsystem

## What To Reject

### 1. ACE As The Main Skyforce Runtime Model

Skyforce should not adopt ACE’s overall platform shape as the main architecture.

Reason:

- ACE is centered on self-improving playbooks
- Skyforce is centered on governed delivery execution
- Skyforce still needs hard orchestration, approvals, safe promotion, and runtime contracts that are stricter than ACE’s main public story

### 2. Playbook Learning As A Replacement For Runtime Gates

Skyforce should not let playbooks replace:

- policy hooks
- validation gates
- approval packets
- promotion controls
- operator authority

Playbooks should improve execution quality, not erase governance.

### 3. Product-Split Complexity Right Now

ACE’s hosted/personal/team/enterprise split is interesting, but Skyforce should not spend near-term effort mirroring that structure.

Reason:

- P0 and early P1 still need a stronger delivery spine
- product packaging is less urgent than reliable execution

## What To Defer

### 1. Rich Team Collaboration Around Shared Playbooks

Useful later, but not needed before the factory spine is stable.

### 2. Hosted-Service Parity

Interesting for future managed Skyforce offerings, but not a current build priority.

### 3. Automatic Playbook Evolution

Skyforce should first capture outcomes and attach exemplars.
Automatic mutation of doctrine or playbooks should come later, with explicit review.

## Recommended MorphOS Follow-On Specs

This repo suggests a short follow-on spec cluster:

1. `PLAYBOOK_DISCOVERY_AND_ATTACHMENT_SPEC.md`
2. `PLAYBOOK_OUTCOME_RECORDING_SPEC.md`
3. `PLAYBOOK_EVOLUTION_GOVERNANCE_SPEC.md`

These should stay clearly subordinate to the existing:

- `WORKFLOW_PACK_AND_REGISTRY_SPEC.md`
- `GENE_TRANSFUSION_EQUIVALENCE_SPEC.md`
- `P0_FACTORY_SPINE_RECOVERY_PLAN.md`

## Repo Landing Map

### `morphOS`

Own:

- playbook doctrine
- playbook attachment rules
- playbook evolution governance
- relationship between workflow packs and playbooks

### `skyforce-core`

Own:

- shared playbook reference contracts
- outcome record schemas
- exemplar and anti-pattern metadata

### `skyforce-symphony`

Own:

- selecting and attaching the playbook for a run
- ensuring one primary playbook is associated to the run
- triggering post-run outcome capture

### `skyforce-harness`

Own:

- emitting the execution evidence and local artifacts that feed the outcome record

### `skyforce-command-centre`

Own:

- projecting playbook guidance and outcome summaries to operators where useful
- not becoming the source of truth for the playbook logic itself

## Recommended Priority

This should be treated as a **P1/P2 learning-layer input**, not a `P0` factory-spine blocker.

Use it after:

- the end-to-end delivery spine is reliable
- promotion and approval posture are clearer
- event and receipt contracts are stable enough to generate useful outcome records

## Bottom Line

`ace-platform` is a strong reference for how Skyforce can learn from real work through reusable playbooks and outcome capture.

It is not the right repo to copy as the main system architecture.

The right gene transfusion is:

- borrow ACE for playbook learning
- keep Skyforce for governed execution
