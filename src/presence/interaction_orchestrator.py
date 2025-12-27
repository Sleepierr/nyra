"""Interaction orchestrator for Phase 7.

Orchestrates real-time interaction decisions (immediate vs inboxed).
Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §1
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from .embodiment_handler import EmbodimentHandler
from .models import EmbodimentType, InteractionDecision, PresenceState
from .presence_manager import PresenceManager


class InteractionOrchestrator:
    """Orchestrates interaction decisions and presence management.

    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md
    Phase 7: Real-time interaction decisions, presence selection integration.
    """

    def __init__(self, presence_manager: PresenceManager, embodiment_handler: EmbodimentHandler) -> None:
        """Initialize interaction orchestrator.

        Args:
            presence_manager: Presence manager instance.
            embodiment_handler: Embodiment handler instance.
        """
        self._presence_manager = presence_manager
        self._embodiment_handler = embodiment_handler
        self._last_interaction_time: Optional[datetime] = None
        self._interaction_history: list[datetime] = []

    def decide_interaction(
        self,
        message_urgency: float = 0.5,  # 0.0-1.0
        user_available: bool = False,
        embodiment_type: EmbodimentType = EmbodimentType.MAC,
        cognitive_load: Optional[float] = None,
    ) -> InteractionDecision:
        """Decide whether to respond immediately or inbox.

        Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §1

        Args:
            message_urgency: Urgency level (0.0-1.0)
            user_available: Whether user is currently available
            embodiment_type: Device embodiment type
            cognitive_load: Estimated cognitive load (0.0-1.0)

        Returns:
            Interaction decision with reasoning.
        """
        current_state = self._presence_manager.get_current_state()
        respond_immediately = False
        reasoning = None

        # Guarded Presence: respond immediately if critical
        if current_state == PresenceState.GUARDED:
            respond_immediately = message_urgency > 0.8
            reasoning = "guarded_presence_critical" if respond_immediately else "guarded_presence_normal"

        # Active Presence: respond immediately if available
        elif current_state == PresenceState.ACTIVE:
            respond_immediately = user_available and message_urgency > 0.3
            reasoning = "active_presence_available" if respond_immediately else "active_presence_inboxed"

        # Background Presence: inbox only
        elif current_state == PresenceState.BACKGROUND:
            respond_immediately = False
            reasoning = "background_presence_inboxed"

        # Quiet Presence: respond when prompted, low urgency inbox
        elif current_state == PresenceState.QUIET:
            respond_immediately = user_available and message_urgency > 0.5
            reasoning = "quiet_presence_prompted" if respond_immediately else "quiet_presence_inboxed"

        # Reflective Presence: slower pacing, respond if important
        elif current_state == PresenceState.REFLECTIVE:
            respond_immediately = user_available and message_urgency > 0.6
            reasoning = "reflective_presence_important" if respond_immediately else "reflective_presence_inboxed"

        # Playful Presence: respond immediately if available
        elif current_state == PresenceState.PLAYFUL:
            respond_immediately = user_available and message_urgency > 0.4
            reasoning = "playful_presence_available" if respond_immediately else "playful_presence_inboxed"

        # Cognitive load override: high load → inbox
        if cognitive_load is not None and cognitive_load > 0.8:
            respond_immediately = False
            reasoning = "high_cognitive_load_inboxed"

        # Update interaction history
        if respond_immediately:
            self._last_interaction_time = datetime.now()
            self._interaction_history.append(datetime.now())
            # Keep only last 100 interactions
            if len(self._interaction_history) > 100:
                self._interaction_history = self._interaction_history[-100:]

        return InteractionDecision(
            respond_immediately=respond_immediately,
            reasoning=reasoning,
            presence_state=current_state,
            timestamp=datetime.now(),
        )

    def get_interaction_recency(self) -> Optional[float]:
        """Get time since last interaction in seconds.

        Returns:
            Seconds since last interaction, or None if no interactions.
        """
        if not self._last_interaction_time:
            return None

        return (datetime.now() - self._last_interaction_time).total_seconds()


