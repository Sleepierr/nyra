"""Interaction subsystem state shells."""

from pydantic import BaseModel

# Subsystems covered: interaction & presence.


class InteractionPresenceLayerState(BaseModel):
    """State shell for subsystem spec: subsystems/base1.0/subsystem_interaction_presence_layer.md. Fields deferred; spec does not mandate persistent state fields in Base 1.0."""

    pass


class HumanIntegrationState(BaseModel):
    """State shell for subsystem spec: subsystems/base1.0/subsystem_human_integration.md. Fields deferred; spec does not mandate persistent state fields in Base 1.0."""

    pass


class SensoryMediaState(BaseModel):
    """State shell for subsystem spec: subsystems/base1.0/subsystem_sensory_media.md. Fields deferred; spec does not mandate persistent state fields in Base 1.0."""

    pass
