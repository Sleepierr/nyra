"""Presence state manager for Phase 7.

Manages presence state selection and transitions via signal convergence.
Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §5
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from .models import PresenceState, PresenceTransition


class PresenceManager:
    """Manages presence state selection and transitions.

    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md
    Phase 7: Signal convergence for presence selection, smooth transitions.
    """

    def __init__(self) -> None:
        """Initialize presence manager."""
        self._current_state: PresenceState = PresenceState.QUIET  # Default: Quiet Presence
        self._last_transition: Optional[PresenceTransition] = None
        self._minimum_dwell_seconds: int = 30  # Minimum time before next transition

    def get_current_state(self) -> PresenceState:
        """Get current presence state."""
        return self._current_state

    def select_presence(
        self,
        emotional_state: Optional[Dict[str, Any]] = None,
        autonomy_band: Optional[int] = None,
        cognitive_load: Optional[float] = None,
        safety_gate_override: bool = False,
        explicit_engagement: bool = False,
        extended_silence: bool = False,
        emotional_disclosure: bool = False,
        play_cues: bool = False,
    ) -> PresenceState:
        """Select presence state via signal convergence.

        Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §5.3

        Args:
            emotional_state: Emotional state dict (valence, arousal, stability)
            autonomy_band: Current autonomy band (0-100)
            cognitive_load: Cognitive load estimate (0.0-1.0)
            safety_gate_override: Guardian facet override → Guarded Presence
            explicit_engagement: Explicit user engagement → Active Presence
            extended_silence: Extended silence → Background Presence
            emotional_disclosure: Emotional disclosure → Reflective Presence
            play_cues: Play cues + safety → Playful Presence

        Returns:
            Selected presence state.
        """
        # Step 1: Safety Gate - Guardian override
        if safety_gate_override:
            return PresenceState.GUARDED

        # Step 2: Default rules (spec §6)
        if extended_silence:
            return PresenceState.BACKGROUND
        if emotional_disclosure:
            return PresenceState.REFLECTIVE
        if explicit_engagement:
            return PresenceState.ACTIVE
        if play_cues and autonomy_band is not None and autonomy_band >= 40:
            # Playful Presence only when safety and autonomy allow
            return PresenceState.PLAYFUL

        # Step 3: Cognitive Load Check
        if cognitive_load is not None and cognitive_load > 0.7:
            # High cognitive load → favor quiet/background
            return PresenceState.QUIET

        # Step 4: Emotional Alignment
        if emotional_state:
            stability = emotional_state.get("stability", 0.8)
            valence = emotional_state.get("valence", 0.0)
            if stability < 0.5:
                # Low stability → reflective or quiet
                return PresenceState.REFLECTIVE
            if valence < -0.3:
                # Negative valence → reflective presence
                return PresenceState.REFLECTIVE

        # Default: Quiet Presence (spec §6 - no signal → Quiet Presence)
        return PresenceState.QUIET

    def transition_to(
        self, new_state: PresenceState, enforce_dwell_time: bool = True
    ) -> Optional[PresenceTransition]:
        """Transition to a new presence state with minimum dwell time enforcement.

        Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §7

        Args:
            new_state: Target presence state.
            enforce_dwell_time: Whether to enforce minimum dwell time.

        Returns:
            PresenceTransition if transition occurred, None if blocked by dwell time.
        """
        # Check minimum dwell time
        if enforce_dwell_time and self._last_transition:
            elapsed = (datetime.now() - self._last_transition.timestamp).total_seconds()
            if elapsed < self._minimum_dwell_seconds:
                # Transition blocked by minimum dwell time
                return None

        # Prevent same-state transitions
        if new_state == self._current_state:
            return None

        # Create transition
        transition = PresenceTransition(
            from_state=self._current_state,
            to_state=new_state,
            timestamp=datetime.now(),
            minimum_dwell_seconds=self._minimum_dwell_seconds,
        )

        # Update state
        self._current_state = new_state
        self._last_transition = transition

        return transition

    def can_transition(self) -> bool:
        """Check if a transition is allowed (respecting minimum dwell time)."""
        if not self._last_transition:
            return True

        elapsed = (datetime.now() - self._last_transition.timestamp).total_seconds()
        return elapsed >= self._minimum_dwell_seconds


