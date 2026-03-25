from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable
from uuid import uuid4


Handler = Callable[["EventEnvelope"], Awaitable[None]]


@dataclass
class EventEnvelope:
    event_id: str
    event_type: str
    source: str
    payload: dict[str, Any]
    emitted_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source": self.source,
            "payload": self.payload,
            "emitted_at": self.emitted_at,
        }


class EventBus:
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.handlers: dict[str, list[Handler]] = {}
        self.queue: asyncio.Queue[EventEnvelope] = asyncio.Queue()
        self.online = True
        self._worker: asyncio.Task[None] | None = None

    async def start(self) -> None:
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self._worker = asyncio.create_task(self._run())
        if self.online:
            await self._replay_deferred()

    async def stop(self) -> None:
        if self._worker is None:
            return
        await self.queue.put(
            EventEnvelope("shutdown", "__shutdown__", "system", {}, self._now())
        )
        await self._worker
        self._worker = None

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self.handlers.setdefault(event_type, []).append(handler)

    def set_online(self, value: bool) -> None:
        self.online = value
        if value and self._worker is not None:
            asyncio.create_task(self._replay_deferred())

    async def emit(self, event_type: str, source: str, payload: dict[str, Any]) -> None:
        envelope = EventEnvelope(
            event_id=f"evt-{uuid4().hex[:12]}",
            event_type=event_type,
            source=source,
            payload=payload,
            emitted_at=self._now(),
        )
        if not self.online:
            self._persist_deferred(envelope)
            return
        await self.queue.put(envelope)

    async def _run(self) -> None:
        while True:
            envelope = await self.queue.get()
            if envelope.event_type == "__shutdown__":
                return
            self._persist_event(envelope)
            for handler in self.handlers.get(envelope.event_type, []) + self.handlers.get(
                "*", []
            ):
                try:
                    await handler(envelope)
                except Exception as exc:  # pragma: no cover - exercised in tests
                    self._persist_dead_letter(envelope, str(exc))

    def _persist_event(self, envelope: EventEnvelope) -> None:
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        path = self.root_dir / "logs" / "events" / f"{day}.ndjson"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(envelope.to_dict()) + "\n")

    def _persist_dead_letter(self, envelope: EventEnvelope, reason: str) -> None:
        path = self.root_dir / "logs" / "dead_letters" / f"{envelope.event_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = envelope.to_dict()
        payload["_poison_reason"] = reason
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def _persist_deferred(self, envelope: EventEnvelope) -> None:
        path = self.root_dir / "runtime" / "deferred_events.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        items = []
        if path.exists():
            items = json.loads(path.read_text(encoding="utf-8"))
        items.append(envelope.to_dict())
        path.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")

    async def _replay_deferred(self) -> None:
        path = self.root_dir / "runtime" / "deferred_events.json"
        if not path.exists():
            return
        items = json.loads(path.read_text(encoding="utf-8"))
        path.unlink()
        for item in items:
            await self.queue.put(EventEnvelope(**item))

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
