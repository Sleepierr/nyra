"""CLI command handler for gate persistence system."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from ..memory.pipeline import MemoryPipeline
from .candidate_tracker import CandidateTracker
from .models import SessionSummary
from .session_manager import SessionManager


class CLIHandler:
    """Handles chat commands for gate persistence system."""

    def __init__(
        self,
        session_manager: SessionManager,
        candidate_tracker: CandidateTracker,
        memory_pipeline: Optional[MemoryPipeline] = None,
    ):
        """Initialize CLI handler.

        Args:
            session_manager: SessionManager for session metadata.
            candidate_tracker: CandidateTracker for memory candidates.
            memory_pipeline: Optional MemoryPipeline for promotion.
        """
        self._session_manager = session_manager
        self._candidate_tracker = candidate_tracker
        self._memory_pipeline = memory_pipeline

    def handle_command(self, command: str) -> Optional[str]:
        """Handle a chat command.

        Args:
            command: Command string (e.g., "/save-summary", "/promote-last 5").

        Returns:
            Response message if command was handled, None otherwise.
        """
        command = command.strip()

        if command == "/save-summary":
            return self._save_summary()

        if command.startswith("/promote-last"):
            parts = command.split()
            n = int(parts[1]) if len(parts) > 1 else 1
            return self._promote_last(n)

        return None

    def _save_summary(self) -> str:
        """Generate and save session summary.

        Returns:
            Success message.
        """
        session = self._session_manager.get_current_session()
        if not session:
            return "No active session to summarize."

        # Build event summary (simplified - would need to read from log file)
        event_summary: Dict[str, Any] = {
            "total_events": session.event_count,
            "session_duration_seconds": None,  # Would calculate from timestamps
        }

        # Get memory candidates
        memory_candidates = self._candidate_tracker.get_candidates()

        # Create summary
        summary = SessionSummary(
            session_metadata=session,
            event_summary=event_summary,
            memory_candidates=memory_candidates,
        )

        # Save to file
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        summary_file = Path("data") / f"session_summary_{timestamp_str}.json"

        summary_file.parent.mkdir(parents=True, exist_ok=True)
        with open(summary_file, "w", encoding="utf-8") as f:
            # Support both Pydantic v1 and v2
            if hasattr(summary, "model_dump"):
                data = summary.model_dump()
            else:
                data = summary.dict()
            json.dump(data, f, indent=2)

        return f"Summary saved to {summary_file}"

    def _promote_last(self, n: int) -> str:
        """Promote last N memory candidates.

        Args:
            n: Number of candidates to promote.

        Returns:
            Success message.
        """
        if not self._memory_pipeline:
            return "Memory pipeline not available for promotion."

        promoted_count = self._candidate_tracker.promote_last_n(n, self._memory_pipeline)

        return f"Promoted {promoted_count} of {n} candidates to long-term memory."

