"""Instance registry API payload models per spec/base1.0/nyrahome_cloud_spec.md §6.2–6.3."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from typing_extensions import Literal

from .instance import Instance


class InstanceRegisterRequest(BaseModel):
    """Request payload for POST /instances/register."""

    instance_id: str
    display_name: str
    instance_kind: Literal["home", "secondary", "transient", "clone"]
    platform: str
    device_model: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None


class InstanceRegisterResponse(BaseModel):
    """Response payload for POST /instances/register."""

    instance: Instance
    server_utc: str
