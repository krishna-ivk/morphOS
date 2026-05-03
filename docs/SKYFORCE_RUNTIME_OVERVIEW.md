# Skyforce Runtime Overview

This document explains Skyforce from the `morphOS` point of view.

If `morphOS` is the operating-model and specification authority, Skyforce is the executable runtime stack that turns those definitions into live behavior.

## Purpose

Skyforce exists to run the system that `morphOS` describes.

It is the practical implementation layer for:

- orchestration
- execution
- contracts
- observability
- approvals
- validation

## Repo Roles

### skyforce-symphony

The orchestration runtime.

Responsibilities:

- workflow execution
- task routing
- node and agent selection
- retries and state tracking
- observability payloads
- execution envelope generation

### skyforce-harness

The execution runtime.

Responsibilities:

- node-local execution
- protocol adapters
- A2A and MCP integration surfaces
- execution receipt generation
- artifact production

### skyforce-api-gateway

The backend adapter and operator-facing API normalization layer.

Responsibilities:

- operator-facing HTTP endpoint shape
- backend proxying and normalization
- action proxy semantics
- compatibility handling for runtime protocol differences

### skyforce-command-centre-live

The primary operator UI.

Responsibilities:

- dashboard and issue-page rendering
- approvals and intervention UX
- fleet health visibility
- validation, execution, and summary-sync presentation
- operator triage and next-step guidance

### skyforce-command-centre

The transitional compatibility UI.

Responsibilities:

- React-based operator surface during migration
- temporary compatibility behavior while LiveView and the gateway take over

### skyforce-core

The shared foundation layer.

Responsibilities:

- contracts used in code
- CLI
- validation manifests
- shared runtime-facing models

## Why Skyforce Matters

`morphOS` is strongest at describing how the system should work.

Skyforce is strongest at:

- actually routing work
- tracking state
- validating outcomes
- exposing operator surfaces
- integrating with the real devices and services you use

## Current Runtime Strengths

Skyforce already has working capability in:

- multi-agent routing
- node-aware routing
- protocol-aware routing
- execution envelopes
- execution receipts
- validation summaries
- CLI inspection flows
- dashboard visibility

The operator layer is now intentionally split:

- `skyforce-api-gateway` for backend operator APIs
- `skyforce-command-centre-live` for the long-term UI
- `skyforce-command-centre` only as a migration-era compatibility surface

## Current Runtime Gaps

Skyforce still needs stronger alignment with `morphOS` in:

- workflow template semantics
- event taxonomy
- policy engine unification
- connectivity mode implementation
- archetype-driven agent registration
- learning and memory integration

## Recommended Relationship

The clean long-term relationship is:

- `morphOS` defines the system
- Skyforce executes the system

That means:

- no second orchestrator in `morphOS`
- no second event bus runtime in `morphOS`
- no duplicate contracts drifting in two places

## Bottom Line

Skyforce is the executable body.

`morphOS` is the model of the organism.

The platform becomes coherent when those two stay separate but aligned.
