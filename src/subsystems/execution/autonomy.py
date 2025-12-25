"""Autonomy framework execution infrastructure for Phase 5.

Implements autonomy score computation, band enforcement, and band transitions.

Phase 5: Basic/minimal scoring algorithms - enough to compute scores and enforce bands.
Per spec: subsystems/base1.0/subsystem_autonomy.md
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import ExecutionContext, SubsystemExecutor
from ...state.keys import SubsystemKeys


# -----------------------------------------------------------------------------
# Data Structures
# -----------------------------------------------------------------------------


class CompetencyDomain(str, Enum):
    """Competency domains for autonomy evaluation.

    Per spec: subsystem_autonomy.md §4.2
    """

    STABILITY = "stability"
    RELIABILITY = "reliability"
    EMOTIONAL_REGULATION = "emotional_regulation"
    COGNITIVE_CONSISTENCY = "cognitive_consistency"
    DRIFT_RESISTANCE = "drift_resistance"
    AUTONOMY_JUDGMENT = "autonomy_judgment"
    PLANNING_EXECUTION_RELIABILITY = "planning_execution_reliability"
    IDENTITY_ALIGNMENT = "identity_alignment"
    MULTI_INSTANCE_INTEGRITY = "multi_instance_integrity"
    SAFETY_MODEL_COMPLIANCE = "safety_model_compliance"


@dataclass
class CompetencyProfile:
    """Competency profile vector.

    Per spec: subsystem_autonomy.md §4.2
    Each domain score ∈ [0, 1]
    """

    stability: float = 0.0
    reliability: float = 0.0
    emotional_regulation: float = 0.0
    cognitive_consistency: float = 0.0
    drift_resistance: float = 0.0
    autonomy_judgment: float = 0.0
    planning_execution_reliability: float = 0.0
    identity_alignment: float = 0.0
    multi_instance_integrity: float = 0.0
    safety_model_compliance: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            "stability": self.stability,
            "reliability": self.reliability,
            "emotional_regulation": self.emotional_regulation,
            "cognitive_consistency": self.cognitive_consistency,
            "drift_resistance": self.drift_resistance,
            "autonomy_judgment": self.autonomy_judgment,
            "planning_execution_reliability": self.planning_execution_reliability,
            "identity_alignment": self.identity_alignment,
            "multi_instance_integrity": self.multi_instance_integrity,
            "safety_model_compliance": self.safety_model_compliance,
        }

    def get(self, domain: CompetencyDomain) -> float:
        """Get competency score for a domain."""
        domain_map = {
            CompetencyDomain.STABILITY: self.stability,
            CompetencyDomain.RELIABILITY: self.reliability,
            CompetencyDomain.EMOTIONAL_REGULATION: self.emotional_regulation,
            CompetencyDomain.COGNITIVE_CONSISTENCY: self.cognitive_consistency,
            CompetencyDomain.DRIFT_RESISTANCE: self.drift_resistance,
            CompetencyDomain.AUTONOMY_JUDGMENT: self.autonomy_judgment,
            CompetencyDomain.PLANNING_EXECUTION_RELIABILITY: self.planning_execution_reliability,
            CompetencyDomain.IDENTITY_ALIGNMENT: self.identity_alignment,
            CompetencyDomain.MULTI_INSTANCE_INTEGRITY: self.multi_instance_integrity,
            CompetencyDomain.SAFETY_MODEL_COMPLIANCE: self.safety_model_compliance,
        }
        return domain_map[domain]


@dataclass
class BandThresholds:
    """Band threshold requirements.

    Per spec: subsystem_autonomy.md §4.3
    """

    score_min: float
    score_max: float
    competency_thresholds: Dict[CompetencyDomain, float]


# Band ranges per spec (simplified for Phase 5)
BAND_THRESHOLDS: Dict[int, BandThresholds] = {
    0: BandThresholds(0.0, 4.9, {domain: 0.05 for domain in CompetencyDomain}),
    1: BandThresholds(5.0, 14.9, {domain: 0.15 for domain in CompetencyDomain}),
    2: BandThresholds(15.0, 29.9, {domain: 0.25 for domain in CompetencyDomain}),
    3: BandThresholds(30.0, 44.9, {domain: 0.35 for domain in CompetencyDomain}),
    4: BandThresholds(45.0, 59.9, {domain: 0.45 for domain in CompetencyDomain}),
    5: BandThresholds(60.0, 69.9, {domain: 0.55 for domain in CompetencyDomain}),
    6: BandThresholds(70.0, 79.9, {domain: 0.65 for domain in CompetencyDomain}),
    7: BandThresholds(80.0, 84.9, {domain: 0.75 for domain in CompetencyDomain}),
    8: BandThresholds(85.0, 89.9, {domain: 0.80 for domain in CompetencyDomain}),
    9: BandThresholds(90.0, 94.9, {domain: 0.85 for domain in CompetencyDomain}),
    10: BandThresholds(95.0, 100.0, {domain: 0.90 for domain in CompetencyDomain}),
}


class AutonomyEvaluator:
    """Computes autonomy score and competency profile.

    Phase 5: Basic/minimal scoring algorithms.
    """

    def __init__(self, context: ExecutionContext) -> None:
        """Initialize the evaluator.

        Args:
            context: Execution context for accessing state.
        """
        self._context = context

    def compute_score(self) -> float:
        """Compute current autonomy score.

        Phase 5: Basic scoring - simple average of competency scores scaled to 0-100.

        Returns:
            Autonomy score in [0, 100].
        """
        profile = self.compute_competency_profile()
        scores = profile.to_dict()
        avg_score = sum(scores.values()) / len(scores) if scores else 0.0
        return min(100.0, max(0.0, avg_score * 100.0))

    def compute_competency_profile(self) -> CompetencyProfile:
        """Compute competency profile from current state.

        Phase 5: Basic computation - returns minimal default values.
        Full logic requires state fields that don't exist yet.

        Returns:
            CompetencyProfile with current competency scores.
        """
        # Phase 5: Basic/minimal logic - return default minimal scores
        # Full evaluation requires state fields that are deferred
        return CompetencyProfile(
            stability=0.1,
            reliability=0.1,
            emotional_regulation=0.1,
            cognitive_consistency=0.1,
            drift_resistance=0.1,
            autonomy_judgment=0.1,
            planning_execution_reliability=0.1,
            identity_alignment=0.2,  # Slightly higher as identity is core
            multi_instance_integrity=0.1,
            safety_model_compliance=0.7,  # High for safety
        )

    def determine_band(self, score: float) -> int:
        """Determine autonomy band from score.

        Args:
            score: The autonomy score.

        Returns:
            Band number (0-10).
        """
        for band in sorted(BAND_THRESHOLDS.keys(), reverse=True):
            thresholds = BAND_THRESHOLDS[band]
            if thresholds.score_min <= score <= thresholds.score_max:
                return band
        # Default to band 0 if score is out of range
        return 0


class BandEnforcer:
    """Enforces band constraints and permissions.

    Phase 5: Basic permission checking.
    """

    def __init__(self, context: ExecutionContext) -> None:
        """Initialize the enforcer.

        Args:
            context: Execution context for accessing state.
        """
        self._context = context
        self._evaluator = AutonomyEvaluator(context)

    def check_permission(self, action: str, required_band: int) -> bool:
        """Check if current autonomy allows an action.

        Phase 5: Basic permission check.

        Args:
            action: Description of the action (for logging).
            required_band: Minimum band required for the action.

        Returns:
            True if action is permitted, False otherwise.
        """
        current_score = self._evaluator.compute_score()
        current_band = self._evaluator.determine_band(current_score)
        return current_band >= required_band

    def check_competency_thresholds(self, required_band: int) -> bool:
        """Check if competency profile meets band requirements.

        Args:
            required_band: The band to check against.

        Returns:
            True if all competency thresholds are met, False otherwise.
        """
        if required_band not in BAND_THRESHOLDS:
            return False

        profile = self._evaluator.compute_competency_profile()
        thresholds = BAND_THRESHOLDS[required_band].competency_thresholds

        for domain, threshold in thresholds.items():
            if profile.get(domain) < threshold:
                return False

        return True

    def get_current_band(self) -> int:
        """Get current autonomy band.

        Returns:
            Current band number.
        """
        score = self._evaluator.compute_score()
        return self._evaluator.determine_band(score)


class BandTransitionManager:
    """Manages band advancement and regression.

    Phase 5: Basic transition logic without full debate integration.
    """

    def __init__(self, context: ExecutionContext) -> None:
        """Initialize the transition manager.

        Args:
            context: Execution context.
        """
        self._context = context
        self._evaluator = AutonomyEvaluator(context)
        self._enforcer = BandEnforcer(context)

    def can_advance(self, target_band: int) -> tuple[bool, List[str]]:
        """Check if band advancement to target is allowed.

        Args:
            target_band: The target band to advance to.

        Returns:
            Tuple of (allowed, list of reasons if not allowed).
        """
        reasons: List[str] = []

        current_band = self._enforcer.get_current_band()
        if target_band <= current_band:
            reasons.append(f"Target band {target_band} not higher than current {current_band}")
            return False, reasons

        score = self._evaluator.compute_score()
        if target_band not in BAND_THRESHOLDS:
            reasons.append(f"Invalid target band {target_band}")
            return False, reasons

        thresholds = BAND_THRESHOLDS[target_band]

        # Check score requirement
        if score < thresholds.score_min:
            reasons.append(
                f"Score {score:.2f} below minimum {thresholds.score_min} for band {target_band}"
            )

        # Check competency thresholds
        if not self._enforcer.check_competency_thresholds(target_band):
            reasons.append(f"Competency thresholds not met for band {target_band}")

        return len(reasons) == 0, reasons

    def can_regress(self, target_band: int) -> tuple[bool, List[str]]:
        """Check if band regression to target is allowed.

        Phase 5: Basic regression check.

        Args:
            target_band: The target band to regress to.

        Returns:
            Tuple of (allowed, list of reasons).
        """
        reasons: List[str] = []

        current_band = self._enforcer.get_current_band()
        if target_band >= current_band:
            reasons.append(f"Target band {target_band} not lower than current {current_band}")
            return False, reasons

        if target_band not in BAND_THRESHOLDS:
            reasons.append(f"Invalid target band {target_band}")
            return False, reasons

        # Phase 5: Regression always allowed if target is valid and lower
        return True, reasons


class AutonomyFrameworkExecutor(SubsystemExecutor):
    """Executes autonomy framework logic.

    Phase 5: Computes scores, enforces bands, manages transitions.
    """

    def __init__(self) -> None:
        """Initialize the autonomy framework executor."""
        super().__init__(SubsystemKeys.AUTONOMY)
        self._evaluator: Optional[AutonomyEvaluator] = None
        self._enforcer: Optional[BandEnforcer] = None
        self._transition_manager: Optional[BandTransitionManager] = None

    def _on_initialized(self) -> None:
        """Initialize autonomy components."""
        if self._context is None:
            return
        self._evaluator = AutonomyEvaluator(self._context)
        self._enforcer = BandEnforcer(self._context)
        self._transition_manager = BandTransitionManager(self._context)

        # Subscribe to events that affect autonomy
        self.context.event_bus.subscribe("emotion.*", self._on_emotional_change)
        self.context.event_bus.subscribe("system.drift_detected", self._on_drift_detected)

    def _on_emotional_change(self, event: Any) -> None:
        """Handle emotional state changes affecting autonomy.

        Phase 5: Basic handler - emit autonomy update event.
        """
        if self._evaluator:
            new_score = self._evaluator.compute_score()
            self.emit_influence_event(
                "autonomy.score_updated",
                {"score": new_score, "band": self._enforcer.get_current_band() if self._enforcer else 0},
            )

    def _on_drift_detected(self, event: Any) -> None:
        """Handle drift detection affecting autonomy.

        Phase 5: Basic handler - may trigger regression.
        """
        # Phase 5: Basic logic - emit event, full regression logic deferred
        self.emit_influence_event("autonomy.drift_impact", {"event": "drift_detected"})

    def _execute_impl(self, input_data: Any) -> Dict[str, Any]:
        """Execute autonomy evaluation.

        Args:
            input_data: Optional input (can be None for periodic evaluation).

        Returns:
            Dictionary with current score, band, and competency profile.
        """
        if self._evaluator is None or self._enforcer is None:
            raise RuntimeError("Autonomy executor not properly initialized")

        score = self._evaluator.compute_score()
        band = self._enforcer.get_current_band()
        profile = self._evaluator.compute_competency_profile()

        return {
            "score": score,
            "band": band,
            "competency_profile": profile.to_dict(),
        }

    def check_permission(self, action: str, required_band: int) -> bool:
        """Check if an action is permitted at current autonomy level.

        Args:
            action: Description of the action.
            required_band: Minimum band required.

        Returns:
            True if permitted, False otherwise.
        """
        if self._enforcer is None:
            return False
        return self._enforcer.check_permission(action, required_band)

