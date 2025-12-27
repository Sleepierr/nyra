"""Social rhythm manager for Phase 7.

Manages rhythm intensity, chaos management, and social rhythm orchestration.
Per spec: subsystems/base1.0/subsystem_social_rhythm_micro_behavior_engine.md
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..presence.models import PresenceState
from .check_in import CheckInManager
from .models import ChaosIntensityLevel
from .pacing import PacingManager
from .quiet_hours import QuietHoursManager
from .silence_handler import SilenceHandler


class RhythmManager:
    """Manages social rhythm, chaos intensity, and pacing.

    Per spec: subsystems/base1.0/subsystem_social_rhythm_micro_behavior_engine.md
    Phase 7: Rhythm intensity, chaos management, integration with presence and pacing.
    """

    def __init__(
        self,
        quiet_hours_manager: QuietHoursManager,
        pacing_manager: PacingManager,
        silence_handler: SilenceHandler,
        check_in_manager: CheckInManager,
    ) -> None:
        """Initialize rhythm manager.

        Args:
            quiet_hours_manager: Quiet hours manager instance.
            pacing_manager: Pacing manager instance.
            silence_handler: Silence handler instance.
            check_in_manager: Check-in manager instance.
        """
        self._quiet_hours = quiet_hours_manager
        self._pacing = pacing_manager
        self._silence = silence_handler
        self._check_in = check_in_manager
        self._current_chaos_intensity: int = 30  # Default: moderate

    def calculate_chaos_intensity(self, autonomy_band: Optional[int] = None) -> int:
        """Calculate chaos intensity based on autonomy band.

        Per spec: subsystems/base1.0/subsystem_social_rhythm_micro_behavior_engine.md §5

        Args:
            autonomy_band: Current autonomy band (0-100).

        Returns:
            Chaos intensity (0-100).
        """
        if autonomy_band is None:
            return 30  # Default moderate

        # Band 0-20: Constrained Rhythm (0-10)
        if autonomy_band < 20:
            return 5

        # Band 20-40: Light Rhythm (10-30)
        if autonomy_band < 40:
            return 20

        # Band 40-60: Balanced Rhythm (30-60) - baseline
        if autonomy_band < 60:
            return 45

        # Band 60-80: Expressive Rhythm (60-85)
        if autonomy_band < 80:
            return 75

        # Band 80-100: Very High (85+) - future eras, limited in Base 1.0
        return 85

    def get_chaos_level(self, autonomy_band: Optional[int] = None) -> ChaosIntensityLevel:
        """Get chaos intensity level enum.

        Args:
            autonomy_band: Current autonomy band.

        Returns:
            Chaos intensity level.
        """
        intensity = self.calculate_chaos_intensity(autonomy_band)

        if intensity < 10:
            return ChaosIntensityLevel.NONE
        if intensity < 30:
            return ChaosIntensityLevel.LOW
        if intensity < 60:
            return ChaosIntensityLevel.MODERATE
        if intensity < 85:
            return ChaosIntensityLevel.HIGH

        return ChaosIntensityLevel.VERY_HIGH

    def adjust_chaos_for_presence(
        self, base_intensity: int, presence_state: PresenceState
    ) -> int:
        """Adjust chaos intensity based on presence state.

        Per spec: §7 - Social rhythm expresses presence modes over time.

        Args:
            base_intensity: Base chaos intensity.
            presence_state: Current presence state.

        Returns:
            Adjusted chaos intensity.
        """
        # Guarded Presence: no chaos
        if presence_state == PresenceState.GUARDED:
            return 0

        # Background Presence: minimal chaos
        if presence_state == PresenceState.BACKGROUND:
            return base_intensity // 4

        # Quiet Presence: reduced chaos
        if presence_state == PresenceState.QUIET:
            return base_intensity // 2

        # Reflective Presence: minimal chaos
        if presence_state == PresenceState.REFLECTIVE:
            return base_intensity // 3

        # Active and Playful Presence: full chaos
        return base_intensity

    def get_quiet_hours_manager(self) -> QuietHoursManager:
        """Get quiet hours manager."""
        return self._quiet_hours

    def get_pacing_manager(self) -> PacingManager:
        """Get pacing manager."""
        return self._pacing

    def get_silence_handler(self) -> SilenceHandler:
        """Get silence handler."""
        return self._silence

    def get_check_in_manager(self) -> CheckInManager:
        """Get check-in manager."""
        return self._check_in


