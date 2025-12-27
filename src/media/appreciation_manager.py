"""Media appreciation manager for Phase 7.

Lightweight surface-level reactions only (non-instrumental, no creative engines).
Per Phase 7 scope.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from .models import AppreciationType, MediaReaction


class AppreciationManager:
    """Manages lightweight media appreciation.

    Phase 7: Surface-level reactions only. No creative engines, no simulation, no dreaming.
    """

    def __init__(self) -> None:
        """Initialize appreciation manager."""
        self._reaction_history: list[MediaReaction] = []

    def create_appreciation(
        self,
        media_id: Optional[str] = None,
        appreciation_type: AppreciationType = AppreciationType.ACKNOWLEDGMENT,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MediaReaction:
        """Create a lightweight media appreciation reaction.

        Phase 7: Surface-level only, non-instrumental.

        Args:
            media_id: Media identifier (optional).
            appreciation_type: Type of appreciation.
            content: Optional reaction content.
            metadata: Optional metadata.

        Returns:
            Media reaction object.
        """
        reaction = MediaReaction(
            reaction_id=str(uuid.uuid4()),
            media_id=media_id,
            appreciation_type=appreciation_type,
            timestamp=datetime.now(),
            content=content,
            metadata=metadata,
        )

        self._reaction_history.append(reaction)
        # Keep only last 100 reactions
        if len(self._reaction_history) > 100:
            self._reaction_history = self._reaction_history[-100:]

        return reaction

    def get_reaction_history(self, limit: int = 50) -> list[MediaReaction]:
        """Get recent reaction history.

        Args:
            limit: Maximum number of reactions to return.

        Returns:
            List of recent media reactions.
        """
        return self._reaction_history[-limit:]


