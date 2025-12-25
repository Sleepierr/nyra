"""Learning subsystem executor for Phase 6.

Execution runtime for learning subsystem.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ...learning.engine import LearningEngine
from ...learning.skill_tree import SkillTree
from ...state.keys import SubsystemKeys
from .base import SubsystemExecutor


class LearningExecutor(SubsystemExecutor):
    """Executes learning subsystem logic.

    Phase 6: Integrates LearningEngine with ExecutionContext.
    """

    def __init__(self) -> None:
        """Initialize learning executor."""
        super().__init__(SubsystemKeys.SKILL_TREE_LEARNING_ENGINE)
        self._learning_engine: Optional[LearningEngine] = None

    def _on_initialized(self) -> None:
        """Initialize learning engine and subscribe to events."""
        if self._context is None:
            return

        skill_tree = SkillTree()
        self._learning_engine = LearningEngine(
            skill_tree=skill_tree,
            context=self._context,
        )

        # Subscribe to experience integration events
        self.context.event_bus.subscribe("experience.integrated", self._on_experience_integrated)

    def _on_experience_integrated(self, event: Any) -> None:
        """Handle experience integration events for learning."""
        # Phase 6: Trigger learning loop on experience integration
        if self._learning_engine:
            self._learning_engine.execute_learning_loop()

    def _execute_impl(self, input_data: Any) -> Dict[str, Any]:
        """Execute learning loop.

        Args:
            input_data: Optional input data.

        Returns:
            Dictionary with learning results.
        """
        if self._learning_engine is None:
            raise RuntimeError("Learning engine not initialized")

        return self._learning_engine.execute_learning_loop()

