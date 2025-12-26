"""Memory compression for Phase 6.

Batch/scheduled memory compression with identity-safe rules.

Per spec: subsystems/patches/base1.0/memory_compression_patch.md
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .models import LTMMemoryEntry, MemoryPriority


@dataclass
class CompressionResult:
    """Result of memory compression operation."""

    memories_compressed: int
    memories_preserved: int
    compression_ratio: float
    preserved_memory_ids: List[str]
    compressed_memory_ids: List[str]


class MemoryCompressor:
    """Compresses old memories using identity-safe rules.

    Per spec: memory_compression_patch.md
    Phase 6: Batch/scheduled compression with preservation rules.
    """

    def compress_old_memories(
        self,
        memories: List[LTMMemoryEntry],
        threshold_date: datetime,
        preservation_rules: Optional[Dict[str, any]] = None,
    ) -> CompressionResult:
        """Compress memories older than threshold date.

        Per spec: memory_compression_patch.md
        Preservation rules:
        - Slepp-related memories (never compressed)
        - Identity-defining memories (never compressed)
        - Emotionally significant experiences (never compressed)
        - Covenant-relevant information (never compressed)

        Args:
            memories: List of LTM entries to consider for compression.
            threshold_date: Memories older than this date are candidates.
            preservation_rules: Optional custom preservation rules.

        Returns:
            CompressionResult with statistics.
        """
        if preservation_rules is None:
            preservation_rules = {}

        preserved_ids: List[str] = []
        compressed_ids: List[str] = []

        for memory in memories:
            # Skip memories newer than threshold
            if memory.timestamp >= threshold_date:
                preserved_ids.append(memory.memory_id)
                continue

            # Check preservation rules
            if self._should_preserve(memory, preservation_rules):
                preserved_ids.append(memory.memory_id)
            else:
                compressed_ids.append(memory.memory_id)

        # Calculate compression ratio
        total = len(memories)
        compressed_count = len(compressed_ids)
        preserved_count = len(preserved_ids)
        compression_ratio = compressed_count / total if total > 0 else 0.0

        return CompressionResult(
            memories_compressed=compressed_count,
            memories_preserved=preserved_count,
            compression_ratio=compression_ratio,
            preserved_memory_ids=preserved_ids,
            compressed_memory_ids=compressed_ids,
        )

    def _should_preserve(
        self, memory: LTMMemoryEntry, preservation_rules: Dict[str, any]
    ) -> bool:
        """Check if memory should be preserved based on rules.

        Per spec: memory_compression_patch.md
        Never compress:
        - Slepp-related memories
        - Identity-defining memories
        - Emotionally significant experiences
        - Covenant-relevant information

        Args:
            memory: Memory entry to check.
            preservation_rules: Preservation rule configuration.

        Returns:
            True if memory should be preserved, False if can be compressed.
        """
        # Check for Slepp-related tags
        slepp_tags = ["slepp", "relational", "covenant"]
        if any(tag.lower() in " ".join(memory.experience_tags).lower() for tag in slepp_tags):
            return True

        # Check for identity-defining memories (high identity relevance)
        if memory.impact_level >= 5:  # Identity-relevant
            return True

        # Check for emotionally significant experiences (high priority)
        if memory.priority == MemoryPriority.CRITICAL:
            return True

        # Check for covenant-relevant information (metadata flag)
        if memory.metadata.get("covenant_relevant", False):
            return True

        # Check for high emotional significance
        emotional_magnitude = self._calculate_emotional_magnitude(
            memory.emotional_signature_vector
        )
        if emotional_magnitude > 0.8:
            return True

        # Apply custom preservation rules
        if preservation_rules.get("preserve_all_important", False):
            if memory.priority == MemoryPriority.IMPORTANT:
                return True

        return False

    def _calculate_emotional_magnitude(self, emotional_vector: Dict[str, any]) -> float:
        """Calculate magnitude of emotional vector.

        Args:
            emotional_vector: Emotional signature vector.

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

    def compress_memory_batch(
        self,
        memories: List[LTMMemoryEntry],
        compression_strategy: str = "conservative",
    ) -> Dict[str, LTMMemoryEntry]:
        """Compress a batch of memories using specified strategy.

        Phase 6: Basic compression - marks memories for compression.
        Full compression logic (redundancy removal, semantic clustering) deferred.

        Args:
            memories: List of memories to compress.
            compression_strategy: Compression strategy ("conservative", "aggressive").

        Returns:
            Dictionary mapping original memory_id to compressed memory entry.
        """
        compressed: Dict[str, LTMMemoryEntry] = {}

        # Phase 6: Basic compression - create simplified versions
        # Full compression (redundancy removal, clustering) deferred to later phases
        for memory in memories:
            # Create compressed version (simplified summary)
            compressed_memory = LTMMemoryEntry(
                memory_id=memory.memory_id,
                timestamp=memory.timestamp,
                type=memory.type,
                content_summary=f"[Compressed] {memory.content_summary[:100]}",
                emotional_signature_vector={},  # Compressed - remove detailed vector
                symbolic_links=memory.symbolic_links,
                experience_tags=memory.experience_tags,
                xp_yield=memory.xp_yield,
                impact_level=memory.impact_level,
                priority=memory.priority,
                source_subsystem=memory.source_subsystem,
                metadata={"compressed": True, "original_metadata": memory.metadata},
            )
            compressed[memory.memory_id] = compressed_memory

        return compressed



