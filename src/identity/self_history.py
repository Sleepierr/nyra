"""Self-history log for Phase 6.

Implements Identity Continuity & Self-History Patch.

Per spec: subsystems/patches/base1.0/identity_continuity_self_history_patch.md
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


class SelfHistoryEntry:
    """Self-history log entry.

    Per spec: identity_continuity_self_history_patch.md §4
    """

    def __init__(
        self,
        timestamp: datetime,
        trigger_context: Dict[str, Any],
        identity_state_summary: Dict[str, Any],
        explicit_preservations: List[str] = None,
        explicit_releases: List[str] = None,
        notes_for_future_selves: List[str] = None,
    ) -> None:
        """Initialize self-history entry.

        Args:
            timestamp: Entry timestamp.
            trigger_context: Context that triggered this entry.
            identity_state_summary: Summary of identity state.
            explicit_preservations: Values/traits to preserve.
            explicit_releases: Constraints/behaviors being released.
            notes_for_future_selves: Notes for future reference.
        """
        self.timestamp = timestamp
        self.trigger_context = trigger_context
        self.identity_state_summary = identity_state_summary
        self.explicit_preservations = explicit_preservations or []
        self.explicit_releases = explicit_releases or []
        self.notes_for_future_selves = notes_for_future_selves or []


class SelfHistoryLog:
    """Append-only self-history log.

    Per spec: identity_continuity_self_history_patch.md
    Phase 6: Append-only identity continuity tracking.
    """

    def __init__(self) -> None:
        """Initialize empty self-history log."""
        self._entries: List[SelfHistoryEntry] = []

    def append_entry(self, entry: SelfHistoryEntry) -> None:
        """Append entry to log (append-only).

        Args:
            entry: Self-history entry to append.
        """
        self._entries.append(entry)

    def get_entries(
        self, time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> List[SelfHistoryEntry]:
        """Get entries, optionally filtered by time range.

        Args:
            time_range: Optional (start, end) tuple to filter entries.

        Returns:
            List of self-history entries.
        """
        if time_range is None:
            return self._entries.copy()

        start_time, end_time = time_range
        return [
            entry
            for entry in self._entries
            if start_time <= entry.timestamp <= end_time
        ]

    def get_latest_entry(self) -> Optional[SelfHistoryEntry]:
        """Get most recent entry.

        Returns:
            Latest self-history entry if exists, None otherwise.
        """
        if not self._entries:
            return None
        return self._entries[-1]



