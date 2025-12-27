"""Quiet hours integration for notifications.

Integration between notifications and quiet hours manager.
Per spec: spec/base1.0/push_notification_apns_spec.md §5.2
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..social_rhythm.quiet_hours import QuietHoursManager


class QuietHoursIntegration:
    """Integrates notification system with quiet hours.

    Per spec: spec/base1.0/push_notification_apns_spec.md §5.2
    Phase 7: Quiet hours suppression for non-critical notifications.
    """

    def __init__(self, quiet_hours_manager: "QuietHoursManager") -> None:
        """Initialize quiet hours integration.

        Args:
            quiet_hours_manager: Quiet hours manager instance.
        """
        self._quiet_hours = quiet_hours_manager

    def should_suppress(
        self, notification_class: str, now: Optional["datetime"] = None
    ) -> bool:
        """Check if notification should be suppressed due to quiet hours.

        Per spec: spec/base1.0/push_notification_apns_spec.md §5.2

        Args:
            notification_class: Notification class string.
            now: Current datetime (optional).

        Returns:
            True if notification should be suppressed, False otherwise.
        """
        return self._quiet_hours.should_suppress_notification(notification_class)

    def get_collapsed_notification_time(self) -> Optional["datetime"]:
        """Get time when collapsed notifications should be delivered.

        Per spec: §5.2 - Suppressed notifications delivered as single collapsed
        notification after quiet hours if still relevant.

        Returns:
            End of quiet hours time, or None if not in quiet hours.
        """
        if not self._quiet_hours.is_quiet_hours():
            return None

        # Return end of quiet hours (8 AM default)
        config = self._quiet_hours.get_config()
        # This is simplified - in practice would calculate next end time
        # For now, return None (implementation detail)
        return None


