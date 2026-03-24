# P1 Implementation Status

## Purpose

Bridge the gap between `P1` doctrine and actual runtime behavior so readers do not
mistake a written `P1` spec for a fully delivered feature.

This document should stay short, practical, and regularly updated.

## Status Scale

- `specified` - doctrine exists, but there is no meaningful runtime implementation yet
- `partially_implemented` - code exists and may be exercised locally, but the behavior is not yet complete or uniformly enforced
- `implemented` - the behavior exists in code, has tests, and is being used as part of the current operator/runtime path

## P1 Status Map

### `P1_EVENT_TAXONOMY_SPEC`

- status: `partially_implemented`
- current proof:
  - Harness timelines now emit explicit event types such as summary, evidence, approval, and sync events
  - Command Centre now classifies normalized event-taxonomy families and stages for run summaries, run bundles, audit events, and operator action receipts
  - Command Centre Live consumes taxonomy-backed event state in the issue operator snapshot
- remaining gap:
  - no fully shared cross-repo event registry yet
  - taxonomy is still runtime-shaped rather than centrally enforced

### `P1_POLICY_HOOKS_SPEC`

- status: `partially_implemented`
- current proof:
  - backend role checks exist for manual runs, approvals, directive actions, durable actions, and publish actions
  - Command Centre now evaluates policy-hook verdicts for manual runs, approvals, directive actions, durable actions, and publish actions through a shared hook evaluator
  - operator action receipts now persist policy-hook verdict data instead of only the action result
- remaining gap:
  - command-boundary hook enforcement is not yet unified across all runtime repos
  - policy hooks are still Command Centre-centric rather than shared across the full factory spine

### `P1_SAFE_PROMOTION_SPEC`

- status: `partially_implemented`
- current proof:
  - Command Centre now exposes promotion preview and apply actions
  - promotion readiness is derived from the run bundle, approval state, and work-order scope
  - promotion actions now produce policy-hook verdicts, audit events, operator action receipts, and operator-facing issue-state updates
- remaining gap:
  - no complete, production-grade promotion/merge execution path is yet proven end to end
  - promotion execution is still a control-plane slice, not a real `skyforce-core` execution seam

### `P1_SUMMARY_PYRAMID_SPEC`

- status: `implemented`
- current proof:
  - Harness emits `status.txt`, `summary_short.md`, `summary_full.md`, and `evidence.json`
  - approval packets and run bundles point to those artifacts
  - Command Centre surfaces those summary layers to operators

### `P1_OPERATOR_LOGIN_SURFACE_SPEC`

- status: `implemented`
- current proof:
  - Command Centre Live has a real login route and protected operator surfaces
  - session-backed operator identity, role, and workspace are live
  - backend write paths support signed operator claims when a shared secret is configured
- remaining gap:
  - no external identity provider or full account lifecycle yet

### `P1_UNIVERSAL_TERMINOLOGY_SPEC`

- status: `partially_implemented`
- current proof:
  - backend run summaries and run bundles now project operator-facing labels for receipt, approval, sync, and promotion state
  - Command Centre Live issue and dashboard views now prefer normalized human-facing labels instead of raw machine state
  - login and operator-scope surfaces now use a more consistent control-plane vocabulary
- remaining gap:
  - terminology is not yet uniformly normalized across all repos, CLI surfaces, and runtime artifacts

## Reading Guidance

- treat `implemented` as the closest thing to current truth
- treat `partially_implemented` as active code-development territory
- treat `specified` as a plan, not a guarantee

## Update Rule

Whenever a `P1` runtime behavior changes materially, update this file in the same
batch as the related spec or implementation change.
