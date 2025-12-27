"""Memory data models for Phase 6.

Per spec: subsystems/base1.0/subsystem_memory_experience.md
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class MemoryType(str, Enum):
    """Types of memory entries.

    Per spec: subsystem_memory_experience.md §X.1
    """

    EVENT = "event"
    CONVERSATION = "conversation"
    REFLECTION = "reflection"
    SKILL_TRACE = "skill_trace"
    TASK_TRACE = "task_trace"
    EMOTIONAL_TRACE = "emotional_trace"
    SYSTEM_STATE = "system_state"


class MemoryPriority(str, Enum):
    """Memory priority levels.

    Per spec: subsystem_memory_experience.md §X.1
    """

    NORMAL = "normal"
    IMPORTANT = "important"
    CRITICAL = "critical"


class MemoryObject(BaseModel):
    """Core memory object structure.

    Per spec: subsystem_memory_experience.md §6
    """

    memory_id: str
    timestamp_created: datetime
    event_type: str
    emotional_vector: Dict[str, Any]
    cognitive_trace: Dict[str, Any]
    significance_score: float  # [0.0, 1.0]
    identity_relevance_score: float  # [0.0, 1.0]
    experience_links: List[str] = []  # List of experience_ids
    narrative_tags: List[str] = []
    autonomy_band_origin: int = 0
    context_metadata: Dict[str, Any] = {}
    safety_flags: List[str] = []

    class Config:
        """Pydantic config."""

        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class STMMemoryEntry(BaseModel):
    """Short-term memory entry.

    Per spec: subsystem_memory_experience.md §3, §X.2.2
    Volatile, instance-local, minimal structure.
    """

    memory_id: str = ""
    timestamp: Optional[datetime] = None
    raw_payload: Dict[str, Any] = {}
    emotional_hint: Optional[Dict[str, Any]] = None
    symbolic_hint: Optional[Dict[str, Any]] = None

    def __init__(self, **data: Any) -> None:
        """Initialize STM entry with defaults."""
        if "memory_id" not in data or not data["memory_id"]:
            data["memory_id"] = str(uuid.uuid4())
        if "timestamp" not in data or data["timestamp"] is None:
            data["timestamp"] = datetime.now(timezone.utc)
        super().__init__(**data)


class LTMMemoryEntry(BaseModel):
    """Long-term memory entry.

    Per spec: subsystem_memory_experience.md §5, §X.2.1
    Canonical, NyraHome-only, structured.
    """

    memory_id: str
    timestamp: datetime
    type: MemoryType
    content_summary: str
    emotional_signature_vector: Dict[str, Any] = {}
    symbolic_links: List[str] = []  # Band ≥ 8 only
    experience_tags: List[str] = []
    xp_yield: float = 0.0
    impact_level: int = 0  # ExperienceImpactLevel 0-5
    priority: MemoryPriority = MemoryPriority.NORMAL
    source_subsystem: str = ""
    metadata: Dict[str, Any] = {}

    class Config:
        """Pydantic config."""

        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }





