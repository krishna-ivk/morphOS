# Ladder Agent Room Review Checklist

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the authoritative cross-repo build order.

## Purpose

Use this checklist when reviewing the Ladder integration proposal or the first
implementation slices for `morphOS-agent-room`.

## Architecture Review

- Is Ladder clearly positioned as a room-level discovery layer rather than a second orchestrator?
- Is canonical Ladder state stored in workspace-scoped durable structures?
- Is artifact rendering treated as projection rather than the only source of truth?
- Is the split between Ladder state, task state, and export state explicit?
- Is `murmur_demo` a reasonable `v1` home for the domain?

## Domain Review

- Are the first object types limited to sources, ideas, and hypotheses?
- Are object relationships explicit rather than inferred from transcript text?
- Are status transitions narrow and enforceable?
- Does hypothesis readiness require success and failure metrics?
- Are later object types like experiments, results, and algorithms deferred until the core model stabilizes?

## UI Review

- Does the UI expose a single coherent Ladder view instead of scattering stages?
- Can users inspect objects without reading the whole transcript?
- Are LiveView events thin and context-driven?
- Does the UI avoid owning state transitions directly?
- Does the design fit the current artifact/data panel model?

## Task Bridge Review

- Are experiments planned to reuse the existing shared task board?
- Is experiment-to-task linkage explicit?
- Is there a clear rule for when a hypothesis becomes executable work?
- Is task linkage deferred out of the first PR slice?

## Export Review

- Is export integration additive rather than disruptive?
- Are only validated or approved Ladder outputs eligible for factory handoff?
- Are speculative ideas kept out of `work_order.json` by default?
- Does the export path remain backward-compatible when no Ladder data exists?

## Testing Review

- Are there domain tests for transition rules?
- Are there LiveView tests for rendering and refresh behavior?
- Are export tests planned before Ladder export files are introduced?
- Does the rollout preserve current room behavior when Ladder is absent?

## Rollout Review

- Is the first PR slice small enough to review comfortably?
- Are experiments/results/algorithms deferred to later slices?
- Is there a clear milestone order?
- Are the main risks called out and mitigated?
- Is there a definition of done for `v1`?

## Approval Prompt

The design is ready to move into implementation when reviewers can answer
`yes` to all of the following:

- The ownership boundaries are clear.
- The first PR scope is small and valuable.
- The persistence choice is appropriate.
- The UI approach matches the current room architecture.
- The rollout plan is realistic.
