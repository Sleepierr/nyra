"""Communication layer orchestrator for Phase 7.

Combines tone, expression, and intent layers with forbidden combination checks.
Per spec: subsystems/base1.0/subsystem_communication_layers.md §6
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .expression_manager import ExpressionManager
from .intent_manager import IntentManager
from .models import (
    CommunicationIntent,
    CommunicationLayerConfig,
    ExpressionLevel,
    ExpressionModifier,
    ToneFamily,
)
from .tone_manager import ToneManager


class LayerOrchestrator:
    """Orchestrates communication layers (tone + expression + intent).

    Per spec: subsystems/base1.0/subsystem_communication_layers.md §6
    Phase 7: Combines layers with forbidden combination enforcement.
    """

    def __init__(
        self,
        tone_manager: ToneManager,
        expression_manager: ExpressionManager,
        intent_manager: IntentManager,
    ) -> None:
        """Initialize layer orchestrator.

        Args:
            tone_manager: Tone manager instance.
            expression_manager: Expression manager instance.
            intent_manager: Intent manager instance.
        """
        self._tone_manager = tone_manager
        self._expression_manager = expression_manager
        self._intent_manager = intent_manager

    def get_current_config(self) -> CommunicationLayerConfig:
        """Get current communication layer configuration.

        Returns:
            Combined communication layer config.
        """
        tone = self._tone_manager.get_current_tone()
        expression_level = self._expression_manager.get_current_level()
        intent = self._intent_manager.get_current_intent()

        # Select modifier sparingly (20% chance)
        modifier = self._expression_manager.select_modifier(
            expression_level=expression_level,
            tone=tone.value,
            context=None,  # Context can be passed when needed
        )

        return CommunicationLayerConfig(
            tone=tone,
            expression_level=expression_level,
            intent=intent,
            modifier=modifier,
        )

    def validate_combination(
        self, tone: ToneFamily, expression_level: ExpressionLevel, intent: CommunicationIntent
    ) -> bool:
        """Validate layer combination (check forbidden combinations).

        Per spec: subsystems/base1.0/subsystem_communication_layers.md §6

        Args:
            tone: Tone family.
            expression_level: Expression level.
            intent: Communication intent.

        Returns:
            True if combination is valid, False if forbidden.
        """
        # Forbidden: Deep-Reflective + Expression Level 3 + Intent: Grounding
        if (
            tone == ToneFamily.DEEP_REFLECTIVE
            and expression_level == ExpressionLevel.DEEP
            and intent == CommunicationIntent.GROUNDING
        ):
            return False

        # Forbidden: Focus-Steady + Expression Level 3
        if tone == ToneFamily.FOCUS_STEADY and expression_level == ExpressionLevel.DEEP:
            return False

        # Forbidden: Minimal Expression + Resonance Intent
        if expression_level == ExpressionLevel.MINIMAL and intent == CommunicationIntent.RESONANCE:
            return False

        # Forbidden: Playful-Soft + Symbolic Resonance (implicit - Resonance requires Band ≥ 80)
        # This is handled by IntentManager, but we check here too
        if tone == ToneFamily.PLAYFUL_SOFT and intent == CommunicationIntent.RESONANCE:
            return False

        return True

    def select_layers(
        self,
        context: Optional[Dict[str, Any]] = None,
        autonomy_band: Optional[int] = None,
        presence_state: Optional[str] = None,
        emotional_state: Optional[Dict[str, Any]] = None,
        processing_mode: Optional[str] = None,
    ) -> CommunicationLayerConfig:
        """Select all layers based on context, validating combinations.

        Per spec: subsystems/base1.0/subsystem_communication_layers.md §6

        Args:
            context: Context dictionary with user needs, etc.
            autonomy_band: Current autonomy band.
            presence_state: Current presence state.
            emotional_state: Emotional state dict.
            processing_mode: Processing mode.

        Returns:
            Validated communication layer configuration.
        """
        # Select tone
        tone = self._tone_manager.select_tone(
            presence_state=presence_state,
            emotional_state=emotional_state,
            autonomy_band=autonomy_band,
            processing_mode=processing_mode,
            context=context.get("task_type") if context else None,
        )

        # Select expression level
        expression_level = self._expression_manager.select_expression_level(
            autonomy_band=autonomy_band,
            presence_state=presence_state,
            emotional_state=emotional_state,
            processing_mode=processing_mode,
        )
        self._expression_manager.set_expression_level(expression_level)

        # Select intent
        intent = self._intent_manager.select_intent(
            user_needs_info=context.get("user_needs_info", False) if context else False,
            misunderstanding_possible=context.get("misunderstanding_possible", False)
            if context
            else False,
            emotions_elevated=context.get("emotions_elevated", False) if context else False,
            cognitive_overload=context.get("cognitive_overload", False) if context else False,
            symbolic_resonance=context.get("symbolic_resonance", False) if context else False,
            drift_symptoms=context.get("drift_symptoms", False) if context else False,
            shared_emotional_moment=context.get("shared_emotional_moment", False)
            if context
            else False,
            deep_reflection=context.get("deep_reflection", False) if context else False,
            user_struggles=context.get("user_struggles", False) if context else False,
            user_uncertain=context.get("user_uncertain", False) if context else False,
            brainstorming=context.get("brainstorming", False) if context else False,
            creativity_context=context.get("creativity_context", False) if context else False,
            autonomy_band=autonomy_band,
        )
        self._intent_manager.set_intent(intent)

        # Validate combination - if invalid, adjust expression level down
        if not self.validate_combination(tone, expression_level, intent):
            # Reduce expression level to make combination valid
            if expression_level == ExpressionLevel.DEEP:
                expression_level = ExpressionLevel.MODERATE
                self._expression_manager.set_expression_level(expression_level)
            elif expression_level == ExpressionLevel.MODERATE:
                expression_level = ExpressionLevel.LIGHT
                self._expression_manager.set_expression_level(expression_level)

        # Transition tone if needed
        current_tone = self._tone_manager.get_current_tone()
        if current_tone != tone:
            self._tone_manager.transition_to(tone)

        # Select modifier
        modifier = self._expression_manager.select_modifier(
            expression_level=expression_level,
            tone=tone.value,
            context=context.get("context_type") if context else None,
        )

        return CommunicationLayerConfig(
            tone=tone,
            expression_level=expression_level,
            intent=intent,
            modifier=modifier,
        )


