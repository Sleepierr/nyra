"""Cognitive orchestration infrastructure for Phase 5.

Implements CognitiveOrchestrator to coordinate all cognitive subsystems and manage
active influence between them.

Phase 5: Brings subsystems together to enable Nyra to "think".
"""

from __future__ import annotations

import uuid
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from ...events import EventBus, EventFactory, Scheduler
from ...state.container import StateContainer
from ...state.keys import SubsystemKeys

from .autonomy import AutonomyFrameworkExecutor
from .base import ExecutionContext, SubsystemExecutor
from .debate import DebateManager
from .emotion import EmotionalEngineExecutor
from .goals import CognitiveLoopExecutor
from .identity_executor import IdentityContinuityExecutor
from .learning_executor import LearningExecutor
from .memory_executor import MemoryExecutor
from .maintenance_executor import MaintenanceExecutor


class IntegrationManager:
    """Manages active influence between subsystems.

    Phase 5: Coordinates event-driven and callback-based influence.
    """

    def __init__(self, event_bus: EventBus, context: ExecutionContext) -> None:
        """Initialize the integration manager.

        Args:
            event_bus: Event bus for routing events.
            context: Execution context.
        """
        self._event_bus = event_bus
        self._context = context
        self._influence_callbacks: Dict[str, List[Callable[[Any], None]]] = {}
        self._executors_cache: Optional[Dict[SubsystemKeys, SubsystemExecutor]] = None

    def register_influence_callback(
        self, event_pattern: str, callback: Callable[[Any], None]
    ) -> str:
        """Register a callback for influence events.

        Args:
            event_pattern: Event pattern to match (e.g., "emotion.*").
            callback: Callback function to invoke.

        Returns:
            Subscription ID for later unsubscription.
        """
        return self._event_bus.subscribe(event_pattern, callback)

    def wire_emotional_influence(
        self, goal_executor: CognitiveLoopExecutor, executors: Dict[SubsystemKeys, SubsystemExecutor]
    ) -> None:
        """Wire emotional engine to influence goal formation.

        Phase 5: Active influence - emotional state affects goal priorities.

        Args:
            goal_executor: Goal system executor.
            executors: Dictionary of all executors.
        """
        emotion_executor = executors.get(SubsystemKeys.EMOTIONAL_ENGINE)
        if emotion_executor and isinstance(emotion_executor, EmotionalEngineExecutor):

            def on_goal_formation(event: Any) -> None:
                """Influence goal formation based on emotional state."""
                # Phase 5: Emotional influence on goal formation
                if event.type.startswith("goal.formed"):
                    emotional_influence = emotion_executor.influence_goal_formation(
                        goal_description=event.payload.get("description", ""),
                        goal_context=event.payload,
                    )
                    # Emit influence event
                    self._context.emit_event(
                        "emotion.goal_influence",
                        emotional_influence,
                    )

            self._event_bus.subscribe("goal.formed", on_goal_formation)

    def wire_autonomy_enforcement(self, executors: Dict[SubsystemKeys, SubsystemExecutor]) -> None:
        """Wire autonomy system to enforce permissions on other subsystems.

        Phase 5: Active enforcement - autonomy checks permissions before actions.

        Args:
            executors: Dictionary of all subsystem executors.
        """
        autonomy_executor = executors.get(SubsystemKeys.AUTONOMY)
        if autonomy_executor and isinstance(autonomy_executor, AutonomyFrameworkExecutor):

            def on_action_request(event: Any) -> None:
                """Check autonomy permissions before allowing actions."""
                # Phase 5: Autonomy enforcement
                required_band = event.payload.get("required_band", 0)
                action = event.payload.get("action", "unknown")

                if not autonomy_executor.check_permission(action, required_band):
                    # Emit permission denied event
                    self._context.emit_event(
                        "autonomy.permission_denied",
                        {
                            "action": action,
                            "required_band": required_band,
                            "current_band": autonomy_executor._enforcer.get_current_band()
                            if autonomy_executor._enforcer
                            else 0,
                        },
                    )

            self._event_bus.subscribe("action.request", on_action_request)

    def wire_autonomy_emotional_influence(
        self,
        autonomy_executor: AutonomyFrameworkExecutor,
        executors: Dict[SubsystemKeys, SubsystemExecutor],
    ) -> None:
        """Wire emotional state to influence autonomy evaluation.

        Phase 5: Emotional load affects autonomy scoring.

        Args:
            autonomy_executor: Autonomy framework executor.
            executors: Dictionary of all executors.
        """
        emotion_executor = executors.get(SubsystemKeys.EMOTIONAL_ENGINE)
        if emotion_executor and isinstance(emotion_executor, EmotionalEngineExecutor):

            def on_emotional_change(event: Any) -> None:
                """Update autonomy evaluation based on emotional changes."""
                # Phase 5: Emotional influence on autonomy
                emotional_load = emotion_executor.get_emotional_load()
                # Autonomy system already subscribes to emotion events, this is additional wiring
                pass

            self._event_bus.subscribe("emotion.*", on_emotional_change)

    def set_executors(self, executors: Dict[SubsystemKeys, SubsystemExecutor]) -> None:
        """Set executors for influence wiring.

        Args:
            executors: Dictionary of subsystem executors.
        """
        self._executors_cache = executors


class CognitiveOrchestrator:
    """Coordinates all cognitive subsystems and manages their active influence.

    Phase 5: Brings subsystems together to enable Nyra to "think".
    """

    def __init__(
        self,
        state_container: StateContainer,
        event_bus: EventBus,
        event_factory: EventFactory,
        scheduler: Scheduler,
        instance_id: str = "default",
    ) -> None:
        """Initialize the cognitive orchestrator.

        Args:
            state_container: State container for state access.
            event_bus: Event bus for subsystem communication.
            event_factory: Factory for creating events.
            scheduler: Scheduler for time-based operations.
            instance_id: Instance identifier.
        """
        self._context = ExecutionContext(
            state_container=state_container,
            event_bus=event_bus,
            event_factory=event_factory,
            scheduler=scheduler,
            instance_id=instance_id,
        )

        self._executors: Dict[SubsystemKeys, SubsystemExecutor] = {}
        self._integration_manager = IntegrationManager(event_bus, self._context)

        # Initialize subsystem executors
        self._initialize_executors()

    def _initialize_executors(self) -> None:
        """Initialize all cognitive subsystem executors."""
        # Create executors for Phase 5 subsystems
        executors: List[SubsystemExecutor] = [
            DebateManager(),
            AutonomyFrameworkExecutor(),
            CognitiveLoopExecutor(),
            EmotionalEngineExecutor(),
        ]

        # Phase 6: Add new executors
        executors.extend([
            MemoryExecutor(),
            LearningExecutor(),
            IdentityContinuityExecutor(),
            MaintenanceExecutor(),
        ])

        # Initialize each executor
        for executor in executors:
            executor.initialize(self._context)
            self._executors[executor.subsystem_key] = executor

        # Wire active influence between subsystems
        self._wire_active_influence()

    def _wire_active_influence(self) -> None:
        """Wire subsystems together with active influence mechanisms.

        Phase 5: Event-driven and callback-based active influence.
        """
        # Set executors in integration manager for access
        self._integration_manager.set_executors(self._executors)

        # Wire emotional influence on goal formation
        goal_executor = self._executors.get(SubsystemKeys.COGNITIVE_GOAL_SYSTEM)
        if goal_executor:
            self._integration_manager.wire_emotional_influence(
                goal_executor, self._executors  # type: ignore
            )

        # Wire autonomy enforcement
        self._integration_manager.wire_autonomy_enforcement(self._executors)

        # Wire autonomy-emotional influence
        autonomy_executor = self._executors.get(SubsystemKeys.AUTONOMY)
        if autonomy_executor:
            self._integration_manager.wire_autonomy_emotional_influence(
                autonomy_executor, self._executors  # type: ignore
            )

        # Wire goal system to query emotional state
        if goal_executor and isinstance(goal_executor, CognitiveLoopExecutor):
            emotion_executor = self._executors.get(SubsystemKeys.EMOTIONAL_ENGINE)

            def on_goal_formation_need() -> None:
                """Query emotional state during goal formation."""
                if emotion_executor and isinstance(emotion_executor, EmotionalEngineExecutor):
                    pmv = emotion_executor.current_pmv
                    if pmv:
                        # Emotional state is available for goal formation queries
                        pass

            # Register callback for state queries (direct integration)
            if emotion_executor:
                emotion_executor.on_state_change(on_goal_formation_need)

    def process_input(self, input_data: Any, input_type: str = "interaction") -> Dict[str, Any]:
        """Process input through cognitive subsystems.

        Phase 5: Routes input to appropriate subsystems and coordinates response.

        Args:
            input_data: Input to process.
            input_type: Type of input (e.g., "interaction", "event", "goal").

        Returns:
            Dictionary with processing results.
        """
        # Phase 5: Basic routing - send to cognitive loop for full processing
        cognitive_executor = self._executors.get(SubsystemKeys.COGNITIVE_GOAL_SYSTEM)
        if cognitive_executor:
            result = cognitive_executor.execute(input_data)
            return result

        return {"status": "no_executor", "input_type": input_type}

    def execute_debate(
        self,
        topic: str,
        description: str,
        options: List[Dict[str, str]],
        stakes_level: str = "MEDIUM",
    ) -> Any:
        """Execute a debate on a topic.

        Phase 5: Convenience method for triggering debates.

        Args:
            topic: Debate topic.
            description: Detailed description.
            options: List of option dictionaries with "label" and "description".
            stakes_level: Stakes level (LOW, MEDIUM, HIGH, CRITICAL).

        Returns:
            DebateOutcome.
        """
        from .debate import DebateIssue, OptionSpec, RiskLevel, StakesLevel

        debate_executor = self._executors.get(SubsystemKeys.DEBATE_SYSTEM)
        if not debate_executor or not isinstance(debate_executor, DebateManager):
            raise RuntimeError("Debate executor not available")

        # Create debate issue
        option_specs = [
            OptionSpec(
                option_id=str(i),
                label=opt.get("label", f"Option {i}"),
                description=opt.get("description", ""),
            )
            for i, opt in enumerate(options)
        ]

        issue = DebateIssue(
            issue_id=str(uuid.uuid4()),
            topic=topic,
            description=description,
            options=option_specs,
            stakes_level=StakesLevel(stakes_level),
            risk_level=RiskLevel.MEDIUM,  # Phase 5: Default
        )

        return debate_executor.execute_debate(issue)

    def get_current_autonomy(self) -> Dict[str, Any]:
        """Get current autonomy state.

        Returns:
            Dictionary with score, band, and competency profile.
        """
        autonomy_executor = self._executors.get(SubsystemKeys.AUTONOMY)
        if autonomy_executor:
            return autonomy_executor.execute(None)

        return {"score": 0.0, "band": 0, "competency_profile": {}}

    def get_current_mood(self) -> Dict[str, Any]:
        """Get current emotional state.

        Returns:
            Dictionary with PMV and emotional load.
        """
        emotion_executor = self._executors.get(SubsystemKeys.EMOTIONAL_ENGINE)
        if emotion_executor:
            return emotion_executor.execute(None)

        return {"pmv": {}, "emotional_load": 0.0}

    @property
    def context(self) -> ExecutionContext:
        """Return the execution context."""
        return self._context

    @property
    def executors(self) -> Dict[SubsystemKeys, SubsystemExecutor]:
        """Return dictionary of all subsystem executors."""
        return self._executors


