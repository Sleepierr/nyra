"""APNs registration models per spec/base1.0/push_notification_apns_spec.md §1.1."""
from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import Literal


class ApnsRegistration(BaseModel):
    """Canonical stored APNs registration record bound to an instance."""

    instance_id: str
    apns_device_token: str
    environment: Literal["sandbox", "production"]

    """No validation beyond Pydantic structural typing is performed."""
