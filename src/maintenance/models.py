"""Maintenance data models for Phase 6.

Per spec: subsystems/base1.0/subsystem_nyrahome_brain.md §X.7
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class MaintenanceTriggerType(str, Enum):
    """Maintenance trigger types.

    Per spec: subsystem_nyrahome_brain.md §X.1
    """

    SCHEDULED = "scheduled"
    MEMORY_PRESSURE = "memory_pressure"
    DRIFT_SIGNAL = "drift_signal"
    AUTONOMY_TRANSITION = "autonomy_transition"
    IDENTITY_REVIEW = "identity_review"
    SYMBOLIC_OVERLOAD = "symbolic_overload"


class MaintenanceTask(BaseModel):
    """Maintenance task structure."""

    task_id: str = ""
    task_type: str = ""
    priority: int = 0
    scheduled_time: Optional[datetime] = None
    status: str = "pending"

    def __init__(self, **data: Any) -> None:
        """Initialize maintenance task with defaults."""
        if "task_id" not in data or not data["task_id"]:
            data["task_id"] = str(uuid.uuid4())
        super().__init__(**data)


class MaintenanceReport(BaseModel):
    """Maintenance execution report."""

    report_id: str = ""
    maintenance_type: str = ""
    start_time: datetime
    end_time: Optional[datetime] = None
    tasks_completed: List[str] = []
    tasks_failed: List[str] = []
    summary: str = ""

    def __init__(self, **data: Any) -> None:
        """Initialize maintenance report with defaults."""
        if "report_id" not in data or not data["report_id"]:
            data["report_id"] = str(uuid.uuid4())
        super().__init__(**data)

