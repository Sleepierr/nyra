"""Maintenance orchestrator for Phase 6.

Coordinates all maintenance activities.

Per spec: subsystems/base1.0/subsystem_nyrahome_brain.md §X.7
"""

from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

from .deep_maintenance import DeepMaintenanceManager
from .micro_maintenance import MicroMaintenanceManager
from .models import MaintenanceReport, MaintenanceTriggerType
from .self_repair import SelfRepairManager

if TYPE_CHECKING:
    from ...events import Scheduler
    from ...subsystems.execution.base import ExecutionContext


class MaintenanceOrchestrator:
    """Coordinates all maintenance activities.

    Phase 6: Coordinates micro, deep, and self-repair maintenance.
    """

    def __init__(
        self,
        context: Optional["ExecutionContext"] = None,
        scheduler: Optional["Scheduler"] = None,
    ) -> None:
        """Initialize maintenance orchestrator.

        Args:
            context: Optional execution context.
            scheduler: Optional scheduler for scheduled maintenance.
        """
        self._context = context
        self._scheduler = scheduler
        self._micro_maintenance = MicroMaintenanceManager()
        self._deep_maintenance = DeepMaintenanceManager()
        self._self_repair = SelfRepairManager()

    def initialize(self) -> None:
        """Initialize scheduled maintenance triggers."""
        # Phase 6: Basic initialization
        # Full scheduled maintenance setup deferred
        pass

    def handle_maintenance_trigger(
        self, trigger: MaintenanceTriggerType, context: Dict[str, Any]
    ) -> Optional[MaintenanceReport]:
        """Handle maintenance trigger.

        Args:
            trigger: Maintenance trigger type.
            context: Trigger context.

        Returns:
            Maintenance report if deep maintenance executed, None otherwise.
        """
        if trigger == MaintenanceTriggerType.DRIFT_SIGNAL:
            self._self_repair.handle_drift_detection(context)
        elif trigger == MaintenanceTriggerType.AUTONOMY_TRANSITION:
            self._self_repair.handle_autonomy_transition(context)
        elif trigger == MaintenanceTriggerType.SCHEDULED:
            return self._deep_maintenance.execute_deep_maintenance()

        return None

    def run_micro_maintenance(self) -> Dict[str, Any]:
        """Run micro-maintenance.

        Returns:
            Micro-maintenance results.
        """
        return self._micro_maintenance.run_micro_maintenance()





