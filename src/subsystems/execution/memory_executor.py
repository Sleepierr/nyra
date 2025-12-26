"""Memory subsystem executor for Phase 6.

Execution runtime for memory subsystem.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ...memory.pipeline import MemoryPipeline
from ...memory.models import STMMemoryEntry
from ...state.keys import SubsystemKeys
from .base import SubsystemExecutor


class MemoryExecutor(SubsystemExecutor):
    """Executes memory subsystem logic.

    Phase 6: Integrates MemoryPipeline with ExecutionContext.
    """

    def __init__(self) -> None:
        """Initialize memory executor."""
        super().__init__(SubsystemKeys.MEMORY_EXPERIENCE)
        self._pipeline: Optional[MemoryPipeline] = None

    def _on_initialized(self) -> None:
        """Initialize memory pipeline and subscribe to events."""
        if self._context is None:
            return

        self._pipeline = MemoryPipeline(
            state_container=self._context._state_container,
        )

        # Subscribe to events that trigger memory capture
        self.context.event_bus.subscribe("interaction.*", self._on_interaction_event)
        self.context.event_bus.subscribe("goal.*", self._on_goal_event)
        self.context.event_bus.subscribe("debate.*", self._on_debate_event)

    def _on_interaction_event(self, event: Any) -> None:
        """Handle interaction events for memory capture."""
        # Phase 6: Basic event handling - trigger memory capture
        pass

    def _on_goal_event(self, event: Any) -> None:
        """Handle goal events for memory capture."""
        # Phase 6: Basic event handling
        pass

    def _on_debate_event(self, event: Any) -> None:
        """Handle debate events for memory capture."""
        # Phase 6: Basic event handling
        pass

    def _execute_impl(self, input_data: Any) -> Dict[str, Any]:
        """Execute memory processing.

        Args:
            input_data: STM entry or raw event data to process.

        Returns:
            Dictionary with processing results.
        """
        if self._pipeline is None:
            raise RuntimeError("Memory pipeline not initialized")

        # Convert input to STM entry if needed
        if isinstance(input_data, STMMemoryEntry):
            stm_entry = input_data
        else:
            # Phase 6: Basic conversion
            stm_entry = STMMemoryEntry(
                raw_payload=input_data if isinstance(input_data, dict) else {"data": str(input_data)},
            )

        # Process through pipeline
        ltm_entry = self._pipeline.process_stm_entry(stm_entry)

        if ltm_entry:
            return {"memory_id": ltm_entry.memory_id, "status": "consolidated"}
        else:
            return {"status": "discarded"}



