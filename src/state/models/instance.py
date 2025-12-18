"""Instance registry models per spec/base1.0/nyrahome_cloud_spec.md §6.1."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from typing_extensions import Literal


class Instance(BaseModel):
    """Canonical stored instance record."""

    instance_id: str
    display_name: str
    instance_kind: Literal["home", "secondary", "transient", "clone"]
    platform: str
    device_model: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None
    created_utc: str
    last_seen_utc: str
    status: Literal["active", "disabled", "revoked"]
    role_hint: Optional[str] = None
    notes: Optional[str] = None

    """No validation beyond Pydantic structural typing is performed."""
