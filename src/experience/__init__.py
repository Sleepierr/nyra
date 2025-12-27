"""Experience system for Phase 6.

Provides experience processing and integration infrastructure.
"""

from .integration import ExperienceIntegrator
from .models import ExperienceImpactLevel, ExperienceObject, XPUpdate
from .processor import ExperienceProcessor

__all__ = [
    "ExperienceObject",
    "ExperienceImpactLevel",
    "XPUpdate",
    "ExperienceProcessor",
    "ExperienceIntegrator",
]





