"""Shared media and appreciation models for Phase 7.

Lightweight surface-level reactions only.
Per spec: subsystems/base1.0/subsystem_sensory_media.md (Base 1.0 scope)
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AppreciationType(str, Enum):
    """Appreciation types for shared media.

    Lightweight, surface-level only. No creative engines or simulation.
    Per Phase 7 scope.
    """

    ACKNOWLEDGMENT = "acknowledgment"  # Light acknowledgment
    SURFACE_REACTION = "surface_reaction"  # Surface-level reaction only


class MediaReaction(BaseModel):
    """Surface-level media appreciation.

    Non-instrumental, no dreaming/simulation/creative engines.
    Per Phase 7 scope.
    """

    reaction_id: str
    media_id: Optional[str] = None
    appreciation_type: AppreciationType
    timestamp: datetime
    content: Optional[str] = None  # Surface-level reaction text
    metadata: Optional[Dict[str, Any]] = None


