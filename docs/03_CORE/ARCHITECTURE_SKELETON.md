# Architecture Skeleton

This section documents all interface specifications for the Cognitive Operating System.

## Interface Overview

The COS architecture is organized into several layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    Applications                               │
├─────────────────────────────────────────────────────────────┤
│              Cognitive Context & Broker                      │
├─────────────────────────────────────────────────────────────┤
│                  Core Capabilities                           │
│  Reasoning │ Memory │ World │ Planning │ Decision │ Learning  │
│            │ Meta-Cognition │ Assistant                      │
├─────────────────────────────────────────────────────────────┤
│                     Services                                 │
│    (Implementations of Core Capabilities)                    │
├─────────────────────────────────────────────────────────────┤
│                     Execution                                │
│           Pipeline Engine │ Task Manager                      │
├─────────────────────────────────────────────────────────────┤
│                     Runtime                                  │
│ Registry │ DI │ Event Bus │ Scheduler │ Configuration        │
└─────────────────────────────────────────────────────────────┘
```

## Core Capabilities

Core capabilities define the stable public interfaces for cognitive functionality.

### Foundational Capabilities

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IReasoningCapability` | Problem solving and inference | [CORE-100](CORE/CORE-100_REASONING_CAPABILITY.md) |
| `IMemoryCapability` | Knowledge storage and retrieval | [CORE-110](CORE/CORE-110_MEMORY_CAPABILITY.md) |
| `IWorldModelCapability` | Semantic representation | [CORE-120](CORE/CORE-120_WORLD_MODEL_CAPABILITY.md) |

### Higher Cognitive Capabilities

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IPlanningCapability` | Goal decomposition and plan generation | [CORE-130](CORE/CORE-130_PLANNING_CAPABILITY.md) |
| `IDecisionCapability` | Alternative selection | [CORE-140](CORE/CORE-140_DECISION_CAPABILITY.md) |
| `ILearningCapability` | Experience-based improvement | [CORE-150](CORE/CORE-150_LEARNING_CAPABILITY.md) |
| `IMetaCognitionCapability` | Self-observation and regulation | [CORE-160](CORE/CORE-160_META_COGNITION_CAPABILITY.md) |
| `IAssistantCapability` | Human-facing interface | [CORE-170](CORE/CORE-170_ASSISTANT_CAPABILITY.md) |

## Execution Interfaces

| Interface | Description | Specification |
|----------|-------------|--------------|
| `ICognitivePipeline` | Cognitive workflow orchestration | [EXEC-110](../EXECUTION/EXEC-110_Reasoning_Pipeline.md) |
| `IRequestLifecycle` | Request processing lifecycle | [EXEC-100](../EXECUTION/EXEC-100_Request_Lifecycle.md) |
| `ICognitiveContext` | Primary execution context | [CORE-004](CORE/CORE-004_COGNITIVE_CONTEXT.md) |

## Runtime Interfaces

Runtime interfaces provide infrastructure services.

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IServiceRegistry` | Service registration and discovery | [RUNTIME-001](../RUNTIME/RUNTIME-001_SERVICE_REGISTRY.md) |
| `IDependencyInjection` | Dependency resolution | [RUNTIME-002](../RUNTIME/RUNTIME-002_DEPENDENCY_INJECTION.md) |
| `IEventBus` | Event publication/subscription | [RUNTIME-003](../RUNTIME/RUNTIME-003_EVENT_BUS.md) |
| `IScheduler` | Task scheduling | [RUNTIME-004](../RUNTIME/RUNTIME-004_SCHEDULER.md) |
| `IPipelineEngine` | Workflow orchestration | [RUNTIME-005](../RUNTIME/RUNTIME-005_PIPELINE_ENGINE.md) |
| `ITaskManager` | Task lifecycle | [RUNTIME-006](../RUNTIME/RUNTIME-006_TASK_MANAGER.md) |
| `IResourceManager` | Resource allocation | [RUNTIME-007](../RUNTIME/RUNTIME-007_RESOURCE_MANAGER.md) |
| `IPluginManager` | Plugin management | [RUNTIME-008](../RUNTIME/RUNTIME-008_PLUGIN_MANAGER.md) |
| `IConfigurationManager` | Configuration management | [RUNTIME-009](../RUNTIME/RUNTIME-009_CONFIGURATION_MANAGER.md) |
| `IRuntimeLifecycle` | Runtime startup/shutdown | [RUNTIME-010](../RUNTIME/RUNTIME-010_RUNTIME_LIFECYCLE.md) |

## Service Interfaces

Services implement core capabilities.

### Reasoning Services

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IReasoningService` | Base reasoning interface | [SERVICE-100](../SERVICES/SERVICE-100_REASONING_SERVICE.md) |

### Memory Services

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IWorkingMemoryService` | Transient workspace | [SERVICE-200](../SERVICES/SERVICE-200_WORKING_MEMORY_SERVICE.md) |
| `ISemanticMemoryService` | Persistent concepts | [SERVICE-210](../SERVICES/SERVICE-210_SEMANTIC_MEMORY_SERVICE.md) |
| `IEpisodicMemoryService` | Historical experiences | [SERVICE-220](../SERVICES/SERVICE-220_EPISODIC_MEMORY_SERVICE.md) |
| `IMemoryConsolidationService` | Memory organization | [SERVICE-230](../SERVICES/SERVICE-230_MEMORY_CONSOLIDATION_SERVICE.md) |

### World Model Services

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IWorldModelService` | Semantic orchestration | [SERVICE-300](../SERVICES/SERVICE-300_WORLD_MODEL_SERVICE.md) |
| `IKnowledgeGraphService` | Graph storage | [SERVICE-310](../SERVICES/SERVICE-310_KNOWLEDGE_GRAPH_SERVICE.md) |
| `ISemanticQueryService` | Semantic queries | [SERVICE-320](../SERVICES/SERVICE-320_SEMANTIC_QUERY_SERVICE.md) |
| `IConstraintValidationService` | Constraint checking | [SERVICE-330](../SERVICES/SERVICE-330_CONSTRAINT_VALIDATION_SERVICE.md) |
| `IPatternMatchingService` | Pattern detection | [SERVICE-340](../SERVICES/SERVICE-340_PATTERN_MATCHING_SERVICE.md) |

### Planning Services

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IPlanningService` | Base planning | [SERVICE-400](../SERVICES/SERVICE-400_PLANNING_SERVICE.md) |
| `IHTNPlanningService` | Hierarchical task network | [SERVICE-410](../SERVICES/SERVICE-410_HTN_PLANNING_SERVICE.md) |
| `IGraphPlanningService` | Graph-based planning | [SERVICE-420](../SERVICES/SERVICE-420_GRAPH_PLANNING_SERVICE.md) |
| `IConstraintPlanningService` | Constraint-based planning | [SERVICE-430](../SERVICES/SERVICE-430_CONSTRAINT_PLANNING_SERVICE.md) |

### Decision Services

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IDecisionService` | Base decision | [SERVICE-500](../SERVICES/SERVICE-500_DECISION_SERVICE.md) |
| `IUtilityDecisionService` | Utility-based selection | [SERVICE-510](../SERVICES/SERVICE-510_UTILITY_DECISION_SERVICE.md) |
| `IPolicyEngineService` | Policy-based decisions | [SERVICE-520](../SERVICES/SERVICE-520_POLICY_ENGINE_SERVICE.md) |
| `IRiskAssessmentService` | Risk evaluation | [SERVICE-530](../SERVICES/SERVICE-530_RISK_ASSESSMENT_SERVICE.md) |

### Learning Services

| Interface | Description | Specification |
|----------|-------------|--------------|
| `ILearningService` | Base learning | [SERVICE-600](../SERVICES/SERVICE-600_LEARNING_SERVICE.md) |
| `IExperienceLearningService` | Experience-based learning | [SERVICE-610](../SERVICES/SERVICE-610_EXPERIENCE_LEARNING_SERVICE.md) |
| `IHeuristicLearningService` | Heuristic refinement | [SERVICE-620](../SERVICES/SERVICE-620_HEURISTIC_LEARNING_SERVICE.md) |
| `IPolicyLearningService` | Policy improvement | [SERVICE-630](../SERVICES/SERVICE-630_POLICY_LEARNING_SERVICE.md) |

### Meta-Cognition Services

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IMetaCognitionService` | Base meta-cognition | [SERVICE-700](../SERVICES/SERVICE-700_META_COGNITION_SERVICE.md) |
| `IReflectionService` | Reasoning reflection | [SERVICE-710](../SERVICES/SERVICE-710_REFLECTION_SERVICE.md) |
| `IConfidenceEstimationService` | Confidence estimation | [SERVICE-720](../SERVICES/SERVICE-720_CONFIDENCE_ESTIMATION_SERVICE.md) |

### Assistant Services

| Interface | Description | Specification |
|----------|-------------|--------------|
| `IAssistantService` | Base assistant | [SERVICE-800](../SERVICES/SERVICE-800_ASSISTANT_SERVICE.md) |
| `IExplanationEngineService` | Explanation generation | [SERVICE-810](../SERVICES/SERVICE-810_EXPLANATION_ENGINE_SERVICE.md) |
| `ITraceVisualizationService` | Trace visualization | [SERVICE-820](../SERVICES/SERVICE-820_TRACE_VISUALIZATION_SERVICE.md) |

## Shared Models

All interfaces use shared Pydantic models defined in `cos/shared/models.py`.

See [Shared Models Reference](SHARED_MODELS.md) for complete model documentation.

## Implementation Status

| Layer | Status |
|-------|--------|
| Core Capabilities | Implemented (Phase 1) |
| Execution | Implemented (Phase 1) |
| Runtime | Implemented (Phase 1) |
| Services | Implemented (Phase 1) |
| Business Logic | Pending (Phases 3-11) |
