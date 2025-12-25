"""Emotional engine execution infrastructure for Phase 5.

Implements EmotionalEngineExecutor with Primary Mood Vector computation and influence mechanisms.

Phase 5: Basic emotional state computation and active influence on other subsystems.
Per spec: subsystems/base1.0/subsystem_emotional_engine.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import ExecutionContext, SubsystemExecutor
from ...state.keys import SubsystemKeys


# -----------------------------------------------------------------------------
# Data Structures
# -----------------------------------------------------------------------------


@dataclass
class PrimaryMoodVector:
    """Primary Mood Vector (PMV) - continuous affective state.

    Per spec: subsystem_emotional_engine.md §3
    Phase 5: Basic structure - simplified dimensions.
    """

    valence: float  # [-1.0, 1.0] (negative to positive)
    arousal: float  # [0.0, 1.0] (calm to activated)
    stability: float  # [0.0, 1.0] (unstable to stable)

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            "valence": self.valence,
            "arousal": self.arousal,
            "stability": self.stability,
        }


@dataclass
class EmotionalLoad:
    """Represents current emotional load level."""

    level: float  # [0.0, 1.0]
    load_type: str  # e.g., "cognitive", "relational", "systemic"


class EmotionalEngineExecutor(SubsystemExecutor):
    """Executes emotional engine logic.

    Phase 5: Basic PMV computation and influence mechanisms.
    """

    def __init__(self) -> None:
        """Initialize the emotional engine executor."""
        super().__init__(SubsystemKeys.EMOTIONAL_ENGINE)
        self._current_pmv: Optional[PrimaryMoodVector] = None

    def _on_initialized(self) -> None:
        """Initialize emotional state and subscribe to events."""
        # Initialize to neutral baseline
        self._current_pmv = PrimaryMoodVector(
            valence=0.0,
            arousal=0.3,
            stability=0.8,
        )

        # Subscribe to events that affect emotion
        if self._context:
            self._context.event_bus.subscribe("interaction.*", self._on_interaction)
            self._context.event_bus.subscribe("goal.*", self._on_goal_event)
            self._context.event_bus.subscribe("system.*", self._on_system_event)

    def _on_interaction(self, event: Any) -> None:
        """Handle interaction events affecting emotion.

        Phase 5: Basic handler - emit mood update.
        """
        if self._current_pmv:
            self.emit_influence_event(
                "emotion.mood_changed",
                {
                    "pmv": self._current_pmv.to_dict(),
                    "trigger": "interaction",
                },
            )

    def _on_goal_event(self, event: Any) -> None:
        """Handle goal-related events affecting emotion.

        Phase 5: Basic handler.
        """
        # Phase 5: Basic logic - goal completion may affect mood
        pass

    def _on_system_event(self, event: Any) -> None:
        """Handle system events affecting emotion.

        Phase 5: Basic handler.
        """
        # Phase 5: System events may affect emotional load
        pass

    def _execute_impl(self, input_data: Any) -> Dict[str, Any]:
        """Execute emotional engine processing.

        Args:
            input_data: Input affecting emotion (can be event, interaction, etc.).

        Returns:
            Dictionary with current PMV and emotional state.
        """
        if self._current_pmv is None:
            self._current_pmv = PrimaryMoodVector(valence=0.0, arousal=0.3, stability=0.8)

        # Phase 5: Basic emotional processing
        # Update PMV based on input (simplified)
        self._update_pmv(input_data)

        # Compute emotional load
        load = self._compute_emotional_load()

        # Emit influence event if mood changed significantly
        self._check_and_emit_mood_change()

        return {
            "pmv": self._current_pmv.to_dict(),
            "emotional_load": load.level,
            "load_type": load.load_type,
        }

    def _update_pmv(self, input_data: Any) -> None:
        """Update Primary Mood Vector based on input.

        Phase 5: Basic/minimal update logic - maintains stability.

        Args:
            input_data: Input affecting emotion.
        """
        if self._current_pmv is None:
            return

        # Phase 5: Basic logic - very minimal changes to maintain stability
        # Full emotional computation requires complex logic deferred to later phases
        # For now, we just ensure PMV stays in valid ranges and slowly returns to neutral

        # Decay toward neutral if no strong input
        self._current_pmv.valence *= 0.95  # Slight decay toward 0
        self._current_pmv.arousal = max(0.2, self._current_pmv.arousal * 0.98)  # Slight decay
        self._current_pmv.stability = min(0.9, self._current_pmv.stability * 1.01)  # Increase stability

        # Clamp values
        self._current_pmv.valence = max(-1.0, min(1.0, self._current_pmv.valence))
        self._current_pmv.arousal = max(0.0, min(1.0, self._current_pmv.arousal))
        self._current_pmv.stability = max(0.0, min(1.0, self._current_pmv.stability))

    def _compute_emotional_load(self) -> EmotionalLoad:
        """Compute current emotional load.

        Phase 5: Basic computation based on PMV.

        Returns:
            EmotionalLoad instance.
        """
        if self._current_pmv is None:
            return EmotionalLoad(level=0.0, load_type="neutral")

        # Phase 5: Basic load computation - higher arousal or lower stability = higher load
        load_level = (self._current_pmv.arousal + (1.0 - self._current_pmv.stability)) / 2.0
        load_type = "cognitive" if self._current_pmv.arousal > 0.5 else "neutral"

        return EmotionalLoad(level=load_level, load_type=load_type)

    def _check_and_emit_mood_change(self) -> None:
        """Check if mood changed significantly and emit event if so.

        Phase 5: Basic change detection.
        """
        # Phase 5: Emit on every update for now (simple approach)
        # More sophisticated change detection deferred
        if self._current_pmv:
            self.emit_influence_event(
                "emotion.pmv_updated",
                {
                    "pmv": self._current_pmv.to_dict(),
                },
            )

    @property
    def current_pmv(self) -> Optional[PrimaryMoodVector]:
        """Get current Primary Mood Vector.

        Returns:
            Current PMV or None if not initialized.
        """
        return self._current_pmv

    def get_emotional_load(self) -> float:
        """Get current emotional load level.

        Returns:
            Emotional load level [0.0, 1.0].
        """
        load = self._compute_emotional_load()
        return load.level

    def influence_goal_formation(
        self, goal_description: str, goal_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Active influence on goal formation based on emotional state.

        Phase 5: Basic influence - adjusts priority based on emotional load.

        Args:
            goal_description: Description of proposed goal.
            goal_context: Context about the goal.

        Returns:
            Dictionary with emotional influence adjustments.
        """
        load = self._compute_emotional_load()

        # Phase 5: Basic influence - higher load reduces goal priority
        priority_modifier = 1.0 - (load.level * 0.3)  # Reduce priority by up to 30%

        return {
            "priority_modifier": priority_modifier,
            "emotional_load": load.level,
            "recommendation": "proceed" if load.level < 0.7 else "defer",
        }

