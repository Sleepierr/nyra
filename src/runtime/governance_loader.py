"""Governance loader for Temporary Gate v1.

HARD-REQUIRED: Gate must refuse to start if governance files are missing.
Loads canonical governance documents and computes SHA256 digests for integrity verification.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from pydantic import BaseModel


class GovernanceFile(BaseModel):
    """Information about a loaded governance file."""

    path: str
    sha256: str
    bytes: int
    exists: bool


class PatchesInfo(BaseModel):
    """Information about patches directory."""

    count: int
    filenames: List[str]
    sha256: str


class GovernanceSnapshot(BaseModel):
    """Complete governance snapshot with all loaded documents and digests."""

    loaded_at: str  # ISO timestamp
    files: List[GovernanceFile]
    patches: PatchesInfo
    overall_sha256: str


class GovernanceLoadError(Exception):
    """Raised when governance loading fails.

    Gate must refuse to start if this exception is raised.
    """

    pass


# Required governance documents (paths relative to repo root)
REQUIRED_GOVERNANCE_FILES = [
    "spec/base1.0/nyra_constitution.md",
    "spec/base1.0/subsystem_index.md",
    "spec/base1.0/interaction_and_clients.md",
    "spec/evolution/autonomy_embodiment_evolution_unlock.md",
    "spec/base1.0/audit_report_v1.md",
]

PATCHES_DIR = "subsystems/patches/base1.0"


def compute_sha256(content: bytes) -> str:
    """Compute SHA256 hash of content.

    Args:
        content: Bytes to hash.

    Returns:
        Hexadecimal SHA256 digest.
    """
    return hashlib.sha256(content).hexdigest()


def load_governance(repo_root: Path) -> GovernanceSnapshot:
    """Load all required governance documents and compute digests.

    HARD-REQUIRED: Raises GovernanceLoadError if any required document is missing.

    Args:
        repo_root: Path to repository root.

    Returns:
        GovernanceSnapshot with all loaded documents and digests.

    Raises:
        GovernanceLoadError: If any required document is missing or unreadable.
    """
    loaded_at = datetime.now(timezone.utc).isoformat()
    files: List[GovernanceFile] = []
    missing_files: List[str] = []

    # Load required governance files
    for rel_path in REQUIRED_GOVERNANCE_FILES:
        file_path = repo_root / rel_path

        if not file_path.exists():
            missing_files.append(rel_path)
            files.append(
                GovernanceFile(
                    path=rel_path,
                    sha256="",
                    bytes=0,
                    exists=False,
                )
            )
            continue

        try:
            content = file_path.read_bytes()
            sha256_digest = compute_sha256(content)
            files.append(
                GovernanceFile(
                    path=rel_path,
                    sha256=sha256_digest,
                    bytes=len(content),
                    exists=True,
                )
            )
        except Exception as e:
            raise GovernanceLoadError(
                f"Failed to read governance file {rel_path}: {e}"
            ) from e

    # Check for missing files
    if missing_files:
        raise GovernanceLoadError(
            f"Missing required governance files: {', '.join(missing_files)}"
        )

    # Load patches directory
    patches_dir = repo_root / PATCHES_DIR
    if not patches_dir.exists():
        raise GovernanceLoadError(f"Patches directory does not exist: {PATCHES_DIR}")

    if not patches_dir.is_dir():
        raise GovernanceLoadError(f"Patches path is not a directory: {PATCHES_DIR}")

    # Get sorted list of patch filenames
    patch_files = sorted(
        [f.name for f in patches_dir.iterdir() if f.is_file() and f.suffix == ".md"]
    )

    # Compute SHA256 of newline-joined sorted filenames
    patches_content = "\n".join(patch_files).encode("utf-8")
    patches_sha256 = compute_sha256(patches_content)

    patches_info = PatchesInfo(
        count=len(patch_files),
        filenames=patch_files,
        sha256=patches_sha256,
    )

    # Compute overall SHA256: hash of all file SHA256s + patches SHA256
    # Combine all file SHA256s in order, then add patches SHA256
    all_hashes = "".join(f.sha256 for f in files) + patches_sha256
    overall_sha256 = compute_sha256(all_hashes.encode("utf-8"))

    return GovernanceSnapshot(
        loaded_at=loaded_at,
        files=files,
        patches=patches_info,
        overall_sha256=overall_sha256,
    )

