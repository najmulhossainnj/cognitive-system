# Cognitive Operating System (COS)

# STANDARD-002 — Document Template Standard

**Document ID:** COS-STD-002

**Version:** 1.0

**Status:** Approved

---

# Purpose

This standard defines the mandatory structure for all specification documents within the Cognitive Operating System repository.

The objective is to ensure consistency, readability, traceability, and compatibility with automated tooling, documentation generation, and AI coding agents.

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

---

# Document Structure

Every specification shall follow the same high-level structure.

```
Title

Document Metadata

Purpose

Scope

Context (if applicable)

Architecture / Design

Requirements

Implementation Guidance

Acceptance Criteria

Related Documents

Future Considerations

Summary
```

Sections may be omitted only if they are not applicable.

---

# Document Metadata

Every document shall begin with:

```
Title

Document ID

Version

Status

Date
```

Example

```
Document ID: COS-CORE-004

Version: 1.0

Status: Draft
```

---

# Requirements

Normative statements shall:

- Use REQ identifiers
- Include an Architectural Requirement Level (ARL)
- Be testable
- Use unambiguous language

Example

```
REQ-MEM-001 [A3]

Applications shall access memory only through the Memory Capability.
```

---

# Acceptance Criteria

Every document defining A2 or A3 requirements shall include measurable acceptance criteria.

Example

| Requirement | Verification |
|-------------|--------------|
| REQ-MEM-001 | Integration Test |
| REQ-MEM-002 | Unit Test |

---

# Related Documents

Every document shall reference related specifications using Document IDs.

Example

- COS-ADR-002
- COS-CORE-004
- COS-SVC-001

---

# Writing Guidelines

Specifications shall:

- use normative language
- avoid ambiguity
- avoid implementation-specific details unless required
- distinguish requirements from recommendations

Preferred terminology:

- shall
- should
- may

Avoid:

- probably
- usually
- maybe
- might

---

# Markdown Guidelines

Documents shall:

- Use ATX headings (`#`)
- Use fenced code blocks
- Use tables for structured data
- Use ASCII diagrams where practical
- Avoid HTML

---

# AI Compatibility

Documents shall be structured so they can be consumed by:

- AI coding agents
- Documentation generators
- Static analysis tools
- Requirement tracing systems

---

# Summary

This standard defines the canonical document structure for all Cognitive Operating System specifications.