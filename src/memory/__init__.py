"""Memory consolidation system for Phase 6.

Provides memory consolidation, indexing, compression, and pipeline infrastructure.
"""

from .compression import CompressionResult, MemoryCompressor
from .consolidation import MemoryConsolidator
from .indexing import MemoryIndex
from .models import (
    LTMMemoryEntry,
    MemoryObject,
    MemoryPriority,
    MemoryType,
    STMMemoryEntry,
)
from .pipeline import MemoryPipeline, PipelineStage

__all__ = [
    # Models
    "MemoryObject",
    "STMMemoryEntry",
    "LTMMemoryEntry",
    "MemoryType",
    "MemoryPriority",
    # Consolidation
    "MemoryConsolidator",
    # Indexing
    "MemoryIndex",
    # Compression
    "MemoryCompressor",
    "CompressionResult",
    # Pipeline
    "MemoryPipeline",
    "PipelineStage",
]



