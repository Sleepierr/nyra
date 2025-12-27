"""Memory consolidation for Phase 6.

Converts STM entries to LTM entries with normalization and safety checks.

Per spec: subsystems/base1.0/subsystem_memory_experience.md §7.4
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .models import LTMMemoryEntry, MemoryObject, MemoryPriority, MemoryType, STMMemoryEntry

if TYPE_CHECKING:
    from ...state.container import StateContainer


class MemoryConsolidator:
    """Consolidates STM entries into structured LTM entries.

    Per spec: subsystem_memory_experience.md §7.4
    Phase 6: STM → LTM conversion with normalization and safety checks.
    """

    def __init__(self, state_container: Optional["StateContainer"] = None) -> None:
        """Initialize the consolidator.

        Args:
            state_container: Optional state container for LTM storage.
        """
        self._state_container = state_container

    def consolidate_stm_to_ltm(self, stm_entry: STMMemoryEntry) -> Optional[LTMMemoryEntry]:
        """Consolidate STM entry to LTM entry.

        Performs normalization, safety checks, and structure conversion.

        Args:
            stm_entry: Short-term memory entry to consolidate.

        Returns:
            Long-term memory entry if consolidation succeeds, None if fails safety checks.
        """
        # Normalize emotional vector
        emotional_vector = self.normalize_emotional_vector(
            stm_entry.emotional_hint or {}
        )

        # Create memory object for safety checks
        memory_object = MemoryObject(
            memory_id=stm_entry.memory_id,
            timestamp_created=stm_entry.timestamp,
            event_type=stm_entry.raw_payload.get("event_type", "unknown"),
            emotional_vector=emotional_vector,
            cognitive_trace=stm_entry.raw_payload.get("cognitive_trace", {}),
            significance_score=stm_entry.raw_payload.get("significance_score", 0.5),
            identity_relevance_score=stm_entry.raw_payload.get("identity_relevance_score", 0.0),
            experience_links=[],
            narrative_tags=[],
            autonomy_band_origin=stm_entry.raw_payload.get("autonomy_band_origin", 0),
            context_metadata=stm_entry.raw_payload.get("context_metadata", {}),
            safety_flags=[],
        )

        # Apply safety checks
        if not self.apply_safety_checks(memory_object):
            return None

        # Determine memory type from raw payload
        memory_type = self._determine_memory_type(stm_entry.raw_payload)

        # Create LTM entry
        ltm_entry = LTMMemoryEntry(
            memory_id=memory_object.memory_id,
            timestamp=memory_object.timestamp_created,
            type=memory_type,
            content_summary=self._create_content_summary(stm_entry.raw_payload),
            emotional_signature_vector=emotional_vector,
            symbolic_links=[],  # Phase 6: No symbolic links (Band ≥ 8 only)
            experience_tags=[],
            xp_yield=0.0,  # Will be calculated later by Experience System
            impact_level=self._calculate_impact_level(memory_object),
            priority=self._determine_priority(memory_object),
            source_subsystem=stm_entry.raw_payload.get("source_subsystem", ""),
            metadata=stm_entry.raw_payload.get("metadata", {}),
        )

        return ltm_entry

    def normalize_emotional_vector(self, raw_vector: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize emotional vector.

        Phase 6: Basic normalization - ensure values are within valid ranges.

        Args:
            raw_vector: Raw emotional vector from STM.

        Returns:
            Normalized emotional vector.
        """
        normalized = {}

        # Phase 6: Basic normalization - clamp values to [-1.0, 1.0] range
        # Full emotional normalization deferred to Emotional Engine integration
        for key, value in raw_vector.items():
            if isinstance(value, (int, float)):
                normalized[key] = max(-1.0, min(1.0, float(value)))
            else:
                normalized[key] = value

        return normalized

    def apply_safety_checks(self, memory: MemoryObject) -> bool:
        """Apply safety checks to memory object.

        Per spec: subsystem_memory_experience.md §6, §7.4
        Enforces:
        - No identity contamination
        - No circular emotional reinforcement
        - No symbolic drift (Phase 6: not applicable, symbolic integration deferred)

        Args:
            memory: Memory object to check.

        Returns:
            True if memory passes safety checks, False otherwise.
        """
        # Check for identity contamination
        # Phase 6: Identity relevance score > threshold requires debate review (not enforced here)
        if memory.identity_relevance_score > 0.8:
            # High identity relevance - flag for debate review
            memory.safety_flags.append("high_identity_relevance")

        # Check for forbidden fields (identity mutation instructions, symbolic fusion)
        if "identity_mutation" in memory.context_metadata:
            return False

        if "symbolic_fusion" in memory.context_metadata:
            return False

        # Check for excessive emotional resonance (threshold: > 0.95)
        emotional_magnitude = self._calculate_emotional_magnitude(memory.emotional_vector)
        if emotional_magnitude > 0.95:
            memory.safety_flags.append("high_emotional_resonance")
            # Phase 6: Still allow, but flag for review

        return True

    def _calculate_emotional_magnitude(self, emotional_vector: Dict[str, Any]) -> float:
        """Calculate magnitude of emotional vector.

        Args:
            emotional_vector: Emotional vector.

        Returns:
            Magnitude as float [0.0, 1.0+].
        """
        if not emotional_vector:
            return 0.0

        # Phase 6: Simple magnitude calculation
        values = [v for v in emotional_vector.values() if isinstance(v, (int, float))]
        if not values:
            return 0.0

        # Calculate L2 norm (normalized)
        sum_sq = sum(v * v for v in values)
        magnitude = (sum_sq / len(values)) ** 0.5
        return min(1.0, magnitude)

    def _determine_memory_type(self, raw_payload: Dict[str, Any]) -> MemoryType:
        """Determine memory type from raw payload.

        Args:
            raw_payload: Raw payload from STM entry.

        Returns:
            MemoryType enum value.
        """
        event_type = raw_payload.get("event_type", "unknown").lower()

        type_mapping = {
            "conversation": MemoryType.CONVERSATION,
            "reflection": MemoryType.REFLECTION,
            "skill": MemoryType.SKILL_TRACE,
            "task": MemoryType.TASK_TRACE,
            "emotional": MemoryType.EMOTIONAL_TRACE,
            "system": MemoryType.SYSTEM_STATE,
        }

        for key, mem_type in type_mapping.items():
            if key in event_type:
                return mem_type

        return MemoryType.EVENT  # Default

    def _create_content_summary(self, raw_payload: Dict[str, Any]) -> str:
        """Create content summary from raw payload.

        Args:
            raw_payload: Raw payload from STM entry.

        Returns:
            Content summary string.
        """
        # Phase 6: Basic summary extraction
        if "content_summary" in raw_payload:
            return str(raw_payload["content_summary"])[:500]  # Limit length

        if "description" in raw_payload:
            return str(raw_payload["description"])[:500]

        return f"Memory entry: {raw_payload.get('event_type', 'unknown')}"

    def _calculate_impact_level(self, memory: MemoryObject) -> int:
        """Calculate experience impact level.

        Per spec: subsystem_memory_experience.md §X.1
        Impact levels: 0 (negligible) to 5 (identity-relevant)

        Args:
            memory: Memory object.

        Returns:
            Impact level 0-5.
        """
        # Phase 6: Basic impact calculation
        significance = memory.significance_score
        identity_relevance = memory.identity_relevance_score

        if identity_relevance > 0.8:
            return 5  # Identity-relevant
        elif significance > 0.8:
            return 4  # High significance
        elif significance > 0.6:
            return 3  # Meaningful
        elif significance > 0.4:
            return 2  # Moderate
        elif significance > 0.2:
            return 1  # Low
        else:
            return 0  # Negligible

    def _determine_priority(self, memory: MemoryObject) -> MemoryPriority:
        """Determine memory priority.

        Args:
            memory: Memory object.

        Returns:
            MemoryPriority enum value.
        """
        impact_level = self._calculate_impact_level(memory)

        if impact_level >= 4:
            return MemoryPriority.CRITICAL
        elif impact_level >= 2:
            return MemoryPriority.IMPORTANT
        else:
            return MemoryPriority.NORMAL





