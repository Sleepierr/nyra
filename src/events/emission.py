"""Event emission infrastructure for Phase 4.

Provides EventFactory for creating properly structured EventEnvelope instances
and EventEmitter protocol for components that emit events.

Phase 4: Structural validation only - no semantic validation or interpretation.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Protocol

from typing_extensions import Literal

from ..state.models.event_envelope import EventEnvelope


class EventEmitter(Protocol):
    """Protocol for components that emit events.

    Phase 4: Interface definition only - no behavior requirements.
    """

    def emit(self, event: EventEnvelope) -> None:
        """Emit an event.

        Args:
            event: The event envelope to emit.
        """
        ...


class EventFactory:
    """Factory for creating properly structured EventEnvelope instances.

    Handles:
    - UUIDv4 event_id generation
    - ISO 8601 UTC timestamp generation
    - Required field validation
    - Structural validation (format checks only)

    Phase 4: No semantic validation or interpretation.
    """

    @staticmethod
    def create(
        source_instance_id: str,
        source_kind: Literal["home", "secondary", "transient", "clone"],
        event_type: str,
        payload: Dict[str, Any],
        seq: int = 0,
        meta: Optional[Dict[str, Any]] = None,
    ) -> EventEnvelope:
        """Create a new EventEnvelope with proper structure.

        Args:
            source_instance_id: Identifier of the instance emitting the event.
            source_kind: Type of instance (home, secondary, transient, clone).
            event_type: Namespaced event type (e.g., "interaction.message_received").
            payload: Event-specific payload data (must be JSON-serializable).
            seq: Sequence number (default 0; NyraHome assigns authoritative seq).
            meta: Optional metadata dictionary.

        Returns:
            A new EventEnvelope instance with properly formatted fields.

        Raises:
            ValueError: If required fields are missing or invalid format.
        """
        # Generate UUIDv4 event_id
        event_id = str(uuid.uuid4())

        # Generate ISO 8601 UTC timestamp (format: YYYY-MM-DDTHH:mm:ss.sssZ)
        # Remove timezone offset before appending Z
        ts_utc = datetime.now(timezone.utc).replace(tzinfo=None).isoformat(timespec="milliseconds") + "Z"

        # Validate event_type format (must be namespaced: domain.action)
        if "." not in event_type:
            raise ValueError(
                f"Event type must be namespaced (domain.action), got: {event_type}"
            )

        # Validate source_kind
        valid_kinds = {"home", "secondary", "transient", "clone"}
        if source_kind not in valid_kinds:
            raise ValueError(
                f"source_kind must be one of {valid_kinds}, got: {source_kind}"
            )

        # Create and return envelope
        return EventEnvelope(
            event_id=event_id,
            seq=seq,
            ts_utc=ts_utc,
            source_instance_id=source_instance_id,
            source_kind=source_kind,
            type=event_type,
            payload=payload,
            meta=meta,
        )


