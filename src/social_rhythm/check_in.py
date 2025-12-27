"""Check-in mechanism for Phase 7.

Lightweight, non-demanding micro-interactions to assess availability.
Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §8
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from ..presence.models import PresenceState
from .models import CheckInRequest


class CheckInManager:
    """Manages lightweight check-in requests.

    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §8
    Phase 7: Brief, non-demanding micro-interactions, optional, ignorable, silence-safe.
    """

    def __init__(self) -> None:
        """Initialize check-in manager."""
        self._pending_check_ins: list[CheckInRequest] = []
        self._last_check_in: Optional[datetime] = None

    def is_eligible_for_check_in(
        self,
        current_presence_state: PresenceState,
        guarded_presence_active: bool = False,
        overload_detected: bool = False,
        do_not_disturb: bool = False,
    ) -> bool:
        """Check if check-in is eligible.

        Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §8.2

        Args:
            current_presence_state: Current presence state.
            guarded_presence_active: Whether Guarded Presence is active.
            overload_detected: Whether overload is detected.
            do_not_disturb: Whether explicit do-not-disturb signal is active.

        Returns:
            True if check-in is eligible, False otherwise.
        """
        # Check-ins forbidden during:
        if guarded_presence_active:
            return False
        if overload_detected:
            return False
        if do_not_disturb:
            return False

        # Check-ins only allowed in Quiet or Background Presence
        if current_presence_state not in (PresenceState.QUIET, PresenceState.BACKGROUND):
            return False

        return True

    def create_check_in(
        self,
        current_presence_state: PresenceState,
        timestamp: Optional[datetime] = None,
    ) -> Optional[CheckInRequest]:
        """Create a check-in request if eligible.

        Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §8.1

        Args:
            current_presence_state: Current presence state.
            timestamp: Check-in timestamp (defaults to now).

        Returns:
            CheckInRequest if created, None if not eligible.
        """
        if timestamp is None:
            timestamp = datetime.now()

        # Check eligibility
        if not self.is_eligible_for_check_in(current_presence_state):
            return None

        # Rate limiting: don't create check-ins too frequently
        if self._last_check_in:
            elapsed = (timestamp - self._last_check_in).total_seconds()
            if elapsed < 300:  # 5 minutes minimum between check-ins
                return None

        check_in = CheckInRequest(
            check_in_id=str(uuid.uuid4()),
            timestamp=timestamp,
            presence_state_required=current_presence_state.value,
        )

        self._pending_check_ins.append(check_in)
        self._last_check_in = timestamp

        return check_in

    def handle_check_in_response(
        self, check_in_id: str, response_type: str
    ) -> Optional[PresenceState]:
        """Handle check-in response and determine presence state.

        Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §8.4

        Args:
            check_in_id: Check-in request ID.
            response_type: Response type ("busy", "available_light", "available", "no_response").

        Returns:
            Recommended presence state, or None.
        """
        # Find check-in
        check_in = None
        for ci in self._pending_check_ins:
            if ci.check_in_id == check_in_id:
                check_in = ci
                break

        if not check_in:
            return None

        # Remove from pending
        self._pending_check_ins = [ci for ci in self._pending_check_ins if ci.check_in_id != check_in_id]

        # Map response to presence state (spec §8.4)
        if response_type == "busy" or response_type == "no_response":
            return PresenceState.BACKGROUND
        if response_type == "available_light":
            return PresenceState.QUIET
        if response_type == "available":
            return PresenceState.ACTIVE

        return None


