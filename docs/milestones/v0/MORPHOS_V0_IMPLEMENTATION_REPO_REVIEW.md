# morphOS v0 Implementation Repo Review

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](MORPHOS_V0_IMPLEMENTATION_BOARD.md) for build order. This document records implementation reality across the local Skyforce repos so roadmap decisions can be grounded in code and test posture rather than doctrine alone.

## Purpose

This review captures the current architectural and testing state of the implementation repos that `morphOS` depends on:

- `skyforce-core`
- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-command-centre-live`

It is intentionally repo-wise and roadmap-oriented.
It is not a claim that every referenced capability is already product-ready.

## Review Scope

The review was performed against local checkouts under:

- `/Users/shivakrishnayadav/conductor/repos/skyforce-core`
- `/Users/shivakrishnayadav/conductor/repos/skyforce-symphony`
- `/Users/shivakrishnayadav/conductor/repos/skyforce-harness`
- `/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live`

Scope rules:

- review first-party source, scripts, and tests
- exclude vendored dependencies, generated assets, and build output
- record the strongest implemented seams, the sharpest risks, and the practical testing posture

## Executive Read

Current runtime truth:

1. `skyforce-symphony` is the strongest runtime repo today. It already behaves like a credible issue-driven execution host with strong workspace isolation, a real observability layer, and a meaningful test suite.
2. `skyforce-core` contains the cleanest reusable contract assets, but it is architecturally mixed: contracts, monolithic CLI orchestration, and a transitional web surface all live together.
3. `skyforce-harness` is still a script-level prototype. It has a useful envelope-to-artifact seam, but not yet a typed execution subsystem with durable validation guarantees.
4. `skyforce-command-centre-live` is best understood as a LiveView operator surface layered on top of an existing backend API. It is cleaner than the older prototype control plane, but it is still an adapter rather than an autonomous governance runtime.

Roadmap consequence:

- the next morphOS roadmap should treat `skyforce-symphony` as the current execution host
- preserve and formalize shared contracts from `skyforce-core`
- treat `skyforce-harness` and `skyforce-command-centre-live` as active implementation targets, not as stable foundations yet

## Repo Review

### `skyforce-core`

Current posture:

- status: `transitional`
- best fit in the stack: shared contracts plus workspace/operator CLI

Main reviewed source surfaces:

- [packages/contracts/src/index.ts](/Users/shivakrishnayadav/conductor/repos/skyforce-core/packages/contracts/src/index.ts)
- [scripts/sky.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-core/scripts/sky.mjs)
- [app/dashboard/page.tsx](/Users/shivakrishnayadav/conductor/repos/skyforce-core/app/dashboard/page.tsx)
- [app/observability/page.tsx](/Users/shivakrishnayadav/conductor/repos/skyforce-core/app/observability/page.tsx)
- [app/page.tsx](/Users/shivakrishnayadav/conductor/repos/skyforce-core/app/page.tsx)
- [lib/linear-bots/server.ts](/Users/shivakrishnayadav/conductor/repos/skyforce-core/lib/linear-bots/server.ts)

Main reviewed tests/checks:

- [scripts/sky-smoke.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-core/scripts/sky-smoke.mjs)
- [test/e2e-sync.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-core/test/e2e-sync.mjs)
- [scripts/harness/run.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-core/scripts/harness/run.mjs)

Strongest seams:

- shared domain contracts are the cleanest reusable asset
- the `sky` CLI already acts as a practical integration adapter across repos, artifacts, and Symphony state
- `.agent-status` file consumption is simple and consistent across API and UI surfaces

Primary architectural risks:

- server trust boundaries are weak or absent
  - client-only protection in [components/AuthGuard.tsx](/Users/shivakrishnayadav/conductor/repos/skyforce-core/components/AuthGuard.tsx)
  - unused server auth helper in [lib/auth-guard.ts](/Users/shivakrishnayadav/conductor/repos/skyforce-core/lib/auth-guard.ts)
  - directly callable LLM proxy in [app/api/brain/route.ts](/Users/shivakrishnayadav/conductor/repos/skyforce-core/app/api/brain/route.ts)
- product surfaces still overstate completeness because several routes are hardcoded or mock-backed
- [scripts/sky.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-core/scripts/sky.mjs) is a large monolith that mixes discovery, validation, formatting, publish flows, and environment diagnosis
- several infrastructure seams appear aspirational rather than actively integrated

Testing posture:

- `npm run lint` could not be executed here because `next` is not installed in this environment
- `node test/e2e-sync.mjs` was not executed in this pass
- `npm run sky:smoke` was not executed in this pass
- `node scripts/harness/run.mjs --suite quick --dry-run` was not executed in this pass
- roadmap guidance for this repo is therefore based on source inspection plus the currently checked-in test entrypoints, not on a clean local green run

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

- [elixir/lib/symphony_elixir.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir.ex)
- [elixir/lib/symphony_elixir/orchestrator.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir/orchestrator.ex)
- [elixir/lib/symphony_elixir/agent_runner.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir/agent_runner.ex)
- [elixir/lib/symphony_elixir/workspace.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir/workspace.ex)
- [elixir/lib/symphony_elixir/work_order.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir/work_order.ex)
- [elixir/lib/symphony_elixir/workflow_template_store.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir/workflow_template_store.ex)
- [elixir/lib/symphony_elixir/workflow_template_planner.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir/workflow_template_planner.ex)
- [elixir/lib/symphony_elixir/workflow_directive_bridge.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir/workflow_directive_bridge.ex)
- [elixir/lib/symphony_elixir_web/presenter.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir_web/presenter.ex)

Main reviewed tests:

- [elixir/test/symphony_elixir/core_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/test/symphony_elixir/core_test.exs)
- [elixir/test/symphony_elixir/app_server_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/test/symphony_elixir/app_server_test.exs)
- [elixir/test/symphony_elixir/orchestrator_status_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/test/symphony_elixir/orchestrator_status_test.exs)
- [elixir/test/symphony_elixir/workspace_and_config_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/test/symphony_elixir/workspace_and_config_test.exs)
- [elixir/test/symphony_elixir/extensions_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/test/symphony_elixir/extensions_test.exs)
- [elixir/test/work_order_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/test/work_order_test.exs)
- [elixir/test/work_order_cli_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/test/work_order_cli_test.exs)
- workflow-template and observability tests under `elixir/test/`

Strongest seams:

- tracker boundary is clean and adapter-based
- workspace isolation is the strongest defended implementation seam in the full stack
- registries and template stores hot-reload filesystem-backed metadata cleanly
- observability is a real architecture layer, not an afterthought

Primary architectural risks:

- [orchestrator.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-symphony/elixir/lib/symphony_elixir/orchestrator.ex) is a large god process and the main future change-risk
- morphOS workflow execution is still heuristic
  - template selection is keyword-based
  - capability routing is keyword-based
  - workflow progress is projection, not durable step state
- approval directives appear observable but not fully executable as a resume/unblock control path
- runtime durability is partial because core running and retry state remains memory-only across restart
- several shell scripts are environment-bound and user-specific

Testing posture:

- `mix test` could not be executed here because `mix` is not installed in this environment
- the checked-in suite is still meaningfully broad by inspection, but the current pass cannot claim a local green run
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

- [scripts/run.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/run.mjs)
- [scripts/consume-execution-envelope.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/consume-execution-envelope.mjs)
- [scripts/inspect-execution-envelope.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/inspect-execution-envelope.mjs)
- [scripts/pickup-execution-envelopes.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/pickup-execution-envelopes.mjs)
- [scripts/build-approval-packet.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/build-approval-packet.mjs)
- [scripts/post-approval-packet.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/post-approval-packet.mjs)
- [scripts/resolve-approval-packet.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/resolve-approval-packet.mjs)
- [scripts/emit-envelope-from-symphony-work-order.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/emit-envelope-from-symphony-work-order.mjs)
- [scripts/run-p0-factory-spine.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/run-p0-factory-spine.mjs)
- [scripts/inspect-protocol-adapters.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/inspect-protocol-adapters.mjs)
- [scripts/emit-heartbeat.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/emit-heartbeat.mjs)
- [scripts/validate-config.mjs](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/scripts/validate-config.mjs)

Main reviewed tests/checks:

- [package.json](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/package.json) scripts
- [config/suites.json](/Users/shivakrishnayadav/conductor/repos/skyforce-harness/config/suites.json)

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
- the repo now has a meaningful set of first-party script-level test entrypoints for approvals, sync updates, run bundles, mock envelope emission, and the P0 factory spine
- despite that improvement, testing is still script-driven rather than module-driven, and there is still no shared typed `src/` layer under test

Roadmap observations:

- record this repo as a script-level prototype
- preserve the current envelope-to-result metadata seam
- extract a typed core before adding more scripts
- keep the growing P0 factory-spine scripts, but move their shared logic under a typed core and add fixture-driven tests around envelope validity, idempotency, path resolution, and step-index rendering

### `skyforce-command-centre-live`

Current posture:

- status: `strong_partial`
- best fit in the stack: operator-facing LiveView surface over an existing backend API

Main reviewed source surfaces:

- [lib/skyforce_command_centre_live/command_centre_api.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live/command_centre_api.ex)
- [lib/skyforce_command_centre_live/dashboard/state.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live/dashboard/state.ex)
- [lib/skyforce_command_centre_live/dashboard/presenter.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live/dashboard/presenter.ex)
- [lib/skyforce_command_centre_live_web/router.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live_web/router.ex)
- [lib/skyforce_command_centre_live_web/operator_auth.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live_web/operator_auth.ex)
- [lib/skyforce_command_centre_live_web/operator_identity_plug.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live_web/operator_identity_plug.ex)
- [lib/skyforce_command_centre_live_web/live/dashboard_live.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live_web/live/dashboard_live.ex)
- [lib/skyforce_command_centre_live_web/live/issue_live.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live_web/live/issue_live.ex)
- [lib/skyforce_command_centre_live_web/live/login_live.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live_web/live/login_live.ex)

Main reviewed tests:

- [test/skyforce_command_centre_live/dashboard/presenter_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/test/skyforce_command_centre_live/dashboard/presenter_test.exs)
- [test/skyforce_command_centre_live/dashboard/state_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/test/skyforce_command_centre_live/dashboard/state_test.exs)
- [test/skyforce_command_centre_live_web/live/dashboard_live_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/test/skyforce_command_centre_live_web/live/dashboard_live_test.exs)
- [test/skyforce_command_centre_live_web/live/issue_live_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/test/skyforce_command_centre_live_web/live/issue_live_test.exs)
- [test/skyforce_command_centre_live_web/live/login_live_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/test/skyforce_command_centre_live_web/live/login_live_test.exs)
- [test/skyforce_command_centre_live_web/controllers/session_controller_test.exs](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/test/skyforce_command_centre_live_web/controllers/session_controller_test.exs)

Strongest seams:

- the repo has a cleaner operator seam than the older prototype because it is explicitly a thin LiveView client over an existing backend API
- session-backed operator auth and route protection are real, not just aspirational
- dashboard state and issue state are cleanly separated into aggregators and presenters instead of one monolith
- the UI is already decomposed into LiveViews and smaller components, which is a much stronger shape than the older single-component frontend

Primary architectural risks:

- this repo is only as trustworthy as the backend it fronts; it does not own the source-of-truth governance model itself
- operator auth is still intentionally minimal, with shared-key or env-backed registry auth in [operator_auth.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live_web/operator_auth.ex)
- query-param session seeding in [operator_identity_plug.ex](/Users/shivakrishnayadav/conductor/repos/skyforce-command-centre-live/lib/skyforce_command_centre_live_web/operator_identity_plug.ex) is pragmatic for demos but not a strong long-term trust boundary
- the backend API client assumes the existing command-centre API contract remains stable; this repo does not yet define its own resilient adapter/versioning layer
- because this repo is primarily a projection layer, it does not close the deeper roadmap gaps around approval execution, audit authority, or promotion semantics by itself

Testing posture:

- `mix test` could not be executed here because `mix` is not installed in this environment
- by source inspection, the repo has meaningful controller, presenter, state, session, and LiveView test coverage
- current verification claims for this repo are therefore based on source and test shape, not on a local green run in this session

Roadmap observations:

- treat this repo as the current operator-facing LiveView shell, not as the core governance engine
- preserve its present strengths: session-backed route protection, clear state/presenter seams, and decomposed LiveView components
- keep roadmap pressure on the backend contracts it depends on, because the safety and authority boundary still lives below this repo
- move next toward stronger operator identity, richer audit semantics, and a more explicit API-versioning seam between the LiveView surface and the underlying command-centre backend

## Cross-Repo Conclusions

These observations should influence the next morphOS roadmap:

1. `skyforce-symphony` is the only repo that currently looks like a durable anchor for the execution host role, but it still needs explicit step execution, durable runnable state, and approval-driven resume behavior.
2. `skyforce-core` should be mined for contracts first, not copied wholesale as an application architecture.
3. `skyforce-harness` should be upgraded from script collection to typed subsystem before morphOS assumes stable receipt and execution guarantees.
4. `skyforce-command-centre-live` should be treated as an operator-facing adapter that still depends on deeper backend governance and execution truth before it can anchor governance-heavy roadmap work.
5. Across repos, the most consistent gap is the difference between observational state and executable state.

## Recommended Roadmap Adjustments

Record these as near-term roadmap realities:

### P0/P1 Reality

- `skyforce-symphony` owns the current believable runtime spine
- `skyforce-core` owns the shared contract extraction path
- `skyforce-harness` is not yet a fully trusted bounded execution engine
- `skyforce-command-centre-live` is not yet a fully trusted governed control plane on its own

### Immediate Follow-On Work

1. extract and freeze the shared contracts that are already real in `skyforce-core`
2. harden Symphony around explicit step transitions, durable recovery, and approval resumes
3. move Harness to typed envelope and receipt validation plus real fixture-driven tests
4. harden the backend authority boundary that Command Centre Live depends on, while preserving the current LiveView decomposition and operator session surfaces
5. align roadmap language so specs stop reading partially implemented surfaces as completed platform layers

## Update Rule

Whenever one of the implementation repos materially changes architecture, control flow, or testing posture, update this review in the same planning wave as the related morphOS roadmap change.
