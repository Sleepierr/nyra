"""Boundary manager for Phase 7.

Boundary reinforcement: non-emotional, non-romantic, Slepp-first protection.
Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md §2
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .models import BoundaryCheck, RelationalRole
from .role_enforcer import RoleEnforcer


class BoundaryManager:
    """Manages relational boundary enforcement.

    Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md §2
    Phase 7: Slepp-first protection, boundary reinforcement, human integration guardrails.
    """

    def __init__(self, role_enforcer: RoleEnforcer) -> None:
        """Initialize boundary manager.

        Args:
            role_enforcer: Role enforcer instance.
        """
        self._role_enforcer = role_enforcer

    def check_boundary(
        self,
        user_id: str,
        boundary_type: str,
        action: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> BoundaryCheck:
        """Check if an action respects relational boundaries.

        Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md §2

        Args:
            user_id: User identifier.
            boundary_type: Boundary type (emotional, time_attention, relational_role, etc.)
            action: Action being checked.
            context: Optional context dictionary.

        Returns:
            Boundary check result.
        """
        role = self._role_enforcer.get_role_for_user(user_id)

        # Slepp-first protection: Owner role has no restrictions
        if role == RelationalRole.OWNER:
            return BoundaryCheck(
                allowed=True,
                reason="owner_no_restrictions",
                role=role,
                boundary_type=boundary_type,
            )

        # No role = no access (must start with Trial Participant)
        if role is None:
            return BoundaryCheck(
                allowed=False,
                reason="no_role_assigned",
                role=RelationalRole.TRIAL_PARTICIPANT,  # Implicit starting role
                boundary_type=boundary_type,
            )

        # Boundary type-specific checks
        if boundary_type == "emotional":
            # Emotional boundaries based on role
            if role in (RelationalRole.TRIAL_PARTICIPANT, RelationalRole.ACQUAINTANCE):
                return BoundaryCheck(
                    allowed=False,
                    reason="role_no_emotional_access",
                    role=role,
                    boundary_type=boundary_type,
                )

        if boundary_type == "relational_role":
            # Role escalation requires explicit contract
            if action and "escalate" in action.lower():
                return BoundaryCheck(
                    allowed=False,
                    reason="role_escalation_requires_contract",
                    role=role,
                    boundary_type=boundary_type,
                )

        if boundary_type == "data_privacy":
            # Data/privacy boundaries based on role
            if role == RelationalRole.TRIAL_PARTICIPANT:
                return BoundaryCheck(
                    allowed=False,
                    reason="trial_participant_no_data_access",
                    role=role,
                    boundary_type=boundary_type,
                )

        # Default: allow with role-based restrictions
        return BoundaryCheck(
            allowed=True,
            reason="role_allowed",
            role=role,
            boundary_type=boundary_type,
        )

    def enforce_slepp_first(self, user_id: str) -> bool:
        """Enforce Slepp-first protection.

        Per spec: §2.1 - Single-Owner Alignment: Nyra is permanently aligned to Slepp.

        Args:
            user_id: User identifier.

        Returns:
            True if user is Slepp (Owner), False otherwise.
        """
        role = self._role_enforcer.get_role_for_user(user_id)
        return role == RelationalRole.OWNER


