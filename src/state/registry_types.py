"""Registry typing contracts for Phase 1 state models."""

from __future__ import annotations

from typing import Iterable, Optional, Protocol, TypeVar

from pydantic import BaseModel

TState = TypeVar("TState", bound=BaseModel)


class RegistryRead(Protocol[TState]):
    """Read-only registry view for retrieving Pydantic state models."""

    def get(self, key: str) -> TState:
        """Return the state model for the registry key; raises if absent."""

    def try_get(self, key: str) -> Optional[TState]:
        """Return the state model for the registry key or ``None`` when missing."""

    def keys(self) -> Iterable[str]:
        """Iterate over available registry keys without imposing ordering semantics."""


class RegistryWrite(Protocol[TState]):
    """Write-capable registry view for updating Pydantic state models."""

    def set(self, key: str, value: TState) -> None:
        """Associate the registry key with the provided state model."""

    def delete(self, key: str) -> None:
        """Remove the registry entry for the key when present."""


class Registry(RegistryRead[TState], RegistryWrite[TState], Protocol[TState]):
    """Canonical registry interface combining read and write capabilities."""

    def reset(self) -> None:
        """Clear all known registry keys and associated state models."""

