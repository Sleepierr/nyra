"""Session manager for gate runtime sessions."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .models import SessionMetadata


class SessionManager:
    """Manages runtime session lifecycle and JSONL file creation."""

    def __init__(self, sessions_dir: Path):
        """Initialize session manager.

        Args:
            sessions_dir: Directory for session JSONL files.
        """
        self._sessions_dir = sessions_dir
        self._sessions_dir.mkdir(parents=True, exist_ok=True)
        self._current_session: Optional[SessionMetadata] = None
        self._current_log_file: Optional[Path] = None

    def start_session(self) -> SessionMetadata:
        """Start a new session.

        Returns:
            SessionMetadata for the new session.
        """
        session_id = str(uuid.uuid4())
        start_timestamp = datetime.now(timezone.utc).isoformat()

        # Create timestamped filename: YYYYMMDD-HHMMSS-<uuid>.jsonl
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp_str}-{session_id[:8]}.jsonl"
        log_file = self._sessions_dir / filename

        self._current_session = SessionMetadata(
            session_id=session_id,
            start_timestamp=start_timestamp,
            event_count=0,
            memory_candidate_count=0,
        )
        self._current_log_file = log_file

        # Update latest.jsonl symlink/copy
        latest_link = self._sessions_dir / "latest.jsonl"
        if latest_link.exists():
            latest_link.unlink()
        try:
            latest_link.symlink_to(log_file.name)
        except OSError:
            # If symlink fails (e.g., on Windows), copy the file
            if log_file.exists():
                import shutil

                shutil.copy2(log_file, latest_link)

        return self._current_session

    def end_session(self) -> None:
        """End the current session."""
        if self._current_session:
            self._current_session.end_timestamp = datetime.now(
                timezone.utc
            ).isoformat()
        self._current_session = None
        self._current_log_file = None

    def get_current_log_file(self) -> Optional[Path]:
        """Get the current session log file path.

        Returns:
            Path to current log file, or None if no active session.
        """
        return self._current_log_file

    def get_current_session(self) -> Optional[SessionMetadata]:
        """Get the current session metadata.

        Returns:
            Current SessionMetadata, or None if no active session.
        """
        return self._current_session

    def increment_event_count(self) -> None:
        """Increment event count for current session."""
        if self._current_session:
            self._current_session.event_count += 1

    def increment_candidate_count(self) -> None:
        """Increment memory candidate count for current session."""
        if self._current_session:
            self._current_session.memory_candidate_count += 1

