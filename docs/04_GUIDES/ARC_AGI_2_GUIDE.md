# ARC-AGI-2 Guide

This guide explains how to use the Cognitive Operating System (COS) to solve ARC-AGI-2 benchmark tasks using the APP-140 ARC Agent with automatic memory-based learning.

## Table of Contents

1. [Overview](#overview)
2. [Memory Architecture](#memory-architecture)
3. [Adding Data](#adding-data)
4. [Automatic Learning](#automatic-learning)
5. [Using the ARC Agent](#using-the-arc-agent)
6. [API Reference](#api-reference)
7. [Examples](#examples)

---

## Overview

The ARC-AGI-2 benchmark consists of grid transformation tasks. Each task contains:

- **Training Examples**: Input-output grid pairs that demonstrate the transformation rule
- **Test Input**: A new input grid that needs to be transformed
- **Expected Output**: The correct output grid (used for evaluation)

**Key Feature**: The ARC Agent automatically learns from experience using COS memory services - no explicit training required!

---

## Memory Architecture

The ARC Agent integrates with COS's multi-memory system for automatic experience-based learning:

```
┌─────────────────────────────────────────────────────────────────┐
│                      ARC Agent (APP-140)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Working     │   │   Semantic    │   │   Episodic    │
│   Memory      │   │   Memory      │   │   Memory      │
├───────────────┤   ├───────────────┤   ├───────────────┤
│ • Task State  │   │ • Patterns    │   │ • Experiences │
│ • Current     │   │ • Concepts    │   │ • Episodes    │
│   Grids       │   │ • Heuristics │   │ • History     │
└───────────────┘   └───────────────┘   └───────────────┘
```

### Memory Types

| Memory Type | Purpose | Contents |
|-------------|---------|----------|
| **WorkingMemory** | Active task processing | Current task state, grid data |
| **SemanticMemory** | Persistent learned knowledge | Transformation patterns, rules |
| **EpisodicMemory** | Past experiences | Solving episodes, successes/failures |

---

## Adding Data

### 1. ARC Task JSON Format

```json
{
  "train": [
    {"input": [[1, 0, 0], [1, 1, 0]], "output": [[0, 1, 1], [0, 1, 1]]},
    {"input": [[2, 0], [2, 2]], "output": [[0, 2], [0, 2]]}
  ],
  "test": [
    {"input": [[3, 0, 0], [3, 3, 0], [3, 0, 0]]}
  ]
}
```

### 2. Adding Tasks to the System

**Method A: Inline Task Definition**

```python
from cos.apps.arc_agent import ARCAgent
import asyncio

async def solve_custom_task():
    agent = ARCAgent()
    
    task_data = {
        "train": [
            {"input": [[1, 0, 0], [1, 1, 0]], "output": [[0, 1, 1], [0, 1, 1]]}
        ],
        "test": [{"input": [[2, 0, 0], [2, 2, 0]]}]
    }
    
    task = agent.load_task(task_data)
    solution = await agent.solve(task)
    print(f"Output: {solution.output_grid}")

asyncio.run(solve_custom_task())
```

**Method B: Loading from File**

```python
import json
from cos.apps.arc_agent import ARCAgent
import asyncio

async def solve_from_file(filepath):
    agent = ARCAgent()
    
    with open(filepath, 'r') as f:
        task_data = json.load(f)
    
    task = agent.load_task(task_data)
    return await agent.solve(task)

solution = asyncio.run(solve_from_file('task.json'))
```

**Method C: Batch Loading**

```python
import json
from cos.apps.arc_agent import ARCAgent
import asyncio
import os

async def solve_batch(tasks_dir):
    agent = ARCAgent()
    results = []
    
    for filename in sorted(os.listdir(tasks_dir)):
        if filename.endswith('.json'):
            with open(os.path.join(tasks_dir, filename), 'r') as f:
                task = agent.load_task(json.load(f))
                solution = await agent.solve(task)
                results.append({'file': filename, 'solution': solution})
    
    return results
```

### 3. Task Data Directory Structure

```
data/
└── arc_tasks/
    ├── task_001.json
    ├── task_002.json
    └── ...
```

### 4. Creating a Task File

Example `task_001.json`:

```json
{
  "id": "task_001",
  "name": "Rotate and Mirror",
  "train": [
    {"input": [[1, 0], [0, 0]], "output": [[0, 0], [0, 1]]}
  ],
  "test": [
    {"input": [[2, 0, 0], [0, 0, 0]]}
  ]
}
```

---

## Automatic Learning

The ARC Agent **automatically learns** from experience - no explicit training required!

### How It Works

```
Task 1 → Solve → Success (confidence >= 0.5) → Store Pattern in Semantic Memory
                                                 Record in Episodic Memory

Task 2 → Check Memory → Found Pattern → Use Experience → Solve Faster/Better
```

### Learning Process

1. **Solve Task**: Agent solves the task using training examples
2. **Evaluate Success**: If confidence >= 0.5, the solution is considered successful
3. **Store Pattern**: Successful transformation patterns are stored in Semantic Memory
4. **Record Episode**: The solving experience is recorded in Episodic Memory
5. **Future Benefit**: Similar tasks can leverage learned patterns

### Memory Query

Before solving each task, the agent checks Semantic Memory for similar patterns:

```python
# The agent automatically queries memory for relevant patterns
learned_patterns = await agent._check_memory_for_patterns(task)
if learned_patterns:
    solution.learned_from_memory = True
```

### Viewing Learned Knowledge

```python
# Get all learned patterns
patterns = await agent.get_learned_patterns()

# Get past experiences
experiences = await agent.get_solving_experiences()

# Get memory statistics
stats = await agent.get_memory_stats()
# Returns: learned_patterns, total_experiences, success_rate, etc.
```

### Example: Automatic Learning Flow

```python
from cos.apps.arc_agent import ARCAgent
import asyncio

async def automatic_learning_demo():
    agent = ARCAgent()
    
    # Task 1: First time - no prior knowledge
    task1 = {
        "train": [{"input": [[1, 0]], "output": [[0, 1]]}],
        "test": [{"input": [[2, 0]]}]
    }
    solution1 = await agent.solve(agent.load_task(task1))
    print(f"Task 1 confidence: {solution1.confidence}")
    
    # Task 2: Agent checks memory and finds patterns
    task2 = {
        "train": [{"input": [[3, 0]], "output": [[0, 3]]}],
        "test": [{"input": [[4, 0]]}]
    }
    solution2 = await agent.solve(agent.load_task(task2))
    print(f"Learned from memory: {solution2.learned_from_memory}")
    
    # Check what was learned
    stats = await agent.get_memory_stats()
    print(f"Learned patterns: {stats['learned_patterns']}")
    print(f"Total experiences: {stats['total_experiences']}")

asyncio.run(automatic_learning_demo())
```

### Benefits of Automatic Learning

| Benefit | Description |
|---------|-------------|
| **No Retraining** | System learns automatically from solving tasks |
| **Pattern Reuse** | Similar tasks benefit from past solutions |
| **Experience Accumulation** | Performance improves over time |
| **Cross-Task Learning** | Patterns learned in one task help others |

---

## Running Training (Legacy)

> **Note**: Explicit training is no longer required. The system learns automatically from solving tasks.

For backward compatibility, you can still use explicit training:

### 1. Training Pipeline

```python
from cos.apps.arc_agent import ARCAgent
import asyncio

async def train_on_task():
    agent = ARCAgent()
    
    task_data = {
        "train": [
            {"input": [[1, 0, 0], [1, 1, 0]], "output": [[0, 1, 1], [0, 1, 1]]},
            {"input": [[2, 0], [2, 2]], "output": [[0, 2], [0, 2]]}
        ],
        "test": [{"input": [[3, 0, 0], [3, 3, 0], [3, 0, 0]]}]
    }
    
    task = agent.load_task(task_data)
    solution = await agent.solve(task)
    
    print(f"Patterns discovered: {len(solution.reasoning_trace)}")
    print(f"Confidence: {solution.confidence}")

asyncio.run(train_on_task())
```

### 3. Interpreting Training Results

```python
solution = await agent.solve(task)

for step in solution.reasoning_trace:
    print(step)

# Example output:
# Training example 1 interpreted
# Training example 2 interpreted
# 5 candidate patterns discovered
# 5 candidate rules generated
# 3 candidates validated
# Selected: move_to_corner
```

### 4. Confidence Scoring

| Validation Result | Confidence |
|-------------------|------------|
| All examples match | 1.0 |
| 50% examples match | 0.5 |
| No examples match | 0.0 |

---

## Using the ARC Agent

### 1. Basic Usage

```python
from cos.apps.arc_agent import ARCAgent
import asyncio

async def basic_usage():
    agent = ARCAgent()
    
    task = agent.load_task({
        "train": [{"input": [[1, 0], [1, 1]], "output": [[0, 1], [0, 1]]}],
        "test": [{"input": [[2, 0], [2, 2]]}]
    })
    
    solution = await agent.solve(task)
    
    print(f"Output grid: {solution.output_grid}")
    print(f"Confidence: {solution.confidence}")
    print(f"Learned from memory: {solution.learned_from_memory}")
    print(f"Steps: {solution.reasoning_trace}")

asyncio.run(basic_usage())
```

### 2. Batch Processing

```python
from cos.apps.arc_agent import ARCAgent
import asyncio

async def batch_process(task_files):
    agent = ARCAgent()
    results = []
    
    for filepath in task_files:
        import json
        with open(filepath, 'r') as f:
            task = agent.load_task(json.load(f))
            solution = await agent.solve(task)
            results.append({
                'file': filepath,
                'confidence': solution.confidence,
                'success': solution.confidence >= 0.5
            })
    
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    print(f"Processed: {total}, Successful: {successful} ({100*successful/total:.1f}%)")
    
    return results
```

### 3. Evaluation Mode

```python
from cos.apps.arc_agent import ARCAgent
import asyncio

async def evaluate_task(task_data):
    agent = ARCAgent()
    task = agent.load_task(task_data)
    solution = await agent.solve(task)
    
    # Compare with expected output if available
    if len(task_data.get('test', [])) > 1:
        expected = task_data['test'][1].get('output')
        if expected:
            return {
                'predicted': solution.output_grid,
                'expected': expected,
                'matches': solution.output_grid == expected,
                'confidence': solution.confidence
            }
    
    return {'predicted': solution.output_grid, 'confidence': solution.confidence}
```

---

## API Reference

### ARCAgent

```python
from cos.apps.arc_agent import ARCAgent
agent = ARCAgent()
```

**Constructor with Memory Services:**
```python
from cos.services.memory.memory_service import (
    WorkingMemoryService,
    SemanticMemoryService,
    EpisodicMemoryService
)

agent = ARCAgent(
    working_memory=WorkingMemoryService(),
    semantic_memory=SemanticMemoryService(),  # Shared for persistence
    episodic_memory=EpisodicMemoryService()    # Shared for persistence
)
```

| Method | Description |
|--------|-------------|
| `load_task(task_data)` | Load an ARC task from JSON |
| `solve(task)` | Solve an ARC task with automatic learning (async) |
| `solve_batch(tasks)` | Solve multiple tasks (async) |
| `get_history()` | Get history of solved tasks |
| `get_learned_patterns()` | Get all learned patterns from semantic memory (async) |
| `get_solving_experiences(limit)` | Get past solving experiences (async) |
| `get_memory_stats()` | Get memory statistics (async) |

### GridInterpreter

```python
from cos.apps.arc_agent import GridInterpreter
interpreter = GridInterpreter()
```

| Method | Description |
|--------|-------------|
| `interpret(grid_pair)` | Interpret input/output pair (async) |
| `interpret_grid(grid, grid_id)` | Interpret single grid (async) |

### PatternDiscovery

```python
from cos.apps.arc_agent import PatternDiscovery
discovery = PatternDiscovery()
```

| Method | Description |
|--------|-------------|
| `discover(training_pairs)` | Discover patterns (async) |

### ARCTask

| Attribute | Type | Description |
|-----------|------|-------------|
| `train` | `list[dict]` | Training examples |
| `test` | `list[dict]` | Test inputs |
| `metadata` | `dict` | Additional metadata |

### ARCSolution

| Attribute | Type | Description |
|-----------|------|-------------|
| `task_id` | `str` | Unique task identifier |
| `input_grid` | `list[list[int]]` | Test input grid |
| `output_grid` | `list[list[int]]` | Predicted output grid |
| `confidence` | `float` | Solution confidence (0-1) |
| `reasoning_trace` | `list[str]` | Steps taken |
| `learned_from_memory` | `bool` | Whether memory patterns were used |

### Memory Statistics (from get_memory_stats)

| Attribute | Type | Description |
|-----------|------|-------------|
| `learned_patterns` | `int` | Number of patterns in semantic memory |
| `total_experiences` | `int` | Number of recorded episodes |
| `successful_solutions` | `int` | Number of successful solutions |
| `average_confidence` | `float` | Average confidence score |
| `success_rate` | `float` | Ratio of successful solutions |

### GridSymbolic

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `str` | Grid identifier |
| `width` | `int` | Grid width |
| `height` | `int` | Grid height |
| `colors` | `dict[int, int]` | Color counts |
| `objects` | `list[dict]` | Detected objects |
| `shapes` | `list[str]` | Recognized shapes |
| `symmetry` | `dict[str, bool]` | Symmetry types |

### Pattern

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Pattern name |
| `description` | `str` | Pattern description |
| `confidence` | `float` | Pattern confidence |
| `parameters` | `dict` | Pattern parameters |

---

## Examples

### Example 1: Simple Translation

```python
import asyncio
from cos.apps.arc_agent import ARCAgent

async def example_translation():
    task = {
        "train": [{"input": [[1, 0], [0, 0]], "output": [[0, 1], [0, 0]]}],
        "test": [{"input": [[2, 0, 0], [0, 0, 0], [0, 0, 0]]}]
    }
    
    agent = ARCAgent()
    solution = await agent.solve(agent.load_task(task))
    
    print(f"Input:  {task['test'][0]['input']}")
    print(f"Output: {solution.output_grid}")
    print(f"Confidence: {solution.confidence}")

asyncio.run(example_translation())
```

### Example 2: Color Change

```python
import asyncio
from cos.apps.arc_agent import ARCAgent

async def example_color_change():
    task = {
        "train": [{"input": [[1, 0], [1, 1]], "output": [[2, 0], [2, 2]]}],
        "test": [{"input": [[3, 0], [3, 3]]}]
    }
    
    agent = ARCAgent()
    solution = await agent.solve(agent.load_task(task))
    
    print(f"Input:  {task['test'][0]['input']}")
    print(f"Output: {solution.output_grid}")

asyncio.run(example_color_change())
```

### Example 3: Full Pipeline with Analysis

```python
import asyncio
from cos.apps.arc_agent import ARCAgent, GridInterpreter, PatternDiscovery

async def full_pipeline():
    task_data = {
        "train": [
            {"input": [[1, 0, 0], [1, 1, 0]], "output": [[0, 1, 1], [0, 1, 1]]},
            {"input": [[2, 0], [2, 2]], "output": [[0, 2], [0, 2]]}
        ],
        "test": [{"input": [[3, 0, 0], [3, 3, 0], [3, 0, 0]]}]
    }
    
    # Step 1: Interpret grids
    interpreter = GridInterpreter()
    pairs = [await interpreter.interpret(e) for e in task_data["train"]]
    
    # Step 2: Discover patterns
    patterns = await PatternDiscovery().discover(pairs)
    print(f"Discovered {len(patterns)} patterns")
    
    # Step 3: Solve
    solution = await ARCAgent().solve(ARCAgent().load_task(task_data))
    print(f"Solution: {solution.output_grid}")

asyncio.run(full_pipeline())
```

### Example 4: Multiple Tasks Batch

```python
import asyncio
from cos.apps.arc_agent import ARCAgent

async def batch_example():
    tasks = [
        {"train": [{"input": [[1, 0]], "output": [[0, 1]]}], "test": [{"input": [[2, 0]]}]},
        {"train": [{"input": [[1, 1], [0, 0]], "output": [[0, 0], [1, 1]]}], "test": [{"input": [[2, 2], [0, 0]]}]},
        {"train": [{"input": [[0, 1], [1, 0]], "output": [[1, 0], [0, 1]]}], "test": [{"input": [[0, 2], [2, 0]]}]}
    ]
    
    agent = ARCAgent()
    solutions = await agent.solve_batch(tasks)
    
    for i, sol in enumerate(solutions):
        print(f"Task {i+1}: confidence={sol.confidence}")

asyncio.run(batch_example())
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty output grid | Check test input format |
| Low confidence | May indicate ambiguous training examples |
| Import errors | Ensure `cos.apps.arc_agent` is in Python path |

---

## See Also

- [APP-140 ARC Agent Documentation](../02_ADR/APP_140_ARC_AGENT.md)
- [Holistic View](../../holistic%20view.txt)
- [COS Architecture](../02_ADR/PHASE_1_ARCHITECTURE_SKELETON.md)
