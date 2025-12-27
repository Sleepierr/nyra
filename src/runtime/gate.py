"""Main Gate class for Temporary Gate v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from ..memory.pipeline import MemoryPipeline
from .governance_loader import (
    GovernanceLoadError,
    GovernanceSnapshot,
    load_governance,
)
from ..gate.candidate_tracker import CandidateTracker
from ..gate.cli_handler import CLIHandler
from ..gate.event_logger import EventLogger
from ..gate.models import GateState
from ..gate.session_manager import SessionManager
from ..gate.state_manager import StateManager
from ..state.models.event_envelope import EventEnvelope


class Gate:
    """Temporary Gate v1 - Safe persistence and governance loading."""

    def __init__(
        self,
        repo_root: Path,
        persist: bool = True,
        promote_memory: bool = False,
        memory_pipeline: Optional["MemoryPipeline"] = None,
    ):
        """Initialize Gate.

        Args:
            repo_root: Path to repository root.
            persist: Enable event logging (default: True).
            promote_memory: Enable memory promotion (default: False).
            memory_pipeline: Optional MemoryPipeline for candidate processing.
        """
        self._repo_root = repo_root
        self._persist = persist
        self._promote_memory = promote_memory
        self._memory_pipeline = memory_pipeline

        # Governance snapshot (loaded during start)
        self._governance_snapshot: Optional[GovernanceSnapshot] = None

        # Gate components
        self._state_manager = StateManager(repo_root / "data" / "gate_state.json")
        self._session_manager = SessionManager(repo_root / "logs" / "runtime_sessions")
        self._event_logger = EventLogger(self._session_manager)
        self._candidate_tracker = CandidateTracker(
            self._session_manager, memory_pipeline, promote_memory
        )
        self._cli_handler = CLIHandler(
            self._session_manager, self._candidate_tracker, memory_pipeline
        )

        # Gate state
        self._started = False

    def start(self) -> None:
        """Start the gate (HARD-REQUIRED: governance must load first).

        Raises:
            GovernanceLoadError: If governance loading fails (gate refuses to start).
        """
        # HARD-REQUIRED: Load governance FIRST
        try:
            self._governance_snapshot = load_governance(self._repo_root)
        except GovernanceLoadError as e:
            print("GOVERNANCE LOAD FAILED", file=__import__("sys").stderr)
            print(str(e), file=__import__("sys").stderr)
            raise

        # Load or initialize gate state
        gate_state = self._state_manager.load()
        if not gate_state:
            # Initialize new state
            gate_state = GateState(
                last_session_id="",
                last_event_id="",
                safe_mode=True,
            )
            self._state_manager.save(gate_state)

        # Start session if persistence is enabled
        if self._persist:
            session = self._session_manager.start_session()
            gate_state.last_session_id = session.session_id
            self._state_manager.save(gate_state)

        self._started = True

    def status(self) -> Dict[str, Any]:
        """Get gate status including governance metadata.

        Returns:
            Dictionary with gate status information.
        """
        session = self._session_manager.get_current_session()
        gate_state = self._state_manager.load()

        status: Dict[str, Any] = {
            "started": self._started,
            "persist": self._persist,
            "promote_memory": self._promote_memory,
        }

        # Governance status
        if self._governance_snapshot:
            status["governance_loaded"] = True
            status["governance_overall_sha256"] = self._governance_snapshot.overall_sha256
            status["governance_loaded_at"] = self._governance_snapshot.loaded_at
            status["patches_count"] = self._governance_snapshot.patches.count
        else:
            status["governance_loaded"] = False
            status["governance_overall_sha256"] = None
            status["governance_loaded_at"] = None
            status["patches_count"] = None

        # Session status
        if session:
            status["current_session_id"] = session.session_id
            status["session_event_count"] = session.event_count
            status["session_candidate_count"] = session.memory_candidate_count
        else:
            status["current_session_id"] = None
            status["session_event_count"] = 0
            status["session_candidate_count"] = 0

        # Gate state
        if gate_state:
            status["last_session_id"] = gate_state.last_session_id
            status["last_event_id"] = gate_state.last_event_id
            status["safe_mode"] = gate_state.safe_mode

        return status

    def log_event(self, event: EventEnvelope) -> None:
        """Log an event (if persistence is enabled).

        Args:
            event: EventEnvelope to log.
        """
        if not self._started:
            return

        if self._persist:
            self._event_logger.log_event(event)

        # Update gate state
        gate_state = self._state_manager.load()
        if gate_state:
            gate_state.last_event_id = event.event_id
            self._state_manager.save(gate_state)

    def process_memory_candidate(self, stm_entry) -> Optional[Dict[str, Any]]:
        """Process a memory candidate.

        Args:
            stm_entry: STMMemoryEntry to process.

        Returns:
            Candidate data if processed, None otherwise.
        """
        if not self._started:
            return None

        return self._candidate_tracker.process_candidate(stm_entry)

    def handle_command(self, command: str) -> Optional[str]:
        """Handle a chat command.

        Args:
            command: Command string.

        Returns:
            Response message if command was handled, None otherwise.
        """
        if not self._started:
            return None

        return self._cli_handler.handle_command(command)

    def shutdown(self) -> None:
        """Shutdown the gate and end current session."""
        if self._started and self._persist:
            self._session_manager.end_session()
        self._started = False

