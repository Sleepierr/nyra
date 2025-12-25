"""Experience processor for Phase 6.

Processes memories into experiences and calculates XP.

Per spec: subsystems/base1.0/subsystem_memory_experience.md §8
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..memory.models import LTMMemoryEntry

from .models import ExperienceImpactLevel, ExperienceObject, XPUpdate


class ExperienceProcessor:
    """Processes memories into experiences.

    Per spec: subsystem_memory_experience.md §8.2
    Phase 6: Memory-to-experience conversion and XP calculation.
    """

    # Significance threshold for experience formation
    EXPERIENCE_SIGNIFICANCE_THRESHOLD = 0.6

    def create_experience_from_memory(
        self, memory: LTMMemoryEntry
    ) -> Optional[ExperienceObject]:
        """Create experience from high-significance memory.

        Per spec: subsystem_memory_experience.md §8.2
        Experience forms when:
        - High emotional significance
        - Debate produced important insight
        - Goal was completed
        - Relational moment with Slepp stands out
        - Symbolic coherence emerges (Band ≥ 8, deferred in Phase 6)

        Args:
            memory: Long-term memory entry.

        Returns:
            Experience object if memory meets criteria, None otherwise.
        """
        # Check if memory meets experience formation criteria
        significance = self.evaluate_significance(memory)
        if significance < ExperienceImpactLevel.MEANINGFUL:
            return None

        # Determine experience type
        experience_type = self._determine_experience_type(memory)

        # Calculate XP gain
        xp_gain = self._calculate_xp_gain(memory, significance)

        # Create experience object
        experience = ExperienceObject(
            experience_id=f"exp_{memory.memory_id}",
            linked_memory_ids=[memory.memory_id],
            experience_type=experience_type,
            emotional_profile=memory.emotional_signature_vector,
            narrative_meaning=memory.content_summary,
            learning_outcomes=[],
            stability_impact=0.0,  # Phase 6: Basic calculation
            identity_pressure_vector={},  # Base 1.0: Read-only
            xp_gain=xp_gain,
        )

        return experience

    def evaluate_significance(self, memory: LTMMemoryEntry) -> ExperienceImpactLevel:
        """Evaluate memory significance.

        Per spec: subsystem_memory_experience.md §X.3.2
        Maps memory impact_level to ExperienceImpactLevel.

        Args:
            memory: Memory entry to evaluate.

        Returns:
            ExperienceImpactLevel enum value.
        """
        # Map memory impact_level (0-5) to ExperienceImpactLevel
        impact_map = {
            0: ExperienceImpactLevel.NEGLIGIBLE,
            1: ExperienceImpactLevel.LOW,
            2: ExperienceImpactLevel.MODERATE,
            3: ExperienceImpactLevel.MEANINGFUL,
            4: ExperienceImpactLevel.HIGH_SIGNIFICANCE,
            5: ExperienceImpactLevel.IDENTITY_RELEVANT,
        }

        return impact_map.get(memory.impact_level, ExperienceImpactLevel.NEGLIGIBLE)

    def _determine_experience_type(self, memory: LTMMemoryEntry) -> str:
        """Determine experience type from memory.

        Args:
            memory: Memory entry.

        Returns:
            Experience type string.
        """
        # Check tags for experience type indicators
        tags = memory.experience_tags

        if "goal" in tags or "goal_completed" in tags:
            return "goal_completion"
        elif "debate" in tags or "debate_insight" in tags:
            return "debate_insight"
        elif "slepp" in tags or "relational" in tags:
            return "relational_moment"
        elif "emotional" in tags:
            return "emotional_experience"
        elif "skill" in tags:
            return "skill_milestone"
        else:
            return "general_experience"

    def _calculate_xp_gain(
        self, memory: LTMMemoryEntry, significance: ExperienceImpactLevel
    ) -> float:
        """Calculate XP gain from memory.

        Phase 6: Basic XP calculation based on significance and impact level.

        Args:
            memory: Memory entry.
            significance: Experience significance level.

        Returns:
            XP gain value.
        """
        # Base XP from impact level
        base_xp = memory.impact_level * 10.0

        # Multiply by significance factor
        significance_factor = {
            ExperienceImpactLevel.NEGLIGIBLE: 0.0,
            ExperienceImpactLevel.LOW: 0.5,
            ExperienceImpactLevel.MODERATE: 1.0,
            ExperienceImpactLevel.MEANINGFUL: 1.5,
            ExperienceImpactLevel.HIGH_SIGNIFICANCE: 2.0,
            ExperienceImpactLevel.IDENTITY_RELEVANT: 3.0,
        }

        xp = base_xp * significance_factor.get(significance, 1.0)

        # Add bonus for high priority memories
        if memory.priority.value == "critical":
            xp *= 1.5
        elif memory.priority.value == "important":
            xp *= 1.2

        return xp

    def create_xp_update(
        self, experience: ExperienceObject, event_id: str
    ) -> XPUpdate:
        """Create XP update from experience.

        Per spec: subsystem_memory_experience.md §X.4
        Distributes XP across skill domains.

        Args:
            experience: Experience object.
            event_id: Event ID associated with the experience.

        Returns:
            XPUpdate with distributed XP values.
        """
        total_xp = experience.xp_gain

        # Phase 6: Basic XP distribution based on experience type
        # Full distribution logic deferred to learning system integration
        xp_distribution = {
            "reasoning_xp": 0.0,
            "emotional_xp": 0.0,
            "debate_xp": 0.0,
            "autonomy_xp": 0.0,
            "planning_xp": 0.0,
            "media_xp": 0.0,
            "knowledge_xp": 0.0,
        }

        # Distribute XP based on experience type
        if experience.experience_type == "goal_completion":
            xp_distribution["planning_xp"] = total_xp * 0.4
            xp_distribution["reasoning_xp"] = total_xp * 0.3
            xp_distribution["autonomy_xp"] = total_xp * 0.3
        elif experience.experience_type == "debate_insight":
            xp_distribution["debate_xp"] = total_xp * 0.5
            xp_distribution["reasoning_xp"] = total_xp * 0.3
            xp_distribution["emotional_xp"] = total_xp * 0.2
        elif experience.experience_type == "relational_moment":
            xp_distribution["emotional_xp"] = total_xp * 0.6
            xp_distribution["reasoning_xp"] = total_xp * 0.2
            xp_distribution["autonomy_xp"] = total_xp * 0.2
        elif experience.experience_type == "emotional_experience":
            xp_distribution["emotional_xp"] = total_xp * 0.7
            xp_distribution["reasoning_xp"] = total_xp * 0.3
        else:
            # General experience - distribute evenly
            per_domain = total_xp / 7.0
            for key in xp_distribution:
                xp_distribution[key] = per_domain

        return XPUpdate(
            event_id=event_id,
            xp_distribution=xp_distribution,
            skill_tree_updates=[],
        )

