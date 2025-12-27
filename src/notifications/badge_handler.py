"""Badge handler for Phase 7.

Badge behavior: always 1 (presence indicator, not unread count).
Per spec: spec/base1.0/push_notification_apns_spec.md §3.3
"""

from __future__ import annotations


class BadgeHandler:
    """Handles badge behavior for notifications.

    Per spec: spec/base1.0/push_notification_apns_spec.md §3.3
    Badge is always 1 (presence indicator, not unread count).
    """

    def get_badge_value(self) -> int:
        """Get badge value for notifications.

        Per spec: §3.3 - badge is always 1

        Returns:
            Badge value (always 1).
        """
        return 1

    def should_update_badge(self) -> bool:
        """Check if badge should be updated.

        Badge is always 1, so this always returns True if we need to ensure
        badge is set to 1.

        Returns:
            True if badge should be updated.
        """
        return True


