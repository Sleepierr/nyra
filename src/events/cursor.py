"""Cursor management infrastructure for Phase 4.

Provides cursor encoding/decoding and cursor state management via StateContainer.

Per spec/base1.0/nyrahome_cloud_spec.md §2: Cursor format is s:<seq>
"""

from __future__ import annotations

import re
from typing import List, Optional, TYPE_CHECKING

from ..state.keys import SyncKeys
from ..state.models.cursor import Cursor
from ..state.models.event_envelope import EventEnvelope

if TYPE_CHECKING:
    from ..state.container import StateContainer


class CursorCodec:
    """Utility class for encoding and decoding cursor strings.

    Cursor format per spec: `s:<seq>` where seq is an int64 sequence number.
    """

    # Regex pattern for cursor format: s:<digits>
    _CURSOR_PATTERN = re.compile(r"^s:(\d+)$")

    @staticmethod
    def encode(seq: int) -> str:
        """Encode a sequence number into a cursor string.

        Args:
            seq: The sequence number to encode.

        Returns:
            A cursor string in the format `s:<seq>`.

        Raises:
            ValueError: If seq is negative.
        """
        if seq < 0:
            raise ValueError(f"Sequence number must be non-negative, got: {seq}")
        return f"s:{seq}"

    @staticmethod
    def decode(cursor: str) -> Optional[int]:
        """Decode a cursor string into a sequence number.

        Args:
            cursor: The cursor string to decode (format: `s:<seq>`).

        Returns:
            The sequence number, or None if the cursor format is invalid.
        """
        match = CursorCodec._CURSOR_PATTERN.match(cursor)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None

    @staticmethod
    def is_valid(cursor: str) -> bool:
        """Check if a cursor string has valid format.

        Args:
            cursor: The cursor string to validate.

        Returns:
            True if the cursor format is valid, False otherwise.
        """
        return CursorCodec.decode(cursor) is not None

    @staticmethod
    def initial_cursor() -> str:
        """Return the canonical starting cursor.

        Per spec: `s:0` is the canonical starting cursor.

        Returns:
            The starting cursor string `s:0`.
        """
        return "s:0"


class CursorManager:
    """Manages cursor state via StateContainer.

    Provides methods to get, update, and advance cursors based on event sequences.
    """

    def __init__(self, container: "StateContainer") -> None:
        """Initialize the cursor manager.

        Args:
            container: The state container for cursor storage.
        """
        self._container = container
        self._codec = CursorCodec()

    def get_current_cursor(self) -> Optional[Cursor]:
        """Retrieve the current cursor from state.

        Returns:
            The current Cursor instance, or None if not set.
        """
        cursor_model = self._container.try_get(SyncKeys.EVENT_CURSOR.value)
        if cursor_model is None:
            return None
        if not isinstance(cursor_model, Cursor):
            return None
        return cursor_model

    def get_current_cursor_string(self) -> str:
        """Get the current cursor as a string, or return initial cursor.

        Returns:
            The current cursor string, or `s:0` if not set.
        """
        cursor = self.get_current_cursor()
        if cursor is None:
            return CursorCodec.initial_cursor()
        return cursor.__root__

    def update_cursor(self, cursor: Cursor) -> None:
        """Store a cursor in state.

        Args:
            cursor: The Cursor instance to store.
        """
        self._container.set(SyncKeys.EVENT_CURSOR.value, cursor)

    def update_cursor_string(self, cursor_str: str) -> None:
        """Store a cursor string in state.

        Args:
            cursor_str: The cursor string to store (format: `s:<seq>`).

        Raises:
            ValueError: If the cursor string format is invalid.
        """
        if not CursorCodec.is_valid(cursor_str):
            raise ValueError(f"Invalid cursor format: {cursor_str}")
        cursor = Cursor(__root__=cursor_str)
        self.update_cursor(cursor)

    def advance_cursor(self, events: List[EventEnvelope]) -> Cursor:
        """Compute and return the next cursor based on a list of events.

        Per spec: next_cursor = s:<max_seq_returned> if events are returned,
        otherwise next_cursor = input cursor.

        Args:
            events: List of events that were processed.

        Returns:
            A new Cursor instance representing the advanced cursor.
        """
        if not events:
            # No events returned - cursor stays the same
            current = self.get_current_cursor_string()
            return Cursor(__root__=current)

        # Find maximum sequence number (only consider events with seq > 0)
        valid_seqs = [event.seq for event in events if event.seq > 0]
        if not valid_seqs:
            # No valid sequences - cursor stays the same
            current = self.get_current_cursor_string()
            return Cursor(__root__=current)

        max_seq = max(valid_seqs)
        next_cursor_str = CursorCodec.encode(max_seq)
        return Cursor(__root__=next_cursor_str)

    def advance_and_store_cursor(self, events: List[EventEnvelope]) -> Cursor:
        """Advance the cursor based on events and store it in state.

        Args:
            events: List of events that were processed.

        Returns:
            The new Cursor instance that was stored.
        """
        new_cursor = self.advance_cursor(events)
        self.update_cursor(new_cursor)
        return new_cursor


