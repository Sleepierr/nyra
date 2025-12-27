"""Presence executor for Phase 7.

Integrates all Phase 7 components: presence, communication, social rhythm, notifications, relational, media.
Per spec: Phase 7 - Interaction, Presence & User-Facing Surface Behavior
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ...communication import (
    ExpressionManager,
    IntentManager,
    LayerOrchestrator,
    ToneManager,
)
from ...media import AppreciationManager
from ...notifications import NotificationManager
from ...presence import (
    EmbodimentHandler,
    InteractionOrchestrator,
    PresenceManager,
)
from ...relational import BoundaryManager, RoleEnforcer, SisterRelationalEngine
from ...social_rhythm import (
    CheckInManager,
    PacingManager,
    QuietHoursManager,
    RhythmManager,
    SilenceHandler,
)
from ...state.keys import SubsystemKeys
from .base import SubsystemExecutor


class PresenceExecutor(SubsystemExecutor):
    """Executes Phase 7 presence and interaction logic.

    Phase 7: Controls how Nyra communicates, paces, and presents herself
    without changing cognition or learning systems.
    """

    def __init__(self) -> None:
        """Initialize presence executor."""
        super().__init__(SubsystemKeys.INTERACTION_PRESENCE_LAYER)
        self._presence_manager: Optional[PresenceManager] = None
        self._interaction_orchestrator: Optional[InteractionOrchestrator] = None
        self._embodiment_handler: Optional[EmbodimentHandler] = None
        self._tone_manager: Optional[ToneManager] = None
        self._expression_manager: Optional[ExpressionManager] = None
        self._intent_manager: Optional[IntentManager] = None
        self._layer_orchestrator: Optional[LayerOrchestrator] = None
        self._quiet_hours_manager: Optional[QuietHoursManager] = None
        self._pacing_manager: Optional[PacingManager] = None
        self._silence_handler: Optional[SilenceHandler] = None
        self._check_in_manager: Optional[CheckInManager] = None
        self._rhythm_manager: Optional[RhythmManager] = None
        self._notification_manager: Optional[NotificationManager] = None
        self._sister_engine: Optional[SisterRelationalEngine] = None
        self._role_enforcer: Optional[RoleEnforcer] = None
        self._boundary_manager: Optional[BoundaryManager] = None
        self._appreciation_manager: Optional[AppreciationManager] = None

    def _on_initialized(self) -> None:
        """Initialize all Phase 7 components and subscribe to events."""
        if self._context is None:
            return

        # Initialize Presence & Interaction Layer
        self._presence_manager = PresenceManager()
        self._embodiment_handler = EmbodimentHandler()
        self._interaction_orchestrator = InteractionOrchestrator(
            self._presence_manager, self._embodiment_handler
        )

        # Initialize Communication Layers
        self._tone_manager = ToneManager()
        self._expression_manager = ExpressionManager()
        self._intent_manager = IntentManager()
        self._layer_orchestrator = LayerOrchestrator(
            self._tone_manager, self._expression_manager, self._intent_manager
        )

        # Initialize Social Rhythm Engine
        self._quiet_hours_manager = QuietHoursManager()
        self._pacing_manager = PacingManager()
        self._silence_handler = SilenceHandler()
        self._check_in_manager = CheckInManager()
        self._rhythm_manager = RhythmManager(
            self._quiet_hours_manager,
            self._pacing_manager,
            self._silence_handler,
            self._check_in_manager,
        )

        # Initialize Notification Manager
        self._notification_manager = NotificationManager(
            self._quiet_hours_manager,
            self._pacing_manager,
            self._context.instance_id,
        )

        # Initialize Relational Safety & Boundaries
        self._sister_engine = SisterRelationalEngine()
        self._role_enforcer = RoleEnforcer()
        self._boundary_manager = BoundaryManager(self._role_enforcer)

        # Initialize Media Appreciation
        self._appreciation_manager = AppreciationManager()

        # Subscribe to Phase 5/6 events (read-only access for context)
        self._context.event_bus.subscribe("emotion.*", self._on_emotion_event)
        self._context.event_bus.subscribe("autonomy.*", self._on_autonomy_event)
        self._context.event_bus.subscribe("goal.*", self._on_goal_event)
        self._context.event_bus.subscribe("interaction.*", self._on_interaction_event)
        self._context.event_bus.subscribe("debate.*", self._on_debate_event)
        self._context.event_bus.subscribe("system.*", self._on_system_event)

    def _on_emotion_event(self, event: Any) -> None:
        """Handle emotion events for presence/communication selection.

        Phase 7: Reads emotional state for presence/communication decisions.
        """
        # Phase 7: Use emotional state for presence selection and communication layers
        # This is read-only - Phase 7 doesn't modify emotional state
        pass

    def _on_autonomy_event(self, event: Any) -> None:
        """Handle autonomy events for expression level bounds.

        Phase 7: Reads autonomy band for expression level and chaos intensity bounds.
        """
        # Phase 7: Use autonomy band for expression level and chaos intensity
        # This is read-only - Phase 7 doesn't modify autonomy
        pass

    def _on_goal_event(self, event: Any) -> None:
        """Handle goal events for notification class selection.

        Phase 7: Uses goal events to determine notification classes (e.g., action_needed).
        """
        # Phase 7: Determine notification classes based on goal events
        pass

    def _on_interaction_event(self, event: Any) -> None:
        """Handle interaction events for presence/interaction decisions.

        Phase 7: Uses interaction events for presence selection and interaction decisions.
        """
        # Phase 7: Update presence and interaction decisions based on interaction events
        pass

    def _on_debate_event(self, event: Any) -> None:
        """Handle debate events for reflective presence triggers.

        Phase 7: Uses debate completion for reflective presence triggers.
        """
        # Phase 7: Trigger reflective presence after debate completion
        pass

    def _on_system_event(self, event: Any) -> None:
        """Handle system events for safety/critical notifications.

        Phase 7: Uses system events for Safety/Critical notifications.
        """
        # Phase 7: Create Safety/Critical notifications for system events
        pass

    def _execute_impl(self, input_data: Any) -> Dict[str, Any]:
        """Execute Phase 7 presence and interaction logic.

        Args:
            input_data: Optional input data.

        Returns:
            Dictionary with Phase 7 execution results.
        """
        if not self._presence_manager or not self._layer_orchestrator:
            raise RuntimeError("Phase 7 components not initialized")

        # Get current presence state
        current_presence = self._presence_manager.get_current_state()

        # Get current communication layer config
        comm_config = self._layer_orchestrator.get_current_config()

        return {
            "presence_state": current_presence.value,
            "tone": comm_config.tone.value,
            "expression_level": comm_config.expression_level.value,
            "intent": comm_config.intent.value,
            "modifier": comm_config.modifier.value if comm_config.modifier else None,
        }


