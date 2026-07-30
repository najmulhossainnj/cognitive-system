# Cognitive Operating System (COS)

# ADR-002 — Cognitive Broker and Capability Model

**Document ID:** COS-ADR-002

**Version:** 2.0

**Status:** Accepted

**Date:** 2026-07-30

---

# Status

Accepted

This Architecture Decision Record establishes the Cognitive Broker as the single public entry point to cognition and introduces the Capability Model used throughout the Cognitive Operating System.

This ADR supersedes any previous Broker API design.

---

# Purpose

Define the public programming model of the Cognitive Operating System.

This ADR specifies:

- the Cognitive Broker
- Cognitive Capabilities
- capability interfaces
- service implementations
- architectural boundaries

---

# Context

The Cognitive Operating System provides numerous cognitive functions including:

- reasoning
- planning
- learning
- memory
- world modelling
- reflection
- assistance

Allowing modules to communicate directly with individual implementations creates:

- tight coupling
- unstable APIs
- duplicated logic
- poor testability
- implementation leakage

COS requires a stable public interface that remains unchanged as implementations evolve.

---

# Problem Statement

How should applications and modules access cognitive functionality while preserving:

- modularity
- replaceability
- interface stability
- implementation independence
- long-term extensibility

---

# Decision

The Cognitive Operating System adopts the **Capability Model**.

Every cognitive operation shall be accessed through the **Cognitive Broker**.

```
context.cognition
```

The Broker exposes **Capabilities** rather than individual methods.

Each Capability represents a cohesive architectural feature with a stable public interface.

Capabilities are implemented by one or more interchangeable Services.

Applications depend only upon Capability Interfaces.

---

# Architectural Model

```
                 Application
                        │
                        ▼
               Cognitive Context
                        │
                        ▼
               context.cognition
                        │
                 Cognitive Broker
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
 Reasoning         Memory           World Model
 Capability      Capability         Capability
      │                 │                 │
      ▼                 ▼                 ▼
ReasoningSvc     GraphMemorySvc    WorldGraphSvc
```

---

# Capability Model

The Broker organizes cognition into capability namespaces.

```
context.cognition
│
├── reasoning
├── memory
├── world
├── meta
├── learning
├── planning
└── assistant
```

Each capability owns its own public interface.

Example:

```python
context.cognition.reasoning.solve(problem)

context.cognition.memory.query(pattern)

context.cognition.world.validate(scene)

context.cognition.meta.reflect(state)

context.cognition.learning.learn(experience)

context.cognition.planning.plan(goal)

context.cognition.assistant.explain(solution)
```

---

# Capability Responsibilities

## Reasoning

Provides symbolic and algorithmic reasoning.

Examples:

- solve
- compare
- infer
- synthesize
- verify

---

## Memory

Provides access to:

- Working Memory
- Semantic Memory
- Episodic Memory

Examples:

- store
- query
- recall
- search

---

## World Model

Provides active knowledge services.

Examples:

- validate
- query
- match
- explain
- constraints
- hypothesize
- similarity

The World Model is an active cognitive service rather than a passive data repository.

---

## Meta

Provides self-reflection.

Examples:

- reflect
- diagnose
- confidence
- repair

---

## Learning

Provides adaptive learning.

Examples:

- learn
- consolidate
- optimize
- evolve

---

## Planning

Provides planning functionality.

Examples:

- plan
- decompose
- schedule
- evaluate

---

## Assistant

Provides developer-facing cognitive assistance.

Examples:

- explain
- summarize
- debug
- recommend

---

# Services

Capabilities are implemented by Services.

Examples

```
Memory Capability

↓

GraphMemoryService

↓

DistributedMemoryService

↓

InMemoryService
```

Applications shall never depend upon Service implementations.

---

# Public Interfaces

Each Capability exposes a stable Interface.

Example

```
IMemoryCapability

↓

GraphMemoryService
```

Applications depend only upon Interfaces.

Services implement Interfaces.

---

# Architectural Requirements

REQ-BROKER-001 [A3]

Every cognitive operation shall pass through the Cognitive Broker.

---

REQ-BROKER-002 [A3]

Applications shall never invoke Service implementations directly.

---

REQ-BROKER-003 [A3]

Applications shall depend only upon Capability Interfaces.

---

REQ-BROKER-004 [A3]

Capabilities shall remain implementation independent.

---

REQ-BROKER-005 [A2]

The Broker shall propagate execution context.

---

REQ-BROKER-006 [A2]

The Broker shall emit telemetry for every request.

---

REQ-BROKER-007 [A2]

The Broker shall publish lifecycle events.

---

REQ-BROKER-008 [A2]

Capability interfaces shall remain stable across minor releases.

---

REQ-BROKER-009 [A3]

Capabilities shall never expose implementation classes.

---

REQ-BROKER-010 [A3]

Services shall communicate through published Interfaces.

---

# Rationale

The Capability Model provides:

- stable public APIs
- implementation independence
- discoverability
- modularity
- extensibility
- testability
- interface versioning
- dependency isolation

It allows Service implementations to evolve without affecting Applications.

---

# Alternatives Considered

## Direct Service Access

Rejected because it tightly couples Applications to implementations.

---

## Global Service Locator

Rejected because dependencies become implicit and difficult to test.

---

## Flat Broker API

Example

```python
context.cognition.solve()

context.cognition.learn()

context.cognition.query()

context.cognition.reflect()
```

Rejected because the interface grows without structure and becomes increasingly difficult to maintain.

---

# Consequences

Positive

- Stable architecture
- Clean separation of concerns
- Better discoverability
- Easier testing
- Pluggable implementations
- Long-term scalability

Negative

- Additional abstraction layer
- Slight increase in implementation complexity

These trade-offs are acceptable.

---

# Implementation Impact

This ADR requires implementation of:

- Cognitive Broker
- Capability Interfaces
- Service Registry
- Interface Contracts
- Context Propagation
- Telemetry Integration
- Event Integration

---

# Acceptance Criteria

| Requirement | Level |
|-------------|-------|
| REQ-BROKER-001 | A3 |
| REQ-BROKER-002 | A3 |
| REQ-BROKER-003 | A3 |
| REQ-BROKER-004 | A3 |
| REQ-BROKER-005 | A2 |
| REQ-BROKER-006 | A2 |
| REQ-BROKER-007 | A2 |
| REQ-BROKER-008 | A2 |
| REQ-BROKER-009 | A3 |
| REQ-BROKER-010 | A3 |

---

# Related Documents

- COS-STD-001 — Architectural Requirement Levels
- COS-ARCH-001 — Architecture Overview
- COS-ADR-001 — Layered Cognitive Architecture

Future References

- COS-CORE-004 — Cognitive Broker
- COS-CORE-004A — Reasoning Capability
- COS-CORE-004B — Memory Capability
- COS-CORE-004C — World Model Capability
- COS-CORE-004D — Meta-Cognition Capability
- COS-CORE-004E — Learning Capability
- COS-CORE-004F — Planning Capability
- COS-CORE-004G — Assistant Capability

---

# Future Considerations

Future versions of COS may introduce additional Capabilities including:

- Multi-Agent Coordination
- Simulation
- Creativity
- Scientific Discovery
- Autonomous Programming
- Natural Language Interaction

These additions shall extend the Capability Model without modifying the Broker architecture.

---

# Decision Summary

The Cognitive Operating System adopts a Capability-Oriented programming model.

The Cognitive Broker serves as the sole public entry point to cognition.

Capabilities define stable architectural contracts.

Services provide interchangeable implementations.

Applications depend only upon Capability Interfaces.

This architecture preserves modularity, extensibility, interface stability, and long-term maintainability while enabling independent evolution of cognitive capabilities.