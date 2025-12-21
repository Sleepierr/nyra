"""Instance registry models per spec/base1.0/nyrahome_cloud_spec.md §6.1."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from typing_extensions import Literal


class Instance(BaseModel):
    """Canonical stored instance record.

    No validation beyond Pydantic structural typing is performed.
    """

    instance_id: str
    display_name: str
    instance_kind: Literal["home", "secondary", "transient", "clone"]
    platform: str
    device_model: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None
