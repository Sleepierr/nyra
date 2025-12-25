"""Identity continuity for Phase 6.

Provides identity version tracking, self-history, dynamic trait management, and era management.
"""

from .continuity import IdentityContinuityManager
from .era_manager import EraManager, IdentityEra
from .self_history import SelfHistoryEntry, SelfHistoryLog
from .trait_drift import DynamicTraitManager

__all__ = [
    "IdentityContinuityManager",
    "SelfHistoryLog",
    "SelfHistoryEntry",
    "DynamicTraitManager",
    "EraManager",
    "IdentityEra",
]

