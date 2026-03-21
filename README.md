# morphOS

`morphOS` is the specification and operating-model repository for the long-term agentic system.

Canonical build-priority note: treat [docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) as the source of truth for what to build next across `morphOS` and Skyforce.

It defines how the platform should think, coordinate, protect itself, and evolve.
It is not the primary runtime.

| Biological System | SkyForce Component | Specification |
|---|---|---|
| **Cell** (atomic unit) | Universal agent template | [cell_spec.md](docs/cell_spec.md) |
| **DNA** (shared blueprint) | Data schemas and contracts | [schemas.md](docs/schemas.md) |
| **Nervous system** | Event bus (inter-agent communication) | [event_bus_spec.md](docs/event_bus_spec.md) |
| **Immune system** | Policy engine (safety enforcement) | [policy_engine_spec.md](docs/policy_engine_spec.md) |
| **Brain** | Orchestrator (workflow coordination) | [agentic_os_architecture.md](docs/agentic_os_architecture.md) |
| **Eyes** | Vision agent | [vision_agent.md](docs/agents/vision_agent.md) |
| **Hands** | Coding agent | [coding_agent.md](docs/agents/coding_agent.md) |
| **White blood cells** | Debugging agent | [debugging_agent.md](docs/agents/debugging_agent.md) |
| **Skeleton inspector** | Architecture agent | [architecture_agent.md](docs/agents/architecture_agent.md) |
| **Hippocampus** | Learning agent | [learning_agent.md](docs/agents/learning_agent.md) |
| **Symbiont cells** | Human roles (21 roles) | [human_cell_spec.md](docs/human_cell_spec.md) |
| **Genome** | Product vision | [product_vision.md](docs/vision/product_vision.md) |
| **Muscles** | Programs and scripts | `programs/`, `scripts/` |
| **Long-term memory** | Capability store | `memory/capability_store.json` |
| **Circulatory system** | Workflow pipelines | `workflows/` |

That role belongs to the Skyforce repos:

- `skyforce-symphony`: orchestration runtime
- `skyforce-harness`: execution and adapter runtime
- `skyforce-command-centre`: operator control plane
- `skyforce-core`: shared contracts, CLI, and validation surface

See [agentic_os_architecture.md](docs/agentic_os_architecture.md) for the full system design.
Use [docs/README.md](docs/README.md) as the documentation index.

## Start Here

If you are reading this as a human operator, builder, or collaborator, use this order:

1. [Human guide](docs/HUMAN_GUIDE.md)
2. [Skyforce runtime overview](docs/SKYFORCE_RUNTIME_OVERVIEW.md)
3. [Buildability plan](docs/morphos_buildability_plan.md)
4. [morphOS vs Skyforce evaluation](docs/morphos_vs_skyforce_evaluation.md)
5. [morphOS v0 core stack](docs/MORPHOS_V0_CORE_STACK.md)
6. [morphOS v0 runtime contracts](docs/MORPHOS_V0_RUNTIME_CONTRACTS.md)
7. [Symphony and Durable authority boundary](docs/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md)
8. [Durable execution handoff contracts](docs/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md)
9. [morphOS v0 upstream adoption map](docs/MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md)
10. [morphOS v0 upstream feature backlog](docs/MORPHOS_V0_UPSTREAM_FEATURE_BACKLOG.md)
11. [Starred repo gene transfusion backlog](docs/STARRED_REPO_GENE_TRANSFUSION_BACKLOG.md)
12. [Agent signal and action model](docs/AGENT_SIGNAL_AND_ACTION_MODEL.md)
13. [Git native work ledger spec](docs/GIT_NATIVE_WORK_LEDGER_SPEC.md)
14. [Filesystem memory topology spec](docs/FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md)
15. [Tool registry and action discovery spec](docs/TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md)
16. [Software factory control flow spec](docs/SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md)
17. [Workflow pack and registry spec](docs/WORKFLOW_PACK_AND_REGISTRY_SPEC.md)
18. [Validation guardrails and review loop spec](docs/VALIDATION_GUARDRAILS_AND_REVIEW_LOOP_SPEC.md)
19. [Digital twin validation spec](docs/DIGITAL_TWIN_VALIDATION_SPEC.md)
20. [Pyramid summary rendering spec](docs/PYRAMID_SUMMARY_RENDERING_SPEC.md)
21. [Policy hooks at workflow boundaries spec](docs/POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md)
22. [Gene transfusion equivalence spec](docs/GENE_TRANSFUSION_EQUIVALENCE_SPEC.md)
23. [Shift work execution semantics spec](docs/SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md)
24. [Workspace admin governance spec](docs/WORKSPACE_ADMIN_GOVERNANCE_SPEC.md)
25. [Parallel workspace execution spec](docs/PARALLEL_WORKSPACE_EXECUTION_SPEC.md)
26. [Semport adoption boundary spec](docs/SEMPORT_ADOPTION_BOUNDARY_SPEC.md)
27. [Code intelligence retrieval spec](docs/CODE_INTELLIGENCE_RETRIEVAL_SPEC.md)
28. [Token and command mediation spec](docs/TOKEN_AND_COMMAND_MEDIATION_SPEC.md)
29. [Digital twin universe rollout spec](docs/DIGITAL_TWIN_UNIVERSE_ROLLOUT_SPEC.md)
30. [Review loop automation spec](docs/REVIEW_LOOP_AUTOMATION_SPEC.md)
31. [Token economy and observability spec](docs/TOKEN_ECONOMY_AND_OBSERVABILITY_SPEC.md)
32. [Context Hub runtime integration spec](docs/CONTEXT_HUB_RUNTIME_INTEGRATION_SPEC.md)
33. [Eval driven acceptance spec](docs/EVAL_DRIVEN_ACCEPTANCE_SPEC.md)
34. [Upstream drift monitoring spec](docs/UPSTREAM_DRIFT_MONITORING_SPEC.md)
35. [Reference context promotion spec](docs/REFERENCE_CONTEXT_PROMOTION_SPEC.md)
36. [Workflow acceptance profile spec](docs/WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md)
37. [Drift response playbook spec](docs/DRIFT_RESPONSE_PLAYBOOK_SPEC.md)
38. [Memory governance and retention spec](docs/MEMORY_GOVERNANCE_AND_RETENTION_SPEC.md)
39. [Workflow profile compatibility spec](docs/WORKFLOW_PROFILE_COMPATIBILITY_SPEC.md)
40. [Reference context staleness and refresh spec](docs/REFERENCE_CONTEXT_STALENESS_AND_REFRESH_SPEC.md)
41. [Pack migration and deprecation spec](docs/PACK_MIGRATION_AND_DEPRECATION_SPEC.md)
42. [Active run policy reevaluation spec](docs/ACTIVE_RUN_POLICY_REEVALUATION_SPEC.md)
43. [Workflow policy profile spec](docs/WORKFLOW_POLICY_PROFILE_SPEC.md)
44. [Workflow profile resolution spec](docs/WORKFLOW_PROFILE_RESOLUTION_SPEC.md)
45. [Workflow profile override governance spec](docs/WORKFLOW_PROFILE_OVERRIDE_GOVERNANCE_SPEC.md)
46. [Workflow profile change management spec](docs/WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md)
47. [Workflow profile observability spec](docs/WORKFLOW_PROFILE_OBSERVABILITY_SPEC.md)
48. [Workflow profile recommendation spec](docs/WORKFLOW_PROFILE_RECOMMENDATION_SPEC.md)
49. [Workflow profile simulation and sandbox spec](docs/WORKFLOW_PROFILE_SIMULATION_AND_SANDBOX_SPEC.md)
50. [Profile doctrine conflict resolution spec](docs/PROFILE_DOCTRINE_CONFLICT_RESOLUTION_SPEC.md)
51. [Profile doctrine stability and freeze spec](docs/PROFILE_DOCTRINE_STABILITY_AND_FREEZE_SPEC.md)
52. [Profile doctrine wave launch spec](docs/PROFILE_DOCTRINE_WAVE_LAUNCH_SPEC.md)
53. [Profile doctrine post wave retrospective spec](docs/PROFILE_DOCTRINE_POST_WAVE_RETROSPECTIVE_SPEC.md)
54. [Profile doctrine multi wave learning spec](docs/PROFILE_DOCTRINE_MULTI_WAVE_LEARNING_SPEC.md)
55. [Profile doctrine maturity model spec](docs/PROFILE_DOCTRINE_MATURITY_MODEL_SPEC.md)
56. [Profile doctrine maturity advancement playbook spec](docs/PROFILE_DOCTRINE_MATURITY_ADVANCEMENT_PLAYBOOK_SPEC.md)
57. [Profile doctrine regression response spec](docs/PROFILE_DOCTRINE_REGRESSION_RESPONSE_SPEC.md)
58. [Software factory techniques for morphOS](docs/SOFTWARE_FACTORY_TECHNIQUES_FOR_MORPHOS.md)
59. [Context architecture](docs/CONTEXT_ARCHITECTURE.md)
60. [Context Hub evaluation](docs/CONTEXT_HUB_EVALUATION.md)
61. [Context Hub integration plan](docs/CONTEXT_HUB_INTEGRATION_PLAN.md)
62. [Roadmap](docs/ROADMAP.md)

## What morphOS Owns

`morphOS` should own:

- the operating model
- workflow language
- policy language
- agent archetypes
- runtime topology definitions
- safe evolution direction

It should not own:

- the main orchestration runtime
- the main event bus runtime
- node execution
- the operator UI

## Current Relationship To Skyforce

The current platform model is:

- `morphOS` defines the organism
- Skyforce runs the organism

That boundary matters. It keeps architecture and runtime from drifting into two overlapping systems.

## What Is Already Real In Skyforce

The Skyforce runtime already implements several `morphOS`-aligned pieces:

- workflow template loading from `morphOS/workflows`
- template selection inside Symphony
- lightweight workflow progress tracking
- runtime-action classification for current steps
- execution envelopes and receipts carrying workflow metadata
- CLI and dashboard visibility for that progress

## Key Docs

- [Agentic OS architecture](docs/agentic_os_architecture.md)
- [Cell spec](docs/cell_spec.md)
- [Schemas](docs/schemas.md)
- [Event bus spec](docs/event_bus_spec.md)
- [Policy engine spec](docs/policy_engine_spec.md)
- [Runtime topology spec](docs/runtime_topology_spec.md)
- [Interaction layer spec](docs/interaction_layer_spec.md)
- [morphOS v0 core stack](docs/MORPHOS_V0_CORE_STACK.md)
- [morphOS v0 runtime contracts](docs/MORPHOS_V0_RUNTIME_CONTRACTS.md)
- [Symphony and Durable authority boundary](docs/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md)
- [Durable execution handoff contracts](docs/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md)
- [morphOS v0 upstream adoption map](docs/MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md)
- [morphOS v0 upstream feature backlog](docs/MORPHOS_V0_UPSTREAM_FEATURE_BACKLOG.md)
- [Starred repo gene transfusion backlog](docs/STARRED_REPO_GENE_TRANSFUSION_BACKLOG.md)
- [Agent signal and action model](docs/AGENT_SIGNAL_AND_ACTION_MODEL.md)
- [Git native work ledger spec](docs/GIT_NATIVE_WORK_LEDGER_SPEC.md)
- [Filesystem memory topology spec](docs/FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md)
- [Tool registry and action discovery spec](docs/TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md)
- [Software factory control flow spec](docs/SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md)
- [Workflow pack and registry spec](docs/WORKFLOW_PACK_AND_REGISTRY_SPEC.md)
- [Validation guardrails and review loop spec](docs/VALIDATION_GUARDRAILS_AND_REVIEW_LOOP_SPEC.md)
- [Digital twin validation spec](docs/DIGITAL_TWIN_VALIDATION_SPEC.md)
- [Pyramid summary rendering spec](docs/PYRAMID_SUMMARY_RENDERING_SPEC.md)
- [Policy hooks at workflow boundaries spec](docs/POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md)
- [Gene transfusion equivalence spec](docs/GENE_TRANSFUSION_EQUIVALENCE_SPEC.md)
- [Shift work execution semantics spec](docs/SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md)
- [Workspace admin governance spec](docs/WORKSPACE_ADMIN_GOVERNANCE_SPEC.md)
- [Parallel workspace execution spec](docs/PARALLEL_WORKSPACE_EXECUTION_SPEC.md)
- [Semport adoption boundary spec](docs/SEMPORT_ADOPTION_BOUNDARY_SPEC.md)
- [Code intelligence retrieval spec](docs/CODE_INTELLIGENCE_RETRIEVAL_SPEC.md)
- [Token and command mediation spec](docs/TOKEN_AND_COMMAND_MEDIATION_SPEC.md)
- [Digital twin universe rollout spec](docs/DIGITAL_TWIN_UNIVERSE_ROLLOUT_SPEC.md)
- [Review loop automation spec](docs/REVIEW_LOOP_AUTOMATION_SPEC.md)
- [Token economy and observability spec](docs/TOKEN_ECONOMY_AND_OBSERVABILITY_SPEC.md)
- [Context Hub runtime integration spec](docs/CONTEXT_HUB_RUNTIME_INTEGRATION_SPEC.md)
- [Eval driven acceptance spec](docs/EVAL_DRIVEN_ACCEPTANCE_SPEC.md)
- [Upstream drift monitoring spec](docs/UPSTREAM_DRIFT_MONITORING_SPEC.md)
- [Reference context promotion spec](docs/REFERENCE_CONTEXT_PROMOTION_SPEC.md)
- [Workflow acceptance profile spec](docs/WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md)
- [Work order schema spec](docs/WORK_ORDER_SCHEMA_SPEC.md)
- [Agent archetypes spec](docs/AGENT_ARCHETYPES_SPEC.md)
- [Approval packet schema spec](docs/APPROVAL_PACKET_SCHEMA_SPEC.md)
- [Execution receipt schema spec](docs/EXECUTION_RECEIPT_SCHEMA_SPEC.md)
- [MVP workflow behavior spec](docs/MVP_WORKFLOW_BEHAVIOR_SPEC.md)
- [Software factory techniques for morphOS](docs/SOFTWARE_FACTORY_TECHNIQUES_FOR_MORPHOS.md)
- [Context architecture](docs/CONTEXT_ARCHITECTURE.md)
- [Context Hub evaluation](docs/CONTEXT_HUB_EVALUATION.md)
- [Context Hub integration plan](docs/CONTEXT_HUB_INTEGRATION_PLAN.md)
- [Profile doctrine recovery and requalification spec](docs/PROFILE_DOCTRINE_RECOVERY_AND_REQUALIFICATION_SPEC.md)
- [Profile doctrine reentry and expansion spec](docs/PROFILE_DOCTRINE_REENTRY_AND_EXPANSION_SPEC.md)
- [Profile doctrine trust decay spec](docs/PROFILE_DOCTRINE_TRUST_DECAY_SPEC.md)
- [Profile doctrine renewal and recertification spec](docs/PROFILE_DOCTRINE_RENEWAL_AND_RECERTIFICATION_SPEC.md)
- [Profile doctrine portfolio health spec](docs/PROFILE_DOCTRINE_PORTFOLIO_HEALTH_SPEC.md)
- [Profile doctrine portfolio intervention spec](docs/PROFILE_DOCTRINE_PORTFOLIO_INTERVENTION_SPEC.md)
- [Profile doctrine portfolio exit criteria spec](docs/PROFILE_DOCTRINE_PORTFOLIO_EXIT_CRITERIA_SPEC.md)
- [Profile doctrine portfolio reentry spec](docs/PROFILE_DOCTRINE_PORTFOLIO_REENTRY_SPEC.md)
- [Profile doctrine portfolio baseline spec](docs/PROFILE_DOCTRINE_PORTFOLIO_BASELINE_SPEC.md)
- [Profile doctrine portfolio SLO and alerting spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SLO_AND_ALERTING_SPEC.md)
- [Profile doctrine portfolio capacity and load spec](docs/PROFILE_DOCTRINE_PORTFOLIO_CAPACITY_AND_LOAD_SPEC.md)
- [Profile doctrine portfolio triage policy spec](docs/PROFILE_DOCTRINE_PORTFOLIO_TRIAGE_POLICY_SPEC.md)
- [Profile doctrine portfolio escalation policy spec](docs/PROFILE_DOCTRINE_PORTFOLIO_ESCALATION_POLICY_SPEC.md)
- [Profile doctrine portfolio decision authority spec](docs/PROFILE_DOCTRINE_PORTFOLIO_DECISION_AUTHORITY_SPEC.md)
- [Profile doctrine portfolio decision audit spec](docs/PROFILE_DOCTRINE_PORTFOLIO_DECISION_AUDIT_SPEC.md)
- [Profile doctrine portfolio review cadence spec](docs/PROFILE_DOCTRINE_PORTFOLIO_REVIEW_CADENCE_SPEC.md)
- [Profile doctrine portfolio exception handling spec](docs/PROFILE_DOCTRINE_PORTFOLIO_EXCEPTION_HANDLING_SPEC.md)
- [Profile doctrine portfolio continuity and failsafe spec](docs/PROFILE_DOCTRINE_PORTFOLIO_CONTINUITY_AND_FAILSAFE_SPEC.md)
- [Profile doctrine portfolio recovery from failsafe spec](docs/PROFILE_DOCTRINE_PORTFOLIO_RECOVERY_FROM_FAILSAFE_SPEC.md)
- [Profile doctrine portfolio maturity scorecard spec](docs/PROFILE_DOCTRINE_PORTFOLIO_MATURITY_SCORECARD_SPEC.md)
- [Profile doctrine portfolio scorecard calibration spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_CALIBRATION_SPEC.md)
- [Profile doctrine portfolio scorecard governance spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_GOVERNANCE_SPEC.md)
- [Profile doctrine portfolio scorecard publication spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_PUBLICATION_SPEC.md)
- [Profile doctrine portfolio scorecard retention and history spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_RETENTION_AND_HISTORY_SPEC.md)
- [Profile doctrine portfolio scorecard consumption policy spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_CONSUMPTION_POLICY_SPEC.md)
- [Profile doctrine portfolio scorecard exception spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_EXCEPTION_SPEC.md)
- [Profile doctrine portfolio scorecard reconciliation spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_RECONCILIATION_SPEC.md)
- [Profile doctrine portfolio scorecard decision binding spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_DECISION_BINDING_SPEC.md)
- [Profile doctrine portfolio scorecard action protocol spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_ACTION_PROTOCOL_SPEC.md)
- [Profile doctrine portfolio scorecard automation boundary spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_AUTOMATION_BOUNDARY_SPEC.md)
- [Profile doctrine portfolio scorecard operator handoff spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_OPERATOR_HANDOFF_SPEC.md)
- [Profile doctrine portfolio scorecard queue discipline spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_QUEUE_DISCIPLINE_SPEC.md)
- [Profile doctrine portfolio scorecard SLA and breach response spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_SLA_AND_BREACH_RESPONSE_SPEC.md)
- [Profile doctrine portfolio scorecard capacity recovery spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_CAPACITY_RECOVERY_SPEC.md)
- [Profile doctrine portfolio scorecard load shedding spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_LOAD_SHEDDING_SPEC.md)
- [Profile doctrine portfolio shed backlog reactivation spec](docs/PROFILE_DOCTRINE_PORTFOLIO_SHED_BACKLOG_REACTIVATION_SPEC.md)

## Current Release

Current specification release line:

- `0.1.0`

This is a specification baseline, not a production runtime release.
