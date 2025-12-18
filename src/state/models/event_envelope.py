"""EventEnvelope model per spec/base1.0/nyrahome_cloud_spec.md §1.1."""
from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel
from typing_extensions import Literal


class EventEnvelope(BaseModel):
    """Canonical event envelope synchronized by NyraHome."""

    event_id: str
    seq: int
    ts_utc: str
    source_instance_id: str
    source_kind: Literal["home", "secondary", "transient", "clone"]
    type: str
    payload: Dict[str, Any]
    meta: Optional[Dict[str, Any]] = None
