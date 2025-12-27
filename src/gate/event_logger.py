"""Event logger for gate persistence system."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Optional

from ..state.models.event_envelope import EventEnvelope
from .session_manager import SessionManager


class EventLogger:
    """Thread-safe event logger that writes EventEnvelope instances as JSONL."""

    def __init__(self, session_manager: SessionManager):
        """Initialize event logger.

        Args:
            session_manager: SessionManager for getting current log file.
        """
        self._session_manager = session_manager
        self._lock = threading.Lock()

    def log_event(self, event: EventEnvelope) -> None:
        """Log an event to the current session JSONL file.

        Args:
            event: EventEnvelope to log.
        """
        log_file = self._session_manager.get_current_log_file()
        if not log_file:
            return

        # Serialize event to JSON
        # Support both Pydantic v1 and v2
        if hasattr(event, "model_dump"):
            event_dict = event.model_dump()
        else:
            event_dict = event.dict()

        # Write as JSONL (one JSON object per line)
        with self._lock:
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    json.dump(event_dict, f, ensure_ascii=False)
                    f.write("\n")
                self._session_manager.increment_event_count()
            except Exception:
                # Log error but don't crash
                pass

