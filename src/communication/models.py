"""Communication layers models for Phase 7.

Models for tone, expression, and intent selection.
Per spec: subsystems/base1.0/subsystem_communication_layers.md
Patches: tone_transition_patch.md, expression_modifiers_patch.md
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class ToneFamily(str, Enum):
    """Canonical tone families.

    Per spec: subsystems/base1.0/subsystem_communication_layers.md §3
    """

    WARM_CLARITY = "warm_clarity"
    PLAYFUL_SOFT = "playful_soft"
    FOCUS_STEADY = "focus_steady"
    GROUNDED_CALM = "grounded_calm"
    DEEP_REFLECTIVE = "deep_reflective"


class ExpressionLevel(int, Enum):
    """Expressiveness levels (0-3 scale).

    Per spec: subsystems/base1.0/subsystem_communication_layers.md §4
    """

    MINIMAL = 0  # Safe/Hard Guardrails/Deep Maintenance
    LIGHT = 1  # Balanced/Focus
    MODERATE = 2  # Warm-Clarity/Exploration
    DEEP = 3  # Reflective/Symbolic Moments


class CommunicationIntent(str, Enum):
    """Communication intent categories.

    Per spec: subsystems/base1.0/subsystem_communication_layers.md §5
    """

    CLARITY = "clarity"
    GROUNDING = "grounding"
    RESONANCE = "resonance"
    ENCOURAGEMENT = "encouragement"
    EXPLORATION = "exploration"


class ToneTransitionCurvature(str, Enum):
    """Tone transition curvature types.

    Per patch: subsystems/patches/base1.0/tone_transition_patch.md
    """

    EASE_IN = "ease_in"
    LINEAR = "linear"
    SMOOTH = "smooth"


class ToneTransition(BaseModel):
    """Tone transition metadata.

    Controls smooth transitions between tones.
    Per patch: subsystems/patches/base1.0/tone_transition_patch.md
    """

    from_tone: ToneFamily
    to_tone: ToneFamily
    curvature: ToneTransitionCurvature = ToneTransitionCurvature.SMOOTH
    micro_emotional_influence: Optional[Dict[str, Any]] = None


class ExpressionModifier(str, Enum):
    """Expression micro-modifiers.

    Applied sparingly to enhance nuance without affecting emotional stability.
    Per patch: subsystems/patches/base1.0/expression_modifiers_patch.md
    """

    SOFTLY = "softly"
    GENTLY = "gently"
    QUIETLY = "quietly"
    LIGHTLY = "lightly"
    SUBTLY = "subtly"
    WARMLY = "warmly"


class CommunicationLayerConfig(BaseModel):
    """Combined communication layer configuration.

    Combines tone, expression level, and intent.
    Per spec: subsystems/base1.0/subsystem_communication_layers.md §6
    """

    tone: ToneFamily
    expression_level: ExpressionLevel
    intent: CommunicationIntent
    modifier: Optional[ExpressionModifier] = None  # Applied sparingly


