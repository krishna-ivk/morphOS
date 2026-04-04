"""Interactive vs Factory Mode enforcement in the orchestrator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


MODE_INTERACTIVE = "interactive"
MODE_FACTORY = "factory"
MODE_AUTO = "auto"

ALL_MODES = {MODE_INTERACTIVE, MODE_FACTORY, MODE_AUTO}


@dataclass
class ModeConfig:
    interrupt_strategy: str
    summary_level: str
    approval_gating: str
    auto_resume: bool
    max_idle_seconds: int
    prompt_for_confirmation: bool


MODE_CONFIGS: dict[str, ModeConfig] = {
    MODE_INTERACTIVE: ModeConfig(
        interrupt_strategy="immediate",
        summary_level="detailed",
        approval_gating="prompt",
        auto_resume=False,
        max_idle_seconds=300,
        prompt_for_confirmation=True,
    ),
    MODE_FACTORY: ModeConfig(
        interrupt_strategy="defer",
        summary_level="headline",
        approval_gating="pause",
        auto_resume=True,
        max_idle_seconds=0,
        prompt_for_confirmation=False,
    ),
}


def get_mode_config(mode: str) -> ModeConfig:
    return MODE_CONFIGS.get(mode, MODE_CONFIGS[MODE_FACTORY])


def should_interrupt_for_approval(mode: str, step_type: str) -> bool:
    config = get_mode_config(mode)
    if config.approval_gating == "prompt":
        return True
    if config.approval_gating == "pause":
        return step_type == "approval"
    return False


def should_auto_resume(mode: str) -> bool:
    return get_mode_config(mode).auto_resume


def get_summary_level(mode: str) -> str:
    return get_mode_config(mode).summary_level


def detect_mode_from_seed(seed_path: str | None, cli_mode: str) -> str:
    if cli_mode != MODE_AUTO:
        return cli_mode
    if seed_path and ("interactive" in seed_path or "pair" in seed_path):
        return MODE_INTERACTIVE
    return MODE_FACTORY


def format_mode_status(mode: str, config: ModeConfig | None = None) -> str:
    config = config or get_mode_config(mode)
    return (
        f"mode={mode} | "
        f"interrupt={config.interrupt_strategy} | "
        f"summary={config.summary_level} | "
        f"approval={config.approval_gating} | "
        f"auto_resume={config.auto_resume}"
    )
