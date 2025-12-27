"""Dynamic trait drift management for Phase 6.

Per spec: subsystems/base1.0/subsystem_identity.md §6.2
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class DynamicTraitManager:
    """Manages controlled Dynamic Trait drift.

    Per spec: subsystem_identity.md §6.2.2
    Phase 6: Controlled trait updates with safety checks.
    """

    # Maximum change per event
    MAX_DELTA_PER_EVENT = 0.05

    def __init__(self) -> None:
        """Initialize dynamic trait manager."""
        self._traits: Dict[str, float] = {}
        self._identity_invariants: Dict[str, Any] = {}

    def update_trait(
        self, trait_name: str, delta: float, identity_reset: bool = False
    ) -> bool:
        """Update Dynamic Identity Trait with controlled drift.

        Per spec: subsystem_identity.md §6.2.2
        Enforces no abrupt changes (max ±0.05 per event unless identity reset).

        Args:
            trait_name: Trait name to update.
            delta: Change amount.
            identity_reset: If True, allows larger changes.

        Returns:
            True if update was applied, False if rejected.
        """
        # Enforce maximum delta per event (unless identity reset)
        if not identity_reset and abs(delta) > self.MAX_DELTA_PER_EVENT:
            delta = self.MAX_DELTA_PER_EVENT if delta > 0 else -self.MAX_DELTA_PER_EVENT

        # Get current value
        current_value = self._traits.get(trait_name, 0.0)

        # Calculate new value
        new_value = current_value + delta

        # Clamp to valid range [0.0, 1.0]
        new_value = max(0.0, min(1.0, new_value))

        # Check identity invariants before updating
        if not self._check_identity_invariants(trait_name, new_value):
            return False

        # Update trait
        self._traits[trait_name] = new_value
        return True

    def get_trait(self, trait_name: str) -> float:
        """Get current trait value.

        Args:
            trait_name: Trait name.

        Returns:
            Trait value [0.0, 1.0], 0.0 if not found.
        """
        return self._traits.get(trait_name, 0.0)

    def _check_identity_invariants(self, trait_name: str, new_value: float) -> bool:
        """Check if trait update violates identity invariants.

        Args:
            trait_name: Trait name.
            new_value: Proposed new value.

        Returns:
            True if invariants satisfied, False otherwise.
        """
        # Phase 6: Basic invariant check
        # Full invariant checking deferred to Identity System integration
        return True

    def set_identity_invariants(self, invariants: Dict[str, Any]) -> None:
        """Set identity invariants for validation.

        Args:
            invariants: Identity invariant configuration.
        """
        self._identity_invariants = invariants.copy()





