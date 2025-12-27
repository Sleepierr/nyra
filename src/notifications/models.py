"""Notification models for Phase 7.

Models for notification classes, payloads, and wording.
Per spec: spec/base1.0/push_notification_apns_spec.md
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class NotificationClass(str, Enum):
    """Notification classes.

    Per spec: spec/base1.0/push_notification_apns_spec.md §2
    """

    ATTENTION_PING = "attention_ping"  # Light cue, low urgency
    ACTION_NEEDED = "action_needed"  # Requires decision, medium urgency
    MESSAGE_DELIVERED = "message_delivered"  # Confirmation, low urgency
    SAFETY_CRITICAL = "safety_critical"  # System safety, high urgency, allowed during quiet hours


class NotificationPayload(BaseModel):
    """APNs notification payload.

    Per spec: spec/base1.0/push_notification_apns_spec.md §3.3
    """

    title: str = "Nyra"
    body: str  # Short, neutral line
    badge: int = 1  # Always 1 (presence indicator, not unread count)
    sound: str = "default"
    content_available: int = 1
    notification_class: NotificationClass
    instance_id: str
    hint: str = "poll"  # Only allowed hint value


class NotificationWording(BaseModel):
    """Non-manipulative notification wording.

    Per spec: spec/base1.0/push_notification_apns_spec.md §6
    Must be: neutral, calm, no guilt/urgency inflation, no romantic language
    """

    text: str
    notification_class: NotificationClass
    metadata: Optional[Dict[str, Any]] = None


