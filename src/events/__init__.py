"""Phase 4 Event & Time Flow infrastructure.

This package provides event emission, queues, cursor management, scheduling,
and routing infrastructure. Phase 4 introduces "movement" without "interpretation".
"""

from .cursor import CursorCodec, CursorManager
from .emission import EventEmitter, EventFactory
from .queue import EventQueue
from .routing import EventBus
from .scheduler import (
    IntervalTrigger,
    OneShotTrigger,
    Scheduler,
    TimeOfDayTrigger,
    Trigger,
    TriggerType,
)

__all__ = [
    # Emission
    "EventFactory",
    "EventEmitter",
    # Queue
    "EventQueue",
    # Cursor
    "CursorCodec",
    "CursorManager",
    # Scheduling
    "Trigger",
    "TriggerType",
    "IntervalTrigger",
    "TimeOfDayTrigger",
    "OneShotTrigger",
    "Scheduler",
    # Routing
    "EventBus",
]




