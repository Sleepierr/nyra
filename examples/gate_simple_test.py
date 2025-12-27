#!/usr/bin/env python3
"""Simple test of Gate system without full event system imports."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.runtime.gate import Gate
from src.runtime.governance_loader import GovernanceLoadError
from src.state.models.event_envelope import EventEnvelope


def main():
    """Simple gate test."""
    repo_root = Path(__file__).parent.parent

    # Initialize gate
    try:
        gate = Gate(repo_root, persist=True, promote_memory=False)
    except Exception as e:
        print(f"Failed to initialize gate: {e}", file=sys.stderr)
        return 1

    # Start gate (will load governance)
    try:
        gate.start()
        print("✓ Gate started successfully")
    except GovernanceLoadError as e:
        print("GOVERNANCE LOAD FAILED", file=sys.stderr)
        print(str(e), file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Failed to start gate: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

    # Print status
    status = gate.status()
    print(f"\nGate Status:")
    print(f"  Governance loaded: {status['governance_loaded']}")
    if status['governance_loaded']:
        print(f"  Governance SHA256: {status['governance_overall_sha256'][:16]}...")
        print(f"  Patches count: {status['patches_count']}")
    print(f"  Current session: {status.get('current_session_id', 'None')}")

    # Create and log a simple event
    event = EventEnvelope(
        event_id="test-event-123",
        seq=0,
        ts_utc="2025-12-27T19:00:00.000Z",
        source_instance_id="test-instance",
        source_kind="transient",
        type="test.example",
        payload={"message": "Hello from gate test"},
    )
    gate.log_event(event)
    print(f"\n✓ Logged event: {event.event_id}")

    # Test CLI command
    response = gate.handle_command("/save-summary")
    if response:
        print(f"\n✓ Command response: {response}")

    # Shutdown
    gate.shutdown()
    print("\n✓ Gate shut down successfully")

    return 0


if __name__ == "__main__":
    sys.exit(main())

