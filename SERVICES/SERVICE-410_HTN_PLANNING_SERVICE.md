# Cognitive Operating System (COS)

# SERVICE-410 — HTN Planning Service Specification

**Document ID:** COS-SVC-410

**Version:** 1.0

**Status:** Draft

---

# Purpose

The HTN (Hierarchical Task Network) Planning Service generates executable plans by recursively decomposing high-level goals into increasingly detailed subtasks using domain knowledge and planning methods.

The service specializes in hierarchical task decomposition and serves as one of the planning engines coordinated by **SERVICE-400 — Planning Service**.

It does not select plans, execute plans, or make decisions.

---

# Scope

This specification defines:

- Goal decomposition
- Task hierarchy generation
- Method selection
- Operator expansion
- Hierarchical plan generation
- Public interfaces
- Configuration
- Events
- Telemetry

This specification does not define:

- Graph search
- Constraint optimization
- Decision making
- Plan execution
- Learning

---

# Architectural Position

```
Planning Capability
        │
        ▼
Planning Service
        │
        ▼
HTN Planning Service
```

---

# Architectural Philosophy

The HTN Planning Service answers:

> **"How can this goal be decomposed into executable tasks?"**

It focuses on hierarchical decomposition rather than search or optimization.

---

# Responsibilities

The HTN Planning Service shall:

- decompose goals into subtasks
- select decomposition methods
- generate task hierarchies
- produce executable task sequences
- maintain decomposition traceability

The service shall not:

- choose among competing plans
- execute plans
- solve resource constraints
- perform graph search

---

# Service Architecture

```
HTN Planning Service

│

├── Goal Decomposer

├── Method Repository

├── Method Selector

├── Task Network Builder

├── Operator Resolver

├── Plan Generator

├── Trace Manager

└── Execution Monitor
```

---

# Planning Pipeline

```
Goal

↓

Method Selection

↓

Task Decomposition

↓

Operator Expansion

↓

Task Network

↓

Executable Plan
```

---

# Planning Concepts

The HTN planner supports:

- Tasks
- Primitive Tasks
- Compound Tasks
- Methods
- Operators
- Preconditions
- Effects

---

# Public Interface

Used internally by the Planning Service.

Representative operations:

```python
decompose()

expand()

generate()

methods()

operators()

trace()
```

---

# Configuration

Configurable parameters include:

- decomposition strategy
- recursion depth
- method priority
- operator policy
- timeout

---

# Events

Representative events:

```
GoalDecomposed

MethodSelected

TaskExpanded

PlanGenerated

PlanningFailed
```

---

# Telemetry

Representative metrics:

- decomposition depth
- planning latency
- task count
- method usage
- operator usage
- plan size

---

# Collaboration

Uses:

- World Model Service
- Working Memory Service
- Constraint Planning Service (validation)

Coordinates through:

- Planning Service

---

# Quality Attributes

- Explainability
- Determinism
- Modularity
- Extensibility
- Traceability

---

# Architectural Requirements

REQ-SVC410-001 [A3]

Support recursive hierarchical task decomposition.

---

REQ-SVC410-002 [A3]

Support reusable planning methods.

---

REQ-SVC410-003 [A3]

Produce traceable task hierarchies.

---

REQ-SVC410-004 [A3]

Remain independent of execution systems.

---

REQ-SVC410-005 [A3]

Operate only under Planning Service coordination.

---

# Acceptance Criteria

- Hierarchical decomposition verified
- Recursive planning verified
- Traceability verified
- Planning integration verified

---

# Related Documents

- CORE-130 — Planning Capability
- SERVICE-400 — Planning Service
- SERVICE-420 — Graph Planning Service
- SERVICE-430 — Constraint Planning Service

---

# Summary

The HTN Planning Service provides hierarchical task decomposition for the Cognitive Operating System. By transforming abstract goals into executable task networks while remaining independent of decision making and execution, it delivers explainable, reusable, and domain-oriented planning capabilities.