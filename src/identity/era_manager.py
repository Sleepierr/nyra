"""Identity era management for Phase 6.

Per spec: subsystems/base1.0/subsystem_identity.md §6.3
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class IdentityEra(BaseModel):
    """Identity era structure.

    Per spec: subsystem_identity.md §6.3
    """

    era_id: str
    name: str
    start_timestamp: datetime
    end_timestamp: Optional[datetime] = None
    themes: List[str] = []
    signature_events: List[str] = []
    emotional_palette_shift: Dict[str, Any] = {}
    identity_morphology: Dict[str, Any] = {}


class EraManager:
    """Manages Identity Eras.

    Per spec: subsystem_identity.md §6.3
    Phase 6: Era tracking and transitions with debate integration.
    """

    def __init__(self) -> None:
        """Initialize era manager."""
        self._eras: Dict[str, IdentityEra] = {}
        self._current_era_id: Optional[str] = None

    def get_current_era(self) -> Optional[IdentityEra]:
        """Get current active era.

        Returns:
            Current era if exists, None otherwise.
        """
        if self._current_era_id:
            return self._eras.get(self._current_era_id)
        return None

    def transition_to_new_era(
        self, new_era: IdentityEra, debate_outcome: Any
    ) -> bool:
        """Transition to new era with debate validation.

        Per spec: subsystem_identity.md §6.3
        Era transitions require deep debate and explicit triggers.

        Args:
            new_era: New era to transition to.
            debate_outcome: Debate outcome validating the transition.

        Returns:
            True if transition succeeded, False otherwise.
        """
        # Phase 6: Basic transition with debate validation
        # Check debate outcome (simplified - full validation deferred)
        if debate_outcome is None:
            return False

        # End current era
        current_era = self.get_current_era()
        if current_era:
            current_era.end_timestamp = datetime.now(timezone.utc)

        # Set new era as current
        self._eras[new_era.era_id] = new_era
        self._current_era_id = new_era.era_id

        return True

    def create_era(
        self,
        name: str,
        themes: List[str],
        emotional_palette_shift: Dict[str, Any],
    ) -> IdentityEra:
        """Create a new era.

        Args:
            name: Era name.
            themes: Era themes.
            emotional_palette_shift: Emotional palette changes.

        Returns:
            Created IdentityEra.
        """
        era_id = f"era_{len(self._eras)}"
        era = IdentityEra(
            era_id=era_id,
            name=name,
            start_timestamp=datetime.now(timezone.utc),
            themes=themes,
            emotional_palette_shift=emotional_palette_shift,
        )
        self._eras[era_id] = era
        return era

