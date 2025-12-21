"""Memory subsystem state shells."""

from pydantic import BaseModel

# Subsystems covered: memory & learning.


class MemoryExperienceState(BaseModel):
    """State shell for subsystem spec: subsystems/base1.0/subsystem_memory_experience.md. Fields deferred; spec does not mandate persistent state fields in Base 1.0."""

    pass


class SkillTreeLearningEngineState(BaseModel):
    """State shell for subsystem spec: subsystems/base1.0/subsystem_skill_tree_learning_engine.md. Fields deferred; spec does not mandate persistent state fields in Base 1.0."""

    pass
