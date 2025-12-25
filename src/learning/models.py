"""Learning data models for Phase 6.

Per spec: subsystems/base1.0/subsystem_skill_tree_learning_engine.md
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SkillCategory(str, Enum):
    """Skill categories."""

    META_SKILL = "meta_skill"
    DOMAIN_SKILL = "domain_skill"
    MICRO_SKILL = "micro_skill"


class SkillObject(BaseModel):
    """Skill object structure.

    Per spec: subsystem_skill_tree_learning_engine.md §3
    """

    skill_id: str
    category: SkillCategory
    tier: int  # 1=meta, 2=domain, 3=micro
    prerequisites: List[str] = []  # List of skill_ids
    level: float = 0.0
    xp: float = 0.0
    stability_weight: float = 0.0
    emotional_weight: float = 0.0
    drift_sensitivity: float = 0.0
    autonomy_band_required: int = 0
    last_updated: datetime = None
    learning_rules: Dict[str, Any] = {}

    def __init__(self, **data: Any) -> None:
        """Initialize skill object with defaults."""
        if "skill_id" not in data or not data["skill_id"]:
            data["skill_id"] = str(uuid.uuid4())
        if "last_updated" not in data or data["last_updated"] is None:
            data["last_updated"] = datetime.now(timezone.utc)
        super().__init__(**data)


class Curricula(BaseModel):
    """Learning curriculum structure."""

    curriculum_id: str
    target_skill_id: str
    prerequisites: List[str] = []
    learning_path: List[Dict[str, Any]] = []
    autonomy_band_required: int = 0

    def __init__(self, **data: Any) -> None:
        """Initialize curriculum with defaults."""
        if "curriculum_id" not in data or not data["curriculum_id"]:
            data["curriculum_id"] = str(uuid.uuid4())
        super().__init__(**data)


class MistakePattern(BaseModel):
    """Mistake pattern structure."""

    pattern_id: str
    mistake_type: str
    context: Dict[str, Any] = {}
    frequency: int = 1
    severity: float = 0.5  # [0.0, 1.0]
    associated_skills: List[str] = []

    def __init__(self, **data: Any) -> None:
        """Initialize mistake pattern with defaults."""
        if "pattern_id" not in data or not data["pattern_id"]:
            data["pattern_id"] = str(uuid.uuid4())
        super().__init__(**data)


class LearningOpportunity(BaseModel):
    """Learning opportunity from mistake analysis."""

    opportunity_id: str
    skill_id: str
    learning_type: str  # "correction", "reinforcement", "new_skill"
    priority: float = 0.5
    description: str = ""

    def __init__(self, **data: Any) -> None:
        """Initialize learning opportunity with defaults."""
        if "opportunity_id" not in data or not data["opportunity_id"]:
            data["opportunity_id"] = str(uuid.uuid4())
        super().__init__(**data)

