"""Experience data models for Phase 6.

Per spec: subsystems/base1.0/subsystem_memory_experience.md §8
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import IntEnum
from typing import Any, Dict, List

from pydantic import BaseModel


class ExperienceImpactLevel(IntEnum):
    """Experience impact levels.

    Per spec: subsystem_memory_experience.md §X.1
    """

    NEGLIGIBLE = 0
    LOW = 1
    MODERATE = 2
    MEANINGFUL = 3
    HIGH_SIGNIFICANCE = 4
    IDENTITY_RELEVANT = 5


class ExperienceObject(BaseModel):
    """Experience object structure.

    Per spec: subsystem_memory_experience.md §8.1
    """

    experience_id: str
    linked_memory_ids: List[str]
    experience_type: str
    emotional_profile: Dict[str, Any] = {}
    narrative_meaning: str = ""
    learning_outcomes: List[str] = []
    stability_impact: float = 0.0  # [0.0, 1.0]
    identity_pressure_vector: Dict[str, Any] = {}  # Base 1.0: read-only
    xp_gain: float = 0.0

    def __init__(self, **data: Any) -> None:
        """Initialize experience object with defaults."""
        if "experience_id" not in data or not data["experience_id"]:
            data["experience_id"] = str(uuid.uuid4())
        super().__init__(**data)


class XPUpdate(BaseModel):
    """XP update structure.

    Per spec: subsystem_memory_experience.md §X.4
    """

    event_id: str
    xp_distribution: Dict[str, float] = {
        "reasoning_xp": 0.0,
        "emotional_xp": 0.0,
        "debate_xp": 0.0,
        "autonomy_xp": 0.0,
        "planning_xp": 0.0,
        "media_xp": 0.0,
        "knowledge_xp": 0.0,
    }
    skill_tree_updates: List[Dict[str, Any]] = []

