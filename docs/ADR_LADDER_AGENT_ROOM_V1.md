# ADR: Ladder In morphOS Agent Room (`v1`)

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the authoritative cross-repo build order.

## Status

Proposed

## Context

`morphOS-agent-room` already provides:

- multi-agent workspace collaboration
- shared task coordination
- artifact rendering
- room decision capture
- factory export handoff

What it does not yet provide strongly enough is a first-class model for the
discovery and validation chain that happens before factory execution.

Today, much of that chain risks being spread across:

- chat transcript shape
- ad hoc artifacts
- human memory
- informal task naming

That makes it harder to preserve:

- why an idea exists
- what hypothesis it led to
- what experiment tested it
- what result was observed
- which methods are now reusable

Daniel Miessler's `Ladder` offers a useful conceptual sequence:

- sources
- ideas
- hypotheses
- experiments
- results
- algorithms

The question is how to integrate that sequence into the current room and
software-factory model without creating a second orchestration system.

## Decision

For `v1`, integrate `Ladder` into `morphOS-agent-room` as a workspace-scoped
domain inside `murmur_demo`.

Specifically:

- persist canonical Ladder state in relational tables
- render Ladder through a derived UI projection in the room
- keep experiments linked to the existing shared task board
- keep export integration additive through `Murmur.FactoryExports`
- do not introduce Ladder as a second runtime orchestrator

## Consequences

### Positive

- discovery state becomes durable, queryable, and exportable
- the room gains a clearer path from ambiguity to validated output
- humans and agents can inspect the learning chain without transcript parsing
- the factory can consume more structured upstream artifacts
- the existing room/task/export architecture stays intact

### Negative

- the room domain becomes broader
- more relational schemas and transitions must be maintained
- the UI gains another structured panel to support
- export selection logic becomes more nuanced once Ladder results exist

### Neutral / Follow-On

- if the Ladder domain proves broadly reusable, it may later be extracted from
  `murmur_demo` into its own umbrella app
- connector parity in Python may be added later if the Python export path
  remains operationally important

## Alternatives Considered

### 1. Keep Ladder out of the room entirely

Rejected because:

- the room is the natural place where discovery and convergence already happen
- the factory should not absorb speculative or ambiguous ideation directly

### 2. Store Ladder state only as artifacts

Rejected because:

- artifacts are better as projections than as the only canonical truth for
  shared room state
- shared querying, linking, and transition validation become weaker

### 3. Store Ladder state only in transcripts

Rejected because:

- transcript-first state is too brittle, implicit, and hard to export cleanly

### 4. Build Ladder as a new umbrella app immediately

Rejected because:

- reuse has not yet been proven strongly enough to justify early extraction
- `murmur_demo` is the existing product/domain home for room behavior

### 5. Let Ladder become a second orchestrator

Rejected because:

- it would duplicate room/runtime responsibilities and create unclear ownership

## `v1` Scope Boundary

Included first:

- sources
- ideas
- hypotheses
- relational persistence
- Ladder projection in the room UI

Deferred to later slices:

- experiments
- results
- algorithms
- export file extensions
- cross-workspace reuse

## Validation

This decision will be considered validated for `v1` if:

- Ladder objects persist across refresh and restart
- the room UI renders them from a backend projection
- hypotheses enforce readiness rules
- the first slice fits cleanly inside `murmur_demo`
- no second orchestration surface is introduced

## Related Documents

- [LADDER_AGENT_ROOM_INTEGRATION.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_INTEGRATION.md)
- [LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md)
- [LADDER_AGENT_ROOM_ROLLOUT_BACKLOG.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_ROLLOUT_BACKLOG.md)
- [LADDER_AGENT_ROOM_FAQ.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_FAQ.md)
