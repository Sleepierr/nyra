"""Memory indexing and retrieval for Phase 6.

Provides indexing, retrieval, and conservative semantic linking.

Per spec: subsystems/base1.0/subsystem_memory_experience.md
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import LTMMemoryEntry


class MemoryIndex:
    """Indexes and retrieves long-term memories.

    Per spec: subsystem_memory_experience.md
    Phase 6: Tag-based indexing, time-based indexing, conservative semantic linking.
    """

    def __init__(self) -> None:
        """Initialize empty memory index."""
        self._memories: Dict[str, LTMMemoryEntry] = {}
        self._tag_index: Dict[str, List[str]] = defaultdict(list)  # tag -> [memory_ids]
        self._time_index: List[str] = []  # Sorted list of memory_ids by timestamp
        self._type_index: Dict[str, List[str]] = defaultdict(list)  # type -> [memory_ids]

    def index_memory(self, memory: LTMMemoryEntry) -> None:
        """Index a memory entry.

        Args:
            memory: Long-term memory entry to index.
        """
        memory_id = memory.memory_id

        # Store memory
        self._memories[memory_id] = memory

        # Index by tags
        for tag in memory.experience_tags:
            if memory_id not in self._tag_index[tag]:
                self._tag_index[tag].append(memory_id)

        # Index by type
        if memory_id not in self._type_index[memory.type.value]:
            self._type_index[memory.type.value].append(memory_id)

        # Index by time (insert sorted)
        if memory_id not in self._time_index:
            self._time_index.append(memory_id)
            # Sort by timestamp (most recent first)
            self._time_index.sort(
                key=lambda mid: self._memories[mid].timestamp, reverse=True
            )

    def query_memories(
        self,
        query: Dict[str, Any],
        limit: Optional[int] = None,
    ) -> List[LTMMemoryEntry]:
        """Query memories using flexible query criteria.

        Args:
            query: Query dictionary with keys like:
                - tags: List of tags to match
                - type: MemoryType value
                - start_time: datetime start
                - end_time: datetime end
                - min_significance: float minimum significance
                - priority: MemoryPriority value
            limit: Optional maximum number of results.

        Returns:
            List of matching LTM entries.
        """
        candidates: Optional[List[str]] = None

        # Filter by tags
        if "tags" in query:
            tag_list = query["tags"]
            if isinstance(tag_list, str):
                tag_list = [tag_list]

            tag_matches = set()
            for tag in tag_list:
                if tag in self._tag_index:
                    tag_matches.update(self._tag_index[tag])

            if candidates is None:
                candidates = list(tag_matches)
            else:
                candidates = [mid for mid in candidates if mid in tag_matches]

        # Filter by type
        if "type" in query:
            mem_type = query["type"]
            type_matches = set(self._type_index.get(mem_type.value, []))

            if candidates is None:
                candidates = list(type_matches)
            else:
                candidates = [mid for mid in candidates if mid in type_matches]

        # If no filters, start with all memories
        if candidates is None:
            candidates = list(self._memories.keys())

        # Apply additional filters
        results: List[LTMMemoryEntry] = []

        for memory_id in candidates:
            memory = self._memories.get(memory_id)
            if not memory:
                continue

            # Time range filter
            if "start_time" in query or "end_time" in query:
                start_time = query.get("start_time")
                end_time = query.get("end_time")
                if start_time and memory.timestamp < start_time:
                    continue
                if end_time and memory.timestamp > end_time:
                    continue

            # Significance filter
            if "min_significance" in query:
                # Phase 6: Use impact_level as proxy for significance
                min_impact = query["min_significance"]
                if memory.impact_level < min_impact:
                    continue

            # Priority filter
            if "priority" in query:
                if memory.priority != query["priority"]:
                    continue

            results.append(memory)

        # Sort by timestamp (most recent first)
        results.sort(key=lambda m: m.timestamp, reverse=True)

        # Apply limit
        if limit is not None and limit > 0:
            results = results[:limit]

        return results

    def get_by_tags(self, tags: List[str], limit: Optional[int] = None) -> List[LTMMemoryEntry]:
        """Get memories by tags.

        Args:
            tags: List of tags to match.
            limit: Optional maximum number of results.

        Returns:
            List of matching LTM entries.
        """
        return self.query_memories({"tags": tags}, limit=limit)

    def get_by_type(
        self, memory_type: str, limit: Optional[int] = None
    ) -> List[LTMMemoryEntry]:
        """Get memories by type.

        Args:
            memory_type: Memory type string.
            limit: Optional maximum number of results.

        Returns:
            List of matching LTM entries.
        """
        return self.query_memories({"type": memory_type}, limit=limit)

    def get_recent(self, limit: int = 10) -> List[LTMMemoryEntry]:
        """Get most recent memories.

        Args:
            limit: Maximum number of results.

        Returns:
            List of most recent LTM entries.
        """
        results: List[LTMMemoryEntry] = []
        for memory_id in self._time_index[:limit]:
            memory = self._memories.get(memory_id)
            if memory:
                results.append(memory)
        return results

    def create_semantic_links(
        self, memory_id: str, max_links: int = 5
    ) -> List[str]:
        """Create conservative semantic links to related memories.

        Phase 6: Conservative semantic linking based on tag overlap and temporal proximity.

        Args:
            memory_id: Memory ID to create links for.
            max_links: Maximum number of links to create.

        Returns:
            List of related memory IDs.
        """
        memory = self._memories.get(memory_id)
        if not memory:
            return []

        # Find memories with overlapping tags
        related_memories: Dict[str, int] = {}  # memory_id -> overlap_score

        for tag in memory.experience_tags:
            for related_id in self._tag_index.get(tag, []):
                if related_id == memory_id:
                    continue

                # Calculate overlap score
                related_mem = self._memories.get(related_id)
                if not related_mem:
                    continue

                overlap = len(
                    set(memory.experience_tags) & set(related_mem.experience_tags)
                )
                if overlap > 0:
                    # Boost score for temporal proximity (within 24 hours)
                    time_diff = abs(
                        (memory.timestamp - related_mem.timestamp).total_seconds()
                    )
                    if time_diff < 86400:  # 24 hours
                        overlap += 1

                    related_memories[related_id] = (
                        related_memories.get(related_id, 0) + overlap
                    )

        # Sort by score and return top links
        sorted_links = sorted(
            related_memories.items(), key=lambda x: x[1], reverse=True
        )
        return [mem_id for mem_id, _ in sorted_links[:max_links]]

    def get_memory(self, memory_id: str) -> Optional[LTMMemoryEntry]:
        """Get memory by ID.

        Args:
            memory_id: Memory ID.

        Returns:
            LTM entry if found, None otherwise.
        """
        return self._memories.get(memory_id)

