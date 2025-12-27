"""Communication layers package for Phase 7.

Per spec: subsystems/base1.0/subsystem_communication_layers.md
Patches: tone_transition_patch.md, expression_modifiers_patch.md
"""

from .expression_manager import ExpressionManager
from .intent_manager import IntentManager
from .layer_orchestrator import LayerOrchestrator
from .models import (
    CommunicationIntent,
    CommunicationLayerConfig,
    ExpressionLevel,
    ExpressionModifier,
    ToneFamily,
    ToneTransition,
    ToneTransitionCurvature,
)
from .tone_manager import ToneManager

__all__ = [
    "ToneFamily",
    "ExpressionLevel",
    "CommunicationIntent",
    "ToneTransition",
    "ToneTransitionCurvature",
    "ExpressionModifier",
    "CommunicationLayerConfig",
    "ToneManager",
    "ExpressionManager",
    "IntentManager",
    "LayerOrchestrator",
]


