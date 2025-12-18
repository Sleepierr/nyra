"""Cursor model per spec/base1.0/nyrahome_cloud_spec.md §2."""
from __future__ import annotations

from pydantic import BaseModel, constr


class Cursor(BaseModel):
    """Opaque cursor token for event synchronization."""

    __root__: constr(regex=r"^s:\d+$")
