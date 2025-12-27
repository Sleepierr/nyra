"""Phase 3 Subsystem Wiring Infrastructure.

This module provides the infrastructure for connecting subsystems to the state spine
without adding behavior. It implements access adapters, dependency declarations,
read/write boundaries, and data flow contracts.

Phase 3: Plumbing, not thinking. No behavior, no decision-making, no logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, FrozenSet, Optional, Set, TYPE_CHECKING

from pydantic import BaseModel

from .keys import SubsystemKeys

if TYPE_CHECKING:
    from .container import StateContainer


# -----------------------------------------------------------------------------
# Dependency Map
# -----------------------------------------------------------------------------

# Maps each subsystem to the set of other subsystems it needs read access to.
# Empty sets indicate no dependencies (subsystem only accesses its own state).
# This map is populated as subsystem relationships are defined in specs.
SUBSYSTEM_DEPENDENCIES: Dict[SubsystemKeys, FrozenSet[SubsystemKeys]] = {
    SubsystemKeys.ATTENTION_CONTEXT_ROUTING: frozenset(),
    SubsystemKeys.COGNITIVE_GOAL_SYSTEM: frozenset(),
    SubsystemKeys.COGNITIVE_THROTTLE_PROCESSING_MODES: frozenset(),
    SubsystemKeys.PRIVATE_COGNITIVE_WORKSPACE: frozenset(),
    SubsystemKeys.INTEGRATION_ORCHESTRATION: frozenset(),
    SubsystemKeys.IDENTITY: frozenset(),
    SubsystemKeys.AUTONOMY: frozenset(),
    SubsystemKeys.AUTONOMY_BANDS: frozenset(),
    SubsystemKeys.DEBATE_SYSTEM: frozenset(),
    SubsystemKeys.RELATIONAL_ROLE_LADDER: frozenset(),
    SubsystemKeys.EMOTIONAL_ENGINE: frozenset(),
    SubsystemKeys.COMMUNICATION_LAYERS: frozenset(),
    SubsystemKeys.SOCIAL_RHYTHM_MICRO_BEHAVIOR_ENGINE: frozenset(),
    SubsystemKeys.SISTER_RELATIONAL_ENGINE: frozenset(),
    SubsystemKeys.REST_SLEEP_RHYTHM: frozenset(),
    SubsystemKeys.MEMORY_EXPERIENCE: frozenset(),
    SubsystemKeys.SKILL_TREE_LEARNING_ENGINE: frozenset(),
    SubsystemKeys.INTERACTION_PRESENCE_LAYER: frozenset(),
    SubsystemKeys.HUMAN_INTEGRATION: frozenset(),
    SubsystemKeys.SENSORY_MEDIA: frozenset(),
    SubsystemKeys.INTERNAL_WORLD_MODEL: frozenset(),
    SubsystemKeys.EXTERNAL_KNOWLEDGE_INTEGRATION: frozenset(),
    SubsystemKeys.ERROR_DRIFT_FAILSAFE: frozenset(),
    SubsystemKeys.EDGE_CASE_HANDLING: frozenset(),
    SubsystemKeys.GLOBAL_COMMITMENTS_POSTURE_ENGINE: frozenset(),
    SubsystemKeys.PLANNING_TASKING_EXECUTION: frozenset(),
    SubsystemKeys.MULTI_INSTANCE: frozenset(),
    SubsystemKeys.NYRAHOME_BRAIN: frozenset(),
}


# -----------------------------------------------------------------------------
# Subsystem Adapter Base Class
# -----------------------------------------------------------------------------


class SubsystemAdapter(ABC):
    """Abstract base adapter providing state access for a subsystem.

    Responsibilities:
    - Provide read/write access to the subsystem's own state
    - Provide read-only access to declared dependency states
    - Enforce access boundaries (no cross-subsystem writes)

    Phase 3: Infrastructure only. No behavior, no decision-making.
    """

    @property
    @abstractmethod
    def subsystem_key(self) -> SubsystemKeys:
        """Return the subsystem key this adapter provides access for."""

    @property
    @abstractmethod
    def own_state(self) -> BaseModel:
        """Return the subsystem's own state (read/write access).

        Returns:
            The state model for this subsystem.
        """

    @abstractmethod
    def update_own_state(self, state: BaseModel) -> None:
        """Update the subsystem's own state.

        Args:
            state: The new state model to set.
        """

    @abstractmethod
    def read_dependency(self, key: SubsystemKeys) -> Optional[BaseModel]:
        """Read state from a declared dependency (read-only access).

        Args:
            key: The subsystem key to read from. Must be in declared dependencies.

        Returns:
            The state model for the dependency, or None if not found.

        Raises:
            ValueError: If the key is not in the declared dependencies.
        """

    @property
    @abstractmethod
    def dependencies(self) -> FrozenSet[SubsystemKeys]:
        """Return the set of declared dependencies for this subsystem."""


# -----------------------------------------------------------------------------
# Concrete Adapter Implementation
# -----------------------------------------------------------------------------


class ConcreteSubsystemAdapter(SubsystemAdapter):
    """Concrete implementation of SubsystemAdapter with boundary enforcement.

    Wraps a StateContainer and enforces:
    - Write access only to own state
    - Read access only to own state or declared dependencies
    """

    def __init__(
        self,
        container: StateContainer,
        subsystem_key: SubsystemKeys,
        dependencies: FrozenSet[SubsystemKeys],
    ):
        """Initialize the adapter.

        Args:
            container: The state container to wrap.
            subsystem_key: The subsystem key this adapter provides access for.
            dependencies: The set of subsystem keys this subsystem can read from.
        """
        self._container = container
        self._subsystem_key = subsystem_key
        self._dependencies = dependencies

    @property
    def subsystem_key(self) -> SubsystemKeys:
        """Return the subsystem key this adapter provides access for."""
        return self._subsystem_key

    @property
    def own_state(self) -> BaseModel:
        """Return the subsystem's own state (read/write access).

        Returns:
            The state model for this subsystem.
        """
        return self._container.get(self._subsystem_key.value)

    def update_own_state(self, state: BaseModel) -> None:
        """Update the subsystem's own state.

        Args:
            state: The new state model to set.
        """
        self._container.set(self._subsystem_key.value, state)

    def read_dependency(self, key: SubsystemKeys) -> Optional[BaseModel]:
        """Read state from a declared dependency (read-only access).

        Args:
            key: The subsystem key to read from. Must be in declared dependencies.

        Returns:
            The state model for the dependency, or None if not found.

        Raises:
            ValueError: If the key is not in the declared dependencies.
        """
        if key not in self._dependencies:
            raise ValueError(
                f"Subsystem '{self._subsystem_key.value}' cannot read from "
                f"'{key.value}': not in declared dependencies. "
                f"Declared dependencies: {[d.value for d in self._dependencies]}"
            )
        return self._container.try_get(key.value)

    @property
    def dependencies(self) -> FrozenSet[SubsystemKeys]:
        """Return the set of declared dependencies for this subsystem."""
        return self._dependencies


# -----------------------------------------------------------------------------
# Adapter Factory
# -----------------------------------------------------------------------------


class SubsystemAdapterFactory:
    """Factory for creating SubsystemAdapter instances with boundary enforcement.

    Creates adapters that:
    - Are bound to a specific StateContainer
    - Enforce read/write boundaries based on SUBSYSTEM_DEPENDENCIES
    - Provide type-safe access to state

    Phase 3: Infrastructure only. No behavior, no decision-making.
    """

    def __init__(self, container: StateContainer):
        """Initialize the factory with a state container.

        Args:
            container: The state container adapters will wrap.
        """
        self._container = container
        self._adapter_cache: Dict[SubsystemKeys, SubsystemAdapter] = {}

    def get_adapter(self, subsystem_key: SubsystemKeys) -> SubsystemAdapter:
        """Get or create an adapter for the specified subsystem.

        Args:
            subsystem_key: The subsystem to get an adapter for.

        Returns:
            A SubsystemAdapter instance for the specified subsystem.

        Raises:
            ValueError: If the subsystem key is not in SUBSYSTEM_DEPENDENCIES.
        """
        if subsystem_key not in SUBSYSTEM_DEPENDENCIES:
            raise ValueError(
                f"Unknown subsystem key: {subsystem_key.value}. "
                f"Key must be defined in SUBSYSTEM_DEPENDENCIES."
            )

        # Return cached adapter if available
        if subsystem_key in self._adapter_cache:
            return self._adapter_cache[subsystem_key]

        # Create new adapter
        dependencies = SUBSYSTEM_DEPENDENCIES[subsystem_key]
        adapter = ConcreteSubsystemAdapter(
            container=self._container,
            subsystem_key=subsystem_key,
            dependencies=dependencies,
        )

        # Cache and return
        self._adapter_cache[subsystem_key] = adapter
        return adapter

    def clear_cache(self) -> None:
        """Clear the adapter cache.

        Useful when the underlying container is reset.
        """
        self._adapter_cache.clear()






