"""Phase 5 Subsystem Execution Infrastructure.

Provides execution runtime for cognitive subsystems, enabling Nyra to "think".
"""

from .autonomy import (
    AutonomyEvaluator,
    AutonomyFrameworkExecutor,
    BandEnforcer,
    BandTransitionManager,
    CompetencyDomain,
    CompetencyProfile,
)
from .base import ExecutionContext, SubsystemExecutor
from .debate import (
    CoreRole,
    CreativeRole,
    DebateIssue,
    DebateManager,
    DebateOutcome,
    DebateRole,
    DebateStage,
    EmotionalRole,
    GuardianRole,
    HistorianRole,
    LongTermRole,
    MetaRole,
    OptionSpec,
    PragmatistRole,
    RoleOpinion,
    RiskLevel,
    StakesLevel,
)
from .emotion import EmotionalEngineExecutor, EmotionalLoad, PrimaryMoodVector
from .goals import (
    CognitiveLoopContext,
    CognitiveLoopExecutor,
    CognitiveLoopStage,
    GoalManager,
    GoalObject,
    GoalOrigin,
    GoalStatus,
    GoalTier,
)
from .identity_executor import IdentityContinuityExecutor
from .learning_executor import LearningExecutor
from .maintenance_executor import MaintenanceExecutor
from .memory_executor import MemoryExecutor
from .orchestration import CognitiveOrchestrator, IntegrationManager

__all__ = [
    # Base
    "SubsystemExecutor",
    "ExecutionContext",
    # Debate
    "DebateRole",
    "DebateManager",
    "DebateIssue",
    "DebateOutcome",
    "DebateStage",
    "RoleOpinion",
    "OptionSpec",
    "StakesLevel",
    "RiskLevel",
    "CoreRole",
    "GuardianRole",
    "LongTermRole",
    "PragmatistRole",
    "HistorianRole",
    "CreativeRole",
    "EmotionalRole",
    "MetaRole",
    # Autonomy
    "AutonomyEvaluator",
    "BandEnforcer",
    "BandTransitionManager",
    "AutonomyFrameworkExecutor",
    "CompetencyDomain",
    "CompetencyProfile",
    # Goals
    "CognitiveLoopExecutor",
    "GoalManager",
    "GoalObject",
    "GoalTier",
    "GoalOrigin",
    "GoalStatus",
    "CognitiveLoopStage",
    "CognitiveLoopContext",
    # Emotion
    "EmotionalEngineExecutor",
    "PrimaryMoodVector",
    "EmotionalLoad",
    # Orchestration
    "CognitiveOrchestrator",
    "IntegrationManager",
    # Phase 6 Executors
    "MemoryExecutor",
    "LearningExecutor",
    "IdentityContinuityExecutor",
    "MaintenanceExecutor",
]


