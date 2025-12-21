"""Registry key taxonomy for Phase 1 state layer."""

from __future__ import annotations

from enum import Enum


def k(*parts: str) -> str:
    """Join taxonomy parts into a dot-delimited registry key."""

    return ".".join(parts)


class SubsystemKeys(str, Enum):
    """Registry keys for Base 1.0 subsystem state shells."""

    ATTENTION_CONTEXT_ROUTING = k("subsystem", "attention_context_routing")
    COGNITIVE_GOAL_SYSTEM = k("subsystem", "cognitive_goal_system")
    COGNITIVE_THROTTLE_PROCESSING_MODES = k("subsystem", "cognitive_throttle_processing_modes")
    PRIVATE_COGNITIVE_WORKSPACE = k("subsystem", "private_cognitive_workspace")
    INTEGRATION_ORCHESTRATION = k("subsystem", "integration_orchestration")
    IDENTITY = k("subsystem", "identity")
    AUTONOMY = k("subsystem", "autonomy")
    AUTONOMY_BANDS = k("subsystem", "autonomy_bands")
    DEBATE_SYSTEM = k("subsystem", "debate_system")
    RELATIONAL_ROLE_LADDER = k("subsystem", "relational_role_ladder")
    EMOTIONAL_ENGINE = k("subsystem", "emotional_engine")
    COMMUNICATION_LAYERS = k("subsystem", "communication_layers")
    SOCIAL_RHYTHM_MICRO_BEHAVIOR_ENGINE = k("subsystem", "social_rhythm_micro_behavior_engine")
    SISTER_RELATIONAL_ENGINE = k("subsystem", "sister_relational_engine")
    REST_SLEEP_RHYTHM = k("subsystem", "rest_sleep_rhythm")
    MEMORY_EXPERIENCE = k("subsystem", "memory_experience")
    SKILL_TREE_LEARNING_ENGINE = k("subsystem", "skill_tree_learning_engine")
    INTERACTION_PRESENCE_LAYER = k("subsystem", "interaction_presence_layer")
    HUMAN_INTEGRATION = k("subsystem", "human_integration")
    SENSORY_MEDIA = k("subsystem", "sensory_media")
    INTERNAL_WORLD_MODEL = k("subsystem", "internal_world_model")
    EXTERNAL_KNOWLEDGE_INTEGRATION = k("subsystem", "external_knowledge_integration")
    ERROR_DRIFT_FAILSAFE = k("subsystem", "error_drift_failsafe")
    EDGE_CASE_HANDLING = k("subsystem", "edge_case_handling")
    GLOBAL_COMMITMENTS_POSTURE_ENGINE = k("subsystem", "global_commitments_posture_engine")
    PLANNING_TASKING_EXECUTION = k("subsystem", "planning_tasking_execution")
    MULTI_INSTANCE = k("subsystem", "multi_instance")
    NYRAHOME_BRAIN = k("subsystem", "nyrahome_brain")


class SyncKeys(str, Enum):
    """Registry keys for synchronization state."""

    EVENT_CURSOR = k("sync", "event_cursor")


class InstanceKeys(str, Enum):
    """Registry keys for instance registry state."""

    INSTANCE_REGISTRY = k("instances", "registry")


class PushKeys(str, Enum):
    """Registry keys for push notification state."""

    APNS_REGISTRATION = k("push", "apns_registration")


SUBSYSTEM_STATE_CLASS_MAP = {
    SubsystemKeys.ATTENTION_CONTEXT_ROUTING.value: "state.subsystems.core.AttentionContextRoutingState",
    SubsystemKeys.COGNITIVE_GOAL_SYSTEM.value: "state.subsystems.core.CognitiveGoalSystemState",
    SubsystemKeys.COGNITIVE_THROTTLE_PROCESSING_MODES.value: "state.subsystems.core.CognitiveThrottleProcessingModesState",
    SubsystemKeys.PRIVATE_COGNITIVE_WORKSPACE.value: "state.subsystems.core.PrivateCognitiveWorkspaceState",
    SubsystemKeys.INTEGRATION_ORCHESTRATION.value: "state.subsystems.core.IntegrationOrchestrationState",
    SubsystemKeys.IDENTITY.value: "state.subsystems.core.IdentityState",
    SubsystemKeys.AUTONOMY.value: "state.subsystems.core.AutonomyState",
    SubsystemKeys.AUTONOMY_BANDS.value: "state.subsystems.core.AutonomyBandsState",
    SubsystemKeys.DEBATE_SYSTEM.value: "state.subsystems.core.DebateSystemState",
    SubsystemKeys.RELATIONAL_ROLE_LADDER.value: "state.subsystems.core.RelationalRoleLadderState",
    SubsystemKeys.EMOTIONAL_ENGINE.value: "state.subsystems.core.EmotionalEngineState",
    SubsystemKeys.COMMUNICATION_LAYERS.value: "state.subsystems.core.CommunicationLayersState",
    SubsystemKeys.SOCIAL_RHYTHM_MICRO_BEHAVIOR_ENGINE.value: "state.subsystems.core.SocialRhythmMicroBehaviorEngineState",
    SubsystemKeys.SISTER_RELATIONAL_ENGINE.value: "state.subsystems.core.SisterRelationalEngineState",
    SubsystemKeys.REST_SLEEP_RHYTHM.value: "state.subsystems.core.RestSleepRhythmState",
    SubsystemKeys.MEMORY_EXPERIENCE.value: "state.subsystems.memory.MemoryExperienceState",
    SubsystemKeys.SKILL_TREE_LEARNING_ENGINE.value: "state.subsystems.memory.SkillTreeLearningEngineState",
    SubsystemKeys.INTERACTION_PRESENCE_LAYER.value: "state.subsystems.interaction.InteractionPresenceLayerState",
    SubsystemKeys.HUMAN_INTEGRATION.value: "state.subsystems.interaction.HumanIntegrationState",
    SubsystemKeys.SENSORY_MEDIA.value: "state.subsystems.interaction.SensoryMediaState",
    SubsystemKeys.INTERNAL_WORLD_MODEL.value: "state.subsystems.perception.InternalWorldModelState",
    SubsystemKeys.EXTERNAL_KNOWLEDGE_INTEGRATION.value: "state.subsystems.perception.ExternalKnowledgeIntegrationState",
    SubsystemKeys.ERROR_DRIFT_FAILSAFE.value: "state.subsystems.perception.ErrorDriftFailSafeState",
    SubsystemKeys.EDGE_CASE_HANDLING.value: "state.subsystems.perception.EdgeCaseHandlingState",
    SubsystemKeys.GLOBAL_COMMITMENTS_POSTURE_ENGINE.value: "state.subsystems.perception.GlobalCommitmentsPostureEngineState",
    SubsystemKeys.PLANNING_TASKING_EXECUTION.value: "state.subsystems.infrastructure.PlanningTaskingExecutionState",
    SubsystemKeys.MULTI_INSTANCE.value: "state.subsystems.infrastructure.MultiInstanceState",
    SubsystemKeys.NYRAHOME_BRAIN.value: "state.subsystems.infrastructure.NyrahomeBrainState",
}
