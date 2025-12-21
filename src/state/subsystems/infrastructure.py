"""Infrastructure subsystem state shells."""

from pydantic import BaseModel

# Subsystems covered: planning, execution, and multi-instance infrastructure.


class PlanningTaskingExecutionState(BaseModel):
    """State shell for subsystem spec: subsystems/base1.0/subsystem_planning_tasking_execution.md. Fields deferred; spec does not mandate persistent state fields in Base 1.0."""

    pass


class MultiInstanceState(BaseModel):
    """State shell for subsystem spec: subsystems/base1.0/subsystem_multi_instance.md. Fields deferred; spec does not mandate persistent state fields in Base 1.0."""

    pass


class NyrahomeBrainState(BaseModel):
    """State shell for subsystem spec: subsystems/base1.0/subsystem_nyrahome_brain.md. Fields deferred; spec does not mandate persistent state fields in Base 1.0."""

    pass
