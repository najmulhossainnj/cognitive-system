# COS Implementation Guidance

## Preserving Architectural Integrity During Implementation

**Document ID:** COS-IMPLEMENTATION-001

**Version:** 1.0

**Status:** Architecture Guidance

---

# Purpose

This document defines how the Cognitive Operating System (COS) should be implemented so that the codebase remains faithful to the architectural specifications.

While individual services may be implemented independently, the runtime architecture, execution pipelines, and application boundaries **must not be bypassed**.

This document serves as an implementation guide for coding agents and developers.

---

# Core Principle

The Cognitive Operating System is **not** a collection of AI services.

It is a layered operating system.

Applications must never orchestrate cognition directly.

Instead, applications submit requests to the Runtime, and the Runtime executes the Cognitive Pipelines.

The intended architecture is:

```text
Applications
        │
        ▼
Runtime
        │
        ▼
Pipeline Engine
        │
        ▼
Execution Pipelines
        │
        ▼
Cognitive Services
        │
        ▼
Infrastructure
```

---

# Architectural Layers

```
┌──────────────────────────┐
│ Applications             │
│ ARC Agent                │
│ Chat Agent               │
│ Coding Agent             │
│ Research Agent           │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Runtime                  │
│ Service Registry          │
│ Dependency Injection      │
│ Event Bus                │
│ Scheduler                │
│ Pipeline Engine          │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Execution Pipelines       │
│ Request Lifecycle         │
│ Reasoning                │
│ Planning                 │
│ Decision                 │
│ Learning                 │
│ Meta                     │
│ Assistant                │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Cognitive Services        │
│ Memory                   │
│ Reasoning                │
│ Planning                │
│ Decision                │
│ Learning                │
│ World Model             │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Infrastructure          │
└──────────────────────────┘
```

Every implementation should preserve this separation.

---

# Applications Must Remain Thin

Applications are orchestration entry points.

Their responsibilities are limited to:

- loading application-specific inputs
- validating requests
- converting inputs into COS Requests
- submitting requests to the Runtime
- formatting responses

Applications shall **not**:

- call reasoning services directly
- coordinate planning
- perform learning
- invoke memory services
- manage execution order

The Runtime owns execution.

---

# Incorrect Architecture

The following pattern bypasses the Runtime:

```python
agent = ARCAgent(...)

solution = await agent.solve(task)

reasoning.solve(...)
planning.generate(...)
decision.decide(...)
```

Although functional, this violates the architectural design.

Applications become coupled to Cognitive Services.

Execution Pipelines are bypassed.

Runtime responsibilities disappear.

This pattern shall not be used outside isolated unit tests.

---

# Correct Architecture

Applications create standardized requests.

```python
request = agent.prepare_request(task)

result = await runtime.execute(request)

solution = agent.format_response(result)
```

Execution is delegated to the Runtime.

The Runtime decides which pipelines execute.

---

# Runtime Responsibilities

The Runtime owns:

- dependency injection
- service lifecycle
- scheduling
- execution order
- event publication
- resource management
- pipeline execution
- configuration

Applications must never replicate these responsibilities.

---

# Pipeline Ownership

Applications do not call services.

Applications call the Runtime.

The Runtime invokes the Pipeline Engine.

The Pipeline Engine invokes Execution Pipelines.

Execution Pipelines coordinate Cognitive Services.

```text
Application
    ↓
Runtime
    ↓
Pipeline Engine
    ↓
Reasoning Pipeline
    ↓
Planning Pipeline
    ↓
Decision Pipeline
    ↓
Learning Pipeline
    ↓
Meta Pipeline
    ↓
Assistant Pipeline
```

This execution order must remain implementation independent.

---

# Dependency Injection

Services shall never be instantiated manually inside applications.

Incorrect:

```python
reasoning = ReasoningService()
planning = PlanningService()
```

Correct:

```python
reasoning = container.get(ReasoningService)
planning = container.get(PlanningService)
```

or

```python
reasoning = runtime.reasoning
```

Service creation belongs to the Dependency Injection container.

---

# Service Registry

Every Cognitive Service shall register itself with the Runtime.

Applications shall discover services through the Runtime.

Applications shall never construct services manually.

---

# World Model Design

The World Model is an architectural subsystem.

It is **not** a single implementation.

Internally it consists of:

```text
World Model
    │
    ├── Knowledge Graph Service
    │
    ├── Semantic Query Service
    │
    ├── Pattern Matching Service
    │
    └── Constraint Validation Service
```

A WorldModelService may exist as a façade.

However, the subsystem shall preserve these internal boundaries.

---

# Reasoning Service Design

The Reasoning Service is a coordinator.

It does not implement every reasoning algorithm itself.

Instead:

```text
Reasoning Service
    │
    ├── Rule-Based Reasoner
    │
    ├── Symbolic Reasoner
    │
    ├── LLM Reasoner
    │
    ├── Probabilistic Reasoner
    │
    └── Hybrid Reasoner
```

The coordinator delegates work to specialized reasoning engines.

---

# ARC Agent Responsibilities

The ARC Agent is intentionally lightweight.

Its responsibilities are:

- load ARC JSON
- validate dataset
- create COS Request
- submit request to Runtime
- receive response
- convert response into ARC grid

It shall not:

- execute reasoning
- plan solutions
- access memory directly
- invoke learning
- perform decision making

These belong to the Cognitive Operating System.

---

# Intended ARC Execution Flow

```text
ARC JSON
    ↓
APP-140 ARC Agent
    ↓
Request Builder
    ↓
Runtime
    ↓
Pipeline Engine
    ↓
Request Lifecycle
    ↓
Reasoning Pipeline
    ↓
Planning Pipeline
    ↓
Decision Pipeline
    ↓
Learning Pipeline
    ↓
Meta Pipeline
    ↓
Assistant Pipeline
    ↓
Response
    ↓
ARC Output Grid
```

This is the canonical execution flow.

---

# Public Interfaces

Applications should interact only with the Runtime.

Example:

```python
request = agent.prepare_request(task)

response = await runtime.execute(request)

solution = agent.format_response(response)
```

Applications should never invoke individual Cognitive Services directly.

---

# Unit Testing Exception

Direct service construction is acceptable only for isolated unit tests.

Example:

```python
matcher = PatternMatchingService()

patterns = await matcher.detect_patterns(grid)
```

This exception exists solely for testing individual components.

Production code shall always execute through the Runtime.

---

# Design Principles

Every implementation should preserve the following principles:

- [ ] Thin Applications
- [ ] Runtime-owned orchestration
- [ ] Pipeline-based execution
- [ ] Dependency Injection
- [ ] Service Registry
- [ ] Event-driven coordination
- [ ] Interface-first design
- [ ] Provider independence
- [ ] Modular Cognitive Services
- [ ] Replaceable implementations

---

# Implementation Checklist

Before merging any implementation, verify the following:

- [ ] Applications do not instantiate Cognitive Services.
- [ ] Applications submit requests to the Runtime.
- [ ] Runtime owns orchestration.
- [ ] Pipeline Engine controls execution order.
- [ ] Execution Pipelines coordinate Cognitive Services.
- [ ] Services are resolved through Dependency Injection.
- [ ] Services are registered in the Service Registry.
- [ ] Cognitive Services remain independent.
- [ ] Public interfaces remain stable.
- [ ] Infrastructure remains replaceable.

---

# Summary

The Cognitive Operating System is designed as a layered cognitive platform rather than a collection of independent AI services.

Applications provide domain-specific entry points.

The Runtime controls execution.

Execution Pipelines coordinate cognition.

Cognitive Services perform specialized intelligence.

Infrastructure provides reusable technical capabilities.

Maintaining these boundaries ensures that the system remains modular, scalable, explainable, testable, and faithful to the architectural specifications while allowing new applications, services, and reasoning engines to be added without redesigning the platform.

---

# Example: Thin ARC Agent

## Application Layer (Thin)

```python
# cos/apps/arc_agent/arc_agent.py

class ARCAgent:
    """Thin application - only prepares requests and formats responses."""

    def prepare_request(self, task_data: dict) -> ARCRequest:
        """Load and validate task data."""
        # Validate required fields
        if "train" not in task_data or "test" not in task_data:
            raise ValueError("Task must have 'train' and 'test' fields")
        
        # Build standardized request
        return ARCRequestBuilder.from_json(task_data)

    async def execute(self, request: ARCRequest) -> ARCResponse:
        """Submit to Runtime for execution."""
        return await self._pipeline.execute(request)

    def format_response(self, response: ARCResponse) -> dict:
        """Format response for application use."""
        return {
            "output": response.result.primary_output,
            "confidence": response.confidence,
        }
```

## Pipeline Layer (Runtime)

```python
# cos/apps/arc_agent/arc_pipeline.py

class ARCCognitivePipeline:
    """Runtime-executable pipeline - coordinates cognitive services."""

    async def execute(self, request: ARCRequest) -> ARCResponse:
        """Execute through cognitive services."""
        
        # Stage 1: Parse
        training_pairs = await self._grid_interpreter.interpret(...)
        
        # Stage 2: Reason (via Reasoning Service)
        patterns = await self._broker.reasoning.solve(...)
        
        # Stage 3: Plan (via Planning Service)
        plan = await self._broker.planning.plan(...)
        
        # Stage 4: Decide (via Decision Service)
        solution = await self._broker.decision.decide(...)
        
        # Stage 5: Learn (via Memory Services)
        if solution.confidence > threshold:
            await self._broker.memory.store(...)
        
        # Stage 6: Reflect (via Meta-Cognition)
        await self._broker.meta.observe(...)
        
        return response
```

## Usage

```python
# Application code
agent = ARCAgent()

# 1. Prepare request
request = agent.prepare_request(task_data)

# 2. Execute via Runtime
response = await agent.execute(request)

# 3. Format response
solution = agent.format_response(response)
```

---

# References

- [COS Capabilities](../01_OVERVIEW/COS_CAPABILITIES.md)
- [Architecture Skeleton](PHASE_1_ARCHITECTURE_SKELETON.md)
- [Runtime Kernel](PHASE_2_RUNTIME_KERNEL.md)
- [Core Services](PHASE_3_CORE_SERVICES.md)
- [Integration](PHASE_4_INTEGRATION_ORCHESTRATION.md)
