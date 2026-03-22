# Workflow Pack And Registry Spec

This document defines how `morphOS` should package, version, validate, and
register reusable workflows.

It is the sixth follow-on specification from the starred repo
gene-transfusion backlog and is primarily informed by:

- `nikilster/clawflows`
- the existing `morphOS/workflows/*.yaml` assets
- the software-factory control flow spec
- the agent and tool models already defined in morphOS

The goal is to turn workflows from “files we happen to load” into a governed
delivery asset that can be:

- reused
- versioned
- validated
- selected safely
- shared across repos and workspaces

## Why This Spec Exists

The current repo already has useful workflows like:

- `feature_pipeline`
- `release_pipeline`
- `repo_evaluation`
- `incident_triage`

That is a strong start.

What is still under-specified is:

- what makes a workflow a reusable pack
- how workflow metadata is declared
- how compatibility is expressed
- how a runtime chooses among available workflows
- how local and imported workflow packs should coexist

Without that structure:

- workflows stay too repo-local
- reuse depends on people remembering filenames
- compatibility drift grows quietly
- imported workflows become hard to trust
- workflow selection logic stays ad hoc

This spec exists to solve that.

## Executive Summary

The correct model is:

- `WorkflowTemplate`
  - one workflow definition with steps and contracts
- `WorkflowPack`
  - a versioned bundle of one or more related workflow templates plus metadata
- `WorkflowRegistry`
  - the catalog of available packs and templates visible to the runtime

The key rule is:

- templates define execution shape
- packs define distribution and versioning
- the registry defines discoverability and selection

## Core Objects

## 1. Workflow Template

### Meaning

A `WorkflowTemplate` is a concrete workflow definition the runtime can execute
or interpret.

Examples:

- feature delivery workflow
- release workflow
- repo evaluation workflow
- incident triage workflow

### Current examples

- `morphOS/workflows/feature_pipeline.yaml`
- `morphOS/workflows/release_pipeline.yaml`
- `morphOS/workflows/repo_evaluation.yaml`

## 2. Workflow Pack

### Meaning

A `WorkflowPack` is a versioned bundle of related workflow templates plus the
metadata needed to reuse them safely.

Examples:

- software-factory core pack
- observability pack
- release-management pack
- job-ops pack

### Why packs matter

Packs let the system reason about:

- provenance
- compatibility
- version evolution
- intended use cases

instead of treating every workflow file as an isolated artifact.

## 3. Workflow Registry

### Meaning

The `WorkflowRegistry` is the discoverable catalog of installed or available
workflow packs and templates.

It answers:

- what workflows exist?
- which pack did this workflow come from?
- which version is installed?
- what kind of work is this workflow for?
- is this template compatible with the current runtime?

## Workflow Pack Layout

Recommended v0 pack layout:

```text
workflow-packs/
  <pack_id>/
    pack.json
    templates/
      <template_id>.yaml
    docs/
      README.md
    schemas/
    tests/
```

### `pack.json`

This should define the pack metadata.

Minimum fields:

- `pack_id`
- `name`
- `version`
- `description`
- `owner`
- `source`
- `compatibility`
- `templates`
- `default_selection_tags`
- `trust_label`

## Workflow Template Metadata

Each workflow template should declare at least:

- `template_id`
- `name`
- `version`
- `purpose`
- `entry_conditions`
- `supported_execution_modes`
- `required_capabilities`
- `supported_step_types`
- `selection_tags`
- `steps`

### Why this matters

The runtime should not infer everything from the file name or step list.

## Pack Compatibility

Every workflow pack should declare compatibility with:

- runtime version range
- supported step types
- required agent roles
- required tool families
- required connectivity capabilities

### Rule

If a pack needs runtime features the local stack does not support, it should be
visible as incompatible rather than silently loaded.

## Registry Layout

Recommended v0 registry shape:

```text
workflows/
  registry/
    packs/
      <pack_id>.json
    templates/
      <template_id>.json
    indexes/
      by_tag.json
      by_pack.json
      by_execution_mode.json
      by_trust_label.json
      by_runtime_support.json
```

## Selection Model

Workflow selection should happen in three layers.

## Layer 1: Eligibility

The runtime should filter workflows based on:

- task kind
- execution mode
- connectivity posture
- required capabilities
- runtime compatibility

## Layer 2: Relevance

Among eligible templates, the runtime should rank by:

- selection tags
- repo or workspace context
- prior success for similar tasks
- operator preference when available

## Layer 3: Authority

The runtime should decide whether:

- a workflow may be auto-selected
- a workflow requires human confirmation
- a workflow is only suggestible, not auto-runnable

## Selection Tags

Templates should support stable selection tags such as:

- `feature_delivery`
- `release`
- `repo_analysis`
- `incident_response`
- `validation_repair`
- `low_risk`
- `approval_gated`
- `offline_capable`

### Rule

Tags should describe behavior and suitability, not team-internal nicknames.

## Trust Labels

Workflow packs and templates should carry trust labels:

- `core`
- `curated`
- `experimental`
- `imported`

### Why

The runtime should distinguish:

- first-party trusted workflows
- curated shared workflows
- experimental packs
- imported community packs

## Pack Installation Modes

The registry should support at least these modes:

- `builtin`
- `workspace_installed`
- `shared_installed`
- `suggested_only`

### Meaning

- `builtin`
  - ships with the platform
- `workspace_installed`
  - installed for one workspace
- `shared_installed`
  - available across multiple workspaces
- `suggested_only`
  - visible for recommendation but not yet enabled

## Validation Rules

Every workflow pack should pass three validation layers.

## 1. Structural validation

Checks:

- metadata fields exist
- template ids are unique
- step ids are unique
- step references are well formed

## 2. Capability validation

Checks:

- required step types are supported
- required agents exist or are mappable
- required tool families are known
- connectivity requirements are valid

## 3. Policy validation

Checks:

- no forbidden step types are introduced
- required approval gates are present where policy demands them
- risky templates are labeled appropriately

## Runtime Support Model

A template may be:

- `supported`
- `partially_supported`
- `unsupported`

### Rule

Partially supported workflows may still be visible, but they should not be
auto-selected without an explicit compatibility warning.

## Relationship To Existing Workflow Files

The current `morphOS/workflows/*.yaml` files should be treated as the first
template set for the first core pack.

Recommended v0 interpretation:

- existing workflow files become templates
- a core pack wraps them with metadata and versioning
- the registry indexes them explicitly

That means the current files are preserved, but the surrounding governance
becomes stronger.

## Relationship To Control Flow

Workflow packs define execution shapes.
They do not replace the factory control states.

Mapping:

- control flow defines the delivery phases
- workflow templates define the step graph used within those phases

## Relationship To Agents And Tools

Workflow templates should declare:

- required agent roles
- allowed step types
- required tool families

They should not hardcode unstable implementation details where local mapping is
better handled by the runtime.

Prefer:

- `required_capabilities: ["validation.run"]`

Avoid:

- “must use exact shell script X” unless the behavior truly depends on it

## Relationship To Gene Transfusion

Workflow packs are the natural packaging unit for reusable behavior transfer.

That means gene transfusion should often produce:

- a new or revised workflow pack
- a new template version
- a new compatibility note

rather than only a prose note in a document.

## Ownership

### `morphOS` owns

- workflow-pack doctrine
- template metadata semantics
- trust-label semantics for packs

### `skyforce-core` owns

- shared pack and template contracts
- registry indexes
- CLI visibility

### `skyforce-symphony` owns

- runtime selection and execution of installed templates
- compatibility checks during load

### `skyforce-command-centre` observes

- available templates
- selected template
- compatibility and trust posture

## What To Build After This Spec

Once this model is accepted, the next useful follow-on specs are:

1. `VALIDATION_GUARDRAILS_AND_REVIEW_LOOP_SPEC.md`
2. `DIGITAL_TWIN_VALIDATION_SPEC.md`
3. `SKILL_PACKAGING_AND_ATTACHMENT_SPEC.md`

## Bottom Line

The correct morphOS workflow model is:

- templates for execution shape
- packs for versioned reuse
- a registry for discovery and selection

That turns workflows from a folder of YAML files into a governed runtime asset.
