# Tool Registry And Action Discovery Spec

This document defines how `morphOS` should describe, discover, and govern tool
surfaces.

It is the fourth follow-on specification from the starred repo
gene-transfusion backlog and is primarily informed by:

- `googleworkspace/cli`
- `ComposioHQ/agent-orchestrator`
- the existing `ToolAction` runtime contract
- the morphOS agent and action model

The goal is to make tool use:

- explicit
- discoverable
- policy-aware
- agent-friendly
- machine-readable

without turning the platform into an unbounded pile of shell commands and MCP
surfaces.

## Why This Spec Exists

The current morphOS docs already acknowledge `ToolAction` as a core shared
runtime contract.

What is still under-specified is:

- how tools are registered
- how agents discover which tools exist
- how tools map to actions
- how risky tools are gated
- how results should be projected back into runtime state

Without that layer:

- agents either get too many tools or too few
- tool use becomes prompt-level convention instead of system behavior
- policy enforcement happens too late
- operator visibility into actions stays weak
- tool integrations drift across repos

This spec exists to prevent that.

## Executive Summary

The correct model is:

- `ToolRegistry`
  - the canonical catalog of tools available to the system
- `ToolDescriptor`
  - the metadata that describes one tool surface
- `ToolAction`
  - the invocation contract for one proposed or executed tool use
- `ActionToToolMapping`
  - the allowed relationship between semantic agent actions and concrete tools

The key rule is:

- agents perform semantic actions
- tools perform concrete side effects
- the registry decides what tools exist
- policy decides whether a tool action is allowed

## Core Objects

## 1. Tool Registry

### Meaning

The `ToolRegistry` is the canonical index of tools the runtime knows how to
offer.

It is not just a list of binaries.
It is the governed catalog of action surfaces available to the platform.

### Responsibilities

- list available tools
- expose capabilities and permissions
- describe risk posture
- define invocation shape
- support filtering by archetype, environment, and policy

## 2. Tool Descriptor

### Meaning

A `ToolDescriptor` is the durable metadata for one tool.

Examples:

- filesystem read tool
- patch application tool
- git branch creation tool
- PR creation tool
- Linear comment tool
- Google Workspace API tool

### Minimum Fields

- `tool_id`
- `name`
- `provider_kind`
- `action_family`
- `description`
- `input_schema_ref`
- `output_schema_ref`
- `required_permissions`
- `risk_level`
- `connectivity_requirement`
- `availability_scope`
- `supported_agent_roles`
- `result_projection_kind`
- `version`

## 3. ToolAction

### Meaning

A `ToolAction` is a proposed or executed use of a tool.

This is the runtime contract that turns:

- agent intent
- tool selection
- policy
- execution evidence

into a traceable action.

### Rule

`ToolAction` is not the same thing as a semantic action.

Example:

- semantic action: `implement_task`
- tool actions inside it:
  - read file
  - apply patch
  - run tests

## 4. Action To Tool Mapping

### Meaning

This is the controlled mapping from semantic actions to permitted concrete
tools.

It answers:

- what tools may a planner use?
- what tools may a coding agent use?
- which tools require approval?
- which tools are read-only?

Without this mapping, tool access becomes vague and role boundaries blur.

## Discovery Model

Tool discovery should happen in three layers.

## Layer 1: Registry Discovery

The runtime should be able to answer:

- what tools exist?
- what do they do?
- what schemas do they use?
- what permissions do they require?

This is the broad catalog view.

## Layer 2: Role-Filtered Discovery

The runtime should be able to answer:

- which of those tools should this agent role even see?

Example:

- planning agents should not see deployment tools by default
- validation agents should not see arbitrary write tools
- communication agents should not see source mutation tools

## Layer 3: Contextual Discovery

The runtime should be able to answer:

- given this run, workspace, connectivity posture, and policy snapshot, which
  of those role-allowed tools are currently usable?

Example filters:

- offline vs connected
- local-only workspace
- approval pending
- workspace policy restrictions

## Registry Layout

Recommended v0 filesystem shape:

```text
tools/
  registry/
    tools/
      <tool_id>.json
    action-mappings/
      <agent_role>.json
    providers/
      <provider_id>.json
    indexes/
      by_role.json
      by_risk.json
      by_provider.json
      by_connectivity.json
```

## Provider Kinds

The registry should support at least these provider kinds:

- `local_program`
- `shell_script`
- `mcp_server`
- `http_api`
- `cli_wrapper`
- `sdk_adapter`

### Why this matters

The runtime should care about invocation and policy semantics, not just whether
something happens to be implemented as a binary or API call.

## Action Families

Tools should be grouped into stable action families.

Recommended initial families:

- `filesystem.read`
- `filesystem.write`
- `code.patch`
- `git.read`
- `git.write`
- `validation.run`
- `artifact.publish`
- `issue.update`
- `communication.send`
- `external.api`
- `deployment.execute`

### Design Rule

Families should describe the type of side effect or capability, not the brand
name of the provider.

Prefer:

- `issue.update`

Avoid:

- `linear_tool`

## Risk Levels

Every tool should have an explicit risk level:

- `low`
- `medium`
- `high`
- `critical`

### Example

- read local file: `low`
- apply patch in workspace: `medium`
- create PR or merge branch: `high`
- production deploy or external write with blast radius: `critical`

## Connectivity Requirement

Every tool should declare a minimum connectivity posture:

- `offline`
- `online_read`
- `online_write`
- `deploy_enabled`

This must align with the connectivity model already used by morphOS.

## Availability Scope

Every tool should declare where it is meant to run:

- `local`
- `workspace`
- `node`
- `global`

### Why this matters

Some tools are safe only in a local workspace.
Some are tied to a node or provider identity.
Some operate across the whole platform.

## Result Projection Kinds

Every tool should declare how its result should be projected back into the
system.

Recommended initial values:

- `none`
- `artifact_ref`
- `state_patch`
- `receipt`
- `event_only`

### Examples

- running tests -> `receipt`
- reading a file -> `artifact_ref` or `none`
- publishing a summary -> `artifact_ref`
- posting a comment -> `receipt`

## Approval Model

Tool execution must support approval-aware gating.

The runtime should be able to answer:

- does this tool action require approval?
- who must approve it?
- is approval scoped to workspace or global authority?

### Rule

Approval should be driven by policy and tool risk posture, not by prompt
wording.

## Operator Visibility

Operators should be able to inspect:

- what tool was requested
- why it was selected
- what policy posture applied
- whether it was blocked or allowed
- what artifact or receipt resulted

This is one reason the registry must stay explicit and structured.

## Agent Experience

Agents should not experience tools as one giant undifferentiated menu.

They should experience:

- a role-appropriate tool surface
- clear tool descriptions
- predictable input and output shapes
- explicit blocked vs allowed feedback

## Relationship To Skills

Skills and tools are related but not identical.

### Skill

- reusable capability or behavior package

### Tool

- concrete execution surface

### Rule

Skills may recommend or compose tools.
The registry still owns tool truth.

## Relationship To The Agent Model

This spec builds directly on `AGENT_SIGNAL_AND_ACTION_MODEL.md`.

Mapping:

- agent performs semantic action
- action may select or request tool actions
- tool registry determines discoverable tools
- policy gates the requested tool action
- tool execution returns machine-readable results

## Relationship To Shared Contracts

This spec should later harden:

- `ToolAction`
- `ArtifactRef`
- `Directive`
- `ApprovalDecision`

It does not replace those contracts.
It explains how tools should be registered and discovered before invocation.

## Ownership

### `morphOS` owns

- tool registry doctrine
- action family semantics
- discovery and filtering rules

### `skyforce-core` owns

- shared registry contracts
- schema definitions
- CLI discovery helpers

### future tool engine owns

- actual invocation runtime
- provider adapters
- result projection plumbing

### `skyforce-symphony` owns

- mapping semantic actions to requested tool actions
- routing tool requests through policy and execution boundaries

### `skyforce-command-centre-live` observes

- operator-visible tool actions and approvals

### `skyforce-api-gateway` owns

- operator-facing tool action normalization for HTTP clients

## What To Build After This Spec

Once this model is accepted, the next useful follow-on specs are:

1. `SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md`
2. `WORKFLOW_PACK_AND_REGISTRY_SPEC.md`
3. `VALIDATION_GUARDRAILS_AND_REVIEW_LOOP_SPEC.md`

## Bottom Line

The correct morphOS tool layer is:

- registry-driven
- role-filtered
- context-filtered
- policy-aware
- machine-readable

It should make tool usage explicit enough that agents, operators, and the
runtime all agree on what concrete action is being requested and why.
