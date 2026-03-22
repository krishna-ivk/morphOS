# Gene Transfusion Equivalence Spec

## Why This Spec Exists

`morphOS` already treats `Gene Transfusion` as a core software-factory technique:

- reuse a strong exemplar
- transfer the behavioral pattern into another repo or surface
- validate that the result still behaves acceptably

What is still missing is a precise contract for the last part:

How do we decide that a transplanted pattern is behaviorally equivalent enough to trust?

This spec defines that contract.

## Executive Summary

Gene transfusion should not mean:

- copy code blindly
- preserve syntax at all costs
- declare success because the UI looks similar

It should mean:

- identify the exemplar behavior that matters
- restate that behavior as a portable contract
- implement it in the target repo or surface
- prove that the target satisfies the required behavior

The system is allowed to change language, framework, structure, and internal mechanics.
It is not allowed to silently lose the behavior that justified the transfer.

## Core Design Goals

- transfer proven patterns without cargo-cult copying
- preserve behavior while allowing local implementation freedom
- make equivalence measurable enough for factory workflows
- support cross-language and cross-framework moves
- produce reviewable proof artifacts instead of relying on intuition

## What Counts As A Gene Transfusion

A gene transfusion is a deliberate transfer of a proven behavioral pattern from a source exemplar into a new target.

Common examples for Skyforce:

- React flow -> LiveView flow
- prototype runtime behavior -> production runtime behavior
- CLI workflow -> dashboard workflow
- one repo's approval or summary pattern -> another repo's equivalent feature
- implementation pattern from an upstream or starred repo -> local Skyforce contract

The transfused asset is the behavioral pattern, not merely the code text.

## What Counts As Equivalence

Equivalence does not require identical source code.

For `morphOS`, a target is equivalent when:

- the required behavior is preserved
- important inputs and outputs remain compatible
- critical failure handling still works
- operator-visible meaning remains consistent
- policy and approval posture are not weakened without explicit acceptance

This means equivalence is behavioral and contractual, not syntactic.

## Equivalence Levels

`morphOS` should support four equivalence levels:

### 1. Exact

Meaning:

- inputs, outputs, and observable behavior should match closely

Use when:

- shared contract implementation must stay near-identical
- protocol or machine-readable outputs are strict

### 2. Functional

Meaning:

- the target may differ internally, but all required user-visible and system-visible behaviors are preserved

Use when:

- moving across frameworks or runtimes
- preserving feature semantics matters more than structure

### 3. Operational

Meaning:

- the main workflow behavior is preserved, even if some secondary experience details differ

Use when:

- the pattern is being ported into a different surface with different ergonomics

### 4. Intent-Only

Meaning:

- the target borrows the design idea, but does not claim strong equivalence

Use when:

- the source is inspiration, not a strict exemplar

This level should not be used for high-risk promotion claims.

## The Exemplar Packet

Every gene transfusion should begin by defining an `Exemplar Packet`.

The packet should capture:

- source repo or source surface
- target repo or target surface
- feature or behavior being transferred
- equivalence level being claimed
- required invariants
- allowed divergences
- validation plan
- policy or approval implications

Without this packet, transfusion work stays too fuzzy to validate properly.

## Required Invariants

Each transfusion must declare the invariants that must survive the move.

Common invariant families:

- input contract invariants
- output contract invariants
- workflow-state invariants
- validation invariants
- operator wording or posture invariants
- approval or policy invariants
- failure-handling invariants

Examples:

- approval-required behavior must still block promotion
- validation findings must still surface in the summary
- retry exhaustion must still route to review
- operator-facing readiness labels must preserve meaning

## Allowed Divergences

A good transfusion spec must also declare what may change safely.

Examples:

- framework or language
- internal component structure
- storage details behind a stable contract
- exact visual layout when preserving workflow meaning
- internal event implementation when exported events remain stable

If allowed divergences are not named, review will either become too strict or too vague.

## Canonical Equivalence Questions

Every transfusion should answer:

1. what behavior from the exemplar is essential?
2. what behavior is incidental?
3. what inputs and outputs must remain compatible?
4. what failure modes must still be handled?
5. what policy or approval gates must remain intact?
6. what evidence will prove the claim?

## Equivalence Proof Methods

`morphOS` should support several proof methods, used together where appropriate.

### 1. Scenario Comparison

Run the same scenarios against source behavior and target behavior.

Useful for:

- workflow transitions
- approval routing
- summary behavior
- operator-state changes

### 2. Contract Comparison

Compare machine-readable contracts and artifact shapes.

Useful for:

- event payloads
- summary artifacts
- approval packets
- promotion packet shapes

### 3. Twin-Assisted Validation

Use the same digital twin scenarios for source and target when external systems are involved.

Useful for:

- integration-heavy transfusions
- cross-repo external action patterns

### 4. Review-Based Equivalence

Use structured human review when behavior is meaningful but not fully automatable.

Useful for:

- operator experience parity
- nuanced workflow visibility
- qualitative UX consistency

## Equivalence Verdicts

The runtime and review surfaces should converge on a small verdict set:

- `equivalent`
- `equivalent_with_noted_divergence`
- `not_equivalent`
- `insufficient_evidence`

Suggested meanings:

- `equivalent`
  - the claimed invariants are satisfied
- `equivalent_with_noted_divergence`
  - required behavior is preserved, but accepted differences exist
- `not_equivalent`
  - required behavior is missing, weakened, or contradictory
- `insufficient_evidence`
  - the target may be good, but the proof packet is incomplete

## Required Transfusion Artifacts

Each transfusion should emit a durable proof packet.

Suggested baseline layout:

- `transfusion/exemplar_packet.json`
- `transfusion/invariants.json`
- `transfusion/allowed_divergences.json`
- `transfusion/scenario_results.json`
- `transfusion/equivalence_verdict.json`
- `transfusion/review_notes.md`

These artifacts should be usable by:

- validation
- review
- promotion posture
- future transfusions borrowing the same exemplar

## Relationship To Validation Guardrails

Gene transfusion equivalence should plug into the broader validation loop.

Typical flow:

1. implement the target behavior
2. run normal validation
3. run transfusion equivalence validation
4. route to review if equivalence is unclear or weak
5. allow promotion only if the claimed equivalence level is sufficiently proven

This prevents a transplanted feature from passing ordinary tests while still losing the intended behavior.

## Relationship To Digital Twins

When the source and target both interact with external systems, digital twins should become the preferred equivalence surface.

That means:

- run comparable twin scenarios for source and target
- compare observed state changes and failure handling
- record fidelity posture and known gaps

Twin validation makes cross-repo behavioral comparison safer and more repeatable.

## Relationship To Policy

A successful transfusion must not silently weaken policy posture.

The equivalence proof should explicitly check whether the target preserves:

- approval requirements
- policy blocks
- authority routing
- protected live-action gates

If the target weakens policy posture, that is either:

- `not_equivalent`, or
- an explicitly accepted divergence requiring review and approval

## Factory Mode vs Interactive Mode

In `factory` mode, equivalence checks should be as deterministic as possible.

In `interactive` mode, the operator may refine the exemplar packet, mark acceptable divergences, or request additional proof.

The core requirement stays the same:

- a transfusion claim must be backed by explicit evidence

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define exemplar packet, invariant, and equivalence verdict contracts
- `skyforce-symphony` should treat transfusion equivalence as an explicit validation track for pattern-transfer workflows
- `skyforce-harness` should emit scenario and artifact comparisons that feed the proof packet
- `skyforce-command-centre` should show the claimed equivalence level and final verdict in review flows

## Recommended First Implementation Slice

The first useful slice should be narrow and practical:

1. define the exemplar packet and verdict contracts
2. support `functional` equivalence first
3. compare summary, approval, and validation behavior across source and target
4. emit an equivalence verdict artifact
5. route `insufficient_evidence` and `not_equivalent` into review

This is enough to make repo-to-repo pattern transfer governable without overbuilding the first pass.

## Recommended Next Specs

This spec should be followed by:

1. `SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md`
2. `WORKSPACE_ADMIN_GOVERNANCE_SPEC.md`
3. `PARALLEL_WORKSPACE_EXECUTION_SPEC.md`

Together, those close more of the remaining gaps around execution mode, authority, and multi-agent delivery discipline.
