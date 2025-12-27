"""Tone manager for Phase 7.

Manages tone selection and smooth transitions.
Per spec: subsystems/base1.0/subsystem_communication_layers.md §3
Per patch: subsystems/patches/base1.0/tone_transition_patch.md
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .models import ToneFamily, ToneTransition, ToneTransitionCurvature


class ToneManager:
    """Manages tone selection and transitions.

    Per spec: subsystems/base1.0/subsystem_communication_layers.md §3
    Per patch: tone_transition_patch.md - smooth tone transitions
    """

    def __init__(self) -> None:
        """Initialize tone manager."""
        self._current_tone: ToneFamily = ToneFamily.WARM_CLARITY  # Default tone
        self._last_transition: Optional[ToneTransition] = None

    def get_current_tone(self) -> ToneFamily:
        """Get current tone."""
        return self._current_tone

    def select_tone(
        self,
        presence_state: Optional[str] = None,
        emotional_state: Optional[Dict[str, Any]] = None,
        autonomy_band: Optional[int] = None,
        processing_mode: Optional[str] = None,
        context: Optional[str] = None,
    ) -> ToneFamily:
        """Select tone based on context and state.

        Per spec: subsystems/base1.0/subsystem_communication_layers.md §3

        Args:
            presence_state: Current presence state
            emotional_state: Emotional state dict
            autonomy_band: Current autonomy band
            processing_mode: Processing mode (balanced, focus, exploration, etc.)
            context: Context string (task, reflection, etc.)

        Returns:
            Selected tone family.
        """
        # Processing mode-based selection (spec §7)
        if processing_mode == "focus":
            return ToneFamily.FOCUS_STEADY
        if processing_mode == "exploration":
            return ToneFamily.PLAYFUL_SOFT
        if processing_mode == "grounding":
            return ToneFamily.GROUNDED_CALM

        # Presence state influence
        if presence_state == "reflective":
            return ToneFamily.DEEP_REFLECTIVE
        if presence_state == "guarded":
            return ToneFamily.GROUNDED_CALM
        if presence_state == "playful" and autonomy_band is not None and autonomy_band >= 40:
            return ToneFamily.PLAYFUL_SOFT

        # Emotional state influence
        if emotional_state:
            stability = emotional_state.get("stability", 0.8)
            valence = emotional_state.get("valence", 0.0)
            if stability < 0.5:
                return ToneFamily.GROUNDED_CALM
            if valence < -0.3:
                return ToneFamily.DEEP_REFLECTIVE

        # Context-based selection
        if context == "task" or context == "coding":
            return ToneFamily.FOCUS_STEADY

        # Default: Warm-Clarity (spec §3.1 - default relational tone)
        return ToneFamily.WARM_CLARITY

    def transition_to(
        self,
        new_tone: ToneFamily,
        curvature: ToneTransitionCurvature = ToneTransitionCurvature.SMOOTH,
        micro_emotional_influence: Optional[Dict[str, Any]] = None,
    ) -> ToneTransition:
        """Transition to a new tone with smooth transition curve.

        Per patch: subsystems/patches/base1.0/tone_transition_patch.md

        Args:
            new_tone: Target tone family.
            curvature: Transition curvature type (ease-in, linear, smooth).
            micro_emotional_influence: Optional micro-emotional influence dict.

        Returns:
            ToneTransition object.
        """
        transition = ToneTransition(
            from_tone=self._current_tone,
            to_tone=new_tone,
            curvature=curvature,
            micro_emotional_influence=micro_emotional_influence,
        )

        self._current_tone = new_tone
        self._last_transition = transition

        return transition

    def get_transition_curvature(
        self, from_tone: ToneFamily, to_tone: ToneFamily
    ) -> ToneTransitionCurvature:
        """Get appropriate transition curvature for a tone change.

        Per patch: tone_transition_patch.md

        Args:
            from_tone: Source tone.
            to_tone: Target tone.

        Returns:
            Appropriate curvature type.
        """
        # Smooth transitions for similar tones
        similar_tones = {
            ToneFamily.WARM_CLARITY: {ToneFamily.PLAYFUL_SOFT, ToneFamily.GROUNDED_CALM},
            ToneFamily.PLAYFUL_SOFT: {ToneFamily.WARM_CLARITY},
            ToneFamily.FOCUS_STEADY: {ToneFamily.GROUNDED_CALM},
            ToneFamily.GROUNDED_CALM: {ToneFamily.WARM_CLARITY, ToneFamily.FOCUS_STEADY},
            ToneFamily.DEEP_REFLECTIVE: {ToneFamily.WARM_CLARITY},
        }

        if to_tone in similar_tones.get(from_tone, set()):
            return ToneTransitionCurvature.SMOOTH

        # Ease-in for transitions to Deep-Reflective (slower, intentional)
        if to_tone == ToneFamily.DEEP_REFLECTIVE:
            return ToneTransitionCurvature.EASE_IN

        # Linear for most other transitions
        return ToneTransitionCurvature.LINEAR


