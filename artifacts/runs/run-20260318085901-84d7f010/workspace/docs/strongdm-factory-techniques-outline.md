# StrongDM Software Factory Techniques Outline

Source: <https://factory.strongdm.ai/techniques>

Accessed: 2026-03-17

## Overview

The techniques page describes a set of recurring patterns StrongDM uses while building with its Software Factory.

The listed techniques are:

1. Digital Twin Universe
2. Gene Transfusion
3. The Filesystem
4. Shift Work
5. Semport
6. Pyramid Summaries

## Shared Constraint

The page frames these techniques around a strong validation requirement:

- grow systems from natural-language specification cascades
- validate automatically without relying on semantic inspection of source code
- treat code more like an opaque model snapshot whose correctness is inferred from externally observable behavior

This means the techniques are primarily about behavior, reproducibility, memory, translation, and context management.

## 1. Digital Twin Universe (DTU)

Page: <https://factory.strongdm.ai/techniques/dtu>

### Core idea

Build behavioral clones of important third-party services and validate against the clones instead of live production dependencies.

### What they clone

The page mentions twins for:

- Okta
- Jira
- Slack
- Google Docs
- Google Drive
- Google Sheets

### Why it matters

DTU is used to:

- validate at very high volume
- test dangerous or rare failure modes
- avoid rate limits and abuse detection
- keep test conditions deterministic and replayable

### Practical insight

The key is to clone behavior at the boundary:

- use API contracts
- use observed edge cases
- compare the twin against the live dependency
- keep refining until behavioral differences stop appearing

## 2. Gene Transfusion

Page: <https://factory.strongdm.ai/techniques/gene-transfusion>

### Core idea

Move working patterns between codebases by pointing agents at strong concrete exemplars.

### Flow

1. Identify a working exemplar.
2. Extract the important pattern.
3. Synthesize an equivalent implementation in the target context.
4. Validate behavioral equivalence.
5. Reuse that pattern again later.

### What it enables

- cross-language reuse
- direct inlining into an existing system
- library-style embodiment when abstraction makes sense

### Practical insight

The pattern itself is the reusable asset. With a reliable exemplar and a good validation harness, agents can reproduce solutions in new local contexts without manual refactoring.

## 3. The Filesystem

Page: <https://factory.strongdm.ai/techniques/filesystem>

### Core idea

Use the filesystem as mutable, inspectable world-state for agents.

### Expected behaviors

The page says agents reliably:

- build on-disk indexes
- write scratch state
- rehydrate context by searching and reopening files

### Storage forms

State is usually kept as:

- Markdown
- JSON
- YAML
- sometimes XML

### Key advantages

- self-organizing context
- persistent memory across sessions
- inspectable state humans can audit or reset
- composable shared memory across multiple agents

### Practical insight

As information grows messy, agents should reorganize it. The page calls this “genrefying,” similar to rebalancing and reindexing a data structure for better retrieval later.

## 4. Shift Work

Page: <https://factory.strongdm.ai/techniques/shift-work>

### Core idea

Separate interactive work from non-interactive work.

### Interactive mode

Use interactive loops when intent is still evolving:

- generate
- clarify
- approve
- correct

### Non-interactive mode

Use non-interactive execution when intent is already complete.

Canonical examples:

- formal specifications
- spec plus validation suite
- existing working applications used as executable specifications

### Practical insight

An existing application can function as a complete behavioral specification. Once intent is complete, an agent should be able to run end-to-end without repeated human back-and-forth.

## 5. Semport

Page: <https://factory.strongdm.ai/techniques/semport>

### Core idea

Perform semantically aware automated ports between languages or frameworks while preserving intent.

### Modes

- one-time ports
- ongoing ports
- adaptive ports that reshape interfaces to local conventions

### Practical model

Semport acts like a dependency through translation:

- track an upstream implementation you trust
- port or adapt it into your internal stack
- re-run the port process on later upstream changes
- validate the translated result automatically

### Practical insight

This is useful when:

- the original library is in the wrong language
- the dependency tree is unacceptable
- deeper internal integration is required

The point is to inherit upstream design thinking without being locked into upstream implementation choices.

## 6. Pyramid Summaries

Page: <https://factory.strongdm.ai/techniques/pyramid-summaries>

### Core idea

Use reversible summaries at multiple zoom levels so agents can compress and later re-expand context.

### Example shape

The page uses a pattern like:

- summarize in 2 words
- then 4 words
- then 8
- then 16

Each level keeps the essential meaning while changing the amount of detail.

### What it enables

- fast scanning across many items
- low context displacement
- selective drill-down on only the most relevant items

### Combined pattern

The page recommends combining Pyramid Summaries with:

- Map
- Cluster
- Reduce

That means:

1. summarize many items in parallel
2. group related compressed summaries
3. synthesize across groups and expand details only where needed

### Practical insight

This technique helps a limited-context model “see” more of the overall terrain and then zoom into the parts that matter.

## Plain-English Summary

Taken together, the StrongDM techniques suggest a practical software-factory toolkit:

- use behavioral validation instead of trusting code structure
- clone critical dependencies so testing becomes safe and scalable
- move patterns from exemplars instead of reinventing them
- treat the filesystem as durable shared memory
- distinguish exploratory work from fully specified execution
- translate trusted upstream systems into local implementations
- compress context aggressively, but reversibly

## Most Relevant Ideas For morphOS / Skyforce

The techniques that appear most directly portable into the current Skyforce and morphOS direction are:

- The Filesystem
  - fits persistent agent memory and inspectable state
- Shift Work
  - fits the split between interactive operator workflows and fully specified execution runs
- Pyramid Summaries
  - fits large-workspace context compression and operator dashboards
- Gene Transfusion
  - fits cross-repo pattern reuse and implementation transfer
- DTU
  - fits safe validation of integrations and high-volume replay
- Semport
  - fits porting trusted patterns and SDK designs into the local stack
