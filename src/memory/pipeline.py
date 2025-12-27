"""Memory pipeline for Phase 6.

5-stage pipeline: CAPTURE → TAG → EVALUATE → CONSOLIDATE → INTEGRATE

Per spec: subsystems/base1.0/subsystem_memory_experience.md §7
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .consolidation import MemoryConsolidator
from .indexing import MemoryIndex
from .models import LTMMemoryEntry, MemoryObject, STMMemoryEntry

if TYPE_CHECKING:
    from ...state.container import StateContainer


class PipelineStage(str, Enum):
    """Memory pipeline stages."""

    CAPTURE = "capture"
    TAG = "tag"
    EVALUATE = "evaluate"
    CONSOLIDATE = "consolidate"
    INTEGRATE = "integrate"


class MemoryPipeline:
    """Executes 5-stage memory processing pipeline.

    Per spec: subsystem_memory_experience.md §7
    Stage 1: CAPTURE - Trigger detection, data collection
    Stage 2: TAG - Tag assignment
    Stage 3: EVALUATE - Significance scoring
    Stage 4: CONSOLIDATE - Normalization, structure conversion, safety checks
    Stage 5: INTEGRATE - Connection to Experience System, XP engine, learning system
    """

    def __init__(
        self,
        state_container: Optional["StateContainer"] = None,
        index: Optional[MemoryIndex] = None,
    ) -> None:
        """Initialize memory pipeline.

        Args:
            state_container: Optional state container for storage.
            index: Optional memory index for retrieval.
        """
        self._state_container = state_container
        self._consolidator = MemoryConsolidator(state_container)
        self._index = index or MemoryIndex()

    def process_stm_entry(
        self, stm_entry: STMMemoryEntry, dry_run: bool = False
    ) -> Optional[LTMMemoryEntry]:
        """Process STM entry through full pipeline.

        Args:
            stm_entry: Short-term memory entry to process.
            dry_run: If True, process through all stages but skip final persistence.

        Returns:
            Consolidated LTM entry if successful, None if discarded.
            In dry_run mode, returns processed entry without persisting to LTM.
        """
        # Stage 1: CAPTURE (already done - stm_entry is the captured data)

        # Stage 2: TAG
        tagged_entry = self._tag(stm_entry)

        # Stage 3: EVALUATE
        evaluated_entry = self._evaluate(tagged_entry)

        # If significance too low, discard
        if evaluated_entry.raw_payload.get("significance_score", 0.0) < 0.1:
            return None

        # Stage 4: CONSOLIDATE
        ltm_entry = self._consolidator.consolidate_stm_to_ltm(evaluated_entry)
        if not ltm_entry:
            return None

        # Stage 5: INTEGRATE (index the memory)
        # In dry_run mode, skip persistence
        if not dry_run:
            self._index.index_memory(ltm_entry)

        # Phase 6: Integration with Experience System will be handled by ExperienceIntegrator
        # Here we just complete the memory pipeline

        return ltm_entry

    def _tag(self, stm_entry: STMMemoryEntry) -> STMMemoryEntry:
        """Stage 2: TAG - Assign tags to memory entry.

        Per spec: subsystem_memory_experience.md §7.2
        Tags: emotional, thematic, relational, narrative, priority, drift-sensitivity

        Args:
            stm_entry: STM entry to tag.

        Returns:
            Tagged STM entry (tags added to raw_payload).
        """
        tags = stm_entry.raw_payload.get("tags", [])

        # Extract emotional tags
        if stm_entry.emotional_hint:
            tags.append("emotional")
            # Add specific emotional tags if present
            for key in stm_entry.emotional_hint.keys():
                if key not in tags:
                    tags.append(f"emotional_{key}")

        # Extract thematic tags from event type
        event_type = stm_entry.raw_payload.get("event_type", "").lower()
        if "goal" in event_type:
            tags.append("goal")
        if "debate" in event_type:
            tags.append("debate")
        if "interaction" in event_type:
            tags.append("interaction")

        # Relational tags (check for Slepp mentions)
        content = str(stm_entry.raw_payload.get("content_summary", "")).lower()
        if "slepp" in content:
            tags.append("relational")
            tags.append("slepp")

        # Narrative tags (basic - full narrative tagging deferred)
        significance = stm_entry.raw_payload.get("significance_score", 0.0)
        if significance > 0.7:
            tags.append("narrative_significant")

        # Priority tags
        if significance > 0.8:
            tags.append("priority_high")
        elif significance > 0.5:
            tags.append("priority_medium")
        else:
            tags.append("priority_low")

        # Drift-sensitivity tags (basic)
        if stm_entry.raw_payload.get("identity_relevance_score", 0.0) > 0.5:
            tags.append("drift_sensitive")

        # Update payload with tags
        stm_entry.raw_payload["tags"] = list(set(tags))  # Remove duplicates

        return stm_entry

    def _evaluate(self, stm_entry: STMMemoryEntry) -> STMMemoryEntry:
        """Stage 3: EVALUATE - Score memory significance.

        Per spec: subsystem_memory_experience.md §7.3
        Evaluation vectors:
        - Emotional significance
        - Cognitive significance
        - Learning potential
        - Narrative impact
        - Identity relevance
        - Autonomy modulation impact
        - Stability impact

        Args:
            stm_entry: Tagged STM entry to evaluate.

        Returns:
            Evaluated STM entry (significance scores updated).
        """
        # Phase 6: Basic significance evaluation
        # Full multi-vector evaluation deferred to later phases

        # Calculate emotional significance
        emotional_significance = 0.0
        if stm_entry.emotional_hint:
            emotional_magnitude = self._calculate_emotional_magnitude(
                stm_entry.emotional_hint
            )
            emotional_significance = emotional_magnitude

        # Calculate cognitive significance (basic heuristic)
        cognitive_trace = stm_entry.raw_payload.get("cognitive_trace", {})
        cognitive_significance = 0.3  # Default moderate
        if cognitive_trace:
            # More complex trace = higher significance
            cognitive_significance = min(1.0, len(str(cognitive_trace)) / 1000.0)

        # Calculate identity relevance (if provided)
        identity_relevance = stm_entry.raw_payload.get("identity_relevance_score", 0.0)

        # Aggregate significance score
        significance = (
            emotional_significance * 0.4
            + cognitive_significance * 0.3
            + identity_relevance * 0.3
        )
        significance = max(0.0, min(1.0, significance))

        # Update payload with scores
        stm_entry.raw_payload["significance_score"] = significance
        stm_entry.raw_payload["emotional_significance"] = emotional_significance
        stm_entry.raw_payload["cognitive_significance"] = cognitive_significance
        stm_entry.raw_payload["identity_relevance_score"] = identity_relevance

        return stm_entry

    def _calculate_emotional_magnitude(self, emotional_vector: Dict[str, Any]) -> float:
        """Calculate magnitude of emotional vector.

        Args:
            emotional_vector: Emotional vector.

        Returns:
            Magnitude as float [0.0, 1.0].
        """
        if not emotional_vector:
            return 0.0

        values = [v for v in emotional_vector.values() if isinstance(v, (int, float))]
        if not values:
            return 0.0

        # Calculate L2 norm (normalized)
        sum_sq = sum(v * v for v in values)
        magnitude = (sum_sq / len(values)) ** 0.5
        return min(1.0, magnitude)

    @property
    def index(self) -> MemoryIndex:
        """Return the memory index."""
        return self._index





