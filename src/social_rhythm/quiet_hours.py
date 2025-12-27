"""Quiet hours enforcement for Phase 7.

Quiet hours configuration and enforcement for notifications.
Per spec: spec/base1.0/push_notification_apns_spec.md §5
"""

from __future__ import annotations

from datetime import datetime, time
from typing import Optional

from .models import QuietHoursConfig


class QuietHoursManager:
    """Manages quiet hours configuration and enforcement.

    Per spec: spec/base1.0/push_notification_apns_spec.md §5
    Default: 11:00 PM → 8:00 AM (local time)
    """

    def __init__(self, config: Optional[QuietHoursConfig] = None) -> None:
        """Initialize quiet hours manager.

        Args:
            config: Quiet hours configuration. Defaults to standard 11 PM - 8 AM.
        """
        self._config = config or QuietHoursConfig()

    def is_quiet_hours(self, now: Optional[datetime] = None) -> bool:
        """Check if current time is within quiet hours.

        Per spec: spec/base1.0/push_notification_apns_spec.md §5.2

        Args:
            now: Current datetime (defaults to now). Uses local time.

        Returns:
            True if within quiet hours, False otherwise.
        """
        if not self._config.enabled:
            return False

        if now is None:
            now = datetime.now()

        current_time = now.time()
        start_time = time(self._config.start_hour, self._config.start_minute)
        end_time = time(self._config.end_hour, self._config.end_minute)

        # Handle quiet hours that span midnight (e.g., 11 PM - 8 AM)
        if start_time > end_time:
            # Quiet hours span midnight
            return current_time >= start_time or current_time < end_time
        else:
            # Quiet hours within same day
            return start_time <= current_time < end_time

    def should_suppress_notification(self, notification_class: str) -> bool:
        """Check if a notification should be suppressed during quiet hours.

        Per spec: spec/base1.0/push_notification_apns_spec.md §5.2

        Args:
            notification_class: Notification class (attention_ping, action_needed, etc.)

        Returns:
            True if notification should be suppressed, False if allowed.
        """
        if not self.is_quiet_hours():
            return False

        # Safety/Critical: Always allowed during quiet hours
        if notification_class == "safety_critical":
            return False

        # Attention Ping / Message Delivered: Suppressed during quiet hours
        if notification_class in ("attention_ping", "message_delivered"):
            return True

        # Action Needed: Suppressed during quiet hours
        if notification_class == "action_needed":
            return True

        return False

    def get_config(self) -> QuietHoursConfig:
        """Get quiet hours configuration."""
        return self._config

    def update_config(self, config: QuietHoursConfig) -> None:
        """Update quiet hours configuration.

        Args:
            config: New quiet hours configuration.
        """
        self._config = config


