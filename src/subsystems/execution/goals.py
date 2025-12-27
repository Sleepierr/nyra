"""Goal system and cognitive loop execution infrastructure for Phase 5.

Implements CognitiveLoopExecutor and GoalManager for goal formation and execution.

Phase 5: Basic goal formation and cognitive loop - minimal logic to enable "thinking".
Per spec: subsystems/base1.0/subsystem_cognitive_goal_system.md
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import ExecutionContext, SubsystemExecutor
from ...state.keys import SubsystemKeys


# -----------------------------------------------------------------------------
# Data Structures
# -----------------------------------------------------------------------------


class GoalTier(str, Enum):
    """Goal hierarchy tiers.

    Per spec: subsystem_cognitive_goal_system.md §2.1
    """

    BIG = "big"
    MID = "mid"
    SUB = "sub"


class GoalOrigin(str, Enum):
    """Goal origin sources."""

    SLEPP = "Slepp"
    NYRA = "Nyra"
    SYSTEM = "System"


class GoalStatus(str, Enum):
    """Goal status values."""

    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class GoalObject(BaseModel):
    """Represents a goal in the goal system.

    Per spec: subsystem_cognitive_goal_system.md §2.2
    """

    goal_id: str
    tier: GoalTier
    description: str
    origin: GoalOrigin
    emotional_context: Dict[str, Any] = {}
    cognitive_context: Dict[str, Any] = {}
    debate_origin_notes: Dict[str, Any] = {}
    dependencies: List[str] = []  # List of goal_ids
    constraints: List[str] = []
    status: GoalStatus = GoalStatus.ACTIVE
    plan_graph: Dict[str, Any] = {}
    progress_score: float = 0.0  # [0.0, 1.0]
    autonomy_flags: Dict[str, Any] = {}


class CognitiveLoopStage(str, Enum):
    """Stages of the cognitive loop.

    Per spec: subsystem_cognitive_goal_system.md §2
    """

    PERCEIVE = "perceive"
    INTERPRET = "interpret"
    EVALUATE = "evaluate"
    PROPOSE = "propose"
    DEBATE = "debate"
    COMMIT = "commit"
    PLAN = "plan"
    ACT = "act"
    REFLECT = "reflect"


@dataclass
class CognitiveLoopContext:
    """Context passed through cognitive loop stages."""

    current_stage: CognitiveLoopStage
    input_data: Any
    interpreted_data: Optional[Dict[str, Any]] = None
    evaluated_options: Optional[List[Any]] = None
    proposed_goal: Optional[GoalObject] = None
    debate_outcome: Optional[Any] = None
    committed_goal: Optional[GoalObject] = None
    plan: Optional[Dict[str, Any]] = None
    action_result: Optional[Any] = None
    reflection: Optional[Dict[str, Any]] = None


class GoalManager:
    """Manages goal lifecycle (formation, commitment, tracking).

    Phase 5: Basic goal management - no persistence, in-memory only.
    """

    def __init__(self, context: ExecutionContext) -> None:
        """Initialize the goal manager.

        Args:
            context: Execution context.
        """
        self._context = context
        self._goals: Dict[str, GoalObject] = {}

    def create_goal(
        self,
        description: str,
        tier: GoalTier,
        origin: GoalOrigin,
        emotional_context: Optional[Dict[str, Any]] = None,
    ) -> GoalObject:
        """Create a new goal.

        Phase 5: Basic goal creation.

        Args:
            description: Goal description.
            tier: Goal tier level.
            origin: Goal origin source.
            emotional_context: Optional emotional context.

        Returns:
            Created GoalObject.
        """
        goal_id = str(uuid.uuid4())
        goal = GoalObject(
            goal_id=goal_id,
            tier=tier,
            description=description,
            origin=origin,
            emotional_context=emotional_context or {},
            status=GoalStatus.ACTIVE,
        )
        self._goals[goal_id] = goal

        # Emit goal formation event
        self._context.emit_event(
            "goal.formed",
            {
                "goal_id": goal_id,
                "tier": tier.value,
                "origin": origin.value,
                "description": description,
            },
        )

        return goal

    def get_goal(self, goal_id: str) -> Optional[GoalObject]:
        """Get a goal by ID.

        Args:
            goal_id: The goal ID.

        Returns:
            GoalObject if found, None otherwise.
        """
        return self._goals.get(goal_id)

    def update_goal(self, goal: GoalObject) -> None:
        """Update a goal.

        Args:
            goal: The updated goal object.
        """
        if goal.goal_id in self._goals:
            self._goals[goal.goal_id] = goal
            self._context.emit_event(
                "goal.updated",
                {"goal_id": goal.goal_id, "status": goal.status.value},
            )

    def get_active_goals(self) -> List[GoalObject]:
        """Get all active goals.

        Returns:
            List of active goals.
        """
        return [g for g in self._goals.values() if g.status == GoalStatus.ACTIVE]


class CognitiveLoopExecutor(SubsystemExecutor):
    """Executes the cognitive loop.

    Per spec: PERCEIVE → INTERPRET → EVALUATE → PROPOSE → DEBATE → COMMIT → PLAN → ACT → REFLECT

    Phase 5: Basic loop execution - minimal logic at each stage.
    """

    def __init__(self) -> None:
        """Initialize the cognitive loop executor."""
        super().__init__(SubsystemKeys.COGNITIVE_GOAL_SYSTEM)
        self._goal_manager: Optional[GoalManager] = None

    def _on_initialized(self) -> None:
        """Initialize goal manager and subscribe to events."""
        if self._context is None:
            return
        self._goal_manager = GoalManager(self._context)

        # Subscribe to events that trigger cognitive processing
        self.context.event_bus.subscribe("interaction.*", self._on_interaction_event)
        self.context.event_bus.subscribe("task.*", self._on_task_event)

    def _on_interaction_event(self, event: Any) -> None:
        """Handle interaction events.

        Phase 5: Basic handler - trigger cognitive loop if needed.
        """
        # Phase 5: Event handling infrastructure
        pass

    def _on_task_event(self, event: Any) -> None:
        """Handle task events.

        Phase 5: Basic handler.
        """
        pass

    def _execute_impl(self, input_data: Any) -> Dict[str, Any]:
        """Execute cognitive loop with input.

        Args:
            input_data: Input to process (can be dict, event, etc.).

        Returns:
            Dictionary with loop execution result.
        """
        context = CognitiveLoopContext(
            current_stage=CognitiveLoopStage.PERCEIVE,
            input_data=input_data,
        )

        # Execute loop stages
        self._perceive(context)
        self._interpret(context)
        self._evaluate(context)
        self._propose(context)

        # Phase 5: Skip debate for now (requires debate manager integration)
        # self._debate(context)

        if context.proposed_goal:
            self._commit(context)

        # Phase 5: Basic planning and action
        if context.committed_goal:
            self._plan(context)
            self._act(context)
            self._reflect(context)

        return {
            "stage": context.current_stage.value,
            "goal_id": context.committed_goal.goal_id if context.committed_goal else None,
            "action_result": context.action_result,
        }

    def _perceive(self, context: CognitiveLoopContext) -> None:
        """Stage 1: PERCEIVE - Receive and filter inputs.

        Phase 5: Basic perception - just record input.
        """
        context.current_stage = CognitiveLoopStage.PERCEIVE
        # Phase 5: Minimal logic - input already in context.input_data

    def _interpret(self, context: CognitiveLoopContext) -> None:
        """Stage 2: INTERPRET - Convert perception to structured meaning.

        Phase 5: Basic interpretation - extract description/type.
        """
        context.current_stage = CognitiveLoopStage.INTERPRET

        # Phase 5: Basic/minimal interpretation
        if isinstance(context.input_data, dict):
            context.interpreted_data = context.input_data.copy()
        else:
            context.interpreted_data = {"raw": str(context.input_data)}

    def _evaluate(self, context: CognitiveLoopContext) -> None:
        """Stage 3: EVALUATE - Assess options and alignment.

        Phase 5: Basic evaluation - check alignment scores (simplified).
        """
        context.current_stage = CognitiveLoopStage.EVALUATE

        # Phase 5: Query emotional and autonomy state
        if self._context:
            try:
                emotion_adapter = self._context.get_adapter(SubsystemKeys.EMOTIONAL_ENGINE)
                autonomy_adapter = self._context.get_adapter(SubsystemKeys.AUTONOMY)
                # Phase 5: State shells are empty, so we proceed with basic logic
            except Exception:
                pass

        context.evaluated_options = [{"option": "proceed", "alignment": 0.5}]

    def _propose(self, context: CognitiveLoopContext) -> None:
        """Stage 4: PROPOSE - Generate goal proposal.

        Phase 5: Basic goal formation.
        """
        context.current_stage = CognitiveLoopStage.PROPOSE

        if not context.interpreted_data or not self._goal_manager:
            return

        # Phase 5: Basic goal formation - extract description
        description = context.interpreted_data.get("description", str(context.input_data))

        goal = self._goal_manager.create_goal(
            description=description[:200],  # Truncate for safety
            tier=GoalTier.SUB,  # Phase 5: Default to SUB tier
            origin=GoalOrigin.NYRA,  # Phase 5: Default to Nyra-originated
        )

        context.proposed_goal = goal

    def _debate(self, context: CognitiveLoopContext) -> None:
        """Stage 5: DEBATE - Run debate if required.

        Phase 5: Debate integration deferred - would require DebateManager.
        """
        context.current_stage = CognitiveLoopStage.DEBATE
        # Phase 5: Debate integration will be handled by orchestrator
        context.debate_outcome = None

    def _commit(self, context: CognitiveLoopContext) -> None:
        """Stage 6: COMMIT - Commit goal to registry.

        Phase 5: Basic commitment.
        """
        context.current_stage = CognitiveLoopStage.COMMIT

        if context.proposed_goal:
            # Phase 5: Basic commit - goal already in manager
            context.committed_goal = context.proposed_goal

            # Emit commit event
            if self._context:
                self._context.emit_event(
                    "goal.committed",
                    {"goal_id": context.committed_goal.goal_id},
                )

    def _plan(self, context: CognitiveLoopContext) -> None:
        """Stage 7: PLAN - Decompose goal into plan.

        Phase 5: Basic planning - minimal plan structure.
        """
        context.current_stage = CognitiveLoopStage.PLAN

        if context.committed_goal:
            # Phase 5: Basic plan - simple single-step plan
            context.plan = {
                "steps": [{"action": "execute", "description": context.committed_goal.description}],
                "complexity": "low",
            }
            context.committed_goal.plan_graph = context.plan

    def _act(self, context: CognitiveLoopContext) -> None:
        """Stage 8: ACT - Execute plan.

        Phase 5: Basic action - emit event, update goal progress.
        """
        context.current_stage = CognitiveLoopStage.ACT

        if context.committed_goal and self._goal_manager:
            # Phase 5: Basic action - just update progress
            context.committed_goal.progress_score = 0.5  # Phase 5: Arbitrary progress
            self._goal_manager.update_goal(context.committed_goal)

            context.action_result = {"status": "executed", "progress": 0.5}

    def _reflect(self, context: CognitiveLoopContext) -> None:
        """Stage 9: REFLECT - Evaluate effectiveness and learn.

        Phase 5: Basic reflection - minimal evaluation.
        """
        context.current_stage = CognitiveLoopStage.REFLECT

        context.reflection = {
            "effectiveness": 0.5,  # Phase 5: Default moderate effectiveness
            "learnings": [],
        }

        # Emit reflection event
        if self._context:
            self._context.emit_event(
                "goal.reflected",
                {
                    "goal_id": context.committed_goal.goal_id if context.committed_goal else None,
                },
            )






