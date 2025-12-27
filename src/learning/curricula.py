"""Learning curricula generation for Phase 6.

Per spec: subsystems/base1.0/subsystem_skill_tree_learning_engine.md
"""

from __future__ import annotations

from typing import List, Optional

from .models import Curricula, SkillObject
from .skill_tree import SkillTree


class CurriculaGenerator:
    """Generates learning curricula for skill progression.

    Phase 6: Basic curriculum generation with autonomy band gating.
    """

    def __init__(self, skill_tree: Optional[SkillTree] = None) -> None:
        """Initialize curricula generator.

        Args:
            skill_tree: Optional skill tree instance.
        """
        self._skill_tree = skill_tree or SkillTree()

    def generate_curriculum_for_skill(
        self, skill_id: str, current_autonomy_band: int = 0
    ) -> Optional[Curricula]:
        """Generate curriculum for a skill.

        Args:
            skill_id: Target skill ID.
            current_autonomy_band: Current autonomy band.

        Returns:
            Curriculum if skill exists and band requirements met, None otherwise.
        """
        skill = self._skill_tree.get_skill(skill_id)
        if not skill:
            return None

        # Check autonomy band requirement
        if current_autonomy_band < skill.autonomy_band_required:
            return None

        # Generate learning path (basic for Phase 6)
        learning_path = []
        for prereq_id in skill.prerequisites:
            prereq_skill = self._skill_tree.get_skill(prereq_id)
            if prereq_skill:
                learning_path.append(
                    {
                        "skill_id": prereq_id,
                        "skill_name": prereq_id,
                        "order": len(learning_path),
                    }
                )

        learning_path.append(
            {"skill_id": skill_id, "skill_name": skill_id, "order": len(learning_path)}
        )

        return Curricula(
            target_skill_id=skill_id,
            prerequisites=skill.prerequisites.copy(),
            learning_path=learning_path,
            autonomy_band_required=skill.autonomy_band_required,
        )





