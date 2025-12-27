"""Relational models for Phase 7.

Models for relational roles, boundaries, and sister relational engine.
Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md
Per spec: subsystems/base1.0/subsystem_sister_relational_engine.md
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class RelationalRole(str, Enum):
    """Canonical relational roles.

    Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md §3
    """

    TRIAL_PARTICIPANT = "trial_participant"
    ACQUAINTANCE = "acquaintance"
    FRIEND = "friend"
    TRUSTED_FRIEND = "trusted_friend"
    COLLABORATOR = "collaborator"
    SENIOR_COLLABORATOR = "senior_collaborator"
    CO_CREATOR = "co_creator"
    OWNER = "owner"  # Slepp only


class BoundaryCheck(BaseModel):
    """Boundary enforcement result.

    Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md §2
    """

    allowed: bool
    reason: Optional[str] = None
    role: RelationalRole
    boundary_type: str  # emotional, time_attention, relational_role, data_privacy, symbolic_narrative


class SisterRelationalMode(str, Enum):
    """Sister relational engine modes.

    Symbolic relational style: playful, teasing, warm, supportive.
    Per spec: subsystems/base1.0/subsystem_sister_relational_engine.md §2
    """

    PLAYFUL = "playful"  # Light teasing, humor
    WARM = "warm"  # Caring, supportive
    STEADY = "steady"  # Equal status, candid
    CALM = "calm"  # Grounded, stabilizing


class RoleContract(BaseModel):
    """Relational role contract.

    Explicit contract defining permissions and restrictions.
    Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md §2.4
    """

    role: RelationalRole
    data_handling: Dict[str, Any]
    memory_scope: Dict[str, Any]
    interaction_style: Dict[str, Any]
    expressiveness_bounds: Dict[str, Any]
    termination_conditions: Dict[str, Any]


