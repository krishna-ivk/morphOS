# morphOS v0 Wave 2 Launch Kit

Wave 2 begins only after Wave 1 has produced stable contracts, runtime states, receipts, and artifacts.

Use [MORPHOS_V0_WAVE1_LAUNCH_KIT.md](MORPHOS_V0_WAVE1_LAUNCH_KIT.md) for the first batch.
Use this file when the runtime backbone is ready and governance plus full operator rollout should begin.

## Wave 2 Goal

Make the runtime governable and operator-usable.

Wave 2 should produce:

- policy hooks at workflow boundaries
- execution-mode-aware orchestration behavior
- workspace-admin routing
- super-admin escalation path
- full operator views for durable state, approvals, and summary pyramid

## Launch Order

### Step 1

Review the Wave 1 outputs and confirm Gate G2 from `MORPHOS_V0_MULTI_AGENT_STATUS_BOARD.md` is satisfied.

### Step 2

Launch these in parallel:

- Agent B for governance hooks
- Agent D for full operator surface rollout

### Step 3

Launch Agent A only if Wave 1 exposed narrow contract gaps.

Agent A in Wave 2 is a repair owner, not the default first mover.

### Step 4

Do not finalize Wave 3 promotion work yet.

Promotion needs stable governance outputs from this wave.

## Hard Gates

1. Wave 1 receipts and artifacts are stable
2. approval states are stable
3. checkpoint persistence is stable
4. Agent D only uses names frozen by Agent A and states frozen by Agent B

## Copy-Paste Prompt: Agent B

```text
You are Agent B for morphOS v0 Wave 2.

Mission:
Implement governance behavior in Symphony using the frozen contracts and stable runtime backbone. Focus on policy hook call sites, execution-mode-aware behavior, workspace-admin routing, and super-admin escalation states.

Own only:
- skyforce-symphony orchestration and tests

Required outputs:
- policy checks at workflow boundaries
- execution-mode-aware orchestration behavior
- workspace-admin approval routing states
- super-admin escalation states
- governance_state_handoff.md

Inputs:
- Wave 1 contract freeze notes
- Wave 1 orchestration state handoff
- morphOS/docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md
- morphOS/docs/milestones/v0/MORPHOS_V0_AGENT_DISPATCH_PACKETS.md

Forbidden surfaces:
- harness runner internals
- final UI copy decisions
- contract changes unless escalated back to Agent A

Close with this handoff packet:
- scope_completed
- files_changed
- contracts_relied_on
- events_changed
- artifacts_emitted
- open_blockers
- next_owner
```

## Copy-Paste Prompt: Agent D

```text
You are Agent D for morphOS v0 Wave 2.

Mission:
Implement the full operator-surface rollout using the frozen terminology and stable runtime states. Focus on summary pyramid views, durable and blocked state visibility, and authority-aware approval surfaces.

Own only:
- sky-force-command-centre-live
- user-facing skyforce-core CLI surfaces

Required outputs:
- summary pyramid rendering
- delivery-first terminology rollout
- durable and blocked state views
- workspace-admin and super-admin distinctions
- operator_release_notes.md

Inputs:
- Wave 1 contract freeze notes
- Wave 1 operator wording map
- Wave 2 governance state handoff from Agent B
- morphOS/docs/UNIVERSAL_DELIVERY_TERMINOLOGY.md

Forbidden surfaces:
- runtime logic
- contract semantics

Close with this handoff packet:
- scope_completed
- files_changed
- contracts_relied_on
- events_changed
- artifacts_emitted
- open_blockers
- next_owner
```

## Copy-Paste Prompt: Agent A

Use only if a governance or UI blocker exposes a contract gap.

```text
You are Agent A for morphOS v0 Wave 2.

Mission:
Resolve only the narrow contract gaps discovered during governance and operator rollout. Keep changes minimal and preserve the Wave 1 freeze wherever possible.

Own only:
- morphOS docs
- skyforce-core contracts

Required outputs:
- contract_delta_notes.md

Inputs:
- Wave 1 contract freeze notes
- Wave 2 blocker report from Agent B or Agent D
- morphOS/docs/milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md

Forbidden surfaces:
- runtime logic
- dashboard implementation
- runner implementation

Close with this handoff packet:
- scope_completed
- files_changed
- contracts_relied_on
- events_changed
- artifacts_emitted
- open_blockers
- next_owner
```

## Wave 2 Success Checklist

- policy hooks fire at workflow boundaries
- execution mode changes behavior in a visible way
- approval routing distinguishes workspace-admin and super-admin paths
- CLI and dashboard use stable delivery terminology
- durable and blocked work are obvious to operators

## Stop Conditions

Pause Wave 2 if:

- Agent D needs a new runtime state name
- Agent B needs to reshape receipts or runner outputs
- authority routing requires a new contract field not covered by Wave 1

If a stop condition happens, hand ownership back to Agent A for a narrow contract delta.
