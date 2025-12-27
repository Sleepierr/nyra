"""Presence and interaction package for Phase 7.

Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md
"""

from .embodiment_handler import EmbodimentHandler
from .interaction_orchestrator import InteractionOrchestrator
from .models import (
    EmbodimentType,
    ExpressionBudget,
    InteractionDecision,
    PresenceState,
    PresenceTransition,
)
from .presence_manager import PresenceManager

__all__ = [
    "PresenceState",
    "PresenceTransition",
    "InteractionDecision",
    "EmbodimentType",
    "ExpressionBudget",
    "PresenceManager",
    "InteractionOrchestrator",
    "EmbodimentHandler",
]


