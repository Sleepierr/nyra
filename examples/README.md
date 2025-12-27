# Gate System Examples

This directory contains examples of how to use the Gate persistence system.

## gate_example.py

Basic example demonstrating:
- Gate initialization with governance loading
- Event logging
- Memory candidate processing
- CLI command handling

### Usage

```bash
python3 examples/gate_example.py
```

### Integration with EventBus

To integrate the gate with the EventBus system:

```python
from src.events.routing import EventBus
from src.runtime.gate import Gate
from src.gate.event_integration import create_gate_event_hook

# Initialize gate
gate = Gate(repo_root, persist=True, promote_memory=False)
gate.start()

# Create event hook
event_hook = create_gate_event_hook(gate._event_logger)

# Subscribe to EventBus
event_bus = EventBus()
event_bus.subscribe("*", event_hook)  # Subscribe to all events
```

### Integration with ExecutionContext

To integrate with ExecutionContext's event emission:

```python
from src.events.routing import EventBus
from src.runtime.gate import Gate
from src.gate.event_integration import create_gate_event_hook

# Initialize gate
gate = Gate(repo_root, persist=True, promote_memory=False)
gate.start()

# Get event bus from execution context
event_bus = context.event_bus

# Subscribe gate logger
event_hook = create_gate_event_hook(gate._event_logger)
event_bus.subscribe("*", event_hook)
```

## Command-Line Flags

The Gate supports the following initialization flags:

- `--persist` (default: `True`): Enable/disable event logging to JSONL files
- `--promote-memory` (default: `False`): Enable/disable automatic memory promotion to LTM

## CLI Commands

The Gate supports the following chat commands:

- `/save-summary`: Generate and save a session summary JSON file
- `/promote-last [N]`: Promote the last N memory candidates to long-term memory

