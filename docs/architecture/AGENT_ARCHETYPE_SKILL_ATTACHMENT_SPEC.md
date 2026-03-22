# Agent Archetype Skill Attachment Spec

## Purpose

This spec defines how the six MVP archetypes attach to reusable registered skills
without changing archetype authority or mission contracts.

It establishes a governed mapping layer between:

- stable role contracts from `AGENT_ARCHETYPES_SPEC.md`
- reusable capability assets from skill packaging and registration
- runtime capability references through `SkillRef`

The goal is to keep archetypes durable as role semantics while allowing
capability implementation to evolve through registered reusable skills.

## Core Principle

Archetypes define role authority. Skills provide reusable capability execution.

Therefore:

- archetype identity and authority boundaries are fixed by archetype doctrine
- skill attachment is governed and replaceable when registration rules are met
- runtime assignment must resolve to registered, policy-eligible `SkillRef` values

This separation prevents prompt-level drift from redefining role authority.

## Grounding In Existing v0 Contracts

This spec is grounded in:

- `docs/architecture/AGENT_ARCHETYPES_SPEC.md`
  - defines the six archetypes, missions, disallowed actions, and default tool posture
- `docs/core-mechanics/SKILL_PACKAGING_AND_REGISTRATION_SPEC.md`
  - defines `SkillPackage`, `SkillRegistration`, lifecycle gates, and activation posture
- `docs/milestones/v0/MORPHOS_V0_RUNTIME_CONTRACTS.md`
  - defines `SkillRef` runtime contract and shared interoperability boundary
- `docs/morphos-software-factory-mvp.md`
  - defines MVP archetypes, required artifact families, and software-factory loop

This spec does not introduce new archetypes and does not redefine archetype
authority.

## Attachment Model

## 1. Attachment Object

An archetype should attach to capabilities through explicit `SkillRef` bindings,
not inline implementation assumptions.

Minimum attachment record shape:

- `archetype_id`
- `skill_ref` (`skill_id`, `version`, and required contracts from `SkillRef`)
- `attachment_mode` (`required`, `preferred`, `fallback`)
- `selection_scope` (`core`, `workspace`, `curated`)
- `policy_profile_ref` (optional)
- `updated_at`

## 2. Attachment Levels

Every archetype may declare three governed levels of skill expectation:

- required skills
  - must resolve before the archetype can execute assigned work
- preferred skills
  - selected first when multiple eligible skills satisfy required contracts
- fallback skills
  - used only when preferred options are unavailable or policy-blocked

## 3. Attachment Eligibility

A skill is attachment-eligible only when:

- its package version is `registered` and currently `active`
- activation posture permits runtime selection in the current scope
- declared `supported_archetypes` includes the target archetype
- required tool families and context layers are satisfiable

## Resolution Rules

Runtime archetype-to-skill resolution should be deterministic and auditable.

## Rule 1: Preserve Archetype Contract

Resolution may not alter archetype mission, disallowed actions, or authority
boundaries from `AGENT_ARCHETYPES_SPEC.md`.

## Rule 2: Resolve Only To Registered Skills

`SkillRef` resolution must target active registrations only.
Unregistered package contents are not runtime-eligible.

## Rule 3: Enforce Contract Compatibility

Selected skills must satisfy:

- `input_contract_refs` required by the assigned workflow step
- `output_contract_refs` needed for downstream handoff
- `required_context_layers` available to this run
- `required_tools` allowed under current tool posture and policy

## Rule 4: Respect Version Posture

Version resolution should follow v0 compatibility rules:

- exact registered versions are preferred
- major-version incompatibility is rejected by default
- minor or patch movement requires compatibility validation

## Rule 5: Produce Attachment Receipts

Each resolution event should emit an auditable record including:

- archetype id
- selected `SkillRef`
- rejected candidates with reason classes
- effective tool posture and policy constraints
- artifact expectations for the step

## Archetype Attachment Expectations

The following subsections define governed skill expectation posture per existing
MVP archetype.

## `planner`

Primary capability posture:

- planning decomposition
- workflow path selection
- acceptance and policy posture shaping

Attachment expectations:

- required
  - work-order interpretation and plan synthesis skills
- preferred
  - routing heuristics and risk-tagging skills
- fallback
  - minimal deterministic planning templates

Output expectation examples:

- run plan artifacts
- routing decisions
- acceptance posture annotations

## `coder`

Primary capability posture:

- implementation change production
- test updates and execution receipts

Attachment expectations:

- required
  - repo mutation and implementation skills aligned to workflow scope
- preferred
  - language- and framework-aware coding skills
- fallback
  - bounded patch and scaffold skills

Output expectation examples:

- code changes
- tests
- execution receipt
- implementation summary

## `reviewer`

Primary capability posture:

- quality and risk review of change sets
- findings and review verdict production

Attachment expectations:

- required
  - diff inspection and finding classification skills
- preferred
  - policy-aware regression risk review skills
- fallback
  - baseline review checklist skills

Output expectation examples:

- review findings
- review verdict
- review packet

## `validator`

Primary capability posture:

- objective check execution or evaluation
- evidence-backed acceptance recommendation

Attachment expectations:

- required
  - validation execution and evidence assembly skills
- preferred
  - contract/schema and multi-check aggregation skills
- fallback
  - deterministic smoke and receipt verification skills

Output expectation examples:

- validation results
- evidence bundle
- validation receipt
- acceptance recommendation

## `releaser`

Primary capability posture:

- governed promotion readiness evaluation
- release packet and transition preparation

Attachment expectations:

- required
  - release-gate evaluation and packaging skills
- preferred
  - release-note and promotion packet assembly skills
- fallback
  - minimal release readiness checklist skills

Output expectation examples:

- promotion packet
- release readiness summary
- release receipt

## `operator_liaison`

Primary capability posture:

- operator-facing handoff and intervention bridging
- clarification and approval request packaging

Attachment expectations:

- required
  - operator packet rendering and queue handoff skills
- preferred
  - urgency classification and next-action framing skills
- fallback
  - basic clarification and approval request templates

Output expectation examples:

- operator handoff packet
- clarification request
- approval request
- operator-visible summary

## Relationship To Tool Posture And Required Artifacts

Skill attachment does not replace archetype tool posture. It operationalizes it.

Rules:

- archetype default tool posture remains defined in
  `AGENT_ARCHETYPES_SPEC.md`
- selected skill `required_tools` must be a subset of archetype-allowed tool
  posture unless an explicit policy exception exists
- if a skill requires tools outside archetype posture, resolution must fail or
  escalate through policy and operator channels

Artifact relationship:

- selected skills should produce or help produce archetype-expected outputs
- expected MVP artifact families remain:
  - `work order`
  - `run plan`
  - `execution receipt`
  - `validation report`
  - `summary pyramid`
  - `approval packet`
  - `run memory index`
- attachment receipts should link produced artifacts to the resolved `SkillRef`
  for lineage and auditability

## Relationship To `SkillRef` And Archetypes

`SkillRef` remains the runtime capability pointer.
Archetypes remain the stable role contracts.

Operational relationship:

- archetype says who is allowed to do what kind of work
- `SkillRef` says which reusable capability implementation is selected
- registration and activation posture determine whether that capability is
  selectable now

This preserves role authority while making reusable capability selection
explicit, governed, and observable.

## Summary

The six MVP archetypes should stay stable as governed role contracts.

This spec defines a deterministic attachment and resolution boundary that maps
those roles to registered reusable skills through `SkillRef`, while preserving
existing authority doctrine, tool posture constraints, and required artifact
lineage.
