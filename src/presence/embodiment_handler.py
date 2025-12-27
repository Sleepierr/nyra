"""Embodiment handler for Phase 7.

Handles device-specific behavior and expression budgets.
Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §9
"""

from __future__ import annotations

from typing import Dict, Optional

from .models import EmbodimentType, ExpressionBudget, PresenceState


class EmbodimentHandler:
    """Handles embodiment-aware behavior and expression budgets.

    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §9
    Phase 7: Device-specific expression budgets and behavior differences.
    """

    def __init__(self) -> None:
        """Initialize embodiment handler."""
        self._embodiment_budgets: Dict[EmbodimentType, ExpressionBudget] = self._initialize_budgets()

    def _initialize_budgets(self) -> Dict[EmbodimentType, ExpressionBudget]:
        """Initialize expression budgets for each embodiment type.

        Per spec: §9.1 - Primary embodiments (Mac, Windows, Phone) are full-presence.
        Peripheral embodiments have compressed expression.
        """
        return {
            # Primary embodiments: full-presence environments
            EmbodimentType.MAC: ExpressionBudget(
                message_length_limit=5000,
                emotional_intensity_limit=1.0,
                facet_visibility_limit=1.0,
                humor_density_limit=1.0,
                check_in_frequency_limit=10,  # per hour
            ),
            EmbodimentType.WINDOWS: ExpressionBudget(
                message_length_limit=5000,
                emotional_intensity_limit=1.0,
                facet_visibility_limit=1.0,
                humor_density_limit=1.0,
                check_in_frequency_limit=10,
            ),
            EmbodimentType.PHONE: ExpressionBudget(
                message_length_limit=5000,
                emotional_intensity_limit=1.0,
                facet_visibility_limit=1.0,
                humor_density_limit=1.0,
                check_in_frequency_limit=10,
            ),
            # Peripheral embodiments: compressed expression
            EmbodimentType.PERIPHERAL: ExpressionBudget(
                message_length_limit=100,  # Short messages only
                emotional_intensity_limit=0.5,  # Reduced emotional intensity
                facet_visibility_limit=0.3,  # Limited facet visibility
                humor_density_limit=0.2,  # Minimal humor
                check_in_frequency_limit=2,  # Fewer check-ins
            ),
        }

    def get_budget(self, embodiment_type: EmbodimentType) -> ExpressionBudget:
        """Get expression budget for an embodiment type.

        Args:
            embodiment_type: The embodiment type.

        Returns:
            Expression budget for that embodiment.
        """
        return self._embodiment_budgets.get(
            embodiment_type,
            self._embodiment_budgets[EmbodimentType.PERIPHERAL],  # Default to compressed
        )

    def adjust_budget_for_presence(
        self, budget: ExpressionBudget, presence_state: PresenceState
    ) -> ExpressionBudget:
        """Adjust expression budget based on presence state.

        Per spec: §4 - Different presence states have different expression capabilities.

        Args:
            budget: Base expression budget.
            presence_state: Current presence state.

        Returns:
            Adjusted expression budget.
        """
        # Guarded Presence: reduced expressiveness
        if presence_state == PresenceState.GUARDED:
            return ExpressionBudget(
                message_length_limit=budget.message_length_limit // 2,
                emotional_intensity_limit=budget.emotional_intensity_limit * 0.3,
                facet_visibility_limit=budget.facet_visibility_limit * 0.2,
                humor_density_limit=0.0,  # Humor forbidden during Guarded Presence (spec §7)
                check_in_frequency_limit=0,  # No check-ins during Guarded
            )

        # Background Presence: minimal output
        if presence_state == PresenceState.BACKGROUND:
            return ExpressionBudget(
                message_length_limit=budget.message_length_limit // 4,
                emotional_intensity_limit=budget.emotional_intensity_limit * 0.2,
                facet_visibility_limit=budget.facet_visibility_limit * 0.1,
                humor_density_limit=0.0,
                check_in_frequency_limit=budget.check_in_frequency_limit // 2,
            )

        # Quiet Presence: minimal output, responds when prompted
        if presence_state == PresenceState.QUIET:
            return ExpressionBudget(
                message_length_limit=budget.message_length_limit // 3,
                emotional_intensity_limit=budget.emotional_intensity_limit * 0.5,
                facet_visibility_limit=budget.facet_visibility_limit * 0.5,
                humor_density_limit=budget.humor_density_limit * 0.3,
                check_in_frequency_limit=budget.check_in_frequency_limit // 2,
            )

        # Reflective Presence: slower pacing, deeper tone
        if presence_state == PresenceState.REFLECTIVE:
            return ExpressionBudget(
                message_length_limit=budget.message_length_limit,
                emotional_intensity_limit=budget.emotional_intensity_limit * 0.8,
                facet_visibility_limit=budget.facet_visibility_limit,
                humor_density_limit=0.0,  # No humor during reflective
                check_in_frequency_limit=budget.check_in_frequency_limit // 3,
            )

        # Active and Playful Presence: full budget
        return budget


