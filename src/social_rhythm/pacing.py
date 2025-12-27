"""Throttling and pacing for Phase 7.

Notification throttling limits and pacing management.
Per spec: spec/base1.0/push_notification_apns_spec.md §4
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .models import ThrottleWindow


class PacingManager:
    """Manages notification throttling and pacing.

    Per spec: spec/base1.0/push_notification_apns_spec.md §4
    Limits: 3 notifications per 5 minutes, 20 per 24 hours (per instance)
    """

    def __init__(self) -> None:
        """Initialize pacing manager."""
        self._throttle_windows: Dict[str, ThrottleWindow] = {}

    def get_throttle_window(self, instance_id: str) -> ThrottleWindow:
        """Get or create throttle window for an instance.

        Args:
            instance_id: Instance identifier.

        Returns:
            Throttle window for that instance.
        """
        if instance_id not in self._throttle_windows:
            self._throttle_windows[instance_id] = ThrottleWindow(instance_id=instance_id)
        return self._throttle_windows[instance_id]

    def can_send_notification(self, instance_id: str, now: Optional[datetime] = None) -> bool:
        """Check if a notification can be sent (respecting throttling limits).

        Per spec: spec/base1.0/push_notification_apns_spec.md §4.1

        Args:
            instance_id: Instance identifier.
            now: Current datetime (defaults to now).

        Returns:
            True if notification can be sent, False if throttled.
        """
        if now is None:
            now = datetime.now()

        window = self.get_throttle_window(instance_id)

        # Clean old notifications (older than 24 hours)
        cutoff_24h = now - timedelta(hours=24)
        cutoff_5min = now - timedelta(minutes=5)

        window.recent_notifications = [
            ts for ts in window.recent_notifications if ts > cutoff_24h
        ]

        # Check 24-hour limit
        if len(window.recent_notifications) >= window.max_per_24h:
            return False

        # Check 5-minute limit
        recent_5min = [ts for ts in window.recent_notifications if ts > cutoff_5min]
        if len(recent_5min) >= window.max_per_5min:
            return False

        return True

    def record_notification(self, instance_id: str, now: Optional[datetime] = None) -> None:
        """Record that a notification was sent.

        Args:
            instance_id: Instance identifier.
            now: Current datetime (defaults to now).
        """
        if now is None:
            now = datetime.now()

        window = self.get_throttle_window(instance_id)
        window.recent_notifications.append(now)

        # Clean old notifications
        cutoff_24h = now - timedelta(hours=24)
        window.recent_notifications = [
            ts for ts in window.recent_notifications if ts > cutoff_24h
        ]

    def get_collapse_window_end(
        self, instance_id: str, notification_class: str, now: Optional[datetime] = None
    ) -> Optional[datetime]:
        """Get collapse window end time for notification class.

        Per spec: spec/base1.0/push_notification_apns_spec.md §4.2
        Collapse window: 60 seconds for Attention Ping / Message Delivered

        Args:
            instance_id: Instance identifier.
            notification_class: Notification class.
            now: Current datetime (defaults to now).

        Returns:
            End time of collapse window, or None if no collapse window.
        """
        if notification_class not in ("attention_ping", "message_delivered"):
            return None  # No collapse window for other classes

        if now is None:
            now = datetime.now()

        # 60-second collapse window
        return now + timedelta(seconds=60)


