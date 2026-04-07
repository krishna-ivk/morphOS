# Context Hub Evaluation

This document evaluates [andrewyng/context-hub](https://github.com/andrewyng/context-hub) from the point of view of `morphOS` and the broader Skyforce platform.

The goal is simple:

- identify what problem it solves well
- identify what it does not solve for us
- define where it should fit in the architecture

## Executive Summary

`context-hub` is useful for Skyforce, but it is not the whole answer to the `morphOS` context and memory problem.

It appears to be strongest as:

- a curated external reference layer
- a persistent annotation layer for coding agents
- a practical grounding tool for framework, API, and package context

It is not, by itself, a full OS-level Context Hub.

It does not define or own:

- workflow execution context
- cross-agent operational state
- long-term memory domains
- policy-aware context access
- artifact lineage
- distributed synchronization across nodes

## Why This Matters

One of the biggest open areas in `morphOS` is the architecture of context and memory.

The current open questions include:

- what context is versus memory
- how context is passed into workflows and agents
- what is durable versus ephemeral
- how context is shared across agents
- how privacy and policy affect context access
- how context relates to artifacts, summaries, receipts, and decisions

`context-hub` helps with one part of that problem:

- reliable retrieval of external, curated reference material

That is valuable, but it is only one layer of the full design.

## What `context-hub` Seems To Solve Well

Based on the current repository description and CLI examples, `context-hub` is a strong fit for:

### 1. Reference Context

This is the problem of giving an agent the right external material at the right time.

Examples:

- framework docs
- SDK docs
- API references
- versioned technical references
- project-specific annotations on those references

For Skyforce, this would be useful for:

- Hermes implementation tasks
- Architect platform work
- Hermes-backed synthesis and drafting support
- validation and review agents that need precise external references

### 2. Session-to-Session Knowledge Carryover

The annotation model is useful because it gives agents or operators a persistent note layer that survives beyond a single run.

That is particularly valuable when:

- a library has quirks
- a framework upgrade path is tricky
- a deployment platform needs repeated setup knowledge
- an external provider has non-obvious constraints

### 3. Grounding Against Hallucination

This is one of the most practical benefits.

If an agent can retrieve curated documentation and attached annotations, it reduces:

- API hallucination
- incorrect version assumptions
- stale framework advice
- unnecessary open-web searching

This aligns well with the way Skyforce already wants Hermes and other agents to work.

## What `context-hub` Does Not Solve

This is the important part.

We should not mistake external knowledge retrieval for the full context architecture.

### 1. Operational Context

Skyforce has a growing runtime surface:

- workflows
- approvals
- validation summaries
- execution envelopes
- receipts
- active directives
- run state

This is operational context, not reference context.

`context-hub` does not appear to define how that should be stored, versioned, queried, or shared across agents.

### 2. Persistent Memory Domains

`morphOS` wants a richer memory model:

- episodic memory
- semantic memory
- task memory
- policy memory

`context-hub` does not seem to define those memory types or how they relate to workflows and orchestration.

### 3. Policy-Aware Context Access

For Skyforce, context access must eventually be policy-aware.

Examples:

- some context should be visible only to trusted agents
- some context should be read-only
- some context should require human approval
- some context should be local-only and never synced

`context-hub` does not appear to solve that governance problem.

### 4. Distributed Node Context

Your platform is hybrid:

- EC2
- Mac Mini
- Windows PC
- Android devices

That means context will eventually need rules for:

- local availability
- sync timing
- cache invalidation
- privacy boundaries
- offline replay

`context-hub` is not a topology-aware node context system.

### 5. Artifact and Decision Lineage

Skyforce already has:

- issue summaries
- validation receipts
- execution receipts
- directives
- workflow progress

We still need a system that can answer:

- what context was used to make a decision
- which artifact came from which workflow step
- what changed after approval or rejection

`context-hub` does not seem to be designed for that.

## Recommended Architecture Split

To reduce confusion, the `morphOS` context problem should be split into three layers.

### Layer 1: Reference Context

Purpose:

- external docs
- provider/API references
- framework/package knowledge
- persistent annotations on references

Best fit:

- `context-hub`

This is where Andrew Ng's project fits best.

### Layer 2: Operational Context

Purpose:

- active workflow context
- run inputs and outputs
- execution envelopes
- receipts
- approvals
- issue-linked context bundles

Best fit:

- Skyforce runtime, likely with contracts in `skyforce-core`
- storage and query surfaces in Symphony and Command Centre

This is not the same thing as external reference retrieval.

### Layer 3: Persistent Memory

Purpose:

- lessons learned
- successful fixes
- reusable patterns
- known policy violations
- architecture guidance derived from history

Best fit:

- future dedicated memory/context subsystem
- possibly a separate repo such as `skyforce-context-hub`

This is the long-term memory system, not just a doc retrieval tool.

## Recommended Role For `context-hub` In Skyforce

Short answer:

- adopt it as a reference context subsystem
- do not stretch it into the whole context architecture

### Good uses

- Hermes looks up framework docs before coding
- Architect reviews versioned platform docs
- Hermes support profiles ground communication summaries in actual technical references
- validation agents fetch source-of-truth package or provider docs

### Bad uses

- storing workflow state
- acting as the canonical receipt store
- cross-node synchronization of operational state
- acting as the system memory layer
- serving as the policy decision log

## Design Implications For `morphOS`

This evaluation suggests the `morphOS` architecture should explicitly separate:

- context retrieval
- operational context
- memory

That separation is currently implied, but not spelled out strongly enough.

Recommended follow-up clarifications in `morphOS`:

1. Add a `context architecture` document that separates these three layers.
2. Define which layer is read-mostly, write-heavy, or policy-gated.
3. Define how workflows reference context without copying too much state.
4. Define how context access differs for Hermes, Architect, support-oriented agent profiles, and validation agents.

## Final Recommendation

`andrewyng/context-hub` is a strong fit for one important part of the problem:

- external reference context

It is not the full `Context Hub` that `morphOS` ultimately needs.

The right move is:

- treat it as an input and possibly a dependency for reference retrieval
- keep designing a broader Skyforce context architecture around operational context and persistent memory

That keeps the architecture honest and prevents us from collapsing three different problems into one tool.
