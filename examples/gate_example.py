#!/usr/bin/env python3
"""Example usage of Gate system.

This demonstrates how to initialize and use the Gate for conversation persistence.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.runtime.gate import Gate
from src.runtime.governance_loader import GovernanceLoadError
from src.events.emission import EventFactory
from src.memory.models import STMMemoryEntry


def main():
    """Example gate usage."""
    repo_root = Path(__file__).parent.parent

    # Initialize gate with defaults (persist=True, promote_memory=False)
    try:
        gate = Gate(repo_root, persist=True, promote_memory=False)
    except Exception as e:
        print(f"Failed to initialize gate: {e}", file=sys.stderr)
        return 1

    # Start gate (will load governance and fail if missing)
    try:
        gate.start()
        print("Gate started successfully")
    except GovernanceLoadError as e:
        print("GOVERNANCE LOAD FAILED", file=sys.stderr)
        print(str(e), file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Failed to start gate: {e}", file=sys.stderr)
        return 1

    # Print status
    status = gate.status()
    print(f"\nGate Status:")
    print(f"  Governance loaded: {status['governance_loaded']}")
    print(f"  Governance SHA256: {status['governance_overall_sha256'][:16]}...")
    print(f"  Patches count: {status['patches_count']}")
    print(f"  Current session: {status.get('current_session_id', 'None')}")

    # Example: Log an event
    event = EventFactory.create(
        source_instance_id="example-instance",
        source_kind="transient",
        event_type="interaction.message_received",
        payload={"text": "Hello, Nyra!"},
    )
    gate.log_event(event)
    print(f"\nLogged event: {event.event_id[:8]}...")

    # Example: Process a memory candidate
    stm_entry = STMMemoryEntry(
        raw_payload={
            "content_summary": "User said hello",
            "significance_score": 0.5,
        }
    )
    candidate = gate.process_memory_candidate(stm_entry)
    if candidate:
        print(f"Processed memory candidate: {candidate['memory_id'][:8]}...")

    # Example: Handle CLI commands
    response = gate.handle_command("/save-summary")
    if response:
        print(f"\nCommand response: {response}")

    # Shutdown
    gate.shutdown()
    print("\nGate shut down successfully")

    return 0


if __name__ == "__main__":
    sys.exit(main())

