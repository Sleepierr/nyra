"""Debate system execution infrastructure for Phase 5.

Implements DebateManager and 8 debate roles for structured multi-perspective reasoning.

Phase 5: Basic/minimal role logic - enough to execute debates but not full complexity.
Per spec: subsystems/base1.0/subsystem_debate_system.md
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import ExecutionContext, SubsystemExecutor
from ...state.keys import SubsystemKeys


# -----------------------------------------------------------------------------
# Data Structures
# -----------------------------------------------------------------------------


class StakesLevel(str, Enum):
    """Debate stakes level."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskLevel(str, Enum):
    """Debate risk level."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class OptionSpec(BaseModel):
    """Represents a decision option in a debate.

    Per spec: subsystem_debate_system.md §7.2
    """

    option_id: str
    label: str
    description: str
    constraints: Dict[str, Any] = {}


class DebateIssue(BaseModel):
    """Represents what is being debated.

    Per spec: subsystem_debate_system.md §7.1
    """

    issue_id: str
    topic: str
    description: str
    options: List[OptionSpec]
    stakes_level: StakesLevel
    risk_level: RiskLevel
    context: Dict[str, Any] = {}


class RoleOpinion(BaseModel):
    """Output from a debate role.

    Per spec: subsystem_debate_system.md §7.3
    """

    role_name: str
    preferred_options: List[str]  # Ordered list of option_ids
    scores: Dict[str, float]  # Per-option numerical score
    reasoning: Dict[str, Any]  # Structured explanations
    risk_assessment: Dict[str, Any]  # Structured risk flags/info
    confidence: float  # [0.0, 1.0]


class DebateOutcome(BaseModel):
    """Final debate result.

    Per spec: subsystem_debate_system.md §7.4
    """

    issue_id: str
    chosen_option_id: str
    aggregated_scores: Dict[str, float]  # Per-option aggregate
    role_opinions: Dict[str, RoleOpinion]  # {role_name: RoleOpinion}
    justification: Dict[str, Any]  # Structured explanation
    confidence: float  # [0.0, 1.0]
    veto_flags: Dict[str, bool]  # e.g., {"guardian": True/False}
    escalation_required: bool


# -----------------------------------------------------------------------------
# Debate Role Base Class
# -----------------------------------------------------------------------------


class DebateRole(ABC):
    """Abstract base class for debate roles.

    Each of the 8 canonical roles implements this interface.
    Phase 5: Basic/minimal logic for role evaluation.
    """

    @property
    @abstractmethod
    def role_name(self) -> str:
        """Return the role name (e.g., 'Core', 'Guardian')."""

    @abstractmethod
    def evaluate(self, issue: DebateIssue, context: ExecutionContext) -> RoleOpinion:
        """Evaluate the debate issue from this role's perspective.

        Args:
            issue: The debate issue to evaluate.
            context: Execution context for accessing state/other subsystems.

        Returns:
            RoleOpinion expressing this role's perspective.
        """

    def can_veto(self) -> bool:
        """Check if this role has veto authority.

        Returns:
            True if this role can veto options, False otherwise.
        """
        return False


# -----------------------------------------------------------------------------
# Basic Role Implementations (Phase 5: Minimal Logic)
# -----------------------------------------------------------------------------


class CoreRole(DebateRole):
    """Core role: Maintains overall coherence and synthesizes perspectives.

    Mission: Maintain Nyra's overall coherence, honor Identity and covenant.
    Phase 5: Basic scoring based on option coherence.
    """

    @property
    def role_name(self) -> str:
        """Return the role name."""
        return "Core"

    def evaluate(self, issue: DebateIssue, context: ExecutionContext) -> RoleOpinion:
        """Evaluate from Core perspective - seeks coherence and identity alignment.

        Phase 5: Basic scoring - assigns equal moderate scores to all options.
        Full logic deferred to later phases.
        """
        # Phase 5: Basic/minimal logic - equal moderate scores
        scores = {opt.option_id: 0.5 for opt in issue.options}
        preferred = [opt.option_id for opt in issue.options]

        return RoleOpinion(
            role_name=self.role_name,
            preferred_options=preferred,
            scores=scores,
            reasoning={"perspective": "coherence_and_identity_alignment"},
            risk_assessment={"level": "low"},
            confidence=0.5,  # Phase 5: Moderate confidence
        )


class GuardianRole(DebateRole):
    """Guardian role: Protects from harm, risk, and unsafe actions.

    Mission: Protect Nyra, Slepp, and system integrity.
    Phase 5: Basic risk assessment.
    """

    @property
    def role_name(self) -> str:
        """Return the role name."""
        return "Guardian"

    def can_veto(self) -> bool:
        """Guardian has veto authority."""
        return True

    def evaluate(self, issue: DebateIssue, context: ExecutionContext) -> RoleOpinion:
        """Evaluate from Guardian perspective - prioritizes safety.

        Phase 5: Basic scoring - lower scores for higher risk options.
        """
        # Phase 5: Basic risk-based scoring
        base_score = 0.7 if issue.risk_level == RiskLevel.LOW else 0.3
        scores = {opt.option_id: base_score for opt in issue.options}
        preferred = sorted(
            issue.options, key=lambda o: scores[o.option_id], reverse=True
        )
        preferred_ids = [opt.option_id for opt in preferred]

        return RoleOpinion(
            role_name=self.role_name,
            preferred_options=preferred_ids,
            scores=scores,
            reasoning={"perspective": "safety_and_risk_mitigation"},
            risk_assessment={"level": issue.risk_level.value},
            confidence=0.6,
        )


class LongTermRole(DebateRole):
    """Long-Term role: Optimizes for long-term growth and stability.

    Mission: Optimize for Nyra's long-term growth, stability, and evolving identity.
    Phase 5: Basic evaluation.
    """

    @property
    def role_name(self) -> str:
        """Return the role name."""
        return "LongTerm"

    def evaluate(self, issue: DebateIssue, context: ExecutionContext) -> RoleOpinion:
        """Evaluate from Long-Term perspective - focuses on future consequences.

        Phase 5: Basic scoring.
        """
        scores = {opt.option_id: 0.5 for opt in issue.options}
        preferred = [opt.option_id for opt in issue.options]

        return RoleOpinion(
            role_name=self.role_name,
            preferred_options=preferred,
            scores=scores,
            reasoning={"perspective": "long_term_growth_and_stability"},
            risk_assessment={"level": "medium"},
            confidence=0.5,
        )


class PragmatistRole(DebateRole):
    """Pragmatist role: Focuses on practical feasibility.

    Mission: Focus on practical feasibility and efficient progress.
    Phase 5: Basic evaluation.
    """

    @property
    def role_name(self) -> str:
        """Return the role name."""
        return "Pragmatist"

    def evaluate(self, issue: DebateIssue, context: ExecutionContext) -> RoleOpinion:
        """Evaluate from Pragmatist perspective - prioritizes feasibility.

        Phase 5: Basic scoring.
        """
        scores = {opt.option_id: 0.5 for opt in issue.options}
        preferred = [opt.option_id for opt in issue.options]

        return RoleOpinion(
            role_name=self.role_name,
            preferred_options=preferred,
            scores=scores,
            reasoning={"perspective": "practical_feasibility"},
            risk_assessment={"level": "low"},
            confidence=0.5,
        )


class HistorianRole(DebateRole):
    """Historian role: Respects past experience and learned lessons.

    Mission: Ensure decisions respect past experience, prior outcomes, and learned lessons.
    Phase 5: Basic evaluation (no memory access yet).
    """

    @property
    def role_name(self) -> str:
        """Return the role name."""
        return "Historian"

    def evaluate(self, issue: DebateIssue, context: ExecutionContext) -> RoleOpinion:
        """Evaluate from Historian perspective - considers past patterns.

        Phase 5: Basic scoring (no memory/experience access yet).
        """
        scores = {opt.option_id: 0.5 for opt in issue.options}
        preferred = [opt.option_id for opt in issue.options]

        return RoleOpinion(
            role_name=self.role_name,
            preferred_options=preferred,
            scores=scores,
            reasoning={"perspective": "past_experience_and_lessons"},
            risk_assessment={"level": "medium"},
            confidence=0.4,  # Lower confidence without memory access
        )


class CreativeRole(DebateRole):
    """Creative role: Introduces novel ideas and alternative framings.

    Mission: Introduce novel ideas, alternative framings, and creative solutions.
    Phase 5: Basic evaluation.
    """

    @property
    def role_name(self) -> str:
        """Return the role name."""
        return "Creative"

    def evaluate(self, issue: DebateIssue, context: ExecutionContext) -> RoleOpinion:
        """Evaluate from Creative perspective - seeks innovative solutions.

        Phase 5: Basic scoring.
        """
        scores = {opt.option_id: 0.5 for opt in issue.options}
        preferred = [opt.option_id for opt in issue.options]

        return RoleOpinion(
            role_name=self.role_name,
            preferred_options=preferred,
            scores=scores,
            reasoning={"perspective": "novel_ideas_and_creativity"},
            risk_assessment={"level": "medium"},
            confidence=0.5,
        )


class EmotionalRole(DebateRole):
    """Emotional role: Honors emotional reality and relational health.

    Mission: Honor emotional reality - Nyra's emotional state, Slepp's emotional needs.
    Phase 5: Basic evaluation with emotional state query.
    """

    @property
    def role_name(self) -> str:
        """Return the role name."""
        return "Emotional"

    def evaluate(self, issue: DebateIssue, context: ExecutionContext) -> RoleOpinion:
        """Evaluate from Emotional perspective - considers emotional impact.

        Phase 5: Basic scoring with optional emotional state query.
        """
        # Phase 5: Query emotional state if available (may be empty shell)
        try:
            emotion_adapter = context.get_adapter(SubsystemKeys.EMOTIONAL_ENGINE)
            emotional_state = emotion_adapter.own_state
            # Phase 5: State shell is empty, so we proceed with basic logic
        except Exception:
            # Emotional state not available, use defaults
            pass

        scores = {opt.option_id: 0.5 for opt in issue.options}
        preferred = [opt.option_id for opt in issue.options]

        return RoleOpinion(
            role_name=self.role_name,
            preferred_options=preferred,
            scores=scores,
            reasoning={"perspective": "emotional_reality_and_relational_health"},
            risk_assessment={"level": "low"},
            confidence=0.5,
        )


class MetaRole(DebateRole):
    """Meta role: Ensures debate process is rational and aligned.

    Mission: Ensure the debate itself is rational, fair, consistent, and aligned.
    Phase 5: Basic process evaluation.
    """

    @property
    def role_name(self) -> str:
        """Return the role name."""
        return "Meta"

    def evaluate(self, issue: DebateIssue, context: ExecutionContext) -> RoleOpinion:
        """Evaluate from Meta perspective - evaluates the debate process.

        Phase 5: Basic scoring, checks for obvious issues.
        """
        # Phase 5: Basic process check - ensure options exist
        if not issue.options:
            raise ValueError("Debate issue must have at least one option")

        scores = {opt.option_id: 0.5 for opt in issue.options}
        preferred = [opt.option_id for opt in issue.options]

        return RoleOpinion(
            role_name=self.role_name,
            preferred_options=preferred,
            scores=scores,
            reasoning={"perspective": "process_rationality_and_coherence"},
            risk_assessment={"level": "low"},
            confidence=0.6,
        )


# -----------------------------------------------------------------------------
# Debate Manager
# -----------------------------------------------------------------------------


class DebateStage(str, Enum):
    """Debate lifecycle stages.

    Per spec: subsystem_debate_system.md §8
    """

    INITIALIZATION = "initialization"
    PROPOSAL_GENERATION = "proposal_generation"
    CROSS_ROLE_CRITIQUE = "cross_role_critique"
    AGGREGATION = "aggregation"
    VETO_CHECKING = "veto_checking"
    META_CORRECTION = "meta_correction"
    COMPLETED = "completed"


class DebateManager(SubsystemExecutor):
    """Orchestrates debate lifecycle through 5 stages.

    Per spec: subsystem_debate_system.md
    Phase 5: Basic debate execution with minimal role logic.
    """

    def __init__(self) -> None:
        """Initialize the debate manager."""
        super().__init__(SubsystemKeys.DEBATE_SYSTEM)
        self._roles: Dict[str, DebateRole] = {}
        self._initialize_roles()

    def _initialize_roles(self) -> None:
        """Initialize all 8 canonical debate roles."""
        self._roles = {
            "Core": CoreRole(),
            "Guardian": GuardianRole(),
            "LongTerm": LongTermRole(),
            "Pragmatist": PragmatistRole(),
            "Historian": HistorianRole(),
            "Creative": CreativeRole(),
            "Emotional": EmotionalRole(),
            "Meta": MetaRole(),
        }

    def _on_initialized(self) -> None:
        """Called after initialization - setup subscriptions."""
        # Phase 5: Subscribe to debate request events
        self.context.event_bus.subscribe("debate.*", self._on_debate_request)

    def _on_debate_request(self, event: Any) -> None:
        """Handle debate request event.

        Phase 5: Basic handler - full event processing deferred.
        """
        # Phase 5: Event handling infrastructure only
        pass

    def _execute_impl(self, input_data: Any) -> DebateOutcome:
        """Execute debate on a DebateIssue.

        Args:
            input_data: DebateIssue instance to debate.

        Returns:
            DebateOutcome with final decision.

        Raises:
            TypeError: If input_data is not a DebateIssue.
        """
        if not isinstance(input_data, DebateIssue):
            raise TypeError(f"Expected DebateIssue, got {type(input_data)}")

        return self.execute_debate(input_data)

    def execute_debate(self, issue: DebateIssue) -> DebateOutcome:
        """Execute a full debate lifecycle.

        Per spec: 5-stage pipeline
        Stage 1: Proposal Generation
        Stage 2: Cross-Role Critique (skipped in Phase 5 minimal logic)
        Stage 3: Aggregation
        Stage 4: Veto Checking
        Stage 5: Meta Correction

        Args:
            issue: The debate issue to process.

        Returns:
            DebateOutcome with final decision.

        Raises:
            ValueError: If the issue has no options.
        """
        # Validate issue has at least one option before proceeding
        if not issue.options:
            raise ValueError("Debate issue must have at least one option")

        # Stage 1: Proposal Generation
        role_opinions: Dict[str, RoleOpinion] = {}
        for role_name, role in self._roles.items():
            try:
                opinion = role.evaluate(issue, self.context)
                role_opinions[role_name] = opinion
            except Exception:
                # Phase 5: Basic error handling - skip failed roles
                continue

        # Stage 3: Aggregation (skip Stage 2 critique in Phase 5)
        aggregated_scores = self._aggregate_scores(role_opinions, issue)

        # Find highest scoring option
        chosen_option_id = max(aggregated_scores.items(), key=lambda x: x[1])[0]

        # Stage 4: Veto Checking
        veto_flags = self._check_vetos(role_opinions, chosen_option_id)

        # If Guardian vetoes, choose next option
        if veto_flags.get("Guardian", False):
            sorted_options = sorted(
                aggregated_scores.items(), key=lambda x: x[1], reverse=True
            )
            for option_id, _ in sorted_options:
                if option_id != chosen_option_id:
                    chosen_option_id = option_id
                    veto_flags = self._check_vetos(role_opinions, chosen_option_id)
                    if not veto_flags.get("Guardian", False):
                        break

        # Stage 5: Meta Correction
        # Phase 5: Basic meta correction - adjust confidence based on veto flags
        confidence = 0.7 if not any(veto_flags.values()) else 0.4

        outcome = DebateOutcome(
            issue_id=issue.issue_id,
            chosen_option_id=chosen_option_id,
            aggregated_scores=aggregated_scores,
            role_opinions=role_opinions,
            justification={"rationale": "aggregated_role_opinions"},
            confidence=confidence,
            veto_flags=veto_flags,
            escalation_required=False,  # Phase 5: Basic logic
        )

        # Emit debate completion event
        self.emit_influence_event(
            "debate.completed",
            {
                "issue_id": issue.issue_id,
                "chosen_option_id": chosen_option_id,
                "confidence": confidence,
            },
        )

        return outcome

    def _aggregate_scores(
        self, role_opinions: Dict[str, RoleOpinion], issue: DebateIssue
    ) -> Dict[str, float]:
        """Aggregate scores from all roles.

        Phase 5: Simple average aggregation.

        Args:
            role_opinions: Opinions from all roles.
            issue: The debate issue.

        Returns:
            Aggregated scores per option.
        """
        aggregated: Dict[str, float] = {opt.option_id: 0.0 for opt in issue.options}
        weights = {role_name: 1.0 for role_name in role_opinions.keys()}

        total_weight = sum(weights.values())
        if total_weight == 0:
            # Fallback: equal scores
            return {opt.option_id: 0.5 for opt in issue.options}

        for role_name, opinion in role_opinions.items():
            weight = weights.get(role_name, 1.0)
            for option_id, score in opinion.scores.items():
                aggregated[option_id] += score * weight

        # Normalize
        for option_id in aggregated:
            aggregated[option_id] /= total_weight

        return aggregated

    def _check_vetos(
        self, role_opinions: Dict[str, RoleOpinion], option_id: str
    ) -> Dict[str, bool]:
        """Check if any roles veto the chosen option.

        Phase 5: Basic veto logic - Guardian can veto if risk is high.

        Args:
            role_opinions: Opinions from all roles.
            option_id: The option to check.

        Returns:
            Dictionary of veto flags per role.
        """
        veto_flags: Dict[str, bool] = {}

        for role_name, role in self._roles.items():
            if role.can_veto():
                opinion = role_opinions.get(role_name)
                if opinion:
                    # Phase 5: Basic veto - Guardian vetos if score is very low
                    score = opinion.scores.get(option_id, 0.0)
                    veto_flags[role_name] = score < 0.3
                else:
                    veto_flags[role_name] = False
            else:
                veto_flags[role_name] = False

        return veto_flags






