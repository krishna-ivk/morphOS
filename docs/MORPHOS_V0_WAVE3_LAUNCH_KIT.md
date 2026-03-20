# morphOS v0 Wave 3 Launch Kit

Wave 3 closes the loop back into source repos.

Use this file only after Wave 1 runtime outputs and Wave 2 governance states are stable.

## Wave 3 Goal

Make validated workspace results promotable through a safe, reviewable, approval-aware path.

Wave 3 should produce:

- promotion readiness checks
- PR or proposal packet generation
- deterministic closeout for missing mandatory artifacts
- safe abort or rollback behavior

## Launch Order

### Step 1

Confirm Gate G3 from `MORPHOS_V0_MULTI_AGENT_STATUS_BOARD.md` is satisfied.

### Step 2

Launch Agent E.

### Step 3

If Agent E needs final operator presentation work for promotion, launch Agent D after Agent E stabilizes the promotion packet shape.

## Hard Gates

1. validation outputs from Agent C are stable
2. approval completion states from Agent B are stable
3. summary artifact names are stable
4. promotion packet contract is frozen

## Copy-Paste Prompt: Agent E

```text
You are Agent E for morphOS v0 Wave 3.

Mission:
Implement the promotion and deterministic closeout path using stable contracts, validation outputs, approval states, and summary artifacts. Focus on readiness checks, reviewable proposal or PR packets, and safe abort behavior.

Own only:
- skyforce-core promotion and closeout logic
- skyforce-symphony promotion orchestration

Required outputs:
- promotion readiness checks
- PR or proposal packet generation
- deterministic closeout behavior for mandatory artifacts
- safe abort or rollback path
- promotion_packet_examples.md

Inputs:
- Wave 1 contract freeze notes
- Wave 1 runner receipt examples
- Wave 2 governance state handoff
- morphOS/docs/morphos-software-factory-mvp.md
- morphOS/docs/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md

Forbidden surfaces:
- contract redesign
- runner redesign
- unrelated UI wording work

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

Use only if promotion needs final operator flow presentation.

```text
You are Agent D for morphOS v0 Wave 3.

Mission:
Implement operator-facing promotion views using the stable promotion packet and closeout states. Focus on readiness visibility, review packet readability, and promotion failure explanations.

Own only:
- sky-force-command-centre-live promotion surfaces
- user-facing skyforce-core CLI promotion views

Required outputs:
- promotion readiness view
- review packet visibility
- promotion failure and rollback explanations
- operator_promotion_notes.md

Inputs:
- Agent E promotion_packet_examples.md
- Wave 2 operator release notes
- morphOS/docs/UNIVERSAL_DELIVERY_TERMINOLOGY.md

Forbidden surfaces:
- runtime promotion semantics
- contract changes

Close with this handoff packet:
- scope_completed
- files_changed
- contracts_relied_on
- events_changed
- artifacts_emitted
- open_blockers
- next_owner
```

## Wave 3 Success Checklist

- promotion requires explicit readiness
- review packets include validation, approvals, and summaries
- deterministic closeout emits missing mandatory artifacts when possible
- invalid promotion attempts fail clearly and safely

## Stop Conditions

Pause Wave 3 if:

- promotion needs a new summary artifact not already frozen
- approval completion states are ambiguous
- validation outputs are insufficient for promotion readiness

If a stop condition happens, reopen the owning lower wave instead of patching around the gap.
