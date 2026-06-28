"""In-memory event bus for Server-Sent Events."""

import asyncio
from datetime import datetime, timezone
from typing import AsyncGenerator, Dict


class EventBus:
    """Simple in-memory publish/subscribe bus for live dashboard updates."""

    def __init__(self):
        self._queues: Dict[int, asyncio.Queue] = {}
        self._counter = 0

    def subscribe(self) -> asyncio.Queue:
        """Create and register a new subscription queue."""
        self._counter += 1
        queue: asyncio.Queue = asyncio.Queue(maxsize=128)
        self._queues[self._counter] = queue
        return queue

    def unsubscribe(self, queue: asyncio.Queue) -> None:
        """Remove a subscription queue."""
        for key, q in list(self._queues.items()):
            if q is queue:
                del self._queues[key]
                return

    async def broadcast(self, event_type: str, payload: dict) -> None:
        """Publish an event to all active subscribers."""
        message = {
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        dead = []
        for queue in self._queues.values():
            try:
                queue.put_nowait(message)
            except asyncio.QueueFull:
                dead.append(queue)
        for queue in dead:
            self.unsubscribe(queue)

    async def stream(self, queue: asyncio.Queue) -> AsyncGenerator[str, None]:
        """Yield SSE-formatted lines from a subscription queue."""
        try:
            while True:
                message = await queue.get()
                data = __import__("json").dumps(message)
                yield f"event: {message['type']}\ndata: {data}\n\n"
        except asyncio.CancelledError:
            self.unsubscribe(queue)
            raise


# Global event bus instance
_bus = EventBus()


def get_bus() -> EventBus:
    return _bus
