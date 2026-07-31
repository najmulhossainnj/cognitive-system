# COS Coding Standards

Version: 1.0

Status: Approved

Document ID: COS-STD-CODING-001

---

## Purpose

This document defines coding standards for the Cognitive Operating System implementation.

---

## Python Standards

### Version

Python 3.11 minimum required.

### Type Hints

All public interfaces must include complete type hints.

```python
def solve(self, task: Task) -> Result:
    """Solve a reasoning task."""
    raise NotImplementedError
```

### Documentation

Every public class and function requires:

- Purpose
- Parameters (Args)
- Return Value (Returns)
- Exceptions (Raises)

```python
def query(self, expression: str) -> list[MemoryItem]:
    """Query the memory store.

    Args:
        expression: The query expression to search for

    Returns:
        List of matching memory items

    Raises:
        QueryError: If the query expression is invalid
    """
    raise NotImplementedError
```

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `CognitiveContext` |
| Interfaces | IPascalCase | `IEventBus` |
| Functions | snake_case | `store_memory` |
| Constants | UPPER_CASE | `MAX_RETRY_COUNT` |
| Modules | snake_case | `event_bus.py` |
| Private | _prefix | `_internal_method` |
| Type Vars | PascalCase | `T` or `TResult` |

---

## Architecture Rules

### Kernel First

Kernel components must remain domain-independent.

### Broker First

All cognitive interactions occur through the Cognitive Broker.

```python
# Correct
context.cognition.reasoning.solve(...)

# Incorrect
reasoning_service.solve(...)
```

### Interfaces Before Implementations

Public interfaces must be designed before implementation.

### Determinism Before Optimization

Never introduce nondeterministic behavior.

---

## Import Organization

```python
# Standard library
from typing import TYPE_CHECKING
from pathlib import Path

# Third-party
from pydantic import BaseModel

# Local application
from cos.kernel.events import IEventBus
from cos.shared.models import Request
```

---

## Error Handling

- Never suppress exceptions silently
- Use structured error objects where appropriate
- Every error should emit telemetry

```python
class ReasoningError(Exception):
    """Error during reasoning operation."""

    def __init__(self, message: str, task_id: str | None = None) -> None:
        super().__init__(message)
        self.task_id = task_id
```

---

## Testing Standards

Every implementation requires:

- Unit tests for public interfaces
- Integration tests for service interactions
- Tests must be deterministic

```python
def test_reasoning_capability():
    """Test reasoning capability interface."""
    capability = _ReasoningCapability()
    
    with pytest.raises(NotImplementedError):
        capability.solve(mock_task)
```

---

## File Organization

```
cos/
├── __init__.py          # Public API exports
├── module/
│   ├── __init__.py      # Package exports
│   ├── interface.py     # Interface definitions
│   ├── implementation.py # Implementation (if needed)
│   └── ...
```

---

## Summary

Follow these standards consistently for maintainable, readable code.
