"""Data models for gate persistence system."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class GateState(BaseModel):
    """Gate state persisted to data/gate_state.json."""

    last_session_id: str
    last_event_id: str
    safe_mode: bool = True
    latest_log_path: Optional[str] = None


class SessionMetadata(BaseModel):
    """Metadata for a runtime session."""

    session_id: str
    start_timestamp: str
    end_timestamp: Optional[str] = None
    event_count: int = 0
    memory_candidate_count: int = 0


class SessionSummary(BaseModel):
    """Complete session summary for /save-summary command."""

    session_metadata: SessionMetadata
    event_summary: Dict[str, Any]  # Event type counts, key events
    memory_candidates: List[Dict[str, Any]]  # Candidate summaries

