"""Expression manager for Phase 7.

Manages expression level (0-3) and micro-modifiers.
Per spec: subsystems/base1.0/subsystem_communication_layers.md §4
Per patch: subsystems/patches/base1.0/expression_modifiers_patch.md
"""

from __future__ import annotations

import random
from typing import Any, Dict, Optional

from .models import ExpressionLevel, ExpressionModifier


class ExpressionManager:
    """Manages expression level and modifiers.

    Per spec: subsystems/base1.0/subsystem_communication_layers.md §4
    Per patch: expression_modifiers_patch.md - expression micro-modifiers
    """

    def __init__(self) -> None:
        """Initialize expression manager."""
        self._current_level: ExpressionLevel = ExpressionLevel.LIGHT  # Default: Level 1
        self._modifier_usage_count: int = 0  # Track modifier usage for sparing application

    def get_current_level(self) -> ExpressionLevel:
        """Get current expression level."""
        return self._current_level

    def select_expression_level(
        self,
        autonomy_band: Optional[int] = None,
        presence_state: Optional[str] = None,
        emotional_state: Optional[Dict[str, Any]] = None,
        processing_mode: Optional[str] = None,
    ) -> ExpressionLevel:
        """Select expression level based on constraints.

        Per spec: subsystems/base1.0/subsystem_communication_layers.md §4

        Args:
            autonomy_band: Current autonomy band (0-100)
            presence_state: Current presence state
            emotional_state: Emotional state dict
            processing_mode: Processing mode

        Returns:
            Selected expression level.
        """
        # Processing mode-based selection (spec §7)
        if processing_mode == "safe_mode" or processing_mode == "hard_guardrails":
            return ExpressionLevel.MINIMAL
        if processing_mode == "focus":
            return ExpressionLevel.LIGHT
        if processing_mode == "exploration":
            return ExpressionLevel.MODERATE
        if processing_mode == "deep_think":
            return ExpressionLevel.DEEP

        # Presence state influence
        if presence_state == "guarded":
            return ExpressionLevel.MINIMAL
        if presence_state == "reflective":
            # Reflective presence can use Level 3, but followed by grounding
            return ExpressionLevel.DEEP

        # Autonomy band bounds
        if autonomy_band is not None:
            if autonomy_band < 20:
                # Band 0-20: Minimal to Light
                return ExpressionLevel.LIGHT
            if autonomy_band < 40:
                # Band 20-40: Light to Moderate
                return ExpressionLevel.LIGHT if random.random() < 0.7 else ExpressionLevel.MODERATE
            if autonomy_band < 60:
                # Band 40-60: Moderate (baseline)
                return ExpressionLevel.MODERATE
            if autonomy_band < 80:
                # Band 60-80: Moderate to Deep
                return ExpressionLevel.MODERATE if random.random() < 0.8 else ExpressionLevel.DEEP
            # Band 80-100: Deep allowed (future eras)

        # Default: Light (Level 1)
        return ExpressionLevel.LIGHT

    def select_modifier(
        self,
        expression_level: ExpressionLevel,
        tone: Optional[str] = None,
        context: Optional[str] = None,
    ) -> Optional[ExpressionModifier]:
        """Select expression modifier sparingly.

        Per patch: subsystems/patches/base1.0/expression_modifiers_patch.md
        Rules: applied sparingly, context-sensitive, not manipulative, never romantic

        Args:
            expression_level: Current expression level
            tone: Current tone family
            context: Context string

        Returns:
            Expression modifier if appropriate, None otherwise.
        """
        # Modifiers only for Level 1-2 (Light to Moderate)
        if expression_level == ExpressionLevel.MINIMAL or expression_level == ExpressionLevel.DEEP:
            return None

        # Apply sparingly (approximately 20% of the time)
        if random.random() > 0.2:
            return None

        self._modifier_usage_count += 1

        # Context-sensitive selection
        if context == "grounding" or context == "stabilizing":
            return ExpressionModifier.GENTLY
        if context == "supportive" or context == "encouraging":
            return ExpressionModifier.WARMLY
        if context == "quiet" or context == "minimal":
            return ExpressionModifier.QUIETLY
        if tone == "playful_soft":
            return ExpressionModifier.LIGHTLY
        if tone == "warm_clarity":
            return ExpressionModifier.SOFTLY

        # Default: subtle (most neutral)
        return ExpressionModifier.SUBTLY

    def set_expression_level(self, level: ExpressionLevel) -> None:
        """Set expression level directly.

        Args:
            level: Expression level to set.
        """
        self._current_level = level


