# Skill Packaging And Registration Spec

## Why This Spec Exists

`morphOS` already defines `SkillRef` as a core runtime contract in
`MORPHOS_V0_RUNTIME_CONTRACTS.md`.

That gives the system a reusable capability reference, but it does not yet define:

- how a reusable skill is packaged as a durable asset
- how a package is registered into a runtime-visible catalog
- how registration is validated and approved before activation
- how archetypes and workflows attach to skills without embedding implementation

`WORKFLOW_PACK_AND_REGISTRY_SPEC.md` already solved this boundary for workflows.
This spec applies the same core doctrine to skills so the platform can treat
skills as governed reusable units instead of ad hoc prompt or folder conventions.

## Executive Summary

The correct v0 model is:

- `SkillPackage`
  - a versioned bundle that contains one or more reusable skills plus metadata
- `SkillRegistration`
  - a validated, approved registry record that makes a package selectable
- `SkillRef`
  - a runtime reference contract used by workflows, archetypes, and assignment logic

The key rule is:

- package defines artifact and metadata truth
- registration defines lifecycle and activation posture
- reference defines runtime linkage

This spec intentionally defines a minimum operational boundary for packaging and
registration. It does not attempt to define the full long-horizon trust and
version governance system.

## Grounding In Existing v0 Contracts

This spec is grounded in four existing documents:

- `docs/milestones/v0/MORPHOS_V0_RUNTIME_CONTRACTS.md`
  - establishes `SkillRef` as a mandatory shared contract and explicitly calls
    for skill registration and versioning rules as follow-on work
- `docs/workflows/WORKFLOW_PACK_AND_REGISTRY_SPEC.md`
  - establishes the pack/registry pattern and validation posture reused here
- `docs/architecture/AGENT_ARCHETYPES_SPEC.md`
  - defines role contracts that require governed skill attachment boundaries
- `docs/milestones/v0/MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md`
  - sets adoption posture for `openai/skills` as semported and locally governed

The result is a local, governed packaging and registration model that preserves
modular capability ideas from upstream without outsourcing runtime meaning.

## Package Vs Registration Vs Reference

## 1. Skill Package

Meaning:

A `SkillPackage` is the reusable distribution asset for one capability family.
It contains executable or interpretable skill assets, contracts, and metadata.

Answers:

- what is included
- who owns it
- what version this package is
- what runtime and capability assumptions it needs

## 2. Skill Registration

Meaning:

A `SkillRegistration` is the governed record that one package version has passed
required checks and is available to runtime selection.

Answers:

- whether the package is installable and selectable
- what lifecycle state it is in
- what approval posture was applied
- where it is active (workspace/shared/core scope)

## 3. Skill Reference

Meaning:

`SkillRef` remains the lightweight runtime pointer used in task routing,
workflow templates, and archetype mappings.

Answers:

- what capability is requested
- what version line is requested
- what interfaces and tool expectations apply

Rule:

`SkillRef` must point to a registered package version for activation.
Unregistered package contents are not runtime-eligible.

## Skill Package Layout

Recommended v0 package layout:

```text
skill-packs/
  <skill_pack_id>/
    package.json
    skills/
      <skill_id>/
        skill.md
        input.schema.json
        output.schema.json
        tools.json
    tests/
      smoke/
    docs/
      README.md
```

Notes:

- file-level implementation details can vary by runtime adapter
- package-level metadata and required contract files are mandatory
- this shape mirrors workflow-pack discipline while keeping skills modular

## Required Package Metadata

`package.json` minimum fields:

- `skill_pack_id`
- `name`
- `version`
- `description`
- `owner`
- `source`
- `adoption_mode`
- `runtime_compatibility`
- `skill_entries`
- `default_activation_posture`
- `created_at`
- `updated_at`

`skill_entries[]` minimum fields:

- `skill_id`
- `name`
- `version`
- `description`
- `provider`
- `input_contract_refs`
- `output_contract_refs`
- `required_tools`
- `required_context_layers`
- `supported_archetypes`

The entry shape aligns directly with the `SkillRef` fields already defined in
`MORPHOS_V0_RUNTIME_CONTRACTS.md`.

## Registration Lifecycle

Every package version should flow through these lifecycle states:

- `draft`
  - package exists but is not submitted for runtime use
- `submitted`
  - package version entered registry intake
- `validated`
  - structural and compatibility checks passed
- `approval_pending`
  - awaiting required authority decision
- `approved`
  - authority granted for installation/activation scope
- `registered`
  - durable registry record created
- `active`
  - package can satisfy `SkillRef` resolution
- `suspended`
  - temporarily excluded from new selection
- `retired`
  - no longer selectable for new runs

Rule:

- only `active` registrations can satisfy new runtime resolution
- in-flight runs may continue on previously resolved versions when policy allows

## Validation And Approval Gates

Registration should pass three required gates before `active`:

## Gate 1: Structural Validation

Checks:

- required package metadata fields exist
- each `skill_id` is unique inside the package
- required contract references resolve
- declared tool families are well-formed

## Gate 2: Compatibility Validation

Checks:

- `runtime_compatibility` is satisfiable in current environment
- required context layers map to runtime contract values
- required tools are discoverable in the tool registry
- declared archetype attachments match known archetype ids

## Gate 3: Approval Validation

Checks:

- required owner or operator approval exists for target scope
- activation posture matches policy constraints
- any required evidence bundle is attached

These gates align with the same doctrine used in workflow-pack validation and
policy-aware activation.

## Activation Posture

Registration should expose one explicit activation posture:

- `core_active`
  - first-party, default-eligible
- `curated_active`
  - governed and selectable, not forced default
- `experimental_limited`
  - selectable only where policy allows
- `suggested_only`
  - visible for planning/recommendation, not auto-activatable

This posture controls selection behavior, not deep trust scoring.

## Minimum Version Handling

v0 version handling should stay minimal and explicit:

- every package and skill entry must declare `version`
- registration records one exact installed version
- `SkillRef.version` resolves against registered versions only
- major-version mismatch is incompatible by default
- minor/patch upgrades are allowed only when compatibility checks pass

Minimum additional required fields for version handling:

- `runtime_compatibility.min_contract_version`
- `runtime_compatibility.max_contract_version`
- `replaces` (optional pointer to prior package version)

This is enough for deterministic v0 resolution and safe upgrade posture without
designing the full future governance system.

## Relationship To SkillRef

`SkillRef` remains the shared runtime object used across orchestration,
assignment, and observability.

This spec adds the missing backing boundary:

- `SkillPackage` provides reusable artifact truth
- `SkillRegistration` provides governed eligibility and lifecycle
- `SkillRef` provides runtime indirection to those registered assets

So `SkillRef` is not replaced. It is made operationally real.

## Explicit Deferrals

This spec intentionally does not define:

- full trust-score doctrine across multi-wave evidence
- global version-governance policy across all repos and environments
- cryptographic signing and supply-chain attestation model
- marketplace-style distribution, discovery, ranking, or monetization
- transitive dependency governance for nested third-party skill bundles

Those are follow-on governance topics. v0 only needs packaging,
registration-lifecycle discipline, and activation posture.

## Ownership

### `morphOS` owns

- packaging and registration doctrine semantics
- lifecycle and activation-posture definitions
- relationship between archetypes, workflows, and `SkillRef`

### `skyforce-core` owns

- shared schema contracts for package metadata and registration records
- deterministic `SkillRef` resolution contract and CLI visibility

### `skyforce-symphony` owns

- runtime skill resolution using active registrations
- policy-aware selection behavior during planning and execution

### policy and operator surfaces own

- approval decisions and activation exceptions
- visibility into registration state and activation posture

## Follow-On Work

After this spec, the highest-value next steps are:

1. define `SkillPackage` and `SkillRegistration` schemas in `skyforce-core`
2. add registry ingestion plus three-gate validation pipeline
3. wire `SkillRef` resolution to active registration records
4. expose registration posture in CLI and operator surfaces
5. define scoped migration/deprecation handling for skill-pack versions

## Bottom Line

`morphOS` should treat reusable skills the same way it treats reusable
workflows: as packaged, validated, and registered assets.

The v0 boundary is simple and sufficient:

- package gives structure
- registration gives governed lifecycle
- `SkillRef` gives runtime linkage

That creates a real packaging and registration boundary for skills now, while
explicitly deferring full trust-and-version governance to later doctrine work.
