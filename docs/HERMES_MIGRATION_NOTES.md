# Hermes Migration Notes

This document replaces the older upstream-runtime reuse analysis as the active workspace-facing migration note.

## Current direction

- Hermes is the preferred agent setup path for Skyforce.
- The current migration slice updates docs, config templates, and planning artifacts first.
- Active runtime code and legacy experimental scripts are intentionally deferred to a later implementation slice.

## What changed in this slice

- workspace and repo docs now describe Hermes as the supported agent path
- config templates now use `HERMES_BASE_URL`, `HERMES_API_KEY`, and `HERMES_MODEL`
- Symphony and Harness example manifests now point at Hermes-oriented agent and node identities
- planning docs no longer position the legacy upstream runtime as the primary fleet/runtime direction

## What is still deferred

- runtime endpoint migration in live application code
- cleanup of legacy upstream-runtime-specific scripts and demos
- any decision to delete or archive the vendored legacy runtime repository itself

## Next recommended slice

1. update runtime code paths that still read legacy gateway env vars or UI copy
2. clean up legacy Hermes demo scripts that still reference the older runtime
3. decide whether the in-workspace legacy runtime snapshot should remain inactive or be retired
