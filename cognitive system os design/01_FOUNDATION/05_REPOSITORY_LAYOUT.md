# Cognitive Operating System (COS)

# Repository Layout

Version: 1.0

Status: Approved

Document ID: COS-REPO-001

---

# Purpose

This document defines the canonical repository organization of the Cognitive Operating System.

Every source file, specification, test, and example shall conform to this layout.

---

# Repository Structure

```
COS/

docs/

src/

tests/

examples/

benchmarks/

research/

scripts/

tools/
```

---

# Documentation

```
docs/

01_FOUNDATION/

02_ADR/

03_CORE/

04_SERVICES/

05_APPLICATIONS/

06_SDK/

07_RESEARCH/
```

Documentation mirrors implementation.

---

# Source Code

```
src/

kernel/

broker/

services/

applications/

sdk/

shared/

config/

telemetry/
```

---

# Kernel

```
kernel/

executive/

scheduler/

memory/

attention/

context/

events/

telemetry/

configuration/
```

Kernel components must never depend upon services or applications.

---

# Broker

```
broker/

cognitive_broker.py

knowledge_router.py

service_dispatcher.py

request_pipeline.py
```

The Broker is the public façade of COS.

---

# Services

```
services/

reasoning/

meta/

learning/

assistant/
```

Each service is independently testable.

---

# Applications

```
applications/

arc/

robotics/

planning/

mathematics/
```

Applications depend only on published APIs.

---

# SDK

```
sdk/

module_sdk/

plugin_sdk/

domain_sdk/

memory_sdk/

testing_sdk/
```

---

# Tests

```
tests/

unit/

integration/

performance/

regression/

acceptance/
```

Every public interface must have corresponding unit and integration tests.

---

# Benchmarks

```
benchmarks/

arc/

performance/

memory/

scheduler/
```

Benchmarks measure system evolution over time.

---

# Research

```
research/

roadmap/

experiments/

papers/

prototypes/
```

Experimental work never directly modifies production code.

---

# Dependency Rules

```
Applications

↓

Services

↓

Broker

↓

Kernel

↓

Shared
```

Dependencies must always point downward.

---

# Repository Standards

Every directory shall contain:

README.md

Public Interfaces

Tests

Documentation

Examples

---

# Naming Conventions

Directories:

snake_case

Classes:

PascalCase

Interfaces:

IInterfaceName

Modules:

snake_case.py

Specifications:

UPPER_CASE.md

---

# Future Growth

Future services, applications, and SDK components shall extend this structure rather than introducing new top-level directories.

Repository consistency is considered a core architectural requirement.