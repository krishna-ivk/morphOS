# morphOS v0 Implementation Repo Review

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](MORPHOS_V0_IMPLEMENTATION_BOARD.md) for build order. This document records implementation reality across the local Skyforce repos so roadmap decisions can be grounded in code and test posture rather than doctrine alone.

## Purpose

This review captures the current architectural and testing state of the implementation repos that `morphOS` depends on:

- `skyforce-core`
- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-command-centre`

It is intentionally repo-wise and roadmap-oriented.
It is not a claim that every referenced capability is already product-ready.

## Review Scope

The review was performed against local checkouts under:

- `/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core`
- `/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony`
- `/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness`
- `/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre`

Scope rules:

- review first-party source, scripts, and tests
- exclude vendored dependencies, generated assets, and build output
- record the strongest implemented seams, the sharpest risks, and the practical testing posture

## Executive Read

Current runtime truth:

1. `skyforce-symphony` is the strongest runtime repo today. It already behaves like a credible issue-driven execution host with strong workspace isolation, a real observability layer, and a meaningful test suite.
2. `skyforce-core` contains the cleanest reusable contract assets, but it is architecturally mixed: contracts, monolithic CLI orchestration, and a transitional web surface all live together.
3. `skyforce-harness` is still a script-level prototype. It has a useful envelope-to-artifact seam, but not yet a typed execution subsystem with durable validation guarantees.
4. `skyforce-command-centre` is best understood as an operator-facing aggregation and control-plane prototype. It has useful normalization and approval surfaces, but it is not yet safely governable.

Roadmap consequence:

- the next morphOS roadmap should treat `skyforce-symphony` as the current execution host
- preserve and formalize shared contracts from `skyforce-core`
- treat `skyforce-harness` and `skyforce-command-centre` as active implementation targets, not as stable foundations yet

## Repo Review

### `skyforce-core`

Current posture:

- status: `transitional`
- best fit in the stack: shared contracts plus workspace/operator CLI

Main reviewed source surfaces:

- [packages/contracts/src/index.ts](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/packages/contracts/src/index.ts)
- [scripts/sky.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/scripts/sky.mjs)
- [app/dashboard/page.tsx](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/app/dashboard/page.tsx)
- [app/observability/page.tsx](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/app/observability/page.tsx)
- [app/api/brain/route.ts](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/app/api/brain/route.ts)
- [app/api/observability/tasks/route.ts](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/app/api/observability/tasks/route.ts)
- [lib/linear-bots/server.ts](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/lib/linear-bots/server.ts)

Main reviewed tests/checks:

- [scripts/sky-smoke.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/scripts/sky-smoke.mjs)
- [test/e2e-sync.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/test/e2e-sync.mjs)
- [scripts/harness/run.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/scripts/harness/run.mjs)

Strongest seams:

- shared domain contracts are the cleanest reusable asset
- the `sky` CLI already acts as a practical integration adapter across repos, artifacts, and Symphony state
- `.agent-status` file consumption is simple and consistent across API and UI surfaces

Primary architectural risks:

- server trust boundaries are weak or absent
  - client-only protection in [components/AuthGuard.tsx](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/components/AuthGuard.tsx)
  - unused server auth helper in [lib/auth-guard.ts](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/lib/auth-guard.ts)
  - directly callable LLM proxy in [app/api/brain/route.ts](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/app/api/brain/route.ts)
- product surfaces overstate completeness because several routes are hardcoded or mock-backed
- [scripts/sky.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-core/scripts/sky.mjs) is a large monolith that mixes discovery, validation, formatting, publish flows, and environment diagnosis
- several infrastructure seams appear aspirational rather than actively integrated

Testing posture:

- `npm run lint` passed during review
- `node test/e2e-sync.mjs` passed
- `npm run sky:smoke` failed because expected fixtures and artifacts were missing
- `node scripts/harness/run.mjs --suite quick --dry-run` failed because harness config was absent

Roadmap observations:

- preserve and likely extract `packages/contracts` first
- treat the CLI as valuable product knowledge but refactor material, not long-term architecture
- do not use the current web surface as a roadmap proof of governance or secure operations
- fix the repo’s own validation story before citing it as a stable exemplar

### `skyforce-symphony`

Current posture:

- status: `strong_partial`
- best fit in the stack: runtime execution host and observability layer

Main reviewed source surfaces:

- [elixir/lib/symphony_elixir.ex](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/lib/symphony_elixir.ex)
- [elixir/lib/symphony_elixir/orchestrator.ex](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/lib/symphony_elixir/orchestrator.ex)
- [elixir/lib/symphony_elixir/agent_runner.ex](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/lib/symphony_elixir/agent_runner.ex)
- [elixir/lib/symphony_elixir/workspace.ex](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/lib/symphony_elixir/workspace.ex)
- [elixir/lib/symphony_elixir/workflow_template_store.ex](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/lib/symphony_elixir/workflow_template_store.ex)
- [elixir/lib/symphony_elixir/workflow_template_planner.ex](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/lib/symphony_elixir/workflow_template_planner.ex)
- [elixir/lib/symphony_elixir/workflow_directive_bridge.ex](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/lib/symphony_elixir/workflow_directive_bridge.ex)
- [elixir/lib/symphony_elixir_web/presenter.ex](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/lib/symphony_elixir_web/presenter.ex)

Main reviewed tests:

- [elixir/test/symphony_elixir/core_test.exs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/test/symphony_elixir/core_test.exs)
- [elixir/test/symphony_elixir/app_server_test.exs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/test/symphony_elixir/app_server_test.exs)
- [elixir/test/symphony_elixir/orchestrator_status_test.exs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/test/symphony_elixir/orchestrator_status_test.exs)
- [elixir/test/symphony_elixir/workspace_and_config_test.exs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/test/symphony_elixir/workspace_and_config_test.exs)
- [elixir/test/symphony_elixir/extensions_test.exs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/test/symphony_elixir/extensions_test.exs)
- workflow-template and observability tests under `elixir/test/`

Strongest seams:

- tracker boundary is clean and adapter-based
- workspace isolation is the strongest defended implementation seam in the full stack
- registries and template stores hot-reload filesystem-backed metadata cleanly
- observability is a real architecture layer, not an afterthought

Primary architectural risks:

- [orchestrator.ex](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-symphony/elixir/lib/symphony_elixir/orchestrator.ex) is a large god process and the main future change-risk
- morphOS workflow execution is still heuristic
  - template selection is keyword-based
  - capability routing is keyword-based
  - workflow progress is projection, not durable step state
- approval directives appear observable but not fully executable as a resume/unblock control path
- runtime durability is partial because core running and retry state remains memory-only across restart
- several shell scripts are environment-bound and user-specific

Testing posture:

- `mix test` passed with `223 tests, 0 failures`
- coverage configuration excludes several critical modules, so headline coverage is stronger than the effective critical-path coverage
- gaps remain around shell scripts, restart/recovery semantics, artifact-reader stores, and registry-specific direct tests

Roadmap observations:

- treat Symphony as the current execution host, not yet as the final general morphOS workflow engine
- the missing piece is a durable step executor with explicit transitions, branching, and approval resumes
- highest-value work is to extract routing/state machines from the orchestrator, replace heuristics with declarative matching, and persist runnable state across restarts

### `skyforce-harness`

Current posture:

- status: `prototype`
- best fit in the stack: artifact and receipt adapter, not yet a general execution subsystem

Main reviewed source surfaces:

- [scripts/run.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness/scripts/run.mjs)
- [scripts/consume-execution-envelope.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness/scripts/consume-execution-envelope.mjs)
- [scripts/inspect-execution-envelope.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness/scripts/inspect-execution-envelope.mjs)
- [scripts/pickup-execution-envelopes.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness/scripts/pickup-execution-envelopes.mjs)
- [scripts/inspect-protocol-adapters.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness/scripts/inspect-protocol-adapters.mjs)
- [scripts/emit-heartbeat.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness/scripts/emit-heartbeat.mjs)
- [scripts/validate-config.mjs](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness/scripts/validate-config.mjs)

Main reviewed tests/checks:

- [package.json](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness/package.json) scripts
- [config/suites.json](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-harness/config/suites.json)

Strongest seams:

- envelope-to-artifact conversion is clear and keeps useful workflow metadata
- human-readable envelope inspection is already a useful operator seam
- config-driven execution and adapter inspection are separated cleanly enough for future extraction

Primary architectural risks:

- receipt creation is effectively schema-free and too trusting
- bulk pickup is brittle because it depends on invocation cwd
- deduplication and state are file-existence based only
- there is no shared typed core under `src/`
- the runner still executes shell commands with thin guardrails
- a numeric `0` current step can render incorrectly because `||` is used instead of a nil-safe check

Testing posture:

- `npm run check:ci` passed
- `npm run smoke` passed
- the current checks are still thin and largely config/smoke oriented
- there are no first-party `tests/` fixtures for malformed envelopes, idempotency, heartbeat correctness, or pickup behavior

Roadmap observations:

- record this repo as a script-level prototype
- preserve the current envelope-to-result metadata seam
- extract a typed core before adding more scripts
- add fixture-driven tests around envelope validity, idempotency, path resolution, and step-index rendering

### `skyforce-command-centre`

Current posture:

- status: `prototype`
- best fit in the stack: operator-facing aggregation and control-plane adapter

Main reviewed source surfaces:

- [main.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/main.py)
- [models.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/models.py)
- [frontend/src/App.jsx](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/frontend/src/App.jsx)
- [frontend/src/main.jsx](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/frontend/src/main.jsx)
- [scripts/api_smoke.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/scripts/api_smoke.py)
- [app.js](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/app.js)
- [server.js](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/server.js)
- [websockets.js](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/websockets.js)

Main reviewed tests:

- [tests/test_actions.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/tests/test_actions.py)
- [tests/test_agents.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/tests/test_agents.py)
- [tests/test_context.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/tests/test_context.py)
- [tests/test_main.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/tests/test_main.py)
- [tests/test_mcp.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/tests/test_mcp.py)
- [tests/test_scaling.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/tests/test_scaling.py)
- [tests/test_symphony.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/tests/test_symphony.py)
- [tests/test_ws.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/tests/test_ws.py)

Strongest seams:

- normalization of artifact and runtime state into shared response models is useful and reusable
- directive and approval records can move through the backend end-to-end
- the frontend already presents a coherent operator surface even though the implementation is concentrated

Primary architectural risks:

- mutating backend routes are effectively unauthenticated while CORS is broadly open
- [main.py](/Users/shivakrishnayadav/Projects/morphos-workspace/skyforce-command-centre/main.py) is a large monolith mixing routes, mock state, adapters, file rewrites, and websocket behavior
- the frontend is concentrated in one large component with no typed client layer and no frontend tests
- realtime behavior is narrow and largely mock-backed
- legacy Express and Socket.IO code is still first-party source, which keeps the runtime boundary ambiguous

Testing posture:

- `PYTHONPATH=. .venv/bin/pytest tests` produced `30 passed, 4 failed`
- failures included broken test imports, stale route expectations, and expectation drift
- `scripts/api_smoke.py` passed only when `PYTHONPATH` was set
- `npm run frontend:build` passed
- there are no frontend unit, component, or e2e tests

Roadmap observations:

- treat this repo as an operator UI and state-aggregation adapter, not as the orchestration engine
- prioritize backend modularization, explicit adapter seams, and auth/RBAC before wider operator use
- split the frontend into domain panels and a typed API client before large feature expansion
- repair CI and stale tests before using this repo as a roadmap exemplar

## Cross-Repo Conclusions

These observations should influence the next morphOS roadmap:

1. `skyforce-symphony` is the only repo that currently looks like a durable anchor for the execution host role, but it still needs explicit step execution, durable runnable state, and approval-driven resume behavior.
2. `skyforce-core` should be mined for contracts first, not copied wholesale as an application architecture.
3. `skyforce-harness` should be upgraded from script collection to typed subsystem before morphOS assumes stable receipt and execution guarantees.
4. `skyforce-command-centre` should be treated as an operator-facing adapter that still needs security, modularization, and frontend testing before it can anchor governance-heavy roadmap work.
5. Across repos, the most consistent gap is the difference between observational state and executable state.

## Recommended Roadmap Adjustments

Record these as near-term roadmap realities:

### P0/P1 Reality

- `skyforce-symphony` owns the current believable runtime spine
- `skyforce-core` owns the shared contract extraction path
- `skyforce-harness` is not yet a fully trusted bounded execution engine
- `skyforce-command-centre` is not yet a fully trusted governed control plane

### Immediate Follow-On Work

1. extract and freeze the shared contracts that are already real in `skyforce-core`
2. harden Symphony around explicit step transitions, durable recovery, and approval resumes
3. move Harness to typed envelope and receipt validation plus real fixture-driven tests
4. add auth, modular backend routing, and frontend test coverage in Command Centre
5. align roadmap language so specs stop reading partially implemented surfaces as completed platform layers

## Update Rule

Whenever one of the implementation repos materially changes architecture, control flow, or testing posture, update this review in the same planning wave as the related morphOS roadmap change.
