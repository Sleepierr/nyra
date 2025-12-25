"""Mistake analysis for Phase 6.

Per spec: subsystems/base1.0/subsystem_skill_tree_learning_engine.md
"""

from __future__ import annotations

from typing import List, Optional

from .models import LearningOpportunity, MistakePattern


class MistakeAnalyzer:
    """Analyzes mistakes for learning opportunities.

    Phase 6: Basic mistake analysis with error correction proposals.
    """

    def analyze_mistake_pattern(
        self, pattern: MistakePattern
    ) -> Optional[LearningOpportunity]:
        """Analyze mistake pattern to identify learning opportunity.

        Args:
            pattern: Mistake pattern to analyze.

        Returns:
            Learning opportunity if valid, None otherwise.
        """
        # Phase 6: Basic analysis
        # Map mistake type to skill ID (simplified)
        skill_id = self._map_mistake_to_skill(pattern.mistake_type)

        if not skill_id:
            return None

        return LearningOpportunity(
            skill_id=skill_id,
            learning_type="correction",
            priority=pattern.severity,
            description=f"Correction needed for {pattern.mistake_type}",
        )

    def _map_mistake_to_skill(self, mistake_type: str) -> Optional[str]:
        """Map mistake type to relevant skill ID.

        Args:
            mistake_type: Type of mistake.

        Returns:
            Skill ID if mapping found, None otherwise.
        """
        # Phase 6: Basic mapping
        mapping = {
            "reasoning_error": "reasoning_skill",
            "emotional_misjudgment": "emotional_intelligence",
            "debate_weakness": "debate_mastery",
            "planning_error": "planning_skill",
            "communication_error": "communication_skill",
        }

        mistake_lower = mistake_type.lower()
        for key, skill_id in mapping.items():
            if key in mistake_lower:
                return skill_id

        return None

