"""Intentional silence handler for Phase 7.

Handles silence as deliberate communication - no follow-up, no escalation.
Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §8.3
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from ..presence.models import PresenceState
from .models import SilenceContext


class SilenceHandler:
    """Handles intentional silence as communication.

    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §8.3
    Silence is treated as valid information - no follow-up, no escalation.
    """

    def __init__(self) -> None:
        """Initialize silence handler."""
        self._active_silence: Optional[SilenceContext] = None

    def start_silence(self, timestamp: Optional[datetime] = None) -> SilenceContext:
        """Start tracking a silence period.

        Args:
            timestamp: Start timestamp (defaults to now).

        Returns:
            Silence context.
        """
        if timestamp is None:
            timestamp = datetime.now()

        self._active_silence = SilenceContext(
            silence_start=timestamp,
            silence_end=None,
            resolved_to_state="background",  # Default: Background Presence
        )

        return self._active_silence

    def resolve_silence(
        self, resolved_to_state: str = "background", timestamp: Optional[datetime] = None
    ) -> Optional[SilenceContext]:
        """Resolve silence to a presence state.

        Per spec: §8.3 - Silence resolves to Background Presence (default).

        Args:
            resolved_to_state: Presence state to resolve to (default: "background").
            timestamp: Resolution timestamp (defaults to now).

        Returns:
            Resolved silence context, or None if no active silence.
        """
        if not self._active_silence:
            return None

        if timestamp is None:
            timestamp = datetime.now()

        self._active_silence.silence_end = timestamp
        self._active_silence.resolved_to_state = resolved_to_state

        resolved = self._active_silence
        self._active_silence = None

        return resolved

    def get_active_silence(self) -> Optional[SilenceContext]:
        """Get active silence context if any.

        Returns:
            Active silence context, or None.
        """
        return self._active_silence

    def is_silence_active(self) -> bool:
        """Check if silence is currently active.

        Returns:
            True if silence is active, False otherwise.
        """
        return self._active_silence is not None


