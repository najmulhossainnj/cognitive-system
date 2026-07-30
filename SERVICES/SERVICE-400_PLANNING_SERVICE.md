# Cognitive Operating System (COS)

# SERVICE-400 — Planning Service Specification

**Document ID:** COS-SVC-400

**Version:** 1.0

**Status:** Draft

---

# Purpose

The Planning Service provides the implementation of the Planning Capability for the Cognitive Operating System.

It transforms goals into executable plans by coordinating specialized planning services, selecting appropriate planning strategies, validating candidate plans, and providing a unified planning interface to the rest of the system.

Unlike individual planning algorithms, the Planning Service does not construct plans directly. It orchestrates specialized planners while exposing a stable cognitive interface.

The service implements the Planning Capability defined in **CORE-130**.

---

# Scope

This specification defines:

- Planning orchestration
- Planner selection
- Goal analysis
- Planning coordination
- Plan validation coordination
- Plan explanation
- Replanning coordination
- Public interfaces
- Configuration
- Events
- Telemetry

This specification does not define:

- HTN planning algorithms
- Graph search algorithms
- Constraint solving
- Decision making
- Plan execution
- Learning

These responsibilities belong to specialized services and higher-level capabilities.

---

# Architectural Position

```
Applications
        │
        ▼
Planning Capability
        │
        ▼
Planning Service
        │
        ▼
Planning Coordination
```

The service implements the public interface defined by **CORE-130 — Planning Capability**.

---

# Architectural Philosophy

The Planning Service answers:

> **"How can this goal be achieved?"**

It coordinates specialized planning services to generate candidate plans while remaining independent of specific planning algorithms.

Planning generates alternatives.

Decision Capability selects among alternatives.

Execution systems carry out the selected plan.

---

# Responsibilities

The Planning Service shall:

- analyze planning requests
- select planning strategies
- coordinate specialized planners
- validate candidate plans
- manage replanning
- explain generated plans
- expose a unified planning interface

The service shall not:

- perform HTN decomposition
- execute graph search
- solve constraints directly
- select the best plan
- execute plans
- perform reasoning

---

# Service Architecture

```
Planning Service

│

├── Goal Analyzer

├── Planner Selector

├── Planning Coordinator

├── Plan Validator

├── Plan Repository

├── Explanation Manager

├── Replanning Manager

└── Execution Monitor
```

Each component has a single architectural responsibility.

---

# Internal Components

## Goal Analyzer

Analyzes planning objectives.

Responsibilities include:

- goal interpretation
- goal classification
- objective normalization
- planning context generation

---

## Planner Selector

Chooses the most appropriate planning strategy.

Supported planners include:

- HTN Planning
- Graph Planning
- Constraint Planning

Planner selection policies are configurable.

---

## Planning Coordinator

Coordinates planning execution.

Responsibilities include:

- planner invocation
- plan aggregation
- execution monitoring
- planner lifecycle management

---

## Plan Validator

Coordinates validation of candidate plans.

Validation may include:

- constraint verification
- feasibility analysis
- resource availability
- dependency verification

Validation is delegated to specialized services.

---

## Plan Repository

Maintains generated plans.

Each plan contains:

- identifier
- objectives
- tasks
- dependencies
- assumptions
- metadata
- version

---

## Explanation Manager

Produces implementation-independent explanations.

Example explanations include:

- planning strategy
- task decomposition
- dependency chains
- planning assumptions

---

## Replanning Manager

Coordinates replanning when:

- goals change
- constraints change
- execution fails
- environment changes

The service supports incremental replanning.

---

# Planning Pipeline

```
Goal

↓

Goal Analysis

↓

Planner Selection

↓

Specialized Planning

↓

Candidate Plans

↓

Validation

↓

Plan Repository

↓

Return Plans
```

Planning generates candidate plans rather than final decisions.

---

# Planning Strategies

The Planning Service coordinates multiple planning approaches.

Representative strategies include:

```
Hierarchical Task Planning

Graph-Based Planning

Constraint-Based Planning
```

Additional planners may be introduced without modifying the public interface.

---

# Public Interface

The service implements:

```python
context.cognition.planning
```

Representative operations include:

```python
createPlan()

replan()

validate()

explain()

status()

cancel()

history()
```

Applications remain unaware of internal planning implementations.

---

# Configuration

Configurable parameters include:

- planner selection policy
- planning timeout
- replanning policy
- validation policy
- optimization strategy
- explanation level

Configuration conforms to **SERVICE-004**.

---

# Lifecycle

The service lifecycle conforms to **SERVICE-001**.

```
Created

↓

Initialized

↓

Registered

↓

Configured

↓

Running

↓

Stopped
```

---

# Events

Representative events include:

```
PlanningStarted

PlannerSelected

PlanGenerated

PlanValidated

PlanRejected

ReplanningStarted

PlanningCompleted
```

Events conform to **STANDARD-005**.

---

# Telemetry

Representative metrics include:

- planning requests
- planner selection frequency
- planning latency
- replanning count
- validation duration
- successful plans
- failed plans

Telemetry conforms to **STANDARD-005**.

---

# Collaboration

## HTN Planning Service

Generates hierarchical task decompositions.

---

## Graph Planning Service

Generates state-space and dependency-based plans.

---

## Constraint Planning Service

Generates plans satisfying temporal, resource, and logical constraints.

---

## World Model Service

Provides semantic context for planning.

---

## Reasoning Capability

Provides understanding of goals and contextual information.

---

## Decision Capability

Evaluates candidate plans and selects the preferred alternative.

Planning does not choose among alternatives.

---

## Working Memory Service

Maintains the active planning workspace.

---

# Quality Attributes

The Planning Service shall optimize for:

- modularity
- extensibility
- scalability
- explainability
- implementation independence
- planning flexibility

---

# Architectural Requirements

REQ-SVC400-001 [A3]

Implement the Planning Capability contract.

---

REQ-SVC400-002 [A3]

Coordinate multiple planning strategies.

---

REQ-SVC400-003 [A3]

Provide planner-independent interfaces.

---

REQ-SVC400-004 [A3]

Support dynamic planner selection.

---

REQ-SVC400-005 [A3]

Coordinate replanning.

---

REQ-SVC400-006 [A2]

Support pluggable planning services.

---

REQ-SVC400-007 [A2]

Publish lifecycle events.

---

REQ-SVC400-008 [A2]

Publish telemetry.

---

REQ-SVC400-009 [A3]

Maintain complete traceability of generated plans.

---

REQ-SVC400-010 [A3]

All collaboration shall occur exclusively through published capability interfaces.

---

# Acceptance Criteria

| Requirement | Verification |
|-------------|--------------|
| REQ-SVC400-001 | Interface Test |
| REQ-SVC400-002 | Multi-Planner Integration Test |
| REQ-SVC400-003 | API Compliance Test |
| REQ-SVC400-004 | Planner Selection Test |
| REQ-SVC400-005 | Replanning Test |
| REQ-SVC400-006 | Planner Replacement Test |
| REQ-SVC400-007 | Event Test |
| REQ-SVC400-008 | Telemetry Test |
| REQ-SVC400-009 | Traceability Test |
| REQ-SVC400-010 | Architecture Compliance Review |

---

# Related Documents

- CORE-130 — Planning Capability
- CORE-100 — Reasoning Capability
- CORE-140 — Decision Capability
- SERVICE-410 — HTN Planning Service
- SERVICE-420 — Graph Planning Service
- SERVICE-430 — Constraint Planning Service
- SERVICE-300 — World Model Service
- SERVICE-200 — Working Memory Service
- SERVICE-001 — Service Lifecycle
- SERVICE-002 — Service Registration
- SERVICE-003 — Service Discovery
- SERVICE-004 — Service Configuration
- STANDARD-005 — Capability Interface Model
- STANDARD-006 — Capability Implementation Model

---

# Future Extensions

Future implementations may support:

- Temporal Planning
- Probabilistic Planning
- Multi-Agent Planning
- Continuous Planning
- Reactive Planning
- Reinforcement Learning Planners
- Human-in-the-Loop Planning

These enhancements shall preserve the public Planning Capability interface while extending the internal planning ecosystem.

---

# Summary

The Planning Service provides the orchestration layer for planning within the Cognitive Operating System. By coordinating specialized planning services, managing planning strategies, validating candidate plans, and exposing a unified capability interface, it separates planning coordination from planning algorithms. This architecture enables the Cognitive Operating System to evolve with new planning approaches while maintaining a stable, implementation-independent interface for applications and higher-level cognitive capabilities.