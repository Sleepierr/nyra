"""Time-based scheduling infrastructure for Phase 4.

Provides trigger types and scheduler for time-based event emission.

Phase 4: Scheduling primitives - triggers fire callbacks which handle event emission.
"""

from __future__ import annotations

import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, time as dt_time, timezone
from enum import Enum
from typing import Callable, Dict, Optional

from typing_extensions import Literal


class TriggerType(str, Enum):
    """Types of time-based triggers."""

    INTERVAL = "interval"
    TIME_OF_DAY = "time_of_day"
    ONE_SHOT = "one_shot"


@dataclass
class Trigger(ABC):
    """Abstract base class for time-based triggers.

    Phase 4: Infrastructure only - no behavior beyond timing.
    """

    trigger_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trigger_type: TriggerType = field(init=False)

    @abstractmethod
    def should_fire(self, now: datetime) -> bool:
        """Check if the trigger should fire at the given time.

        Args:
            now: The current UTC datetime.

        Returns:
            True if the trigger should fire, False otherwise.
        """
        pass

    @abstractmethod
    def mark_fired(self, now: datetime) -> None:
        """Mark that the trigger has fired at the given time.

        Used to track last fire time for interval triggers and to mark
        one-shot triggers as consumed.

        Args:
            now: The current UTC datetime.
        """
        pass

    @abstractmethod
    def is_active(self) -> bool:
        """Check if the trigger is still active (can fire again).

        Returns:
            True if the trigger can still fire, False if it's exhausted.
        """
        pass


@dataclass
class IntervalTrigger(Trigger):
    """Trigger that fires at regular intervals.

    Example: Every 30 seconds, every 5 minutes.
    """

    interval_seconds: float
    last_fired: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Set trigger type after initialization."""
        self.trigger_type = TriggerType.INTERVAL
        if self.interval_seconds <= 0:
            raise ValueError(f"Interval must be positive, got: {self.interval_seconds}")

    def should_fire(self, now: datetime) -> bool:
        """Check if enough time has passed since last fire.

        Args:
            now: The current UTC datetime.

        Returns:
            True if the interval has elapsed, False otherwise.
        """
        if self.last_fired is None:
            return True  # First fire

        elapsed = (now - self.last_fired).total_seconds()
        return elapsed >= self.interval_seconds

    def mark_fired(self, now: datetime) -> None:
        """Record that the trigger fired at the given time.

        Args:
            now: The current UTC datetime.
        """
        self.last_fired = now

    def is_active(self) -> bool:
        """Interval triggers are always active (until explicitly cancelled).

        Returns:
            True always.
        """
        return True


@dataclass
class TimeOfDayTrigger(Trigger):
    """Trigger that fires at specific UTC times of day.

    Example: Fire at 12:00 UTC every day.
    """

    hour: int
    minute: int = 0
    second: int = 0
    last_fired_date: Optional[str] = None  # ISO date string (YYYY-MM-DD)

    def __post_init__(self) -> None:
        """Set trigger type and validate time."""
        self.trigger_type = TriggerType.TIME_OF_DAY
        if not (0 <= self.hour < 24):
            raise ValueError(f"Hour must be 0-23, got: {self.hour}")
        if not (0 <= self.minute < 60):
            raise ValueError(f"Minute must be 0-59, got: {self.minute}")
        if not (0 <= self.second < 60):
            raise ValueError(f"Second must be 0-59, got: {self.second}")

    def should_fire(self, now: datetime) -> bool:
        """Check if current time matches the trigger time and hasn't fired today.

        Args:
            now: The current UTC datetime.

        Returns:
            True if the current time matches and hasn't fired today, False otherwise.
        """
        today = now.date().isoformat()

        # Check if already fired today
        if self.last_fired_date == today:
            return False

        # Check if current time matches trigger time (within the same second)
        target_time = dt_time(self.hour, self.minute, self.second)
        current_time = now.time()
        return (
            current_time.hour == target_time.hour
            and current_time.minute == target_time.minute
            and current_time.second == target_time.second
        )

    def mark_fired(self, now: datetime) -> None:
        """Record that the trigger fired today.

        Args:
            now: The current UTC datetime.
        """
        self.last_fired_date = now.date().isoformat()

    def is_active(self) -> bool:
        """Time-of-day triggers are always active (until explicitly cancelled).

        Returns:
            True always.
        """
        return True


@dataclass
class OneShotTrigger(Trigger):
    """Trigger that fires once after a delay.

    Example: Fire after 60 seconds, then never again.
    """

    delay_seconds: float
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fired: bool = False

    def __post_init__(self) -> None:
        """Set trigger type and validate delay."""
        self.trigger_type = TriggerType.ONE_SHOT
        if self.delay_seconds < 0:
            raise ValueError(f"Delay must be non-negative, got: {self.delay_seconds}")

    def should_fire(self, now: datetime) -> bool:
        """Check if delay has elapsed and trigger hasn't fired yet.

        Args:
            now: The current UTC datetime.

        Returns:
            True if delay has elapsed and not yet fired, False otherwise.
        """
        if self.fired:
            return False

        elapsed = (now - self.created_at).total_seconds()
        return elapsed >= self.delay_seconds

    def mark_fired(self, now: datetime) -> None:
        """Mark that the trigger has fired.

        Args:
            now: The current UTC datetime.
        """
        self.fired = True

    def is_active(self) -> bool:
        """Check if trigger hasn't fired yet.

        Returns:
            True if not yet fired, False if already fired.
        """
        return not self.fired


class Scheduler:
    """Manages time-based triggers and executes their callbacks.

    Phase 4: Callbacks handle event emission - scheduler only manages timing.
    """

    def __init__(self) -> None:
        """Initialize an empty scheduler."""
        self._triggers: Dict[str, Trigger] = {}
        self._callbacks: Dict[str, Callable[[], None]] = {}
        self._lock = threading.Lock()
        self._running = False

    def register_trigger(
        self, trigger: Trigger, callback: Callable[[], None]
    ) -> str:
        """Register a trigger with a callback.

        Args:
            trigger: The trigger to register.
            callback: Function to call when trigger fires (no arguments).

        Returns:
            The trigger_id for later cancellation.
        """
        with self._lock:
            self._triggers[trigger.trigger_id] = trigger
            self._callbacks[trigger.trigger_id] = callback
            return trigger.trigger_id

    def cancel_trigger(self, trigger_id: str) -> None:
        """Cancel a registered trigger.

        Args:
            trigger_id: The ID of the trigger to cancel.
        """
        with self._lock:
            self._triggers.pop(trigger_id, None)
            self._callbacks.pop(trigger_id, None)

    def tick(self) -> None:
        """Evaluate all triggers and fire their callbacks if needed.

        Should be called periodically (e.g., every second) to check triggers.
        Thread-safe.

        Callbacks are executed outside the lock to avoid deadlocks if they
        attempt to register or cancel triggers.
        """
        now = datetime.now(timezone.utc)

        # Collect triggers that should fire and their callbacks while holding lock
        to_fire: list[tuple[str, Callable[[], None], Trigger]] = []
        with self._lock:
            for trigger_id, trigger in self._triggers.items():
                if trigger.is_active() and trigger.should_fire(now):
                    callback = self._callbacks.get(trigger_id)
                    if callback:
                        to_fire.append((trigger_id, callback, trigger))

        # Execute callbacks outside the lock to avoid deadlocks
        # (callbacks may attempt to register/cancel triggers)
        for trigger_id, callback, trigger in to_fire:
            try:
                callback()
            except Exception:
                # Phase 4: Basic error handling - log and continue
                pass

        # Reacquire lock to mark triggers and clean up one-shot triggers
        with self._lock:
            for trigger_id, callback, trigger in to_fire:
                trigger.mark_fired(now)

                # Remove one-shot triggers after firing
                if not trigger.is_active():
                    self._triggers.pop(trigger_id, None)
                    self._callbacks.pop(trigger_id, None)

    def get_active_triggers(self) -> list[Trigger]:
        """Get list of all active triggers.

        Returns:
            List of active trigger instances.
        """
        with self._lock:
            return [t for t in self._triggers.values() if t.is_active()]

