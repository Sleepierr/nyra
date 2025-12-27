"""Notification manager for Phase 7.

Notification creation, routing, and integration with social rhythm.
Per spec: spec/base1.0/push_notification_apns_spec.md
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..social_rhythm.pacing import PacingManager
from ..social_rhythm.quiet_hours import QuietHoursManager
from .badge_handler import BadgeHandler
from .models import NotificationClass, NotificationPayload
from .quiet_hours_integration import QuietHoursIntegration
from .wording import WordingGenerator


class NotificationManager:
    """Manages notification creation and routing.

    Per spec: spec/base1.0/push_notification_apns_spec.md
    Phase 7: Notification class selection, wording, badge, quiet hours integration.
    """

    def __init__(
        self,
        quiet_hours_manager: QuietHoursManager,
        pacing_manager: PacingManager,
        instance_id: str,
    ) -> None:
        """Initialize notification manager.

        Args:
            quiet_hours_manager: Quiet hours manager instance.
            pacing_manager: Pacing manager instance.
            instance_id: Instance identifier.
        """
        self._quiet_hours = quiet_hours_manager
        self._pacing = pacing_manager
        self._instance_id = instance_id
        self._wording_generator = WordingGenerator()
        self._badge_handler = BadgeHandler()
        self._quiet_hours_integration = QuietHoursIntegration(quiet_hours_manager)

    def create_notification(
        self,
        notification_class: NotificationClass,
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[NotificationPayload]:
        """Create a notification payload if allowed.

        Per spec: spec/base1.0/push_notification_apns_spec.md

        Args:
            notification_class: Notification class.
            context: Optional context dictionary.

        Returns:
            Notification payload if created, None if suppressed/throttled.
        """
        # Check quiet hours suppression
        if self._quiet_hours_integration.should_suppress(notification_class.value):
            return None

        # Check throttling limits
        if not self._pacing.can_send_notification(self._instance_id):
            return None

        # Generate wording
        wording = self._wording_generator.generate_wording(notification_class, context)

        # Create payload
        payload = NotificationPayload(
            title="Nyra",
            body=wording.text,
            badge=self._badge_handler.get_badge_value(),  # Always 1
            sound="default",
            content_available=1,
            notification_class=notification_class,
            instance_id=self._instance_id,
            hint="poll",  # Only allowed hint value (spec §3.3)
        )

        # Record notification
        self._pacing.record_notification(self._instance_id)

        return payload

    def should_suppress(self, notification_class: NotificationClass) -> bool:
        """Check if notification should be suppressed.

        Args:
            notification_class: Notification class.

        Returns:
            True if should be suppressed, False otherwise.
        """
        # Check quiet hours
        if self._quiet_hours_integration.should_suppress(notification_class.value):
            return True

        # Check throttling
        if not self._pacing.can_send_notification(self._instance_id):
            return True

        return False


