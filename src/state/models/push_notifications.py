"""Push notification intent models per spec/base1.0/push_notification_apns_spec.md §§2-6."""
from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import Literal


NotificationClass = Literal[
    "attention_ping",
    "action_needed",
    "message_delivered",
    "safety_critical",
]
"""Enumerated push notification classes defined in the Base 1.0 spec."""


WakeHint = Literal["poll"]
"""Wake hint instructing clients to poll for state."""


class PushNotificationIntent(BaseModel):
    """Canonical internal representation of a push notification intent."""

    notification_class: NotificationClass
    instance_id: str
    preview_text: str
    hint: WakeHint = "poll"

    """No validation beyond Pydantic structural typing is performed."""
