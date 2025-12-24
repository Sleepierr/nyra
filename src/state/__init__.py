"""State namespace package for Phase 1, Phase 2, and Phase 3 definitions."""

from .container import StateContainer
from .wiring import (
    SUBSYSTEM_DEPENDENCIES,
    ConcreteSubsystemAdapter,
    SubsystemAdapter,
    SubsystemAdapterFactory,
)

__all__ = [
    "StateContainer",
    "SUBSYSTEM_DEPENDENCIES",
    "SubsystemAdapter",
    "ConcreteSubsystemAdapter",
    "SubsystemAdapterFactory",
]
