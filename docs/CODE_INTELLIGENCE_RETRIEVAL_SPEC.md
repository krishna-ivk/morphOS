# Code Intelligence Retrieval Spec

## Why This Spec Exists

`morphOS` already defines:

- a three-layer context architecture
- a filesystem memory topology
- semport and gene-transfusion rules

What is still missing is a concrete retrieval model for code-aware work.

This spec defines that model.

## Executive Summary

Code intelligence retrieval should help agents answer questions like:

- where is this feature implemented?
- what contracts does this module depend on?
- what files likely matter for this bug?
- what symbols, tests, workflows, or configs are related?

It should do that without collapsing:

- source code facts
- runtime state
- long-term memory

into one vague retrieval bucket.

The correct posture is:

- code retrieval is a specialized reference-context capability
- operational state is layered in separately
- persistent memory may guide retrieval, but does not replace code truth

## Core Design Goals

- make code retrieval precise enough for implementation work
- keep retrieval attributable to repo state and source files
- support semantic, structural, and workflow-aware retrieval
- avoid mixing live run state into code facts
- improve agent relevance without hiding provenance

## What Code Intelligence Retrieval Is

Code intelligence retrieval is the system that helps agents locate relevant code artifacts and relationships inside a repo or workspace.

Typical retrieval targets:

- files
- symbols
- modules
- tests
- configs
- workflows
- contracts
- ownership hints

It should answer:

- what is relevant?
- why is it relevant?
- how trustworthy is that relevance?

## What It Is Not

Code intelligence retrieval is not:

- the whole context system
- a substitute for operational context
- a free-form long-term memory store
- an excuse to skip reading the actual code

It should narrow the search space, not replace grounded inspection.

## Retrieval Layers For Code Work

Code retrieval should be treated as a layered capability.

### 1. Structural Retrieval

Use explicit structure from the repo.

Examples:

- file paths
- imports
- symbol definitions
- references
- tests linked to modules
- workflow files linked to targets

### 2. Semantic Retrieval

Use embeddings or semantic matching to find conceptually related code or docs.

Examples:

- “approval routing” matching authority-related code
- “summary rendering” matching CLI and dashboard summary surfaces

### 3. Graph Retrieval

Use relationship edges between artifacts.

Examples:

- symbol -> call site
- module -> tests
- workflow -> runner
- contract -> implementation -> UI surface

### 4. Historical Guidance

Use persistent memory or prior run evidence only to guide likely relevance.

Examples:

- past fixes that touched the same subsystem
- known hot spots for policy issues

This layer should be advisory, not authoritative about current code truth.

## Relationship To The Three Context Layers

### Reference Context

Code retrieval belongs primarily here when it is answering factual questions about the repo state.

Examples:

- which file defines this symbol
- what modules import this contract
- which tests cover this feature

### Operational Context

Operational context may filter or prioritize retrieval based on the current run.

Examples:

- current changed files
- active issue scope
- current failing test
- current workflow phase

### Persistent Memory

Persistent memory may bias retrieval toward historically useful areas.

Examples:

- known fix patterns
- recurring policy hotspots
- subsystem-specific lessons

It must not override current code facts.

## Canonical Retrieval Objects

`morphOS` should support at least these object types:

- `CodeArtifactRef`
- `SymbolRef`
- `CodeRelation`
- `RetrievalQuery`
- `RetrievalResult`
- `RetrievalEvidence`

Suggested meanings:

- `CodeArtifactRef`
  - file, module, config, workflow, or test artifact
- `SymbolRef`
  - function, class, type, module export, command, or workflow step id
- `CodeRelation`
  - structural or inferred link between two artifacts
- `RetrievalQuery`
  - machine-readable retrieval request
- `RetrievalResult`
  - ranked result set
- `RetrievalEvidence`
  - why a result was returned

## Retrieval Query Types

The first useful query families should be:

- `symbol_lookup`
- `semantic_search`
- `call_graph_expansion`
- `test_mapping`
- `contract_implementation_mapping`
- `workflow_mapping`
- `ownership_hint_lookup`
- `change_impact_query`

These cover most real implementation and review needs.

## Retrieval Evidence

Every retrieval result should say why it appeared.

Suggested evidence fields:

- `match_type`
- `source_index`
- `score`
- `relation_path`
- `current_repo_revision`
- `trust_label`

Examples of `match_type`:

- `path_match`
- `symbol_match`
- `semantic_match`
- `graph_match`
- `historical_hint`

Agents should not have to guess why a result was returned.

## Ranking Rules

Retrieval ranking should prefer:

1. exact structural matches
2. directly related graph matches
3. high-confidence semantic matches
4. historical hints

This prevents semantic search from overpowering exact repo facts.

## Retrieval Scopes

Retrieval should support explicit scope boundaries:

- current repo
- current workspace
- allowed sibling repos
- shared contract packages
- workflow templates

Default behavior should be conservative.
Do not let broad multi-repo retrieval happen silently when the task is clearly repo-local.

## Graph Model

The system should eventually support a lightweight code-intelligence graph.

Useful edge types:

- `defines`
- `references`
- `imports`
- `tests`
- `implements`
- `uses_contract`
- `invokes_tool`
- `drives_workflow`
- `renders_state`

This graph does not need to be perfect to be useful.
It only needs to be stable enough to support practical retrieval.

## Retrieval Outputs For Agents

The retrieval system should return:

- top relevant artifacts
- short rationale for each
- relation hints
- suggested next inspection targets

Good retrieval output narrows the investigation path.
It should not dump dozens of weak matches by default.

## Retrieval Outputs For Operators

Operator-facing retrieval is usually secondary.
When surfaced, it should help explain:

- why the system believes certain files or subsystems are involved
- why a suggested owner or reviewer was selected
- how a changed contract relates to downstream surfaces

## Policy And Trust Boundaries

Code retrieval should respect:

- workspace boundaries
- trust labels
- sensitivity labels
- operator-only or local-only restrictions

A powerful retrieval layer without access control becomes a governance leak.

## Freshness And Revision Awareness

Code retrieval must be aware of repo revision.

Minimum expectations:

- results should record the repo revision or snapshot used
- indexes should be refreshable after code changes
- stale indexes should be detectable

If retrieval does not know what revision it reflects, its trust drops sharply.

## Relationship To Parallel Execution

Parallel slices may need different retrieval scopes.

Examples:

- one slice searches contracts only
- one slice searches UI rendering paths
- one slice searches test impact

Slice-aware retrieval helps reduce duplicate exploration and token waste.

## Relationship To Gene Transfusion And Semport

Code intelligence retrieval should help:

- identify exemplar implementations
- map source behavior to target code locations
- discover local translation boundaries

This makes both gene transfusion and semport more grounded.

## Required Artifacts

The retrieval layer should emit durable or inspectable artifacts when needed.

Suggested baseline:

- `retrieval/query.json`
- `retrieval/results.json`
- `retrieval/graph_refs.json`
- `retrieval/evidence.json`

These can remain ephemeral for routine use, but they are valuable for:

- review
- debugging retrieval quality
- agent handoff packets

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define retrieval query, result, and evidence contracts
- future context or retrieval subsystem should build indexes and graph projections
- `skyforce-symphony` should request retrieval in a scope-aware way
- `skyforce-command-centre` may expose retrieval rationale where operator trust benefits

## Recommended First Implementation Slice

The first useful slice should be narrow and practical:

1. support `symbol_lookup`, `semantic_search`, and `contract_implementation_mapping`
2. return file paths, symbol refs, and short relevance reasons
3. record repo revision in every result set
4. keep retrieval repo-local by default
5. add optional graph edges for tests and contracts

That is enough to improve implementation quality without overbuilding a full code graph platform.

## Recommended Next Specs

This spec should be followed by:

1. `TOKEN_AND_COMMAND_MEDIATION_SPEC.md`
2. `DIGITAL_TWIN_UNIVERSE_ROLLOUT_SPEC.md`
3. `REVIEW_LOOP_AUTOMATION_SPEC.md`

Together, those continue the remaining efficiency, twin-expansion, and review-automation work.
