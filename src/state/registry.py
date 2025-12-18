"""Skeleton registry interface adhering to the Phase 1 state architecture."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, Optional

from .registry_types import Registry, RegistryRead, RegistryWrite, StateModel


class RegistryBase(Registry[StateModel], ABC, Generic[StateModel]):
    """Abstract base for registry implementations.

    This skeleton defines the canonical access surface for registry operations
    without prescribing storage, concurrency, or lifecycle details.
    """

    @abstractmethod
    def get(self, key: str) -> StateModel:
        """Retrieve the state model associated with the registry key."""

    @abstractmethod
    def try_get(self, key: str) -> Optional[StateModel]:
        """Return the state model for the registry key or ``None`` when missing."""

    @abstractmethod
    def keys(self) -> Iterable[str]:
        """Iterate over available registry keys without imposing ordering semantics."""

    @abstractmethod
    def set(self, key: str, value: StateModel) -> None:
        """Associate the registry key with the provided state model."""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove the registry entry for the key when present."""

    @abstractmethod
    def reset(self) -> None:
        """Clear all known registry keys and associated state models."""


class ReadOnlyRegistry(RegistryRead[StateModel], ABC, Generic[StateModel]):
    """Read-only registry surface for components that must not mutate state."""

    @abstractmethod
    def get(self, key: str) -> StateModel:
        """Retrieve the state model associated with the registry key."""

    @abstractmethod
    def try_get(self, key: str) -> Optional[StateModel]:
        """Return the state model for the registry key or ``None`` when missing."""

    @abstractmethod
    def keys(self) -> Iterable[str]:
        """Iterate over available registry keys without imposing ordering semantics."""


class WriteOnlyRegistry(RegistryWrite[StateModel], ABC, Generic[StateModel]):
    """Write-only registry surface for isolated mutation pathways."""

    @abstractmethod
    def set(self, key: str, value: StateModel) -> None:
        """Associate the registry key with the provided state model."""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove the registry entry for the key when present."""

