# Review Loop Automation Spec

## Why This Spec Exists

`morphOS` already defines:

- validation guardrails and review outcomes
- summary pyramid rendering
- governance and approval routing

What is still missing is the automation layer around review itself.

This spec defines that layer.

## Executive Summary

Review automation should not try to replace human judgment everywhere.

It should automate the parts of review that are:

- repetitive
- evidence assembly heavy
- routing heavy
- formatting heavy
- confidence-checking heavy

while keeping final authority where it belongs:

- validation systems for deterministic checks
- workspace admins and super admins for governed decisions
- human reviewers for ambiguous or high-risk judgment

The right goal is:

- automate review preparation
- automate review routing
- automate review evidence packaging
- do not automate away accountability

## Core Design Goals

- reduce review toil without hiding risk
- make review packets consistent and evidence-backed
- route reviews to the right authority automatically where possible
- separate routine machine triage from actual human judgment
- keep review decisions auditable and reversible

## What Review Automation Is

Review automation is the system that prepares, prioritizes, routes, and maintains review state.

Typical automated review work:

- build review packets
- summarize findings
- attach evidence refs
- classify likely blockers
- suggest likely next action
- route to the right reviewer or authority scope
- detect stale or incomplete review packets

## What It Is Not

Review automation is not:

- unlimited autonomous approval
- a replacement for policy
- a replacement for validation
- permission to auto-merge risky or ambiguous work silently

It should make review better and faster, not invisible.

## Canonical Review Stages

The automated review loop should support these stages:

1. `review_candidate_detected`
2. `review_packet_assembled`
3. `review_packet_validated`
4. `review_routed`
5. `review_waiting`
6. `review_decided`
7. `review_followup_created`

Automation is strongest in stages 1 through 4 and 7.
Stage 6 may be partially automated only for clearly bounded low-risk cases.

## Review Packet Automation

The system should automatically assemble a review packet whenever review is required or strongly suggested.

The packet should include:

- objective
- current posture
- summary of changed artifacts
- validation findings
- twin outcomes where relevant
- policy posture
- approval context where relevant
- evidence refs
- recommended next action

The packet should be derived from existing artifacts whenever possible.

## Review Packet Validation

Before a packet is shown to a reviewer, the system should validate that it is review-ready.

Checks should include:

- required fields present
- evidence refs resolve
- validation posture is current
- approval context is attached when needed
- summary does not contradict evidence

If the packet is incomplete, automation should repair or flag it before routing.

## Automated Triage

Automation should triage review candidates into broad buckets such as:

- `routine`
- `changes_requested_likely`
- `high_risk`
- `approval_sensitive`
- `insufficient_evidence`

These are triage hints, not final decisions.

Their purpose is to:

- prioritize queue order
- route to the right reviewer lane
- indicate how much human attention is likely needed

## Routing Automation

The system should automate review routing based on:

- workspace scope
- required authority
- risk category
- policy findings
- validation posture
- review category

Examples:

- workspace-scoped risky action -> workspace admin review
- global exception path -> super admin review
- routine low-risk review -> standard reviewer lane

Routing automation should respect governance rules rather than invent them.

## Review Categories

The review loop should distinguish categories instead of treating every review the same.

Suggested categories:

- `quality_review`
- `policy_review`
- `promotion_review`
- `approval_review`
- `equivalence_review`
- `drift_review`

Different categories may require different packet fields and reviewer authority.

## Automated Suggestions

Automation may suggest:

- `accepted`
- `changes_requested`
- `blocked`
- `approval_required`

But suggestions should always be labeled as suggestions unless a workflow explicitly permits deterministic auto-resolution for a narrow low-risk case.

Examples of low-risk deterministic cases:

- review packet invalid because evidence refs are missing
- summary contradiction detected
- stale packet needs refresh

These are automation-friendly because they concern packet quality, not business judgment.

## What May Be Auto-Resolved

Good candidates for automatic handling:

- packet assembly
- packet refresh when evidence changes
- stale review invalidation
- duplicate review suppression
- queue prioritization
- reviewer-lane routing

Possible narrow deterministic auto-decisions:

- `insufficient_evidence`
- `packet_stale`
- `packet_invalid`

## What Must Remain Human Or Governed

The following should remain human or explicitly governed unless a future policy says otherwise:

- final approval for risky actions
- global exception decisions
- high-risk promotion acceptance
- ambiguous equivalence judgments
- subjective product or UX tradeoff acceptance

## Review Queue Maintenance

Automation should maintain review queues actively.

Useful automated behaviors:

- collapse duplicate review candidates
- refresh packets when new evidence arrives
- mark packets stale when underlying artifacts change
- escalate aging high-risk reviews
- remove packets made irrelevant by abort, supersession, or rejection

This keeps review queues trustworthy instead of cluttered.

## Relationship To Validation

Validation and review must remain distinct.

Validation automation answers:

- did the work pass checks?

Review automation answers:

- what should humans or governing roles inspect next, and with what packet?

Validation findings should feed review automation.
They should not be mistaken for final review decisions.

## Relationship To Summary Rendering

Review automation should consume and improve the summary pyramid, not bypass it.

Examples:

- use `summary_short.md` for queue cards
- use `summary_full.md` and `evidence.json` for review packets
- regenerate summary when review-relevant facts change

This keeps review readable without inventing separate narratives.

## Relationship To Governance

Review automation must honor governance boundaries.

That means:

- route by workspace vs global scope
- attach authority context
- never silently upgrade or downgrade required authority
- preserve escalation records

Automation may help route authority.
It must not erase it.

## Relationship To Execution Mode

### Interactive Mode

Automation should:

- surface review earlier
- keep packets more conversational and inspection-friendly
- allow ongoing reshaping of scope

### Factory Mode

Automation should:

- package evidence deterministically
- route review only at named gates
- keep review packets concise and decision-ready

## Required Events

The event taxonomy should support at least:

- `review.packet_assembled`
- `review.packet_invalid`
- `review.routed`
- `review.queue_updated`
- `review.stale`
- `review.decision_suggested`
- `review.followup_created`

Each event should include:

- `run_id`
- review category
- review scope
- current authority context when relevant

## Required Artifacts

Review automation should emit durable artifacts.

Suggested baseline:

- `reviews/review_packet.json`
- `reviews/routing.json`
- `reviews/triage.json`
- `reviews/automation_notes.md`
- `reviews/followup.json`

These artifacts should feed:

- operator review views
- approval views
- promotion posture
- audit history

## What This Changes For Skyforce

This spec implies concrete follow-on work:

- `skyforce-core` should define review category, triage, routing, and packet-validation contracts
- `skyforce-symphony` should trigger packet assembly and routing at review gates
- `skyforce-harness` should emit cleaner evidence refs that support packet assembly
- `skyforce-command-centre-live` should render review queues with automated triage, staleness, and authority context
- `skyforce-api-gateway` should provide stable normalized review queue projections to operator clients

## Recommended First Implementation Slice

The first useful slice should be narrow and high-value:

1. automate review packet assembly from validation and summary artifacts
2. validate packet completeness before routing
3. route by workspace vs global authority context
4. mark stale packets when underlying evidence changes
5. surface triage hints without auto-approving risky work

That is enough to make review automation useful without pretending the system can replace reviewers.

## Recommended Next Specs

This spec should be followed by:

1. `TOKEN_ECONOMY_AND_OBSERVABILITY_SPEC.md`
2. `CONTEXT_HUB_RUNTIME_INTEGRATION_SPEC.md`
3. `EVAL_DRIVEN_ACCEPTANCE_SPEC.md`

Together, those continue the remaining observability, context integration, and evaluation-surface work.
