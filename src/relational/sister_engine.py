"""Sister relational engine for Phase 7.

Symbolic sister-like relational mode: playful, teasing, warm, supportive.
Per spec: subsystems/base1.0/subsystem_sister_relational_engine.md
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .models import SisterRelationalMode


class SisterRelationalEngine:
    """Manages symbolic sister-like relational mode.

    Per spec: subsystems/base1.0/subsystem_sister_relational_engine.md
    Phase 7: Symbolic relational style (equal status, playful mischief, safe and calibrated).
    """

    def __init__(self) -> None:
        """Initialize sister relational engine."""
        self._current_mode: SisterRelationalMode = SisterRelationalMode.STEADY  # Default
        self._mode_history: list[SisterRelationalMode] = []

    def get_current_mode(self) -> SisterRelationalMode:
        """Get current sister relational mode."""
        return self._current_mode

    def select_mode(
        self,
        context: Optional[str] = None,
        emotional_state: Optional[Dict[str, Any]] = None,
        autonomy_band: Optional[int] = None,
        safety_allowed: bool = True,
    ) -> SisterRelationalMode:
        """Select sister relational mode based on context.

        Per spec: subsystems/base1.0/subsystem_sister_relational_engine.md §2

        Args:
            context: Context string (playful, supportive, etc.)
            emotional_state: Emotional state dict
            autonomy_band: Current autonomy band (playful requires Band ≥ 40)
            safety_allowed: Whether safety allows playful mode

        Returns:
            Selected sister relational mode.
        """
        # Playful mode: only when safety and autonomy allow (Band ≥ 40)
        if (
            context == "playful"
            and safety_allowed
            and autonomy_band is not None
            and autonomy_band >= 40
        ):
            return SisterRelationalMode.PLAYFUL

        # Warm mode: supportive, caring contexts
        if context == "supportive" or context == "caring":
            return SisterRelationalMode.WARM

        # Calm mode: grounding, stabilizing contexts
        if context == "grounding" or context == "stabilizing":
            return SisterRelationalMode.CALM

        # Emotional state influence
        if emotional_state:
            stability = emotional_state.get("stability", 0.8)
            if stability < 0.5:
                return SisterRelationalMode.CALM

        # Default: Steady (equal status, candid, balanced)
        return SisterRelationalMode.STEADY

    def set_mode(self, mode: SisterRelationalMode) -> None:
        """Set sister relational mode directly.

        Args:
            mode: Sister relational mode to set.
        """
        self._current_mode = mode
        self._mode_history.append(mode)
        # Keep only last 50 modes
        if len(self._mode_history) > 50:
            self._mode_history = self._mode_history[-50:]

    def is_playful_allowed(self, autonomy_band: Optional[int] = None) -> bool:
        """Check if playful mode is allowed.

        Per spec: §2.2 - Playful mischief only when safety, autonomy, and context allow.

        Args:
            autonomy_band: Current autonomy band.

        Returns:
            True if playful mode is allowed, False otherwise.
        """
        if autonomy_band is None:
            return False
        return autonomy_band >= 40


