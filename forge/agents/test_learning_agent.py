import json
import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent.parent / "forge" / "agents")
)

import learning_agent
from learning_agent import (
    LearningAgent,
    CapabilityStore,
    Pattern,
    BugFix,
    ArchitectureLesson,
)


def _make_store(tmpdir: str) -> str:
    return os.path.join(tmpdir, "capability_store.json")


def _make_run_state(**overrides) -> dict:
    state = {
        "status": "completed",
        "tasks": [{"id": "t1"}, {"id": "t2"}, {"id": "t3"}, {"id": "t4"}],
        "tool_actions": [
            {"tool_name": "bash"},
            {"tool_name": "read"},
            {"tool_name": "edit"},
        ],
        "decisions": [
            {
                "context": "service extraction",
                "lesson": "Extract shared providers before they become coupling hazards",
                "impact": "reduced cross-repo dependencies",
                "category": "architecture",
            }
        ],
        "retries": 0,
    }
    state.update(overrides)
    return state


def _make_test_results(**overrides) -> dict:
    result = {"passed": 5, "failed": 0}
    result.update(overrides)
    return result


def test_store_creates_empty():
    with tempfile.TemporaryDirectory() as td:
        path = _make_store(td)
        store = CapabilityStore(path)
        assert store.store["patterns"] == []
        assert store.store["bug_fixes"] == []
        assert store.store["architecture_lessons"] == []
        assert store.store["version"] == "0.1.0"


def test_store_upsert_pattern_new():
    with tempfile.TemporaryDirectory() as td:
        store = CapabilityStore(_make_store(td))
        store.upsert_pattern(
            Pattern(
                context="test",
                description="good pattern",
                category="testing",
                first_seen="2026-01-01",
                last_seen="2026-01-01",
            )
        )
        assert len(store.store["patterns"]) == 1
        assert store.store["patterns"][0]["description"] == "good pattern"


def test_store_upsert_pattern_dedup():
    with tempfile.TemporaryDirectory() as td:
        store = CapabilityStore(_make_store(td))
        store.upsert_pattern(
            Pattern(
                context="test",
                description="same pattern",
                category="testing",
                first_seen="2026-01-01",
                last_seen="2026-01-01",
            )
        )
        store.upsert_pattern(
            Pattern(
                context="test",
                description="same pattern",
                category="testing",
                first_seen="2026-02-01",
                last_seen="2026-02-01",
            )
        )
        assert len(store.store["patterns"]) == 1
        assert store.store["patterns"][0]["use_count"] == 2


def test_store_save_and_reload():
    with tempfile.TemporaryDirectory() as td:
        path = _make_store(td)
        store = CapabilityStore(path)
        store.upsert_pattern(
            Pattern(
                context="x",
                description="persisted",
                category="y",
                first_seen="now",
                last_seen="now",
            )
        )
        store.save()

        store2 = CapabilityStore(path)
        assert len(store2.store["patterns"]) == 1
        assert store2.store["patterns"][0]["description"] == "persisted"


def test_store_prune_by_age():
    with tempfile.TemporaryDirectory() as td:
        store = CapabilityStore(_make_store(td))
        old = "2025-01-01T00:00:00+00:00"
        store.store["patterns"].append(
            {
                "context": "old",
                "description": "stale",
                "category": "x",
                "first_seen": old,
                "last_seen": old,
                "use_count": 0,
                "run_ids": [],
            }
        )
        store.store["patterns"].append(
            {
                "context": "new",
                "description": "fresh",
                "category": "x",
                "first_seen": "2026-04-01T00:00:00+00:00",
                "last_seen": "2026-04-01T00:00:00+00:00",
                "use_count": 1,
                "run_ids": [],
            }
        )
        original_max = learning_agent.MAX_STORE_SIZE
        learning_agent.MAX_STORE_SIZE = 10
        try:
            store.prune_if_needed()
            assert len(store.store["patterns"]) == 1
            assert store.store["patterns"][0]["description"] == "fresh"
        finally:
            learning_agent.MAX_STORE_SIZE = original_max


def test_agent_rejects_empty_run():
    with tempfile.TemporaryDirectory() as td:
        agent = LearningAgent(_make_store(td))
        result = agent.process_run({})
        assert result["health"]["status"] == "failing"
        assert result["health"]["errors"]


def test_agent_extracts_patterns():
    with tempfile.TemporaryDirectory() as td:
        agent = LearningAgent(_make_store(td))
        result = agent.process_run(
            run_state=_make_run_state(),
            test_results=_make_test_results(),
            run_id="run-001",
        )
        assert result["totals"]["patterns"] >= 2
        assert result["health"]["status"] == "healthy"


def test_agent_extracts_lessons():
    with tempfile.TemporaryDirectory() as td:
        agent = LearningAgent(_make_store(td))
        result = agent.process_run(
            run_state=_make_run_state(retries=2),
            run_id="run-002",
        )
        assert result["totals"]["lessons"] >= 2


def test_agent_extracts_bug_fixes():
    with tempfile.TemporaryDirectory() as td:
        agent = LearningAgent(_make_store(td))
        result = agent.process_run(
            run_state=_make_run_state(status="completed"),
            test_results=_make_test_results(
                failed=1,
                failures=[
                    {
                        "symptom": "TypeError on None",
                        "root_cause": "Missing null check",
                        "fix_applied": "Added guard clause",
                    }
                ],
            ),
            run_id="run-003",
        )
        assert result["totals"]["bug_fixes"] == 1
        assert result["health"]["status"] == "healthy"


def test_agent_dedup_on_second_run():
    with tempfile.TemporaryDirectory() as td:
        agent = LearningAgent(_make_store(td))
        agent.process_run(run_state=_make_run_state(), run_id="r1")
        agent.process_run(run_state=_make_run_state(), run_id="r2")
        assert len(agent.store.store["patterns"]) == 2


def test_agent_store_persists():
    with tempfile.TemporaryDirectory() as td:
        path = _make_store(td)
        agent = LearningAgent(path)
        agent.process_run(run_state=_make_run_state(), run_id="persist")

        agent2 = LearningAgent(path)
        assert agent2.store.store["patterns"]


if __name__ == "__main__":
    import unittest

    unittest.main()
