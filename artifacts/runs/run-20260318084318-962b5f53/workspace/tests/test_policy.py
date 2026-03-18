from skyforce.runtime.policy_engine import PolicyEngine


def test_policy_engine_loads_enabled_policy_files(repo_root):
    engine = PolicyEngine(repo_root)
    assert "block_secret_in_code" in engine.policy_bundle
    assert "network_write_gate" in engine.policy_bundle
    assert "deployment_gate" in engine.policy_bundle


def test_policy_engine_blocks_secret_output(repo_root):
    engine = PolicyEngine(repo_root)
    decision = engine.check_output_for_secrets(
        "run-test", "coding_agent", {"token": "sk-abcdefghijklmnopqrstuvwxyz123456"}
    )
    assert decision.allowed is False
    assert decision.rule_id == "block_secret_in_code"


def test_policy_engine_defers_for_connectivity(repo_root):
    engine = PolicyEngine(repo_root)
    decision = engine.check_step_start(
        repo_root / "artifacts" / "runs",
        "run-test",
        {"id": "dependency_scan", "requires_connectivity": "online_read"},
        {"connectivity_mode": "offline"},
    )
    assert decision.allowed is False
    assert decision.action == "defer"
    assert decision.rule_id == "network_write_gate"
