"""Event routing infrastructure for Phase 4.

Provides EventBus for routing events to handlers based on type patterns.

Phase 4: Pure routing - no interpretation or semantic processing.
"""

from __future__ import annotations

import threading
import uuid
from typing import Callable, Dict, List

from ..state.models.event_envelope import EventEnvelope


class EventBus:
    """Routes events to handlers based on event type patterns.

    Pattern matching:
    - Exact match: `interaction.message_received` matches exactly that
    - Prefix match: `interaction.*` matches all `interaction.*` event types
    - Suffix match: `*.message_received` matches all `*.message_received` event types

    Phase 4: Simple string pattern matching - no regex, no semantic interpretation.
    """

    def __init__(self) -> None:
        """Initialize an empty event bus."""
        self._subscriptions: Dict[str, Dict[str, Callable[[EventEnvelope], None]]] = {}
        self._lock = threading.Lock()

    def _match_pattern(self, pattern: str, event_type: str) -> bool:
        """Check if an event type matches a pattern.

        Args:
            pattern: The pattern to match (may contain `*` wildcards).
            event_type: The event type to check.

        Returns:
            True if the event type matches the pattern, False otherwise.
        """
        # Exact match
        if pattern == event_type:
            return True

        # Prefix match: pattern.*
        if pattern.endswith(".*"):
            prefix = pattern[:-2]  # Remove ".*"
            return event_type.startswith(prefix + ".")

        # Suffix match: *.suffix
        if pattern.startswith("*."):
            suffix = pattern[2:]  # Remove "*."
            return event_type.endswith("." + suffix)

        # Full wildcard
        if pattern == "*":
            return True

        return False

    def subscribe(
        self, pattern: str, handler: Callable[[EventEnvelope], None]
    ) -> str:
        """Subscribe a handler to events matching a pattern.

        Args:
            pattern: The event type pattern to match (e.g., "interaction.*").
            handler: Function to call when a matching event is emitted.

        Returns:
            A subscription ID for later unsubscription.
        """
        subscription_id = str(uuid.uuid4())

        with self._lock:
            if pattern not in self._subscriptions:
                self._subscriptions[pattern] = {}
            self._subscriptions[pattern][subscription_id] = handler

        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe a handler using its subscription ID.

        Args:
            subscription_id: The subscription ID returned by subscribe().
        """
        with self._lock:
            for pattern_subscriptions in self._subscriptions.values():
                pattern_subscriptions.pop(subscription_id, None)

            # Clean up empty patterns
            empty_patterns = [
                pattern
                for pattern, subs in self._subscriptions.items()
                if not subs
            ]
            for pattern in empty_patterns:
                self._subscriptions.pop(pattern, None)

    def emit(self, event: EventEnvelope) -> None:
        """Emit an event to all matching subscribers.

        Routes the event to all handlers whose patterns match the event type.

        Args:
            event: The event envelope to emit.
        """
        matching_handlers: List[Callable[[EventEnvelope], None]] = []

        with self._lock:
            for pattern, handlers in self._subscriptions.items():
                if self._match_pattern(pattern, event.type):
                    matching_handlers.extend(handlers.values())

        # Call handlers outside the lock to avoid deadlocks
        for handler in matching_handlers:
            try:
                handler(event)
            except Exception:
                # Phase 4: Basic error handling - log and continue
                pass

    def get_subscription_count(self) -> int:
        """Get the total number of active subscriptions.

        Returns:
            The total number of active subscriptions across all patterns.
        """
        with self._lock:
            return sum(len(handlers) for handlers in self._subscriptions.values())

