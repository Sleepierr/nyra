"""Event integration for gate persistence system.

Provides hooks to integrate gate event logging with the event emission system.
"""

from __future__ import annotations

from typing import Optional

from ..state.models.event_envelope import EventEnvelope
from .event_logger import EventLogger


class GateEventEmitter:
    """Event emitter wrapper that logs events to gate."""

    def __init__(self, event_logger: Optional[EventLogger] = None):
        """Initialize gate event emitter.

        Args:
            event_logger: Optional EventLogger for persistence.
        """
        self._event_logger = event_logger

    def emit(self, event: EventEnvelope) -> None:
        """Emit an event and log it to gate if logger is available.

        Args:
            event: EventEnvelope to emit.
        """
        if self._event_logger:
            self._event_logger.log_event(event)


def create_gate_event_hook(event_logger: EventLogger):
    """Create an event hook function for integration.

    Args:
        event_logger: EventLogger instance.

    Returns:
        Callable that can be registered with event system.
    """
    def hook(event: EventEnvelope) -> None:
        """Event hook that logs to gate."""
        event_logger.log_event(event)

    return hook

