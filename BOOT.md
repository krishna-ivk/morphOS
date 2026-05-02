# BOOT.md

Run a bounded Pi startup self-check for the Skyforce workspace using the configured Codex-auth OpenClaw model.

1. Confirm the active workspace is this repository root.
2. Review `launch-stack.sh` and the newest files in `logs/` to verify Skyforce and OpenClaw startup health.
3. If Pi/OpenClaw startup is blocked by a local workspace or configured OpenClaw state/config issue, prefer the configured Codex-auth startup path and make the smallest safe local repair before re-checking.
4. Do not edit product source code, do not commit, do not send messages, do not change credentials, and do not modify deployment or network settings.
5. If no repair is needed, reply with `NO_REPLY`. If you made a local startup repair, reply with a one-line summary followed by `NO_REPLY`.
