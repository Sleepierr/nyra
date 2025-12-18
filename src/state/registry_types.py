"""Registry typing contracts for Phase 1 state models."""

from __future__ import annotations

from typing import Iterable, Optional, Protocol, TypeVar

from pydantic import BaseModel

StateModel = TypeVar("StateModel", bound=BaseModel)


class RegistryRead(Protocol[StateModel]):
    """Read-only registry view for retrieving Pydantic state models."""

    def get(self, key: str) -> StateModel:
        """Return the state model for the registry key; raises if absent."""

    def try_get(self, key: str) -> Optional[StateModel]:
        """Return the state model for the registry key or ``None`` when missing."""

    def keys(self) -> Iterable[str]:
        """Iterate over available registry keys without imposing ordering semantics."""


class RegistryWrite(Protocol[StateModel]):
    """Write-capable registry view for updating Pydantic state models."""

    def set(self, key: str, value: StateModel) -> None:
        """Associate the registry key with the provided state model."""

    def delete(self, key: str) -> None:
        """Remove the registry entry for the key when present."""


class Registry(RegistryRead[StateModel], RegistryWrite[StateModel], Protocol[StateModel]):
    """Canonical registry interface combining read and write capabilities."""

    def reset(self) -> None:
        """Clear all known registry keys and associated state models."""

