# Cognitive Operating System (COS)

# STANDARD-001 — Architectural Requirement Levels (ARL)

Version: 1.0

Status: Approved

Document ID: COS-STD-001

---

# Purpose

This document defines the Architectural Requirement Level (ARL) classification system used throughout the Cognitive Operating System documentation.

Every requirement defined in Foundation, ADR, CORE, SERVICES, APPLICATIONS, SDK, and TEST specifications shall be assigned an Architectural Requirement Level.

This standard establishes the relative strength of architectural requirements and enables consistent implementation, code review, verification, and future evolution.

---

# Scope

This standard applies to:

- Foundation Documents
- Architecture Decision Records (ADRs)
- Core Specifications
- Service Specifications
- Application Specifications
- SDK Specifications
- Test Specifications
- Coding-Agent Instructions

---

# Requirement Levels

The Cognitive Operating System defines four requirement levels.

| Level | Name | Meaning | Violation Allowed |
|--------|------|---------|-------------------|
| A0 | Informational | Background information or implementation notes | Yes |
| A1 | Recommendation | Strong engineering recommendation | Yes, with justification |
| A2 | Required | Mandatory architectural requirement | Only through an approved ADR |
| A3 | Architectural Invariant | Fundamental rule of the Cognitive Operating System | Never |

---

# A0 — Informational

Informational statements provide background context.

They do not define required behavior.

Example:

```text
[A0]

The scheduler currently uses a priority queue.
```

Informational statements may change without architectural review.

---

# A1 — Recommendation

Recommendations describe preferred engineering practices.

Alternative implementations are permitted when justified.

Example:

```text
[A1]

Services should prefer immutable data structures.
```

Recommendations improve consistency but are not mandatory.

---

# A2 — Required

Required requirements define mandatory architectural behavior.

Implementations shall satisfy all A2 requirements unless an Architecture Decision Record explicitly approves an exception.

Example:

```text
[A2]

Every Service shall emit telemetry events.
```

Violations require architectural review.

---

# A3 — Architectural Invariant

Architectural Invariants define the fundamental structure of the Cognitive Operating System.

These rules shall never be violated.

Changing an A3 requirement requires a new major architecture revision.

Example:

```text
[A3]

Applications shall never access Kernel internals.
```

Architectural Invariants define the identity of COS.

---

# Requirement Identifiers

Every normative requirement shall receive a unique identifier.

Format:

```
REQ-<CATEGORY>-NNN
```

Examples:

```
REQ-ARCH-001

REQ-MEM-004

REQ-BROKER-012

REQ-LEARN-007
```

Requirement identifiers shall remain stable across document revisions.

---

# Usage

Requirements shall be written using the following format.

Example:

```
REQ-ARCH-001 [A3]

The Cognitive Kernel shall remain domain-independent.
```

Example:

```
REQ-BROKER-004 [A2]

The Cognitive Broker shall emit telemetry for every request.
```

Example:

```
REQ-META-002 [A1]

Reflection reports should include confidence estimates.
```

---

# Relationship to Testing

Every A2 and A3 requirement shall have one or more verification tests.

Example:

```
Requirement

↓

Implementation

↓

Unit Test

↓

Integration Test

↓

Acceptance Test
```

Traceability shall be maintained throughout the repository.

---

# Relationship to ADRs

Architecture Decision Records define or modify architectural requirements.

An ADR may:

- Introduce a new requirement.
- Modify an A2 requirement.
- Deprecate an A1 recommendation.

An ADR shall not invalidate an A3 Architectural Invariant without creating a new architecture version.

---

# Coding-Agent Guidance

Coding agents shall interpret requirement levels as follows.

A3

- Never violate.
- Report any conflict immediately.

A2

- Implement completely.
- Flag any missing implementation.

A1

- Implement when practical.
- Recommend improvements.

A0

- Ignore during implementation unless specifically requested.

---

# Review Checklist

Every document shall satisfy the following.

✓ Normative requirements are identified.

✓ Every requirement has an ARL.

✓ A2 and A3 requirements are testable.

✓ Requirement identifiers are unique.

✓ Requirement wording is unambiguous.

---

# Summary

Architectural Requirement Levels establish a consistent method for classifying the strength of architectural requirements throughout the Cognitive Operating System.

This standard provides the foundation for architecture governance, implementation traceability, testing, code review, and future architectural evolution.