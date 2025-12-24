"""Base execution infrastructure for Phase 5.

Provides SubsystemExecutor base class and ExecutionContext for subsystem runtime.

Phase 5: Infrastructure that enables subsystems to execute and influence each other.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional, TYPE_CHECKING

from ...events import EventBus, EventFactory, Scheduler
from ...state.keys import SubsystemKeys
from ...state.models.event_envelope import EventEnvelope
from ...state.wiring import SubsystemAdapter, SubsystemAdapterFactory

if TYPE_CHECKING:
    from ...state.container import StateContainer


class ExecutionContext:
    """Execution context providing access to state, events, and other subsystems.

    Provides unified access to:
    - State adapters (via SubsystemAdapterFactory)
    - Event bus for communication
    - Event factory for creating events
    - Scheduler for time-based operations

    Phase 5: Infrastructure only - no behavior.
    """

    def __init__(
        self,
        state_container: "StateContainer",
        event_bus: EventBus,
        event_factory: EventFactory,
        scheduler: Scheduler,
        instance_id: str,
    ) -> None:
        """Initialize execution context.

        Args:
            state_container: The state container for state access.
            event_bus: Event bus for subsystem communication.
            event_factory: Factory for creating events.
            scheduler: Scheduler for time-based operations.
            instance_id: Current instance identifier.
        """
        self._state_container = state_container
        self._event_bus = event_bus
        self._event_factory = event_factory
        self._scheduler = scheduler
        self._instance_id = instance_id
        self._adapter_factory = SubsystemAdapterFactory(state_container)

    @property
    def instance_id(self) -> str:
        """Return the current instance ID."""
        return self._instance_id

    def get_adapter(self, subsystem_key: SubsystemKeys) -> SubsystemAdapter:
        """Get an adapter for accessing subsystem state.

        Args:
            subsystem_key: The subsystem to get an adapter for.

        Returns:
            A SubsystemAdapter instance.
        """
        return self._adapter_factory.get_adapter(subsystem_key)

    def emit_event(
        self,
        event_type: str,
        payload: dict[str, Any],
        source_kind: str = "home",
        meta: Optional[dict[str, Any]] = None,
    ) -> EventEnvelope:
        """Emit an event to the event bus.

        Args:
            event_type: Namespaced event type (e.g., "emotion.mood_changed").
            payload: Event payload data.
            source_kind: Source instance kind (home, secondary, transient, clone).
            meta: Optional metadata.

        Returns:
            The created event envelope.
        """
        event = self._event_factory.create(
            source_instance_id=self._instance_id,
            source_kind=source_kind,  # type: ignore
            event_type=event_type,
            payload=payload,
            meta=meta,
        )
        self._event_bus.emit(event)
        return event

    @property
    def event_bus(self) -> EventBus:
        """Return the event bus for direct access if needed."""
        return self._event_bus

    @property
    def scheduler(self) -> Scheduler:
        """Return the scheduler for direct access if needed."""
        return self._scheduler


class SubsystemExecutor(ABC):
    """Abstract base class for subsystem executors.

    Each cognitive subsystem implements an executor that:
    - Has access to execution context (state, events, scheduler)
    - Can execute logic (makes decisions, processes inputs)
    - Can emit influence events
    - Can register callbacks for state changes
    - Integrates with other subsystems

    Phase 5: Enables subsystems to "think" and influence each other.
    """

    def __init__(self, subsystem_key: SubsystemKeys) -> None:
        """Initialize the subsystem executor.

        Args:
            subsystem_key: The subsystem this executor manages.
        """
        self._subsystem_key = subsystem_key
        self._context: Optional[ExecutionContext] = None
        self._adapter: Optional[SubsystemAdapter] = None
        self._state_change_callbacks: List[Callable[[], None]] = []

    @property
    def subsystem_key(self) -> SubsystemKeys:
        """Return the subsystem key this executor manages."""
        return self._subsystem_key

    def initialize(self, context: ExecutionContext) -> None:
        """Initialize the executor with execution context.

        Args:
            context: The execution context providing state/event access.
        """
        self._context = context
        self._adapter = context.get_adapter(self._subsystem_key)
        self._on_initialized()

    @abstractmethod
    def _on_initialized(self) -> None:
        """Called after context and adapter are set up.

        Subclasses can override to perform initialization logic.
        """

    def execute(self, input_data: Any) -> Any:
        """Execute subsystem logic with given input.

        Args:
            input_data: Input to process (type varies by subsystem).

        Returns:
            Execution result (type varies by subsystem).

        Raises:
            RuntimeError: If executor is not initialized.
        """
        if self._context is None or self._adapter is None:
            raise RuntimeError(
                f"Executor for {self._subsystem_key.value} not initialized. "
                "Call initialize() first."
            )
        return self._execute_impl(input_data)

    @abstractmethod
    def _execute_impl(self, input_data: Any) -> Any:
        """Subclass-specific execution logic.

        Args:
            input_data: Input to process.

        Returns:
            Execution result.
        """

    def on_state_change(self, callback: Callable[[], None]) -> None:
        """Register a callback to be called when subsystem state changes.

        Args:
            callback: Function to call when state changes (no arguments).
        """
        self._state_change_callbacks.append(callback)

    def _notify_state_change(self) -> None:
        """Notify all registered callbacks of a state change."""
        for callback in self._state_change_callbacks:
            try:
                callback()
            except Exception:
                # Phase 5: Basic error handling - continue on callback errors
                pass

    def emit_influence_event(
        self, event_type: str, payload: dict[str, Any], meta: Optional[dict[str, Any]] = None
    ) -> EventEnvelope:
        """Emit an influence event to notify other subsystems.

        Args:
            event_type: Namespaced event type.
            payload: Event payload.
            meta: Optional metadata.

        Returns:
            The created event envelope.

        Raises:
            RuntimeError: If executor is not initialized.
        """
        if self._context is None:
            raise RuntimeError("Executor not initialized")
        return self._context.emit_event(
            event_type=event_type,
            payload=payload,
            source_kind="home",  # Phase 5: Default to home
            meta=meta,
        )

    @property
    def adapter(self) -> SubsystemAdapter:
        """Return the state adapter for this subsystem.

        Returns:
            The SubsystemAdapter instance.

        Raises:
            RuntimeError: If executor is not initialized.
        """
        if self._adapter is None:
            raise RuntimeError("Executor not initialized")
        return self._adapter

    @property
    def context(self) -> ExecutionContext:
        """Return the execution context.

        Returns:
            The ExecutionContext instance.

        Raises:
            RuntimeError: If executor is not initialized.
        """
        if self._context is None:
            raise RuntimeError("Executor not initialized")
        return self._context
