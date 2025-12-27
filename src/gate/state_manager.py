"""State manager for gate persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .models import GateState


class StateManager:
    """Manages gate state persistence to data/gate_state.json."""

    def __init__(self, state_file: Path):
        """Initialize state manager.

        Args:
            state_file: Path to gate_state.json file.
        """
        self._state_file = state_file
        self._state_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Optional[GateState]:
        """Load gate state from file.

        Returns:
            GateState if file exists, None otherwise.
        """
        if not self._state_file.exists():
            return None

        try:
            with open(self._state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return GateState(**data)
        except Exception:
            return None

    def save(self, state: GateState) -> None:
        """Save gate state to file (atomic write).

        Args:
            state: GateState to save.
        """
        # Atomic write: write to temp file, then rename
        temp_file = self._state_file.with_suffix(".json.tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                # Support both Pydantic v1 and v2
                if hasattr(state, "model_dump"):
                    data = state.model_dump()
                else:
                    data = state.dict()
                json.dump(data, f, indent=2)
            temp_file.replace(self._state_file)
        except Exception:
            # Clean up temp file on error
            if temp_file.exists():
                temp_file.unlink()
            raise

