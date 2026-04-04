# Documentation Guide

Use this folder as the main entry point for SkyForce specifications.

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](milestones/v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md) when you need the authoritative cross-repo build order.

## Sections

- `agents/` - role definitions for specialized agent cells
- `vision/` - product vision and problem framing inputs
- `human_roles/` - human collaborators, responsibilities, and escalation paths
- `architecture/`, `core-mechanics/`, `doctrines/`, `workflows/`, and `milestones/` - organized system specifications and planning docs

## Start Here

- `architecture/agentic_os_architecture.md` - overall operating system design
- `milestones/v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md` - canonical prioritized build board
- `milestones/v1/MORPHOS_V1_RELEASE_TARGET.md` - release-definition document for aiming the current `v0` work toward a real `v1.0` launch
- `milestones/v1/MORPHOS_SPEC_BASELINE.md` - current spec baseline and grounded production-readiness judgment for the active stack
- `milestones/v1/MORPHOS_RELEASE_READINESS_CHECKLIST.md` - operational release checklist with repo-by-repo completion estimates and the current critical path
- repo-owned `v1.0` implementation requirements now live in each runtime repo as `MORPHOS_V1_REQUIREMENTS.md` so execution details stay close to owning code
- `milestones/v0/MORPHOS_V0_IMPLEMENTATION_REPO_REVIEW.md` - repo-wise architectural and testing reality check across the active Skyforce implementation repos
- `milestones/P1/P1_IMPLEMENTATION_STATUS.md` - practical bridge between `P1` doctrine and what is actually implemented in code right now
- `examples/P0_GOLDEN_PATH_WORK_ORDER.json` - canonical sample work-order packet for the first factory-spine proving run

## Runtime-Critical

These are the most important documents when the goal is to keep implementation and
operator behavior aligned to the real factory spine.

- `milestones/P0/P0_FACTORY_SPINE_RECOVERY_PLAN.md` - recovery posture for proving the first real end-to-end factory transaction before expanding doctrine again
- `milestones/P0/P0_FACTORY_SPINE_IMPLEMENTATION_CHECKLIST.md` - concrete cross-repo build order for the first intake-to-approval transaction
- `skyforce-harness` `npm run release-gate:p0` - current single-command release gate for proving the P0 spine twice with bounded retry/second-run coverage
- `milestones/P0/P0_GOLDEN_PATH_SEED_PACKET.md` - narrow golden-path seed used to prove Symphony, Harness, and Command Centre integration
- `milestones/v0/MORPHOS_V0_IMPLEMENTATION_REPO_REVIEW.md` - implementation-repo review that records which stack layers are currently strong, transitional, or still prototype-grade
- `core-mechanics/WORK_ORDER_SCHEMA_SPEC.md` - normalized intake contract
- `core-mechanics/EXECUTION_RECEIPT_SCHEMA_SPEC.md` - execution proof contract
- `core-mechanics/APPROVAL_PACKET_SCHEMA_SPEC.md` - approval artifact contract
- `core-mechanics/PYRAMID_SUMMARY_RENDERING_SPEC.md` - shared summary model for operator and approval surfaces
- `core-mechanics/POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md` - named runtime policy gates
- `architecture/AGENT_ARCHETYPES_SPEC.md` - core MVP archetype contract

## P0 Proven Spine

These docs describe the currently prioritized proving path and its immediately
adjacent governance model.

- `milestones/P0/P0_DURABLE_LIFECYCLE_SPEC.md`
- `milestones/P0/P0_END_TO_END_DELIVERY_SPINE_SPEC.md`
- `milestones/P0/P0_INTERACTIVE_VS_FACTORY_MODE_SPEC.md`
- `milestones/P0/P0_PROGRAM_AND_APPROVAL_EXECUTION_SPEC.md`
- `milestones/P0/P0_SUPER_ADMIN_MODEL_SPEC.md`
- `milestones/P0/P0_WORKSPACE_ADMIN_MODEL_SPEC.md`

## P1 In Flight

These are the next-layer specs that should be read as `post-P0` runtime shaping
documents, not as claims that every behavior is already fully implemented.

- `milestones/P1/P1_IMPLEMENTATION_STATUS.md`
- `milestones/P1/P1_EVENT_TAXONOMY_SPEC.md`
- `milestones/P1/P1_POLICY_HOOKS_SPEC.md`
- `milestones/P1/P1_SAFE_PROMOTION_SPEC.md`
- `milestones/P1/P1_SUMMARY_PYRAMID_SPEC.md`
- `milestones/P1/P1_OPERATOR_LOGIN_SURFACE_SPEC.md`
- `milestones/P1/P1_UNIVERSAL_TERMINOLOGY_SPEC.md`

## Canonical Examples

Use `docs/examples/` for stable reference packets, not for operator scratch output
or ad hoc runtime experiments.

- `examples/P0_GOLDEN_PATH_WORK_ORDER.json` - canonical `P0` work order

## Long-Horizon Doctrine

The doctrine stack is still useful, but it should be read after the spine and
runtime-critical specs, not before them.

- `doctrines/` - long-horizon portfolio doctrine, freeze, maturity, scorecard, and governance documents

## Broader Catalog

The remaining lists below provide the fuller catalog of architecture, workflow,
handoff, and doctrine materials.

- `milestones/v0/MORPHOS_V0_MULTI_AGENT_IMPLEMENTATION_PLAN.md` - cross-repo parallel execution plan with dependencies, lineage, and exclusivity rules
- `milestones/v0/MORPHOS_V0_AGENT_DISPATCH_PACKETS.md` - ready-to-assign packets and dependency matrix for parallel agent execution
- `milestones/v0/MORPHOS_V0_MULTI_AGENT_STATUS_BOARD.md` - live ownership, gate, and handoff board for running parallel agents
- `contract_freeze_notes.md` - Wave 1 Agent A freeze artifact for execution mode, authority, events, summaries, and promotion
- `orchestration_state_handoff.md` - Wave 1 Agent B handoff artifact for Symphony runtime payload and approval-state alignment
- `runner_receipt_examples.md` - Wave 1 Agent C handoff artifact for Harness receipt and evidence alignment
- `operator_surface_wording_map.md` - Wave 1 Agent D inventory artifact for command-centre and CLI terminology rollout
- `milestones/v0/MORPHOS_V0_WAVE1_LAUNCH_KIT.md` - exact first-wave launch order and copy-paste prompts for agent startup
- `milestones/v0/MORPHOS_V0_WAVE2_LAUNCH_KIT.md` - governance and operator rollout launch kit for the second wave
- `milestones/v0/MORPHOS_V0_WAVE3_LAUNCH_KIT.md` - promotion and deterministic closeout launch kit for the third wave
- `STARRED_REPO_GENE_TRANSFUSION_BACKLOG.md` - execution-ordered backlog derived from starred repos, biased toward Elixir/Erlang first and Rust second
- `STARRED_REPO_STATUS_AND_NEXT_STEPS.md` - repo-by-repo map of which starred-repo ideas are already real in Skyforce, what is still missing, and which repo should own the next move
- `GENE_TRANSFUSION_FROM_ACE_PLATFORM.md` - focused adoption map for what Skyforce should borrow from ACE for playbook learning, outcome capture, and MCP portability without copying ACE as the main runtime
- `core-mechanics/AGENT_SIGNAL_AND_ACTION_MODEL.md` - agent/action/signal/directive runtime semantics bridging Symphony, Durable, and Jido-style agent behavior
- `core-mechanics/GIT_NATIVE_WORK_LEDGER_SPEC.md` - git-backed operational history layout for plans, decisions, checkpoints, validation, and promotion state
- `core-mechanics/FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md` - three-layer filesystem layout for reference context, operational context, and persistent memory
- `core-mechanics/TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md` - registry-driven model for tool descriptors, role-filtered discovery, and policy-aware ToolAction invocation
- `core-mechanics/SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md` - phase-based delivery control flow with named gates, interventions, and promotion-ready posture
- `workflows/WORKFLOW_PACK_AND_REGISTRY_SPEC.md` - versioned workflow pack model with template metadata, trust labels, compatibility, and registry-driven selection
- `core-mechanics/VALIDATION_GUARDRAILS_AND_REVIEW_LOOP_SPEC.md` - layered quality-check loop with findings, bounded rework, review routing, and evidence-backed promotion posture
- `core-mechanics/DIGITAL_TWIN_VALIDATION_SPEC.md` - first-class validation surface for external-system behavior using safe, replayable twins and fidelity-aware verdicts
- `core-mechanics/PYRAMID_SUMMARY_RENDERING_SPEC.md` - shared four-layer summary model that keeps CLI, operator, approval, and promotion views anchored to the same evidence
- `core-mechanics/POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md` - named policy gates for phase transitions, tool use, validation, live actions, promotion, and closeout
- `core-mechanics/GENE_TRANSFUSION_EQUIVALENCE_SPEC.md` - exemplar-packet and invariant-based proof model for showing that a borrowed pattern still behaves acceptably in the target repo
- `core-mechanics/SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md` - concrete runtime semantics for how `interactive` and `factory` differ across planning, interruption, retries, validation, approvals, and summaries
- `core-mechanics/WORKSPACE_ADMIN_GOVERNANCE_SPEC.md` - governance model for workspace-scoped approvals, super-admin escalation, overrides, and auditable authority decisions
- `core-mechanics/PARALLEL_WORKSPACE_EXECUTION_SPEC.md` - slice-based model for safe concurrent work across workspaces, worktrees, validation, conflicts, reintegration, and promotion
- `core-mechanics/SEMPORT_ADOPTION_BOUNDARY_SPEC.md` - rule set for when upstream ideas are adopted directly, wrapped, semported into local contracts, or used only as design influence
- `core-mechanics/CODE_INTELLIGENCE_RETRIEVAL_SPEC.md` - code-aware retrieval model for symbols, files, contracts, tests, graph relations, and evidence-backed relevance without blurring context layers
- `core-mechanics/TOKEN_AND_COMMAND_MEDIATION_SPEC.md` - runtime layer for budgeting context, choosing commands, preferring narrow reads before writes, and avoiding wasteful or unsafe execution
- `core-mechanics/DIGITAL_TWIN_UNIVERSE_ROLLOUT_SPEC.md` - phased rollout plan for bringing twins online safely across Linear, GitHub, Slack, Google Workspace, and approval systems
- `core-mechanics/REVIEW_LOOP_AUTOMATION_SPEC.md` - automation layer for assembling review packets, routing review lanes, maintaining queues, and surfacing triage without removing human authority
- `core-mechanics/TOKEN_ECONOMY_AND_OBSERVABILITY_SPEC.md` - observability model for context spend, command use, waste patterns, budget posture, and efficiency signals across runs and slices
- `core-mechanics/TOOL_EXECUTION_ENGINE_SPEC.md` - approval-aware runtime execution boundary for `ToolAction` invocation, adapter normalization, durable result projection, and idempotent retries
- `core-mechanics/SKILL_PACKAGING_AND_REGISTRATION_SPEC.md` - packaging, validation, registration, and lifecycle model for governed reusable skills that can satisfy runtime `SkillRef` resolution
- `architecture/CONTEXT_HUB_RUNTIME_INTEGRATION_SPEC.md` - runtime boundary for requesting, attaching, labeling, caching, and citing reference context without confusing it with workflow state or memory
- `core-mechanics/EVAL_DRIVEN_ACCEPTANCE_SPEC.md` - evidence-backed acceptance model that combines evals, validation, review, policy, and governance instead of relying on narrative confidence
- `core-mechanics/UPSTREAM_DRIFT_MONITORING_SPEC.md` - monitoring model for detecting when upstream docs, contracts, behavior, or twin assumptions drift enough to require reevaluation
- `core-mechanics/REFERENCE_CONTEXT_PROMOTION_SPEC.md` - governed path for promoting repeatedly useful reference-context lessons and annotations into persistent memory without losing provenance or drift linkage
- `workflows/WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md` - reusable acceptance contract attached to workflow templates so validation, review, and promotion criteria do not have to be reinvented each run
- `core-mechanics/WORK_ORDER_SCHEMA_SPEC.md` - normalized intake schema for turning raw seeds into one durable work-order artifact for the software factory MVP
- `architecture/AGENT_ARCHETYPES_SPEC.md` - role contract for the 6 MVP factory archetypes: planner, coder, reviewer, validator, releaser, and operator liaison
- `architecture/AGENT_ARCHETYPE_SKILL_ATTACHMENT_SPEC.md` - governed mapping layer that lets archetypes attach to registered reusable skills without changing archetype authority
- `core-mechanics/APPROVAL_PACKET_SCHEMA_SPEC.md` - structured approval artifact schema for governed decisions so review and approval stay evidence-backed rather than UI-only
- `core-mechanics/EXECUTION_RECEIPT_SCHEMA_SPEC.md` - structured execution proof schema for what a workflow step or archetype actually did, changed, and validated
- `core-mechanics/MVP_WORKFLOW_BEHAVIOR_SPEC.md` - behavioral contract for the 5 MVP workflows: feature delivery, bug fix, repo evaluation, release preparation, and incident triage
- `milestones/P0/P0_FACTORY_SPINE_RECOVERY_PLAN.md` - execution reset plan that freezes most new doctrine work and focuses the platform on one complete end-to-end factory transaction
- `milestones/P0/P0_FACTORY_SPINE_IMPLEMENTATION_CHECKLIST.md` - concrete cross-repo checklist for delivering the first real intake-to-merge software factory transaction
- `core-mechanics/DRIFT_RESPONSE_PLAYBOOK_SPEC.md` - operational playbook for classifying, containing, reevaluating, remediating, and resolving upstream drift without improvising trust decisions
- `core-mechanics/MEMORY_GOVERNANCE_AND_RETENTION_SPEC.md` - lifecycle model for retaining, cooling, archiving, demoting, expiring, holding, and deleting memory with trust, drift, and governance awareness
- `workflows/WORKFLOW_PROFILE_COMPATIBILITY_SPEC.md` - compatibility layer for composing workflow templates, acceptance profiles, tool families, runtime features, modes, and governance expectations safely
- `core-mechanics/REFERENCE_CONTEXT_STALENESS_AND_REFRESH_SPEC.md` - freshness model for cached and attached reference context, including aging, refresh-before-use, drift-triggered downgrade, and quarantine rules
- `core-mechanics/PACK_MIGRATION_AND_DEPRECATION_SPEC.md` - transition model for upgrading, replacing, deprecating, and retiring workflow packs and related assets without silent drift
- `core-mechanics/ACTIVE_RUN_POLICY_REEVALUATION_SPEC.md` - mid-run reevaluation model for deciding when active workflows may continue, narrow scope, pause, replan, restart, or terminate under changed conditions
- `workflows/WORKFLOW_POLICY_PROFILE_SPEC.md` - reusable workflow-level policy contract for required gates, restricted action families, approval posture, exceptions, and governance expectations
- `workflows/WORKFLOW_PROFILE_RESOLUTION_SPEC.md` - deterministic resolution model for turning pack defaults, template overrides, mode, governance, and compatibility into one active workflow contract
- `workflows/WORKFLOW_PROFILE_OVERRIDE_GOVERNANCE_SPEC.md` - governance model for scoped, expiring, auditable overrides to the resolved workflow contract without undermining profile discipline
- `workflows/WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md` - change-management model for proposing, reviewing, staging, activating, and deprecating workflow profile updates safely
- `workflows/WORKFLOW_PROFILE_OBSERVABILITY_SPEC.md` - observability model for tracking profile selection, override patterns, incompatibility hotspots, rollout impact, and doctrine drift in real usage
- `workflows/WORKFLOW_PROFILE_RECOMMENDATION_SPEC.md` - advisory model for suggesting better profile choices and doctrine updates from observability signals without bypassing governed resolution
- `workflows/WORKFLOW_PROFILE_SIMULATION_AND_SANDBOX_SPEC.md` - safe simulation model for testing candidate profiles, overrides, and recommendations against baseline behavior before activation
- `doctrines/PROFILE_DOCTRINE_CONFLICT_RESOLUTION_SPEC.md` - arbitration model for resolving disagreements between compatibility, governance, recommendations, operator preference, and observed fit
- `doctrines/PROFILE_DOCTRINE_STABILITY_AND_FREEZE_SPEC.md` - stability and freeze model for deciding when profile doctrine is reliable enough to lock for a release wave and how to reopen it safely
- `doctrines/PROFILE_DOCTRINE_WAVE_LAUNCH_SPEC.md` - wave-launch protocol for operating a frozen profile doctrine under real delivery conditions, including monitoring, exceptions, and stop signals
- `doctrines/PROFILE_DOCTRINE_POST_WAVE_RETROSPECTIVE_SPEC.md` - post-wave review model for turning wave evidence into findings, simulations, change requests, and improved future freeze criteria
- `doctrines/PROFILE_DOCTRINE_MULTI_WAVE_LEARNING_SPEC.md` - cross-wave learning model for turning repeated retrospective evidence into durable doctrine trends and longer-horizon improvements
- `doctrines/PROFILE_DOCTRINE_MATURITY_MODEL_SPEC.md` - maturity ladder for classifying doctrine from exploratory to institutionalized based on wave evidence, stability, and regression signals
- `doctrines/PROFILE_DOCTRINE_MATURITY_ADVANCEMENT_PLAYBOOK_SPEC.md` - operational playbook for moving doctrine between maturity stages with checklist-based evidence, approval, and readiness gates
- `doctrines/PROFILE_DOCTRINE_REGRESSION_RESPONSE_SPEC.md` - response playbook for detecting maturity regression, containing risk, regressing confidence honestly, and recovering doctrine safely
- `doctrines/PROFILE_DOCTRINE_RECOVERY_AND_REQUALIFICATION_SPEC.md` - governed recovery model for rebuilding trust after regression through repair, proving, limited reuse, and explicit requalification
- `doctrines/PROFILE_DOCTRINE_REENTRY_AND_EXPANSION_SPEC.md` - staged expansion model for growing recovered doctrine from limited reuse back into broader wave participation and normal use
- `doctrines/PROFILE_DOCTRINE_TRUST_DECAY_SPEC.md` - freshness model for how doctrine confidence narrows over time when evidence ages without a dramatic regression event
- `doctrines/PROFILE_DOCTRINE_RENEWAL_AND_RECERTIFICATION_SPEC.md` - governed refresh and recertification model for restoring fresher and stronger doctrine trust claims after evidence ages
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_HEALTH_SPEC.md` - portfolio-level health model for rolling up doctrine stability, decay, recovery, and risk across many doctrine areas at once
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_INTERVENTION_SPEC.md` - portfolio-level action model for coordinated response when doctrine weakness becomes concentrated, strategic, or wave-blocking
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_EXIT_CRITERIA_SPEC.md` - portfolio-level closure model for deciding when coordinated doctrine intervention can safely step down or end
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_REENTRY_SPEC.md` - portfolio-level transition model for returning from intervention posture back into ordinary doctrine management with visible watchpoints
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_BASELINE_SPEC.md` - steady-state operating model for ordinary doctrine portfolio stewardship when no extraordinary intervention is active
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SLO_AND_ALERTING_SPEC.md` - operational measurement model for doctrine portfolio health using SLO families, alert rules, severities, and escalation posture
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_CAPACITY_AND_LOAD_SPEC.md` - capacity-aware operations model for doctrine stewardship load, backlog pressure, and overload-driven portfolio risk
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_TRIAGE_POLICY_SPEC.md` - prioritization policy for deciding which doctrine work happens now, next cycle, normally, or only under watch when portfolio pressure is high
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_ESCALATION_POLICY_SPEC.md` - escalation boundary model for deciding when doctrine issues should leave ordinary queue management and enter formal portfolio-level review
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_DECISION_AUTHORITY_SPEC.md` - authority-routing model for deciding which portfolio layer may approve, defer, escalate, or reject a doctrine decision
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_DECISION_AUDIT_SPEC.md` - audit model for preserving who decided what, under which authority, from what evidence, and with what follow-up across the doctrine portfolio
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_REVIEW_CADENCE_SPEC.md` - recurring review-rhythm model for daily watch, weekly portfolio, wave-readiness, and post-wave doctrine oversight
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_EXCEPTION_HANDLING_SPEC.md` - exception-governance model for unusual doctrine cases that do not fit normal cadence, routing, or baseline handling cleanly
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_CONTINUITY_AND_FAILSAFE_SPEC.md` - degraded-governance model for keeping doctrine portfolio operation safe when cadence, authority, tooling, or evidence is impaired
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_RECOVERY_FROM_FAILSAFE_SPEC.md` - staged restoration model for returning safely from degraded or failsafe doctrine governance back to normal confidence and oversight
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_MATURITY_SCORECARD_SPEC.md` - multidimensional maturity rollup for summarizing doctrine portfolio strength across health, cadence, authority, auditability, resilience, and operability
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_CALIBRATION_SPEC.md` - calibration model for keeping maturity scorecard ratings evidence-backed, consistent, challengeable, and resistant to inflation
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_GOVERNANCE_SPEC.md` - ownership and approval model for scorecard updates, disputes, overrides, and material maturity claims
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_PUBLICATION_SPEC.md` - audience-specific publication model for rendering the governed scorecard with the right detail, freshness, and caveat posture per surface
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_RETENTION_AND_HISTORY_SPEC.md` - retention and trend-history model for preserving scorecard snapshots, comparisons, and aging posture without confusing past maturity with current truth
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_CONSUMPTION_POLICY_SPEC.md` - role-aware policy for how published doctrine scorecards may guide attention, support decisions, and be rejected when insufficient
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_EXCEPTION_SPEC.md` - exception-governance model for rare scorecard cases that need temporary deviation from normal calibration, publication, or consumption rules
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_RECONCILIATION_SPEC.md` - reconciliation model for resolving conflicts between current scorecard truth, historical trend, disputes, and exceptions into one usable posture
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_DECISION_BINDING_SPEC.md` - decision-binding model for how reconciled doctrine scorecards act as advisory, constraining, or gate inputs in portfolio decisions
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_ACTION_PROTOCOL_SPEC.md` - action protocol for converting scorecard-driven decision outcomes into observation, review, constraint, pause, escalation, and remediation steps
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_AUTOMATION_BOUNDARY_SPEC.md` - automation-boundary model for deciding which scorecard-driven portfolio actions may execute automatically, which need review, and which must stay governed
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_OPERATOR_HANDOFF_SPEC.md` - structured operator-handoff model for passing scorecard-driven portfolio actions across review, approval, escalation, and stale-refresh boundaries
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_QUEUE_DISCIPLINE_SPEC.md` - queue-discipline model for ordering, aging, deferring, escalating, and closing scorecard-driven operator handoffs
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_SLA_AND_BREACH_RESPONSE_SPEC.md` - service-level and breach-response model for timing, escalation, and recovery of scorecard-driven operator work
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_CAPACITY_RECOVERY_SPEC.md` - recovery model for sustained scorecard-queue overload, including intake control, bottleneck handling, restoration, and exit rules
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_LOAD_SHEDDING_SPEC.md` - explicit load-shedding model for intentionally reducing lower-value scorecard work under overload with visible risk labels and recovery rules
- `doctrines/PROFILE_DOCTRINE_PORTFOLIO_SHED_BACKLOG_REACTIVATION_SPEC.md` - controlled reactivation model for restoring intentionally shed doctrine work through filtering, refresh, rate limits, and queue-safe re-entry
- `milestones/P0/P0_GOLDEN_PATH_SEED_PACKET.md` - concrete first factory-spine seed tying work-order intake to Symphony planning, Harness execution, receipt generation, and operator-facing next actions
- `milestones/P1/P1_EVENT_TAXONOMY_SPEC.md` - small universal event language for run, step, validation, approval, and promotion transitions across the factory
- `milestones/P1/P1_POLICY_HOOKS_SPEC.md` - first post-P0 runtime policy boundaries for intake, execution, validation, approval, and promotion transitions
- `milestones/P1/P1_SAFE_PROMOTION_SPEC.md` - governed model for moving validated output from isolated workspaces back into the source repository safely
- `milestones/P1/P1_SUMMARY_PYRAMID_SPEC.md` - first operator-facing summary hierarchy for compressing receipts and logs into readable delivery views
- `milestones/P1/P1_OPERATOR_LOGIN_SURFACE_SPEC.md` - first production login surface for Command Centre Live, including operator session shape, route protection, UI copy, and acceptance criteria
- `milestones/P1/P1_IMPLEMENTATION_STATUS.md` - current `P1` implementation bridge showing which `P1` specs are specified only, partially implemented, or already live in code
- `milestones/P1/P1_UNIVERSAL_TERMINOLOGY_SPEC.md` - operator language mapping that keeps delivery surfaces readable while preserving internal precision
- `cell_spec.md` - shared template for all agent definitions
- `architecture/schemas.md` - data contracts and shared structures
- `interaction_layer_spec.md` - how humans and agents communicate
- `policy_engine_spec.md` - safety and approval model

## Authoring Conventions

- put new agent role docs in `docs/agents/`
- put new vision inputs in `docs/vision/`
- keep cross-cutting system specs in the organized subfolders under `docs/`
- keep workspace-wide operating rules in the root `AGENTS.md`
