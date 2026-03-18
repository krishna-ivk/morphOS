# StrongDM Software Factory Principles Outline

Source: <https://factory.strongdm.ai/principles>

Accessed: 2026-03-17

## Core Philosophy

The page presents a simple software-factory loop:

1. Start with a seed.
2. Validate against realistic conditions.
3. Feed results back into the system.
4. Spend enough tokens to keep the loop running effectively.

In shorthand, the model is:

- seed
- validation harness
- feedback loop
- tokens as fuel

## Principle 1: Seed

Every software effort needs an initial seed.

That seed can be:

- a PRD
- a specification
- a few sentences
- a screenshot
- an existing codebase

The point is that the starting artifact does not need to be traditional or large. It just needs to give the model something concrete to grow from.

## Principle 2: Validation

Validation should be end-to-end and as close to the real operating environment as possible.

The page explicitly says validation should reflect:

- customers
- integrations
- economics

This means the harness should not stop at unit correctness. It should test whether the system behaves acceptably in realistic usage and business conditions.

## Principle 3: Feedback

A sample of system output should be fed back into the inputs.

This creates a closed loop that:

- helps the system self-correct
- allows correctness to compound over time
- keeps the model improving against holdout scenarios

The loop is meant to continue until holdout scenarios pass consistently, not just once.

## Principle 4: Tokens Are Fuel

The page argues that understanding validation and feedback is easy in theory, but making it work requires creative engineering and enough token budget.

Their practical heuristic is:

- for each obstacle, convert the problem into a representation the model can understand

## Recommended Input Signals For The Loop

The principles page lists examples of evidence and feedback signals to feed into the system:

- traces
- screen captures
- conversation transcripts
- incident replays
- adversarial use
- agentic simulation
- just-in-time surveys
- customer interviews
- price elasticity testing

## Plain-English Summary

StrongDM's principles describe software development as a growth loop:

- begin from any meaningful seed
- validate in realistic, end-to-end conditions
- feed representative outputs back into the system
- invest enough tokens and engineering effort to keep the loop improving

The emphasis is less on handcrafted code review and more on repeated validation, real-world feedback, and sustained iteration.
