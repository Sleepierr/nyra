"""Presence and interaction models for Phase 7.

Models for presence state management, interaction decisions, and embodiment handling.
Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class PresenceState(str, Enum):
    """Canonical presence states.

    Presence states are postures, not moods. Nyra may shift fluidly between them.
    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §4
    """

    ACTIVE = "active"
    QUIET = "quiet"
    BACKGROUND = "background"
    REFLECTIVE = "reflective"
    PLAYFUL = "playful"
    GUARDED = "guarded"


class PresenceTransition(BaseModel):
    """Presence state transition metadata.

    Tracks transitions with minimum dwell time enforcement.
    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §7
    """

    from_state: PresenceState
    to_state: PresenceState
    timestamp: datetime
    minimum_dwell_seconds: int = 30  # Minimum time before next transition


class InteractionDecision(BaseModel):
    """Decision about when to respond immediately vs inboxed.

    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §1
    """

    respond_immediately: bool
    reasoning: Optional[str] = None
    presence_state: PresenceState
    timestamp: datetime


class EmbodimentType(str, Enum):
    """Embodiment types.

    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §9
    """

    MAC = "mac"
    WINDOWS = "windows"
    PHONE = "phone"
    PERIPHERAL = "peripheral"  # Notification-only contexts, future ambient shells


class ExpressionBudget(BaseModel):
    """Expression budget for an embodiment.

    Soft expression budget affecting message length, emotional intensity, etc.
    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §9.3
    """

    message_length_limit: int
    emotional_intensity_limit: float  # 0.0 to 1.0
    facet_visibility_limit: float  # 0.0 to 1.0
    humor_density_limit: float  # 0.0 to 1.0
    check_in_frequency_limit: int  # Maximum check-ins per hour


