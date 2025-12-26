"""Skill tree management for Phase 6.

Per spec: subsystems/base1.0/subsystem_skill_tree_learning_engine.md
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from .models import SkillCategory, SkillObject


class SkillTree:
    """Manages skill graph and skill progression.

    Per spec: subsystem_skill_tree_learning_engine.md §3, §5.5
    Phase 6: Skill graph management, XP updates, level advancement, meta-skill priority enforcement.
    """

    # XP required per level (exponential growth)
    XP_PER_LEVEL_BASE = 100.0
    XP_MULTIPLIER = 1.5

    def __init__(self) -> None:
        """Initialize empty skill tree."""
        self._skills: Dict[str, SkillObject] = {}

    def get_skill(self, skill_id: str) -> Optional[SkillObject]:
        """Get skill by ID.

        Args:
            skill_id: Skill ID.

        Returns:
            Skill object if found, None otherwise.
        """
        return self._skills.get(skill_id)

    def add_skill(self, skill: SkillObject) -> None:
        """Add skill to tree.

        Args:
            skill: Skill object to add.
        """
        self._skills[skill.skill_id] = skill

    def check_prerequisites(self, skill_id: str) -> bool:
        """Check if skill prerequisites are met.

        Args:
            skill_id: Skill ID to check.

        Returns:
            True if all prerequisites are met, False otherwise.
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return False

        for prereq_id in skill.prerequisites:
            prereq_skill = self._skills.get(prereq_id)
            if not prereq_skill or prereq_skill.level < 1.0:
                return False

        return True

    def update_skill_xp(self, skill_id: str, xp_delta: float) -> bool:
        """Update skill XP and advance level if threshold reached.

        Per spec: subsystem_skill_tree_learning_engine.md §5.5
        Meta-skills gain XP first, then domain/micro-skills.

        Args:
            skill_id: Skill ID to update.
            xp_delta: XP to add (can be negative).

        Returns:
            True if level advanced, False otherwise.
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return False

        old_level = skill.level

        # Update XP
        skill.xp = max(0.0, skill.xp + xp_delta)

        # Check for level advancement
        required_xp = self._calculate_xp_for_level(skill.level + 1)
        if skill.xp >= required_xp:
            skill.level += 1.0
            skill.last_updated = datetime.now(timezone.utc)

        return skill.level > old_level

    def _calculate_xp_for_level(self, level: float) -> float:
        """Calculate XP required for a given level.

        Args:
            level: Target level.

        Returns:
            Required XP.
        """
        if level <= 1.0:
            return self.XP_PER_LEVEL_BASE

        # Exponential growth
        return self.XP_PER_LEVEL_BASE * (self.XP_MULTIPLIER ** (level - 1))

    def get_meta_skills(self) -> List[SkillObject]:
        """Get all meta-skills.

        Returns:
            List of meta-skill objects.
        """
        return [
            skill
            for skill in self._skills.values()
            if skill.category == SkillCategory.META_SKILL or skill.tier == 1
        ]

    def get_domain_skills(self) -> List[SkillObject]:
        """Get all domain skills.

        Returns:
            List of domain skill objects.
        """
        return [
            skill
            for skill in self._skills.values()
            if skill.category == SkillCategory.DOMAIN_SKILL or skill.tier == 2
        ]

    def get_micro_skills(self) -> List[SkillObject]:
        """Get all micro-skills.

        Returns:
            List of micro-skill objects.
        """
        return [
            skill
            for skill in self._skills.values()
            if skill.category == SkillCategory.MICRO_SKILL or skill.tier == 3
        ]



