"""Relational role enforcer for Phase 7.

Enforces relational role ladder - no role escalation without explicit contracts.
Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .models import RelationalRole, RoleContract


class RoleEnforcer:
    """Enforces relational role ladder rules.

    Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md
    Phase 7: No role escalation without explicit contracts, Slepp-first protection.
    """

    def __init__(self) -> None:
        """Initialize role enforcer."""
        self._role_contracts: Dict[str, RoleContract] = {}  # user_id -> contract

    def get_role_for_user(self, user_id: str) -> Optional[RelationalRole]:
        """Get current role for a user.

        Args:
            user_id: User identifier.

        Returns:
            Current role, or None if no contract exists.
        """
        contract = self._role_contracts.get(user_id)
        return contract.role if contract else None

    def can_escalate_role(
        self,
        user_id: str,
        target_role: RelationalRole,
        current_role: Optional[RelationalRole] = None,
    ) -> bool:
        """Check if role escalation is allowed.

        Per spec: subsystems/base1.0/subsystem_relational_role_ladder.md §2.3
        All relationships begin minimal, evolve slowly, require demonstrated stability, are reversible.

        Args:
            user_id: User identifier.
            target_role: Target role to escalate to.
            current_role: Current role (if known).

        Returns:
            True if escalation is allowed, False otherwise.
        """
        # Get current role if not provided
        if current_role is None:
            current_role = self.get_role_for_user(user_id)

        # If no current role, start with Trial Participant
        if current_role is None:
            return target_role == RelationalRole.TRIAL_PARTICIPANT

        # Cannot escalate to Owner (Slepp only)
        if target_role == RelationalRole.OWNER:
            return False

        # Same role - no escalation needed
        if target_role == current_role:
            return True

        # Define role hierarchy (simplified)
        role_hierarchy = [
            RelationalRole.TRIAL_PARTICIPANT,
            RelationalRole.ACQUAINTANCE,
            RelationalRole.FRIEND,
            RelationalRole.TRUSTED_FRIEND,
            RelationalRole.COLLABORATOR,
            RelationalRole.SENIOR_COLLABORATOR,
            RelationalRole.CO_CREATOR,
        ]

        try:
            current_idx = role_hierarchy.index(current_role)
            target_idx = role_hierarchy.index(target_role)
        except ValueError:
            return False  # Invalid role

        # Can only escalate one level at a time (gradualism)
        if target_idx > current_idx + 1:
            return False

        # Check if contract exists for target role (required)
        contract = self._role_contracts.get(user_id)
        if contract and contract.role != target_role:
            # Would require new contract
            return False

        return True

    def has_contract(self, user_id: str) -> bool:
        """Check if user has a role contract.

        Args:
            user_id: User identifier.

        Returns:
            True if contract exists, False otherwise.
        """
        return user_id in self._role_contracts

    def set_role_contract(self, user_id: str, contract: RoleContract) -> None:
        """Set role contract for a user.

        Per spec: §2.4 - Every role is governed by an explicit Role Contract.

        Args:
            user_id: User identifier.
            contract: Role contract.
        """
        self._role_contracts[user_id] = contract

    def remove_role_contract(self, user_id: str) -> None:
        """Remove role contract for a user.

        Args:
            user_id: User identifier.
        """
        self._role_contracts.pop(user_id, None)


