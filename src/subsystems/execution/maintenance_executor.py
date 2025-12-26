"""Maintenance subsystem executor for Phase 6.

Execution runtime for maintenance subsystem.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ...maintenance.orchestrator import MaintenanceOrchestrator
from ...maintenance.models import MaintenanceTriggerType
from ...state.keys import SubsystemKeys
from .base import SubsystemExecutor


class MaintenanceExecutor(SubsystemExecutor):
    """Executes maintenance subsystem logic.

    Phase 6: Integrates MaintenanceOrchestrator with ExecutionContext.
    """

    def __init__(self) -> None:
        """Initialize maintenance executor."""
        super().__init__(SubsystemKeys.NYRAHOME_BRAIN)
        self._orchestrator: Optional[MaintenanceOrchestrator] = None

    def _on_initialized(self) -> None:
        """Initialize maintenance orchestrator."""
        if self._context is None:
            return

        self._orchestrator = MaintenanceOrchestrator(
            context=self._context,
            scheduler=self._context.scheduler,
        )
        self._orchestrator.initialize()

        # Subscribe to maintenance trigger events
        self.context.event_bus.subscribe("system.drift_detected", self._on_drift_detected)
        self.context.event_bus.subscribe("autonomy.band_transition", self._on_autonomy_transition)

    def _on_drift_detected(self, event: Any) -> None:
        """Handle drift detection for self-repair."""
        if self._orchestrator:
            self._orchestrator.handle_maintenance_trigger(
                MaintenanceTriggerType.DRIFT_SIGNAL,
                event.payload if hasattr(event, "payload") else {},
            )

    def _on_autonomy_transition(self, event: Any) -> None:
        """Handle autonomy transition for maintenance."""
        if self._orchestrator:
            self._orchestrator.handle_maintenance_trigger(
                MaintenanceTriggerType.AUTONOMY_TRANSITION,
                event.payload if hasattr(event, "payload") else {},
            )

    def _execute_impl(self, input_data: Any) -> Dict[str, Any]:
        """Execute maintenance processing.

        Args:
            input_data: Optional input data.

        Returns:
            Dictionary with maintenance results.
        """
        if self._orchestrator is None:
            raise RuntimeError("Maintenance orchestrator not initialized")

        # Run micro-maintenance
        micro_results = self._orchestrator.run_micro_maintenance()

        return {
            "micro_maintenance": micro_results,
        }



