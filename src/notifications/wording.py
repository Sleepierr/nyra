"""Notification wording generation for Phase 7.

Non-manipulative, tone-safe notification wording.
Per spec: spec/base1.0/push_notification_apns_spec.md §6
"""

from __future__ import annotations

from typing import Dict, Optional

from .models import NotificationClass, NotificationWording


class WordingGenerator:
    """Generates non-manipulative notification wording.

    Per spec: spec/base1.0/push_notification_apns_spec.md §6
    Must be: neutral, calm, no guilt/urgency inflation, no romantic language
    """

    def generate_wording(
        self, notification_class: NotificationClass, context: Optional[Dict[str, Any]] = None
    ) -> NotificationWording:
        """Generate notification wording for a notification class.

        Per spec: spec/base1.0/push_notification_apns_spec.md §6

        Args:
            notification_class: Notification class.
            context: Optional context dictionary.

        Returns:
            Notification wording object.
        """
        text = self._get_wording_for_class(notification_class, context)

        return NotificationWording(
            text=text,
            notification_class=notification_class,
            metadata=context,
        )

    def _get_wording_for_class(
        self, notification_class: NotificationClass, context: Optional[Dict[str, Any]]
    ) -> str:
        """Get wording text for a notification class.

        Per spec: §6.1 - Allowed examples:
        - "There's something to review when you're free."
        - "A new update is available."
        - "Action needed: a decision is pending."

        Args:
            notification_class: Notification class.
            context: Optional context.

        Returns:
            Wording text.
        """
        # Attention Ping: Light cue that something is available
        if notification_class == NotificationClass.ATTENTION_PING:
            return "There's something to review when you're free."

        # Action Needed: Something requires an explicit user decision
        if notification_class == NotificationClass.ACTION_NEEDED:
            return "Action needed: a decision is pending."

        # Message Delivered: Confirmation that a user-facing message exists
        if notification_class == NotificationClass.MESSAGE_DELIVERED:
            return "A new update is available."

        # Safety / Critical: System safety or integrity issue
        if notification_class == NotificationClass.SAFETY_CRITICAL:
            return "System notification: attention required."

        # Default fallback
        return "Notification available."


