"""State Container for Phase 2 State Runtime Spine.

This module implements the mutable state container that holds all subsystem
state shells and provides keyed access via the Registry interface.

Per spec: Phase 2 makes state "live" without adding behavior.
"""

from __future__ import annotations

import importlib
from typing import Dict, Iterable, Optional

from pydantic import BaseModel

from .keys import SubsystemKeys, SUBSYSTEM_STATE_CLASS_MAP
from .registry_types import Registry


class StateContainer:
    """Mutable, long-lived container for Nyra state models.

    Responsibilities:
    - Hold subsystem state shells
    - Provide keyed access via Registry interface
    - Hybrid initialization (eager subsystems, lazy aux state)
    - Support mutation via set()/delete()

    Phase 2: Single global scope (instance_id ignored but accepted for future design)
    """

    def __init__(self, instance_id: Optional[str] = None):
        """Initialize container with optional instance_id (reserved for future instance scoping).

        Eagerly instantiates all SubsystemKeys state shells.

        Args:
            instance_id: Optional instance identifier (reserved for future use; ignored in Phase 2).
        """
        # Phase 2: instance_id is stored but not used (reserved for future instance scoping)
        self._instance_id = instance_id

        # In-memory dictionary for state storage
        self._state: Dict[str, BaseModel] = {}

        # Eagerly initialize all subsystem state shells
        self._initialize_subsystems()

    def _initialize_subsystems(self) -> None:
        """Eagerly instantiate all SubsystemKeys state shells."""
        for key_enum in SubsystemKeys:
            key = key_enum.value
            class_path = SUBSYSTEM_STATE_CLASS_MAP[key]
            state_class = self._import_class(class_path)
            self._state[key] = state_class()

    def _import_class(self, class_path: str) -> type[BaseModel]:
        """Import a class from a string import path.

        Args:
            class_path: Dot-separated module path, e.g., "state.subsystems.core.IdentityState"

        Returns:
            The imported class

        Raises:
            ImportError: If the class cannot be imported
        """
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def _lazy_initialize_auxiliary(self, key: str) -> Optional[BaseModel]:
        """Attempt to lazily instantiate auxiliary state for a key.

        Args:
            key: The registry key string

        Returns:
            Instantiated state model if key is known and can be instantiated without parameters, None otherwise

        Note:
            Models that require constructor parameters (e.g., Cursor, ApnsRegistration) are not
            lazily initialized. They must be created via set() with proper initialization.
        """
        # Map auxiliary keys to their state classes that can be instantiated without parameters
        # Models requiring parameters (Cursor, ApnsRegistration) are excluded from lazy initialization
        auxiliary_map: Dict[str, type[BaseModel]] = {
            # InstanceKeys.INSTANCE_REGISTRY: No explicit model defined in Phase 1/2
            # SyncKeys.EVENT_CURSOR: Cursor requires __root__ parameter, cannot lazily initialize
            # PushKeys.APNS_REGISTRATION: ApnsRegistration requires parameters, cannot lazily initialize
            # Skip lazy initialization for keys without defined models or that require parameters
        }

        state_class = auxiliary_map.get(key)
        if state_class is not None:
            return state_class()

        return None

    def get(self, key: str) -> BaseModel:
        """Retrieve the state model associated with the registry key.

        Args:
            key: The registry key string

        Returns:
            The state model for the key

        Raises:
            KeyError: If the key is not found (after lazy initialization attempt)
        """
        # Try direct lookup first
        if key in self._state:
            return self._state[key]

        # Attempt lazy initialization for auxiliary keys
        instance = self._lazy_initialize_auxiliary(key)
        if instance is not None:
            self._state[key] = instance
            return instance

        # Key not found
        raise KeyError(f"State not found for key: {key}")

    def try_get(self, key: str) -> Optional[BaseModel]:
        """Return the state model for the registry key or None when missing.

        Args:
            key: The registry key string

        Returns:
            The state model for the key, or None if not found
        """
        try:
            return self.get(key)
        except KeyError:
            return None

    def keys(self) -> Iterable[str]:
        """Iterate over available registry keys without imposing ordering semantics.

        Returns:
            An iterable of registry key strings
        """
        return self._state.keys()

    def set(self, key: str, value: BaseModel) -> None:
        """Associate the registry key with the provided state model.

        Args:
            key: The registry key string
            value: The state model instance (must be a BaseModel)
        """
        if not isinstance(value, BaseModel):
            raise TypeError(f"State value must be a BaseModel instance, got {type(value)}")
        self._state[key] = value

    def delete(self, key: str) -> None:
        """Remove the registry entry for the key when present.

        Args:
            key: The registry key string
        """
        self._state.pop(key, None)

    def reset(self) -> None:
        """Clear all known registry keys and associated state models."""
        self._state.clear()
        # Re-initialize subsystems after reset
        self._initialize_subsystems()
