"""Subsystem execution package for Phase 5.

This package contains the runtime execution infrastructure for cognitive subsystems.
State shells are in src/state/subsystems/, execution logic is here.
"""

from .execution import (
    AutonomyEvaluator,
    AutonomyFrameworkExecutor,
    BandEnforcer,
    BandTransitionManager,
    CognitiveLoopExecutor,
    CognitiveOrchestrator,
    CompetencyDomain,
    CompetencyProfile,
    DebateManager,
    DebateRole,
    EmotionalEngineExecutor,
    ExecutionContext,
    GoalManager,
    IntegrationManager,
    PrimaryMoodVector,
    SubsystemExecutor,
)

__all__ = [
    "SubsystemExecutor",
    "ExecutionContext",
    "CognitiveOrchestrator",
    "IntegrationManager",
    "DebateManager",
    "DebateRole",
    "AutonomyFrameworkExecutor",
    "AutonomyEvaluator",
    "BandEnforcer",
    "BandTransitionManager",
    "CognitiveLoopExecutor",
    "GoalManager",
    "EmotionalEngineExecutor",
    "PrimaryMoodVector",
    "CompetencyDomain",
    "CompetencyProfile",
]
