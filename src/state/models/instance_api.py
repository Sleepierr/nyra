"""Instance registry API payload models per spec/base1.0/nyrahome_cloud_spec.md §6.2–6.3."""
from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import Literal

from .instance import Instance


class InstanceRegisterRequest(BaseModel):
    """Request payload for POST /instances/register."""

    instance_id: str
    display_name: str
    instance_kind: Literal["home", "secondary", "transient", "clone"]
    platform: str
    device_model: str | None = None
    os_version: str | None = None
    app_version: str | None = None


class InstanceRegisterResponse(BaseModel):
    """Response payload for POST /instances/register."""

    instance: Instance
    server_utc: str


class InstanceHeartbeatRequest(BaseModel):
    """Request payload for POST /instances/heartbeat."""

    status: Literal["active"]


class InstanceHeartbeatResponse(BaseModel):
    """Response payload for POST /instances/heartbeat."""

    ok: bool
    server_utc: str

    """No validation beyond Pydantic structural typing is performed."""
