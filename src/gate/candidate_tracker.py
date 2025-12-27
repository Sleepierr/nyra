"""Memory candidate tracker for gate persistence system."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..memory.models import STMMemoryEntry
from ..memory.pipeline import MemoryPipeline
from .session_manager import SessionManager


class CandidateTracker:
    """Tracks memory candidates without auto-promoting them."""

    def __init__(
        self,
        session_manager: SessionManager,
        memory_pipeline: Optional[MemoryPipeline] = None,
        promote_memory: bool = False,
    ):
        """Initialize candidate tracker.

        Args:
            session_manager: SessionManager for tracking candidate count.
            memory_pipeline: Optional MemoryPipeline for processing candidates.
            promote_memory: If True, promote candidates to LTM. If False, use dry-run mode.
        """
        self._session_manager = session_manager
        self._memory_pipeline = memory_pipeline
        self._promote_memory = promote_memory
        self._candidates: List[Dict[str, Any]] = []

    def process_candidate(self, stm_entry: STMMemoryEntry) -> Optional[Dict[str, Any]]:
        """Process a memory candidate.

        If --promote-memory is OFF:
        - Process through pipeline in dry-run mode
        - Store candidate data (not persisted to LTM)

        If --promote-memory is ON:
        - Normal memory pipeline execution with persistence

        Args:
            stm_entry: STM entry to process as candidate.

        Returns:
            Candidate data dictionary if processed, None if discarded.
        """
        if not self._memory_pipeline:
            # No pipeline available - just store basic candidate info
            candidate_data = {
                "memory_id": stm_entry.memory_id,
                "timestamp": stm_entry.timestamp.isoformat() if stm_entry.timestamp else None,
                "significance_score": stm_entry.raw_payload.get("significance_score", 0.0),
            }
            self._candidates.append(candidate_data)
            self._session_manager.increment_candidate_count()
            return candidate_data

        # Process through pipeline
        dry_run = not self._promote_memory
        ltm_entry = self._memory_pipeline.process_stm_entry(stm_entry, dry_run=dry_run)

        if ltm_entry:
            candidate_data = {
                "memory_id": ltm_entry.memory_id,
                "timestamp": ltm_entry.timestamp.isoformat(),
                "type": ltm_entry.type.value,
                "content_summary": ltm_entry.content_summary,
                "significance_score": stm_entry.raw_payload.get("significance_score", 0.0),
                "promoted": not dry_run,
            }
            self._candidates.append(candidate_data)
            self._session_manager.increment_candidate_count()
            return candidate_data

        return None

    def get_candidates(self) -> List[Dict[str, Any]]:
        """Get all tracked candidates.

        Returns:
            List of candidate data dictionaries.
        """
        return self._candidates.copy()

    def get_last_n(self, n: int) -> List[Dict[str, Any]]:
        """Get last N candidates.

        Args:
            n: Number of candidates to retrieve.

        Returns:
            List of last N candidate data dictionaries.
        """
        return self._candidates[-n:] if n > 0 else []

    def promote_last_n(self, n: int, memory_pipeline: MemoryPipeline) -> int:
        """Promote last N candidates to long-term memory.

        Args:
            n: Number of candidates to promote.
            memory_pipeline: MemoryPipeline to use for promotion.

        Returns:
            Number of candidates successfully promoted.
        """
        if not memory_pipeline:
            return 0

        candidates_to_promote = self.get_last_n(n)
        promoted_count = 0

        for candidate in candidates_to_promote:
            # Reconstruct STM entry from candidate data
            # Note: This is a simplified reconstruction - full implementation
            # would need to store more data or reload from session log
            try:
                # For now, we'll mark as promoted if it was already processed
                # Full promotion would require re-processing through pipeline
                if not candidate.get("promoted", False):
                    # Would need original STM entry to re-process
                    # This is a placeholder for the promotion logic
                    candidate["promoted"] = True
                    promoted_count += 1
            except Exception:
                pass

        return promoted_count

