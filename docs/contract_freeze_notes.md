# morphOS v0 Contract Freeze Notes

This is the Agent A freeze artifact for Wave 1.

It freezes the minimum shared shapes needed by downstream runtime, CLI, dashboard, and promotion work.
These notes are intentionally narrower than the full architecture docs.

## Freeze Scope

This freeze covers five shared areas:

- execution mode
- human authority and approval routing
- event taxonomy
- summary and approval artifacts
- promotion packet minimum shape

## Freeze Decision 1: Execution Mode

### Frozen values

- `interactive`
- `factory`

### Runtime meaning

- `interactive`
  - intent may still evolve during the run
  - follow-up human input may change the next step without treating the run as complete plan execution
  - the runtime should expect more pauses, clarification, and operator shaping
- `factory`
  - the intent is considered sufficiently specified
  - the runtime may continue through deterministic steps until a policy, validation, or approval gate stops it

### Contract placement

Freeze these additions in shared contracts:

- add `ExecutionMode = "interactive" | "factory"`
- add `execution_mode: ExecutionMode` to `WorkflowRun`
- add `execution_mode_source: "declared" | "inferred"` to `WorkflowRun`
- add `execution_mode_locked?: boolean` to `WorkflowRun`

### Implementation rule

- Agent B owns behavior differences after this field exists
- Agent D may surface the field but must not invent new mode names

## Freeze Decision 2: Human Authority And Approval Routing

### Frozen role values

- `workspace_admin`
- `super_admin`

### Frozen scope values

- `workspace`
- `global`

### Contract placement

Freeze these additions in shared contracts:

- add `HumanAuthorityRole = "workspace_admin" | "super_admin"`
- add `AuthorityScope = "workspace" | "global"`
- add `workspace_id: string` to `WorkflowRun`
- add `workspace_admin_id?: string` to `WorkflowRun`
- add `authority_scope?: AuthorityScope` to `Directive`
- add `required_approver_role?: HumanAuthorityRole` to `Directive`
- add `approval_target_id?: string` to `Directive`
- add `decider_role?: HumanAuthorityRole` to `ApprovalDecision`
- add `authority_scope?: AuthorityScope` to `ApprovalDecision`

### Routing rule freeze

- workspace-scoped risky actions default to `workspace_admin`
- cross-workspace, global-policy, or exception-path actions escalate to `super_admin`
- approval artifacts must record both actor id and actor role

### Non-goals in this freeze

- no deep org chart
- no delegated admin tree
- no temporary override windows yet

## Freeze Decision 3: Event Taxonomy

### Frozen event families

- `run.*`
- `task.*`
- `approval.*`
- `validation.*`
- `summary.*`
- `promotion.*`
- `policy.*`
- `checkpoint.*`

### Frozen minimum event names

- `run.created`
- `run.mode_declared`
- `run.blocked`
- `run.completed`
- `task.started`
- `task.completed`
- `task.failed`
- `approval.requested`
- `approval.approved`
- `approval.rejected`
- `validation.completed`
- `summary.published`
- `promotion.ready`
- `promotion.requested`
- `promotion.completed`
- `policy.blocked`
- `checkpoint.created`
- `checkpoint.restored`
- `checkpoint.invalidated`

### Contract placement

The existing `EventEnvelope` in `skyforce-core/packages/contracts/src/index.ts:119` remains the outer envelope.

Freeze these additions and conventions:

- keep `event_type` as the canonical event name field
- treat the name list above as the only approved shared names for the first implementation wave
- require `run_id` for every runtime event after run creation
- require `issue_identifier` on run-, approval-, validation-, summary-, and promotion-family events when a source issue exists
- require the payload to include the relevant stable ids rather than free-text-only summaries

### Mapping rule

- repo-local names may exist temporarily during migration
- any surface that exports cross-repo state must map to the frozen names above

## Freeze Decision 4: Summary And Approval Artifacts

### Frozen required run artifacts

- `summaries/status.txt`
- `summaries/summary_short.md`
- `summaries/summary_full.md`
- `summaries/evidence.json`
- `approvals/approval_packet.json`

### Artifact meaning

- `status.txt`
  - one-line run posture for humans and machines
- `summary_short.md`
  - short human-readable recap
- `summary_full.md`
  - detailed narrative with context and outcomes
- `evidence.json`
  - machine-readable references to validation, receipts, and artifacts
- `approval_packet.json`
  - structured approval context, risk, actor, and decision surface

### Contract freeze

Freeze the following required keys for generated summaries:

- `status.txt`
  - run id
  - current posture
  - current or terminal step
- `evidence.json`
  - `run_id`
  - `issue_identifier`
  - `validation_artifact_refs`
  - `receipt_artifact_refs`
  - `summary_generated_at`
- `approval_packet.json`
  - `run_id`
  - `issue_identifier`
  - `authority_scope`
  - `required_approver_role`
  - `risk_level`
  - `supporting_artifact_refs`

### Deterministic closeout rule

- if an agent omits `summary_short.md` or `evidence.json`, deterministic closeout may emit them later
- no downstream repo may rename these artifact files in v0

## Freeze Decision 5: Promotion Packet Minimum Shape

### Frozen readiness inputs

- stable validation outputs exist
- approval state is terminal and acceptable
- summary artifacts exist
- source workspace and target repo are known

### Frozen promotion packet fields

- `run_id`
- `issue_identifier`
- `workspace_id`
- `source_repo`
- `target_repo`
- `proposed_branch`
- `summary_short_ref`
- `summary_full_ref`
- `evidence_ref`
- `validation_artifact_refs`
- `approval_decision_ref`
- `promotion_readiness`
- `created_at`

### Frozen readiness values

- `not_ready`
- `ready_for_review`
- `ready_for_promotion`

### Implementation rule

- Agent E owns promotion behavior after this packet exists
- Agent D may render promotion readiness but may not redefine readiness states

## Current Contract Surface Vs Frozen Target

The current contracts already provide useful foundations in `skyforce-core/packages/contracts/src/index.ts`:

- `WorkflowRun` already has `run_id`, `status`, and `connectivity_mode`
- `Directive` already has `kind`, `summary`, and `payload`
- `ApprovalDecision` already has `decided_by` and terminal decision state
- `EventEnvelope` already provides the cross-repo envelope
- `ArtifactRef` already supports file-backed artifact linkage

The main freeze delta is:

- add explicit execution-mode fields
- add explicit workspace and approver-role fields
- freeze canonical event names
- freeze required artifact names and minimum keys
- freeze the promotion packet shape and readiness states

## Downstream Consumption Rules

- Agent B consumes execution-mode, authority, checkpoint, and event-name freezes
- Agent C consumes event-name, artifact-name, and evidence-shape freezes
- Agent D consumes delivery terminology, summary names, and authority-role freezes
- Agent E consumes summary, approval, validation, and promotion packet freezes

## Migration Notes

- existing repo-local event names should map into the frozen taxonomy before cross-repo publication
- existing summary surfaces may keep local rendering details, but artifact filenames must remain frozen
- any runtime need for extra fields should be raised as a narrow delta, not a rewrite of the freeze

## Handoff Packet

- `scope_completed`
  - froze shared names and minimum fields for Wave 1
- `files_changed`
  - `morphOS/docs/contract_freeze_notes.md`
  - `morphOS/docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_STATUS_BOARD.md`
  - `morphOS/docs/README.md`
- `contracts_relied_on`
  - `skyforce-core/packages/contracts/src/index.ts`
  - `morphOS/docs/milestones/v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md`
  - `morphOS/docs/morphos-software-factory-mvp.md`
  - `morphOS/docs/human_cell_spec.md`
  - `morphOS/docs/policy_engine_spec.md`
  - `morphOS/docs/event_bus_spec.md`
- `events_changed`
  - no code events changed yet; canonical event names frozen for downstream implementation
- `artifacts_emitted`
  - `morphOS/docs/contract_freeze_notes.md`
- `open_blockers`
  - shared contract code in `skyforce-core` still needs to be updated to match this freeze
- `next_owner`
  - Agent B for orchestration backbone
