# Ladder Agent Room FAQ

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the authoritative cross-repo build order. This FAQ is a plain-language companion to [LADDER_AGENT_ROOM_INTEGRATION.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_INTEGRATION.md), [LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md), and [LADDER_AGENT_ROOM_ROLLOUT_BACKLOG.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_ROLLOUT_BACKLOG.md).

## What problem is this solving?

Today, an agent room is good at conversation, collaboration, and convergence,
but it is weaker at preserving the structure of discovery itself.

Ladder gives the room a durable way to represent:

- what we observed
- what we think might work
- what we decided to test
- what actually happened
- what methods are now reusable

## Why use Ladder in the room at all?

Because the room is the right place for messy exploration, but the factory is
the wrong place for it.

The room should absorb ambiguity and turn it into structured, evidence-backed
objects. The factory should consume only the more settled outputs.

## Why not just use chat transcripts?

Because transcripts are good for conversation but bad as a canonical system of
record for discovery state.

Problems with transcript-only storage:

- hard to query
- hard to validate
- hard to export cleanly
- too dependent on prompt wording
- too easy to lose object relationships

## Why not keep everything in artifacts only?

Artifacts are a strong UI and projection mechanism, but they should not be the
only durable truth for shared Ladder state.

The recommended model is:

- relational tables for truth
- artifact projection for display

That keeps shared ownership, persistence, and export logic cleaner.

## Why put Ladder in `murmur_demo` first?

Because that is where the room product behavior already lives.

`murmur_demo` already owns:

- decisions
- export logic
- workspace UI behavior

Starting there avoids premature abstraction. If Ladder later proves reusable
across multiple Murmur-based products, it can be extracted then.

## Why not create a new umbrella app right away?

Because that adds packaging overhead before the domain has stabilized.

The simpler move is:

- prove the domain in `murmur_demo`
- complete one room-to-export cycle
- extract later only if reuse is real

## Why not let Ladder become the orchestrator?

Because `morphOS-agent-room` already has runtime orchestration surfaces.

If Ladder also becomes an orchestrator, you get:

- duplicate state machines
- unclear ownership
- harder debugging
- confused operator expectations

Ladder is most useful here as a discovery grammar, not a second engine.

## Why connect experiments to the shared task board?

Because experiments are not only ideas. They are work.

The task board already provides:

- persistence
- shared visibility
- assignees
- statuses

So the clean split is:

- Ladder explains why we are doing work
- tasks track the execution of that work

## Why require evidence for validated results?

Because without evidence, validation becomes opinion dressed up as state.

The whole point of Ladder in this context is to improve the quality of what gets
handed into the factory. Evidence-backed validation is the minimum guardrail.

## Why require human approval for algorithms or factory promotion?

Because promoted methods and exported work can shape downstream execution.

That is a governance boundary, not just a UX preference.

The room can stay fast and exploratory, but the jump from discovery to
repeatable or executable factory input should be explicit.

## Why keep export integration last?

Because export should reflect stable domain semantics, not define them.

If export comes first, the system gets shaped around file output before the room
model itself is solid. That usually creates rework.

## What should the first PR actually prove?

It should prove only this:

- shared Ladder objects can persist
- the UI can render them
- the room can move from source to idea to hypothesis cleanly

That is enough to validate the approach without pulling in experiments, results,
algorithms, and exports all at once.

## What are the biggest ways this could go wrong?

The main failure modes are:

- the UI becomes the real source of truth
- artifact projection gets mistaken for canonical persistence
- the first slice gets too big
- speculative work leaks into export
- task status and Ladder status drift without clear ownership

## What would success look like?

Success means:

- a room can preserve discovery as structured state
- humans and agents can inspect the learning chain quickly
- experiments connect cleanly to shared execution
- only validated work moves toward export
- the factory receives better upstream artifacts without needing raw transcript interpretation

## What should happen next after the docs?

The most practical next move is one of:

1. convert the rollout backlog into real issues
2. implement the first PR slice in `morphos-agent-room`

Anything beyond that is probably more planning than the system needs right now.
