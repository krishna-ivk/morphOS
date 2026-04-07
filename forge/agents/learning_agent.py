"""Learning Agent — The Hippocampus.

Extracts reusable patterns, bug fixes, and architecture lessons from
completed runs and stores them in the long-term capability store.

See docs/agents/learning_agent.md for the full specification.
"""

import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

MAX_STORE_SIZE = 1_000_000
PRUNE_TARGET_SIZE = 800_000
PRUNE_AGE_DAYS = 30
MIN_CONFIDENCE_RUNS = 2


@dataclass
class Pattern:
    context: str
    description: str
    category: str
    first_seen: str = ""
    last_seen: str = ""
    use_count: int = 1
    run_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "context": self.context,
            "description": self.description,
            "category": self.category,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "use_count": self.use_count,
            "run_ids": self.run_ids,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Pattern":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class BugFix:
    symptom: str
    root_cause: str
    fix: str
    category: str = ""
    first_seen: str = ""
    last_seen: str = ""
    use_count: int = 1
    run_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "symptom": self.symptom,
            "root_cause": self.root_cause,
            "fix": self.fix,
            "category": self.category,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "use_count": self.use_count,
            "run_ids": self.run_ids,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "BugFix":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ArchitectureLesson:
    context: str
    lesson: str
    impact: str
    category: str = ""
    first_seen: str = ""
    last_seen: str = ""
    use_count: int = 1
    run_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "context": self.context,
            "lesson": self.lesson,
            "impact": self.impact,
            "category": self.category,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "use_count": self.use_count,
            "run_ids": self.run_ids,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ArchitectureLesson":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class CapabilityStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self.store = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text())
            except (json.JSONDecodeError, OSError) as exc:
                logger.error("Capability store corrupted: %s", exc)
                return self._empty()
        return self._empty()

    @staticmethod
    def _empty() -> dict:
        now = datetime.now(timezone.utc).isoformat()
        return {
            "version": "0.1.0",
            "created_at": now,
            "updated_at": now,
            "patterns": [],
            "bug_fixes": [],
            "architecture_lessons": [],
        }

    def save(self):
        self.store["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.store, indent=2) + "\n")

    def size_bytes(self) -> int:
        return len(json.dumps(self.store).encode())

    # -- Mutators -----------------------------------------------------------

    def upsert_pattern(self, pattern: Pattern):
        existing = self._find_duplicate_pattern(pattern)
        if existing:
            existing["use_count"] += 1
            if pattern.run_ids:
                existing.setdefault("run_ids", []).extend(pattern.run_ids)
            existing["last_seen"] = pattern.last_seen or existing.get("last_seen", "")
            logger.info(
                "Pattern already known — incremented use_count to %d",
                existing["use_count"],
            )
        else:
            self.store["patterns"].append(pattern.to_dict())
            logger.info("New pattern stored: %s", pattern.description[:80])

    def upsert_bug_fix(self, fix: BugFix):
        existing = self._find_duplicate_bug_fix(fix)
        if existing:
            existing["use_count"] += 1
            if fix.run_ids:
                existing.setdefault("run_ids", []).extend(fix.run_ids)
            existing["last_seen"] = fix.last_seen or existing.get("last_seen", "")
            logger.info(
                "Bug fix already known — incremented use_count to %d",
                existing["use_count"],
            )
        else:
            self.store["bug_fixes"].append(fix.to_dict())
            logger.info("New bug fix stored: %s", fix.symptom[:80])

    def upsert_lesson(self, lesson: ArchitectureLesson):
        existing = self._find_duplicate_lesson(lesson)
        if existing:
            existing["use_count"] += 1
            if lesson.run_ids:
                existing.setdefault("run_ids", []).extend(lesson.run_ids)
            existing["last_seen"] = lesson.last_seen or existing.get("last_seen", "")
            logger.info(
                "Lesson already known — incremented use_count to %d",
                existing["use_count"],
            )
        else:
            self.store["architecture_lessons"].append(lesson.to_dict())
            logger.info("New lesson stored: %s", lesson.lesson[:80])

    # -- Deduplication ------------------------------------------------------

    def _find_duplicate_pattern(self, pattern: Pattern) -> Optional[dict]:
        for entry in self.store["patterns"]:
            if (
                entry.get("description", "").lower() == pattern.description.lower()
                and entry.get("category", "") == pattern.category
            ):
                return entry
        return None

    def _find_duplicate_bug_fix(self, fix: BugFix) -> Optional[dict]:
        for entry in self.store["bug_fixes"]:
            if (
                entry.get("symptom", "").lower() == fix.symptom.lower()
                and entry.get("root_cause", "").lower() == fix.root_cause.lower()
            ):
                return entry
        return None

    def _find_duplicate_lesson(self, lesson: ArchitectureLesson) -> Optional[dict]:
        for entry in self.store["architecture_lessons"]:
            if (
                entry.get("lesson", "").lower() == lesson.lesson.lower()
                and entry.get("context", "").lower() == lesson.context.lower()
            ):
                return entry
        return None

    # -- Pruning ------------------------------------------------------------

    def prune_if_needed(self):
        if self.size_bytes() <= MAX_STORE_SIZE:
            return

        logger.info(
            "Store at %d bytes, pruning to %d", self.size_bytes(), PRUNE_TARGET_SIZE
        )
        self._prune_section("patterns")
        self._prune_section("bug_fixes")
        self._prune_section("architecture_lessons")

        while self.size_bytes() > PRUNE_TARGET_SIZE:
            lowest = self._find_lowest_use_count_entry()
            if lowest is None:
                break
            section, idx = lowest
            self.store[section].pop(idx)
            logger.info("Pruned lowest-use_count entry from %s", section)

    def _prune_section(self, section: str):
        cutoff = time.time() - (PRUNE_AGE_DAYS * 86400)
        kept = []
        for entry in self.store.get(section, []):
            last_seen = entry.get("last_seen", "")
            if last_seen:
                try:
                    ts = datetime.fromisoformat(last_seen).timestamp()
                    if ts < cutoff and entry.get("use_count", 0) == 0:
                        continue
                except (ValueError, OSError):
                    pass
            kept.append(entry)
        self.store[section] = kept

    def _find_lowest_use_count_entry(self):
        candidates = []
        for section in ("patterns", "bug_fixes", "architecture_lessons"):
            for idx, entry in enumerate(self.store.get(section, [])):
                candidates.append((section, idx, entry.get("use_count", 0)))
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[2])
        sec, idx, _ = candidates[0]
        return sec, idx


# -- Learning Agent ---------------------------------------------------------


class LearningAgent:
    """Extracts reusable knowledge from completed runs."""

    def __init__(self, capability_store_path: str):
        self.store = CapabilityStore(capability_store_path)
        self.health = {
            "status": "healthy",
            "current_step": "idle",
            "items_processed": 0,
            "errors": [],
        }

    def process_run(
        self,
        run_state: dict,
        event_log: Optional[List[dict]] = None,
        test_results: Optional[dict] = None,
        run_id: str = "",
    ):
        """Main entry point — process a single completed run."""
        self.health["current_step"] = "reading_run_data"
        self.health["errors"] = []

        if not run_state:
            self.health["status"] = "failing"
            self.health["errors"].append("Cannot learn without completed run data")
            logger.warning("Learning agent rejected: no run state provided")
            return self._summary()

        now = datetime.now(timezone.utc).isoformat()

        # Extract patterns
        self.health["current_step"] = "extracting_patterns"
        patterns = self._extract_patterns(run_state, test_results, now, run_id)
        for p in patterns:
            self.store.upsert_pattern(p)
            self.health["items_processed"] += 1

        # Extract bug fixes
        self.health["current_step"] = "extracting_fixes"
        fixes = self._extract_bug_fixes(run_state, test_results, event_log, now, run_id)
        for f in fixes:
            self.store.upsert_bug_fix(f)
            self.health["items_processed"] += 1

        # Extract architecture lessons
        self.health["current_step"] = "extracting_lessons"
        lessons = self._extract_lessons(run_state, now, run_id)
        for l in lessons:
            self.store.upsert_lesson(l)
            self.health["items_processed"] += 1

        # Dedup and prune
        self.health["current_step"] = "deduplicating"
        self.health["current_step"] = "pruning"
        self.store.prune_if_needed()

        # Write store
        self.health["current_step"] = "writing_store"
        self.store.save()

        self.health["status"] = "healthy"
        self.health["current_step"] = "idle"
        logger.info(
            "Learning agent processed %d items from run %s",
            self.health["items_processed"],
            run_id or "unknown",
        )
        return self._summary()

    def _summary(self) -> dict:
        return {
            "health": dict(self.health),
            "store_size_bytes": self.store.size_bytes(),
            "totals": {
                "patterns": len(self.store.store["patterns"]),
                "bug_fixes": len(self.store.store["bug_fixes"]),
                "lessons": len(self.store.store["architecture_lessons"]),
            },
        }

    # -- Extraction heuristics ----------------------------------------------

    def _extract_patterns(
        self, run_state: dict, test_results: Optional[dict], now: str, run_id: str
    ) -> List[Pattern]:
        patterns = []
        status = run_state.get("status", "")
        if status == "completed" or status == "success":
            # Successful task decomposition
            tasks = run_state.get("tasks", [])
            if len(tasks) > 3:
                patterns.append(
                    Pattern(
                        context="task decomposition",
                        description=f"Successfully decomposed work into {len(tasks)} sub-tasks",
                        category="workflow",
                        first_seen=now,
                        last_seen=now,
                        run_ids=[run_id] if run_id else [],
                    )
                )

            # Successful validations
            if test_results and test_results.get("passed", 0) > 0:
                patterns.append(
                    Pattern(
                        context="test validation",
                        description=f"All {test_results['passed']} tests passed on first run",
                        category="testing",
                        first_seen=now,
                        last_seen=now,
                        run_ids=[run_id] if run_id else [],
                    )
                )

        # Extract tool usage patterns from event log
        if run_state.get("tool_actions"):
            tool_names = [a.get("tool_name", "") for a in run_state["tool_actions"]]
            unique_tools = set(tool_names)
            if len(unique_tools) >= 3:
                patterns.append(
                    Pattern(
                        context="tool orchestration",
                        description=f"Effective use of {len(unique_tools)} distinct tools: {', '.join(sorted(unique_tools))}",
                        category="tooling",
                        first_seen=now,
                        last_seen=now,
                        run_ids=[run_id] if run_id else [],
                    )
                )

        return patterns

    def _extract_bug_fixes(
        self,
        run_state: dict,
        test_results: Optional[dict],
        event_log: Optional[List[dict]],
        now: str,
        run_id: str,
    ) -> List[BugFix]:
        fixes = []

        # From test failures that were resolved
        if test_results and test_results.get("failed", 0) > 0:
            failures = test_results.get("failures", [])
            for failure in failures:
                fixes.append(
                    BugFix(
                        symptom=failure.get("symptom", "Test failure"),
                        root_cause=failure.get("root_cause", "Unknown"),
                        fix=failure.get("fix_applied", "Unknown fix"),
                        category="test",
                        first_seen=now,
                        last_seen=now,
                        run_ids=[run_id] if run_id else [],
                    )
                )

        # From event log error events
        if event_log:
            for event in event_log:
                if event.get("level") in ("error", "ERROR", "critical"):
                    fix_action = event.get("fix_applied")
                    if fix_action:
                        fixes.append(
                            BugFix(
                                symptom=event.get(
                                    "message", event.get("error", "Unknown error")
                                ),
                                root_cause=event.get(
                                    "root_cause", "Investigated during run"
                                ),
                                fix=fix_action,
                                category=event.get("category", "runtime"),
                                first_seen=now,
                                last_seen=now,
                                run_ids=[run_id] if run_id else [],
                            )
                        )

        return fixes

    def _extract_lessons(
        self, run_state: dict, now: str, run_id: str
    ) -> List[ArchitectureLesson]:
        lessons = []

        # From run metadata about architectural decisions
        decisions = run_state.get("decisions", [])
        for decision in decisions:
            lessons.append(
                ArchitectureLesson(
                    context=decision.get("context", "run execution"),
                    lesson=decision.get("lesson", decision.get("decision", "")),
                    impact=decision.get("impact", "unknown"),
                    category=decision.get("category", "general"),
                    first_seen=now,
                    last_seen=now,
                    run_ids=[run_id] if run_id else [],
                )
            )

        # From retries — if a run needed retries, there's a lesson
        retries = run_state.get("retries", 0)
        if retries > 0:
            lessons.append(
                ArchitectureLesson(
                    context="run reliability",
                    lesson=f"Run required {retries} retries — consider adding pre-flight checks",
                    impact="reduced execution time and resource waste",
                    category="reliability",
                    first_seen=now,
                    last_seen=now,
                    run_ids=[run_id] if run_id else [],
                )
            )

        return lessons
