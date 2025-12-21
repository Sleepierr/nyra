"""APNs registration API payload models per spec/base1.0/push_notification_apns_spec.md §1.1."""
from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import Literal


class ApnsRegisterRequest(BaseModel):
    """Request payload for POST /push/apns/register."""

    apns_device_token: str
    environment: Literal["sandbox", "production"]


class ApnsRegisterResponse(BaseModel):
    """Response payload for POST /push/apns/register."""

    ok: bool

    """No validation beyond Pydantic structural typing is performed."""
