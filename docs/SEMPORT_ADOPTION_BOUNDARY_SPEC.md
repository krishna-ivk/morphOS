# Semport Adoption Boundary Spec

## Why This Spec Exists

`morphOS` already says we should not treat upstream systems as a pile of dependencies.

It also already names four possible adoption postures:

- direct adoption
- wrapped adoption
- semported adoption
- design influence only

What is still missing is a sharper rule for when semporting is the right move and where its boundary should sit.

This spec defines that rule.

## Executive Summary

Semport means:

- preserve upstream intent
- translate it into local contracts, runtime surfaces, or operator semantics
- avoid copying implementation shape blindly

It is the right move when we want the behavioral value of an upstream design but still need local authority over:

- contracts
- trust boundaries
- policy
- observability
- operator language
- runtime ownership splits

The key rule is:

- adopt upstream strength
- keep local meaning

## Core Design Goals

- stop upstream adoption from becoming unstructured copying
- preserve behavior while allowing local runtime bias
- keep Skyforce authoritative over policy, trust, and operator semantics
- make it obvious which upstream ideas are runtime dependencies versus local reinterpretations
- support Elixir-first and Rust-second implementation choices without losing upstream design value

## What Semport Is

Semport is a disciplined translation of upstream behavior or design intent into local system boundaries.

It is not:

- vendor lock-in by imitation
- wholesale code copy
- generic inspiration with no proof of lineage

A good semport keeps:

- the important behavior
- the conceptual boundary
- the useful invariant

while allowing:

- different language
- different runtime placement
- different local contracts
- different operator-facing wording

## When To Semport

Semport is the right choice when one or more of these are true:

- the upstream design is strong, but local contracts must stay authoritative
- the upstream runtime is useful, but it cannot own policy or trust semantics
- the upstream shape is conceptually right, but the implementation language differs
- the platform needs a local adapter or projection layer anyway
- operator surfaces need local delivery language instead of upstream protocol language

## When Not To Semport

Do not semport when:

- direct adoption is safe and local authority is not meaningfully threatened
- only loose inspiration is being taken, with no stable lineage worth preserving
- the local system actually needs the upstream runtime behavior directly, not a translated facsimile
- the idea is too underspecified to translate responsibly

In those cases, prefer:

- direct adoption
- wrapped adoption
- or design influence only

## The Four Adoption Modes Revisited

### 1. Direct Adoption

Use when:

- upstream runtime behavior can remain mostly intact
- local semantics do not need deep reinterpretation

Risk:

- hidden authority drift if used too broadly

### 2. Wrapped Adoption

Use when:

- the upstream runtime should remain active
- but Skyforce needs local control over boundaries and projections

Risk:

- wrapper becomes thin ceremony unless ownership is explicit

### 3. Semported Adoption

Use when:

- local contracts or runtime placement must change
- but the upstream behavior or conceptual boundary should survive

Risk:

- accidental cargo-culting if intent is not restated clearly

### 4. Design Influence Only

Use when:

- the upstream contributes useful ideas
- but no strong lineage or compatibility claim is needed

Risk:

- vague “inspired by” claims that offer little discipline

## The Semport Boundary Question

Every semport effort must answer:

- what remains upstream-owned?
- what becomes locally owned?
- where is the translation boundary?

For `morphOS`, the local side should remain authoritative for:

- policy meaning
- trust and approval boundaries
- workspace and global governance
- operator-facing delivery semantics
- shared contracts in `skyforce-core`
- evidence, summary, and audit conventions

That means semport usually sits at the boundary between:

- upstream design intent
- local system meaning

## Canonical Semport Packet

Every semport should begin with a `Semport Packet`.

Minimum fields:

- `source_system`
- `source_concept`
- `adoption_mode`
- `local_target`
- `preserved_intent`
- `local_ownership_boundary`
- `non_ported_elements`
- `validation_plan`

This keeps semporting explicit instead of implicit.

## What Must Be Preserved

A semport should name the parts of the upstream behavior that must survive translation.

Typical preserved elements:

- conceptual boundary
- lifecycle semantics
- event meaning
- state transitions
- operator expectation
- failure-handling posture

Examples:

- Symphony’s orchestration-vs-execution distinction
- Durable’s checkpoint and retry authority
- Context Hub’s curated reference retrieval and annotations
- Skills’ capability packaging model

## What Must Stay Local

A semport should also name what Skyforce refuses to outsource.

Typical local-only elements:

- policy language
- approval-routing meaning
- workspace and global governance
- delivery terminology
- artifact names and evidence posture
- promotion readiness rules

This is where semport differs from thin wrapping.

## Semport Evidence

Semport claims should not rest on narrative alone.

Each semport should produce evidence that:

- the important upstream intent was preserved
- the local boundary is clear
- the translated behavior still works in Skyforce context

Useful proof methods:

- contract comparison
- behavior scenarios
- operator-surface comparison
- integration tests against local runtime boundaries

## Example Semport Decisions

### Symphony

Good semport candidates:

- local runtime contracts for workflow state and directives
- operator-facing delivery posture derived from orchestration behavior

Do not semport:

- overall policy language
- memory semantics

### Durable

Good semport candidates:

- local `ExecutionCheckpoint` record shapes
- status and checkpoint projections into Skyforce contracts

Do not semport:

- workflow meaning
- step selection authority

### Context Hub

Good semport candidates:

- local context contracts
- trust labels
- reference-vs-operational-vs-memory separation

Do not semport:

- full operational runtime state ownership

### Skills

Good semport candidates:

- local skill taxonomy
- archetype-to-skill attachment
- capability references in contracts

Do not semport:

- agent archetype meaning itself

## Semport Decision Rules

Before semporting, ask:

1. is the upstream concept stable enough to preserve?
2. does Skyforce need local ownership of semantics?
3. would direct adoption create authority confusion?
4. can the preserved intent be validated after translation?
5. is the local target repo the right place for the translated boundary?

If the answer to these is mostly yes, semport is likely the right mode.

## Relationship To Gene Transfusion

Semport and gene transfusion are related, but not the same.

- gene transfusion moves a proven pattern from one codebase or surface to another
- semport moves an upstream concept into a local contract or runtime boundary

Gene transfusion usually asks:

- does the target behave like the exemplar?

Semport usually asks:

- did we preserve the upstream intent while relocating authority locally?

## Relationship To Parallel Execution

Semport work should be parallelized carefully.

Good parallel slices:

- one slice defines local contract translation
- one slice maps operator surface implications
- one slice validates runtime behavior against the semport packet

Bad parallel slices:

- multiple slices redefining the same upstream concept differently

## Required Artifacts

Each semport should emit durable artifacts.

Suggested baseline:

- `semport/packet.json`
- `semport/preserved_intent.md`
- `semport/local_boundary.md`
- `semport/validation_results.json`
- `semport/adoption_verdict.json`

These artifacts should feed:

- review
- future upstream drift analysis
- implementation lineage

## Upstream Drift

Semport does not end when the first translation lands.

The platform should also track:

- what upstream version or concept snapshot was used
- known divergence from upstream
- whether later upstream changes require local reevaluation

Suggested verdicts:

- `aligned`
- `aligned_with_local_divergence`
- `drift_detected`
- `revisit_required`

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define semport packet and adoption verdict contracts
- `morphOS` should mark which major upstream concepts are direct, wrapped, semported, or influence-only
- `skyforce-symphony` and other runtime repos should cite semport packets when translating upstream behavior into local code
- `skyforce-command-centre` should expose local delivery semantics without leaking upstream protocol language unnecessarily

## Recommended First Implementation Slice

The first useful slice should be narrow and high-value:

1. define the `Semport Packet`
2. apply it to Symphony and Durable boundaries first
3. record preserved intent and local ownership boundaries
4. emit semport adoption verdicts in design artifacts
5. use those packets as lineage for future implementation work

That is enough to make semport actionable instead of philosophical.

## Recommended Next Specs

This spec should be followed by:

1. `CODE_INTELLIGENCE_RETRIEVAL_SPEC.md`
2. `TOKEN_AND_COMMAND_MEDIATION_SPEC.md`
3. `DIGITAL_TWIN_UNIVERSE_ROLLOUT_SPEC.md`

Together, those continue the remaining retrieval, execution-efficiency, and twin-expansion work.
