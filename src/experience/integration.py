"""Experience integration for Phase 6.

Integrates experiences into subsystems (learning, planning, emotional regulation, etc.).

Per spec: subsystems/base1.0/subsystem_memory_experience.md §7.5
"""

from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

from .models import ExperienceObject, XPUpdate

if TYPE_CHECKING:
    from ...state.container import StateContainer
    from ...subsystems.execution.base import ExecutionContext


class ExperienceIntegrator:
    """Integrates experiences into subsystems.

    Per spec: subsystem_memory_experience.md §7.5
    Phase 6: Connects experiences to learning, planning, emotional regulation, attention routing, autonomy calibration.

    Ensures no identity modification (Base 1.0 constraint).
    """

    def __init__(self, context: Optional["ExecutionContext"] = None) -> None:
        """Initialize the integrator.

        Args:
            context: Optional execution context for subsystem access.
        """
        self._context = context

    def integrate_experience(self, experience: ExperienceObject) -> Dict[str, Any]:
        """Integrate experience into subsystems.

        Per spec: subsystem_memory_experience.md §7.5
        Integration connects memory to:
        - Experience System (already done)
        - XP engine
        - Learning system updates
        - Planning optimizations
        - Emotional regulation updates
        - Attention routing refinements
        - Autonomy calibration

        Args:
            experience: Experience object to integrate.

        Returns:
            Dictionary with integration results.
        """
        results: Dict[str, Any] = {}

        # Create XP update
        xp_update = self._create_xp_update(experience)
        results["xp_update"] = xp_update

        # Integrate with learning system (will be handled by LearningExecutor)
        if self._context:
            self._context.emit_event(
                "experience.integrated",
                {
                    "experience_id": experience.experience_id,
                    "experience_type": experience.experience_type,
                    "xp_gain": experience.xp_gain,
                },
            )

        # Phase 6: Basic integration
        # Full integration with planning optimizations, emotional regulation, attention routing,
        # and autonomy calibration will be handled by respective executors via event routing

        return results

    def _create_xp_update(self, experience: ExperienceObject) -> XPUpdate:
        """Create XP update from experience.

        Args:
            experience: Experience object.

        Returns:
            XPUpdate structure.
        """
        # Basic XP distribution (full logic in ExperienceProcessor)
        # Import here to avoid circular dependency
        from .processor import ExperienceProcessor

        processor = ExperienceProcessor()
        return processor.create_xp_update(experience, experience.experience_id)

