# Ladder Agent Room Docset

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the authoritative cross-repo build order.

## Purpose

This file is the entry point for the Ladder-in-agent-room documentation set.

Use it when you want to understand:

- the architecture
- the implementation approach
- the rollout order
- the review posture
- the key decisions behind the design

## Reading Order

### 1. Architecture

Read first if you want the full conceptual and structural design:

- [LADDER_AGENT_ROOM_INTEGRATION.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_INTEGRATION.md)

### 2. Execution Brief

Read next if you want the shortest implementation-oriented summary:

- [LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md)

### 3. Rollout Planning

Read this when turning the design into issues or PR slices:

- [LADDER_AGENT_ROOM_ROLLOUT_BACKLOG.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_ROLLOUT_BACKLOG.md)

### 4. Decision Record

Read this when you want the durable architectural choice in ADR form:

- [ADR_LADDER_AGENT_ROOM_V1.md](/Users/shivakrishnayadav/Documents/skyforce/docs/ADR_LADDER_AGENT_ROOM_V1.md)

### 5. FAQ

Read this when you want the plain-language explanation of the main choices:

- [LADDER_AGENT_ROOM_FAQ.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_FAQ.md)

### 6. Review Checklist

Read this when reviewing the proposal or the first implementation slices:

- [LADDER_AGENT_ROOM_REVIEW_CHECKLIST.md](/Users/shivakrishnayadav/Documents/skyforce/docs/LADDER_AGENT_ROOM_REVIEW_CHECKLIST.md)

## Which Doc To Use For What

| Need | Best Doc |
|---|---|
| Understand the full architecture | `LADDER_AGENT_ROOM_INTEGRATION.md` |
| Start the first PR | `LADDER_AGENT_ROOM_IMPLEMENTATION_BRIEF.md` |
| Create issues or backlog items | `LADDER_AGENT_ROOM_ROLLOUT_BACKLOG.md` |
| Review the core architectural decision | `ADR_LADDER_AGENT_ROOM_V1.md` |
| Explain the design to a broader audience | `LADDER_AGENT_ROOM_FAQ.md` |
| Run a design or implementation review | `LADDER_AGENT_ROOM_REVIEW_CHECKLIST.md` |

## Current Recommendation

The docset is now broad enough for planning and review.

The next high-value step is implementation in `../morphos-agent-room`, starting
with the first PR slice defined in the implementation brief and rollout
backlog.
