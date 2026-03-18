# Archetype: Hermes

## Definition
Hermes is a self-improving agent archetype designed for high-concurrency code execution, knowledge persistence, and autonomous skill acquisition.

## Capabilities
- **Parallel Execution**: Capable of managing multi-threaded task resolution.
- **Skill Creation**: Automatically distills successful patterns into reusable skills.
- **Self-Correction**: Uses internal "thought" loops to verify its own work before submission.
- **Workspace Context**: Natively understands multi-repo topologies when provided with `AGENTS.md`.

## Skyforce Role
In the Skyforce platform, Hermes serves as a **Resolution Agent** for Symphony. It is tasked with:
1. Analyzing issues from the tracker.
2. Executing code changes across repos using provided tooling.
3. Validating changes against the platform's multi-agent validation model.

## Preferred Tools
- `sky`: For workspace inspection and status.
- `ripgrep`: For code search.
- `npm`/`python`: For test execution.
