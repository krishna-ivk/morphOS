# morphOS Roadmap

Canonical priority note: roadmap phases live here, but the current implementation order is tracked in [MORPHOS_V0_IMPLEMENTATION_BOARD.md](milestones/v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md).

This roadmap tracks how `morphOS` should evolve from a strong specification repository into a stable operating-model authority for the Skyforce runtime stack.

It is intentionally scoped around definition, contracts, and integration.
It does not turn `morphOS` into a second runtime platform.

## Release Direction

Aim for:

- `v1.0` as the first real release target

Interpretation:

- the active `v0` work is the proving track
- `v1.0` is the first release bar
- use [milestones/v1/MORPHOS_V1_RELEASE_TARGET.md](milestones/v1/MORPHOS_V1_RELEASE_TARGET.md) as the release-definition document

## Roadmap Principles

1. `morphOS` defines, Skyforce implements.
2. Shared contracts must converge in `skyforce-core`.
3. Runtime behavior belongs in `skyforce-symphony` and `skyforce-harness`.
4. Human visibility and approvals belong in `skyforce-command-centre-live`, with backend normalization in `skyforce-api-gateway`.
5. Self-evolution must remain proposal-driven until validation and policy are mature.

## Version 0.1.x — Foundation Baseline

Status:

- current

Goals:

- establish `morphOS` as a clear specification repo
- document buildability and repo boundaries
- prepare a versioned release shape

Deliverables:

- descriptive repository README
- changelog
- package manifest
- evaluation of `morphOS` vs Skyforce
- buildability plan
- roadmap

Exit criteria:

- the role of `morphOS` is clear
- the repo is ready to go private without losing meaning

## Version 0.2.x — Contract Alignment

Goals:

- align the strongest `morphOS` specs with executable shared contracts

Primary work:

- define event envelope contracts
- define policy contracts
- define connectivity mode contracts
- define topology contracts
- define workflow template contracts
- define agent cell and archetype contracts

Expected implementation repo:

- `skyforce-core`

Exit criteria:

- `morphOS` docs and `skyforce-core` contracts no longer drift on core models

## Version 0.3.x — Workflow Template Integration

Goals:

- make `morphOS` workflow templates usable by the Skyforce runtime

Primary work:

- template validation
- template loading in Symphony
- initial supported step types
- runtime exposure of loaded templates

Expected implementation repo:

- `skyforce-symphony`

Supported initial step types:

- sequential
- parallel
- conditional
- approval
- retry metadata

Exit criteria:

- Symphony can load and expose `morphOS` workflow templates

## Version 0.4.x — Event and Policy Integration

Goals:

- bring `morphOS` event and policy design into the real runtime loop

Primary work:

- align event taxonomy across runtime repos
- emit typed workflow and execution events
- add policy evaluation hooks in Symphony and Harness
- expose policy and event visibility in Command Centre Live via the gateway

Expected implementation repos:

- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-api-gateway`
- `skyforce-command-centre-live`
- `skyforce-core`

Exit criteria:

- runtime events and policy decisions map clearly back to `morphOS` specs

## Version 0.5.x — Agent Archetype Runtime Mapping

Goals:

- translate `morphOS` agent definitions into runtime-usable registrations

Primary work:

- machine-readable archetype format
- import path into Symphony Agent Hub
- policy and capability mapping per archetype
- node preference and protocol support mapping

Expected implementation repos:

- `morphOS`
- `skyforce-core`
- `skyforce-symphony`

Exit criteria:

- runtime agent registrations can be derived from `morphOS` archetypes

## Version 0.6.x — Connectivity and Topology Awareness

Goals:

- implement the offline/online/hybrid model as a real platform behavior

Primary work:

- connectivity flags
- deferred actions
- node topology classes
- topology-aware routing and visibility

Expected implementation repos:

- `skyforce-core`
- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-command-centre`

Exit criteria:

- the runtime reflects the topology and connectivity model defined in `morphOS`

## Version 0.7.x — Memory and Learning Foundations

Goals:

- create a safe, explicit first memory and learning layer

Primary work:

- memory domain definitions
- learning artifact schema
- proposal format for learned improvements
- write authority and retention rules

Open constraints:

- no autonomous self-modification
- no uncontrolled policy mutation

Exit criteria:

- learning produces governed proposals rather than direct structural changes

## Version 0.8.x — Proposal-Driven Evolution

Goals:

- allow the system to propose changes to itself in a traceable way

Primary work:

- improvement proposal artifacts
- validation integration
- human approval flow
- evolution audit trail

Expected implementation repos:

- `morphOS`
- `skyforce-core`
- `skyforce-symphony`
- `skyforce-command-centre`

Exit criteria:

- the system can recommend improvements without bypassing trust boundaries

## Not On The Immediate Roadmap

These are intentionally deferred:

- a separate `morphOS` runtime orchestrator
- a separate `morphOS` event bus implementation
- unconstrained self-modifying code generation
- automatic policy rewriting without approval
- fully autonomous human-role emulation

## Success Measures

The roadmap is working if:

- `morphOS` stays strategically clean
- Skyforce runtime becomes more coherent over time
- fewer concepts are duplicated across repos
- policies and events become consistent
- workflow definitions become portable
- learning remains observable and governable

## Current Recommendation

Build next:

1. contract alignment
2. workflow template loading
3. event alignment
4. policy hooks
5. agent archetype mapping

Do not build next:

1. autonomous self-modification
2. separate runtime infrastructure inside `morphOS`

## v1.0 Release Gate

The roadmap should now be read with one practical question in mind:

- does this work move the stack closer to the `v1.0` release target?

For the current release bar, see:

- [milestones/v1/MORPHOS_V1_RELEASE_TARGET.md](milestones/v1/MORPHOS_V1_RELEASE_TARGET.md)
