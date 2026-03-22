import asyncio
import json
import pytest
import datetime
from pathlib import Path

from skyforce.runtime.event_bus import EventBus, EventEnvelope

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

@pytest.mark.asyncio
async def test_event_bus_pubsub(temp_dir):
    bus = EventBus(root_dir=temp_dir)
    await bus.start()
    
    received_events = []
    
    async def my_handler(env: EventEnvelope):
        received_events.append(env)
        
    bus.subscribe("task.created", my_handler)
    
    await bus.emit("task.created", "orchestrator", {"task_id": "123"})
    
    # allow queue to process
    await asyncio.sleep(0.1)
    
    assert len(received_events) == 1
    assert received_events[0].event_type == "task.created"
    assert received_events[0].payload["task_id"] == "123"
    
    await bus.stop()

@pytest.mark.asyncio
async def test_event_bus_wildcard(temp_dir):
    bus = EventBus(root_dir=temp_dir)
    await bus.start()
    
    received_events = []
    
    async def orchestrator_handler(env: EventEnvelope):
        received_events.append(env)
        
    bus.subscribe("*", orchestrator_handler)
    
    await bus.emit("any.event", "source", {"k": "v"})
    await bus.emit("another.event", "source", {})
    
    await asyncio.sleep(0.1)
    
    assert len(received_events) == 2
    
    await bus.stop()

@pytest.mark.asyncio
async def test_event_bus_persistence(temp_dir):
    bus = EventBus(root_dir=temp_dir)
    await bus.start()
    
    await bus.emit("task.completed", "coding_agent", {"result": "ok"})
    await asyncio.sleep(0.1)
    
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    log_file = temp_dir / "logs" / "events" / f"{date_str}.ndjson"
    
    assert log_file.exists()
    content = log_file.read_text().strip()
    data = json.loads(content)
    assert data["event_type"] == "task.completed"
    assert data["source"] == "coding_agent"
    
    await bus.stop()

@pytest.mark.asyncio
async def test_event_bus_deferred(temp_dir):
    bus = EventBus(root_dir=temp_dir)
    bus.set_online(False)
    
    await bus.emit("test.event", "source", {"foo": "bar"})
    
    deferred_file = temp_dir / "runtime" / "deferred_events.json"
    assert deferred_file.exists()
    
    data = json.loads(deferred_file.read_text())
    assert len(data) == 1
    assert data[0]["event_type"] == "test.event"
    
    # now set online
    received = []
    async def hndlr(e): received.append(e)
    bus.subscribe("test.event", hndlr)
    
    await bus.start()
    bus.set_online(True)
    await asyncio.sleep(0.1)
    
    assert len(received) == 1
    assert received[0].payload["foo"] == "bar"
    assert not deferred_file.exists()
    
    await bus.stop()

@pytest.mark.asyncio
async def test_event_bus_poison(temp_dir):
    bus = EventBus(root_dir=temp_dir)
    await bus.start()
    
    async def failing_handler(env: EventEnvelope):
        raise ValueError("Simulated failure")
        
    bus.subscribe("fail.event", failing_handler)
    
    await bus.emit("fail.event", "test", {})
    await asyncio.sleep(0.1)
    
    dead_letters_dir = temp_dir / "logs" / "dead_letters"
    poison_files = list(dead_letters_dir.glob("*.json"))
    
    assert len(poison_files) == 1
    poison_data = json.loads(poison_files[0].read_text())
    assert poison_data["_poison_reason"] == "Simulated failure"
    assert poison_data["event_type"] == "fail.event"
    
    await bus.stop()
