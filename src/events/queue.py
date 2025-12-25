"""Event queue infrastructure for Phase 4.

Provides in-memory FIFO queue for event buffering and ordering.

Phase 4: In-memory only - no persistence.
"""

from __future__ import annotations

import threading
from typing import List, Optional

from ..state.models.event_envelope import EventEnvelope


class EventQueue:
    """In-memory FIFO queue for EventEnvelope instances.

    Orders events by `seq` if available, otherwise by `ts_utc` timestamp.
    Thread-safe operations for Phase 4 basic concurrency.

    Phase 4: No persistence - all events are in-memory only.
    """

    def __init__(self) -> None:
        """Initialize an empty event queue."""
        self._events: List[EventEnvelope] = []
        self._lock = threading.Lock()

    def enqueue(self, event: EventEnvelope) -> None:
        """Add an event to the queue.

        Events are inserted in order: by `seq` if available, otherwise by `ts_utc`.

        Args:
            event: The event envelope to add to the queue.
        """
        with self._lock:
            self._events.append(event)
            # Sort by seq if available (seq > 0), otherwise by ts_utc timestamp
            # Per spec: seq is the canonical ordering key, so seq>0 events take precedence
            # Events with seq=0 are sorted chronologically by ts_utc among themselves
            self._events.sort(key=lambda e: (e.seq if e.seq > 0 else float("inf"), e.ts_utc))

    def dequeue(self) -> Optional[EventEnvelope]:
        """Remove and return the first event from the queue.

        Returns:
            The first event in the queue, or None if the queue is empty.
        """
        with self._lock:
            if not self._events:
                return None
            return self._events.pop(0)

    def peek(self) -> Optional[EventEnvelope]:
        """Return the first event without removing it.

        Returns:
            The first event in the queue, or None if the queue is empty.
        """
        with self._lock:
            if not self._events:
                return None
            return self._events[0]

    def size(self) -> int:
        """Return the number of events in the queue.

        Returns:
            The number of events currently in the queue.
        """
        with self._lock:
            return len(self._events)

    def is_empty(self) -> bool:
        """Check if the queue is empty.

        Returns:
            True if the queue is empty, False otherwise.
        """
        return self.size() == 0

    def clear(self) -> None:
        """Remove all events from the queue."""
        with self._lock:
            self._events.clear()


