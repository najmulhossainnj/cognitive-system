# APP-140 — ARC Agent Application

**Status:** Implemented

**Date:** 2026-07-31

## Context

The ARC Agent is an application built on the Cognitive Operating System to solve tasks from the ARC-AGI-2 benchmark. This document describes how the agent bridges the benchmark dataset and the cognitive architecture.

## Architecture

```
ARC-AGI-2 JSON Task
        │
        ▼
  APP-140 ARC Agent
        │
        ├── Grid Interpreter (perception)
        ├── Pattern Discovery (pattern matching)
        └── ARC Solver (reasoning, planning, decision)
        │
        ▼
  Predicted Output Grid
```

## Components

### ARCAgent

Main entry point for ARC task solving.

```python
from cos.apps.arc_agent import ARCAgent

agent = ARCAgent()
task = agent.load_task(task_data)
solution = await agent.solve(task)
```

### GridInterpreter

Performs perception on grid data:

- Object detection
- Color analysis
- Shape recognition
- Bounding box calculation
- Connected component analysis
- Symmetry detection

### PatternDiscovery

Discovers candidate transformation patterns:

- Translation
- Reflection
- Rotation
- Scaling
- Copy/Delete
- Color changes
- Position changes

### ARCSolver

Solves tasks using the cognitive pipeline:

1. Generate candidate rules
2. Validate against training examples
3. Select best rule (decision engine)
4. Apply to test input
5. Reflection

## Integration with COS

The ARC Agent uses the following COS components:

| COS Layer | Usage |
|-----------|-------|
| **ReasoningService** | Pattern analysis |
| **MemoryService** | Working memory for task state |
| **DecisionService** | Rule selection |
| **MetaCognitionService** | Reflection |

## Usage Example

```python
from cos.apps.arc_agent import ARCAgent
import asyncio

async def solve_task():
    agent = ARCAgent()
    
    task_data = {
        "train": [
            {"input": [[1, 0], [1, 1]], "output": [[0, 1], [0, 1]]}
        ],
        "test": [
            {"input": [[2, 0], [2, 2]]}
        ]
    }
    
    task = agent.load_task(task_data)
    solution = await agent.solve(task)
    
    print(f"Confidence: {solution.confidence}")
    print(f"Output: {solution.output_grid}")

asyncio.run(solve_task())
```

## Verification

```python
# Test output:
Task loaded: 2 training examples, 1 test cases
Task ID: task_1
Confidence: 0.5
Reasoning trace:
  - Training example 1 interpreted
  - Training example 2 interpreted
  - Grid input perceived
  - 5 candidate patterns discovered
  - 5 candidate rules generated
  - 3 candidates validated
  - Selected: move_to_corner
```

## Consequences

### Positive
- ARC tasks solved using cognitive architecture
- Modular design for easy extension
- Integration with all COS services

### Negative
- Basic transformation rules (placeholder implementations)
- Limited pattern detection

### Neutral
- Demonstrates COS capability for domain-specific applications

## References

- [holistic view.txt](file:///workspace/project/cognitive-system/holistic%20view.txt) - Full ARC-AGI-2 integration design
- [Phase 3 Core Services](PHASE_3_CORE_SERVICES.md) - COS services used
- [Phase 4 Integration](PHASE_4_INTEGRATION_ORCHESTRATION.md) - Pipeline orchestration
