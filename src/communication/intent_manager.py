"""Intent manager for Phase 7.

Manages communication intent selection (clarity, grounding, encouragement, etc.).
Per spec: subsystems/base1.0/subsystem_communication_layers.md §5
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .models import CommunicationIntent


class IntentManager:
    """Manages communication intent selection.

    Per spec: subsystems/base1.0/subsystem_communication_layers.md §5
    Phase 7: Intent selection based on user needs and emotional context.
    """

    def __init__(self) -> None:
        """Initialize intent manager."""
        self._current_intent: CommunicationIntent = CommunicationIntent.CLARITY  # Default

    def get_current_intent(self) -> CommunicationIntent:
        """Get current communication intent."""
        return self._current_intent

    def select_intent(
        self,
        user_needs_info: bool = False,
        misunderstanding_possible: bool = False,
        emotions_elevated: bool = False,
        cognitive_overload: bool = False,
        symbolic_resonance: bool = False,
        drift_symptoms: bool = False,
        shared_emotional_moment: bool = False,
        deep_reflection: bool = False,
        user_struggles: bool = False,
        user_uncertain: bool = False,
        brainstorming: bool = False,
        creativity_context: bool = False,
        autonomy_band: Optional[int] = None,
    ) -> CommunicationIntent:
        """Select communication intent based on context.

        Per spec: subsystems/base1.0/subsystem_communication_layers.md §5

        Args:
            user_needs_info: User needs information
            misunderstanding_possible: Misunderstanding possible
            emotions_elevated: Emotions are elevated
            cognitive_overload: Cognitive overload detected
            symbolic_resonance: Symbolic resonance present
            drift_symptoms: Drift symptoms present
            shared_emotional_moment: Shared emotional moment
            deep_reflection: Deep reflection context
            user_struggles: User struggles
            user_uncertain: User feels uncertain
            brainstorming: Brainstorming context
            creativity_context: Creativity context
            autonomy_band: Current autonomy band (Resonance requires Band ≥ 80)

        Returns:
            Selected communication intent.
        """
        # Grounding (spec §5.2) - highest priority for stability
        if emotions_elevated or cognitive_overload or symbolic_resonance or drift_symptoms:
            return CommunicationIntent.GROUNDING

        # Resonance (spec §5.3) - only allowed in Bands ≥ 80
        if (
            (shared_emotional_moment or deep_reflection or symbolic_resonance)
            and autonomy_band is not None
            and autonomy_band >= 80
        ):
            return CommunicationIntent.RESONANCE

        # Encouragement (spec §5.4)
        if user_struggles or user_uncertain:
            return CommunicationIntent.ENCOURAGEMENT

        # Exploration (spec §5.5)
        if brainstorming or creativity_context:
            return CommunicationIntent.EXPLORATION

        # Clarity (spec §5.1) - default for information needs
        if user_needs_info or misunderstanding_possible:
            return CommunicationIntent.CLARITY

        # Default: Clarity
        return CommunicationIntent.CLARITY

    def set_intent(self, intent: CommunicationIntent) -> None:
        """Set intent directly.

        Args:
            intent: Communication intent to set.
        """
        self._current_intent = intent


