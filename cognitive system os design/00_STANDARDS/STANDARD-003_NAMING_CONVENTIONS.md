# Cognitive Operating System (COS)

# STANDARD-003 — Naming Conventions

**Document ID:** COS-STD-003

**Version:** 1.0

**Status:** Approved

---

# Purpose

This standard defines naming conventions used throughout the Cognitive Operating System.

Consistent naming improves readability, traceability, automation, and long-term maintainability.

---

# Repository Naming

Directories use uppercase prefixes.

Examples

```
00_STANDARDS
01_FOUNDATION
02_ADR
03_CORE
04_SERVICES
05_APPLICATIONS
06_SDK
07_TESTING
08_EXAMPLES
09_APPENDICES
```

---

# Document Naming

Format

```
CATEGORY-NNN_DESCRIPTION.md
```

Examples

```
ADR-002_COGNITIVE_BROKER.md

CORE-004_COGNITIVE_BROKER.md

SVC-003_REASONING_SERVICE.md
```

---

# Document IDs

Every specification receives a permanent identifier.

Examples

```
COS-ADR-001

COS-CORE-004

COS-SVC-003

COS-APP-001

COS-SDK-002
```

Document IDs shall never change.

---

# Requirement IDs

```
REQ-ARCH-001

REQ-BROKER-004

REQ-MEM-002

REQ-WORLD-003
```

Requirements are unique.

Requirement IDs are never reused.

---

# Test IDs

```
TEST-ARCH-001

TEST-MEM-003

TEST-WORLD-002
```

---

# Interface Naming

Interfaces begin with "I".

Examples

```
IMemoryCapability

IReasoningCapability

ICognitiveBroker

IEventBus
```

---

# Capability Naming

Capabilities describe public functionality.

Examples

```
Memory Capability

Planning Capability

Reasoning Capability

World Model Capability
```

---

# Service Naming

Services implement capabilities.

Suffix

```
Service
```

Examples

```
GraphMemoryService

PlanningService

RuleReasoningService
```

---

# Event Naming

Events use the past tense.

Examples

```
MemoryStored

TaskCompleted

ReflectionFinished

ConstraintViolated
```

---

# Class Naming

Classes use PascalCase.

Variables use snake_case.

Constants use UPPER_CASE.

---

# File Naming

Markdown

```
UPPER_CASE_WITH_UNDERSCORES.md
```

Python

```
snake_case.py
```

---

# Summary

Consistent naming enables reliable tooling, documentation generation, and architectural traceability.