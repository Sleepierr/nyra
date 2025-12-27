"""Social rhythm models for Phase 7.

Models for quiet hours, throttling, pacing, and intentional silence.
Per spec: subsystems/base1.0/subsystem_social_rhythm_micro_behavior_engine.md
Per spec: spec/base1.0/push_notification_apns_spec.md
"""

from __future__ import annotations

from datetime import datetime, time
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class QuietHoursConfig(BaseModel):
    """Quiet hours configuration.

    Per spec: spec/base1.0/push_notification_apns_spec.md §5.1
    Default: 11:00 PM → 8:00 AM (local time)
    """

    start_hour: int = 23  # 11 PM
    start_minute: int = 0
    end_hour: int = 8  # 8 AM
    end_minute: int = 0
    enabled: bool = True


class ThrottleWindow(BaseModel):
    """Throttling window state.

    Per spec: spec/base1.0/push_notification_apns_spec.md §4.1
    Limits: 3 notifications per 5 minutes, 20 per 24 hours
    """

    instance_id: str
    recent_notifications: List[datetime] = []
    max_per_5min: int = 3
    max_per_24h: int = 20


class CheckInRequest(BaseModel):
    """Lightweight check-in request.

    Brief, non-demanding micro-interaction to assess availability.
    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §8
    """

    check_in_id: str
    timestamp: datetime
    presence_state_required: Optional[str] = None  # Only in Quiet/Background


class SilenceContext(BaseModel):
    """Intentional silence context.

    Silence treated as valid information - no follow-up, no escalation.
    Per spec: subsystems/base1.0/subsystem_interaction_presence_layer.md §8.3
    """

    silence_start: datetime
    silence_end: Optional[datetime] = None
    resolved_to_state: str = "background"  # Default: Background Presence


class ChaosIntensityLevel(str, Enum):
    """Chaos intensity levels.

    Scales with autonomy band.
    Per spec: subsystems/base1.0/subsystem_social_rhythm_micro_behavior_engine.md §5
    """

    NONE = "none"  # 0-10 (Band 0-20)
    LOW = "low"  # 10-30 (Band 20-40)
    MODERATE = "moderate"  # 30-60 (Band 40-60)
    HIGH = "high"  # 60-85 (Band 60-80)
    VERY_HIGH = "very_high"  # 85+ (Band 80-100, future)


