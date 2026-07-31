# Cognitive Operating System (COS)

A reusable cognitive architecture for domain-independent reasoning.

## Overview

The Cognitive Operating System is a layered cognitive platform that separates infrastructure, cognition, and applications. It provides:

- **Deterministic execution** - Every operation is reproducible and traceable
- **Explainable reasoning** - Every decision can be explained
- **Modular cognitive services** - Services are independently testable
- **Long-term evolution** - Architecture supports future extensions

## Architecture

```
Applications
      |
      v
Cognitive Context
      |
      v
Cognitive Broker
      |
      v
Cognitive Services
      |
      v
Cognitive Kernel
```

## Installation

```bash
pip install cos
```

## Quick Start

```python
from cos import CognitiveContext

# Create a context
context = CognitiveContext.create()

# Use cognitive capabilities
result = context.cognition.reasoning.solve(task)
explanation = context.cognition.assistant.explain(result)
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/cos.git
cd cos

# Install dependencies
uv sync --all-extras --dev

# Run tests
pytest tests/

# Run linting
ruff check .
ruff format .
```

### Project Structure

```
cos/
├── kernel/          # Deterministic runtime infrastructure
│   ├── executive/   # Task execution control
│   ├── scheduler/   # Task scheduling
│   ├── events/      # Event bus
│   ├── telemetry/   # Observability
│   └── configuration/
├── broker/          # Cognitive Broker (public facade)
├── services/         # Cognitive capability implementations
│   ├── reasoning/
│   ├── memory/
│   ├── meta/
│   └── learning/
├── applications/    # Domain-specific applications
│   ├── arc/         # ARC solver application
│   └── ...
└── sdk/             # Software development kits
```

## Phases

See [development_roadmap.txt](development_roadmap.txt) for the complete development plan:

- Phase 0: Repository Foundation
- Phase 1: Architecture Skeleton
- Phase 2: Runtime
- Phase 3-18: Core services, applications, and production

## Contributing

1. Read the [Developer Guide](docs/01_FOUNDATION/06_DEVELOPER_GUIDE.md)
2. Follow the [Coding Standards](docs/00_STANDARDS/)
3. Submit changes through pull requests

## License

MIT License - see LICENSE file for details.
