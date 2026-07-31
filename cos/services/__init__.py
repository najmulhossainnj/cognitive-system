"""Services module for the Cognitive Operating System.

This module provides cognitive services including:
- Reasoning Service
- Memory Services (Working, Semantic, Episodic)
- World Model Services
- Planning Services
- Decision Services
- Learning Services
- Meta-Cognition Services
- Assistant Services
"""

from cos.services.base import ServiceBase, IService, ServiceStatus
from cos.services.reasoning.reasoning_service import (
    ReasoningService,
    IReasoningService,
)
from cos.services.memory.memory_service import (
    WorkingMemoryService,
    IWorkingMemoryService,
    SemanticMemoryService,
    ISemanticMemoryService,
    EpisodicMemoryService,
    IEpisodicMemoryService,
    MemoryConsolidationService,
    IMemoryConsolidationService,
)
from cos.services.world.world_service import (
    WorldModelService,
    IWorldModelService,
    KnowledgeGraphService,
    IKnowledgeGraphService,
    SemanticQueryService,
    ISemanticQueryService,
    ConstraintValidationService,
    IConstraintValidationService,
    PatternMatchingService,
    IPatternMatchingService,
)
from cos.services.planning.planning_service import (
    PlanningService,
    IPlanningService,
    HTNPlanningService,
    IHTNPlanningService,
    GraphPlanningService,
    IGraphPlanningService,
    ConstraintPlanningService,
    IConstraintPlanningService,
)
from cos.services.decision.decision_service import (
    DecisionService,
    IDecisionService,
    UtilityDecisionService,
    IUtilityDecisionService,
    PolicyEngineService,
    IPolicyEngineService,
    RiskAssessmentService,
    IRiskAssessmentService,
)
from cos.services.learning.learning_service import (
    LearningService,
    ILearningService,
    ExperienceLearningService,
    IExperienceLearningService,
    HeuristicLearningService,
    IHeuristicLearningService,
    PolicyLearningService,
    IPolicyLearningService,
)
from cos.services.meta.meta_service import (
    MetaCognitionService,
    IMetaCognitionService,
    ReflectionService,
    IReflectionService,
    ConfidenceEstimationService,
    IConfidenceEstimationService,
)
from cos.services.assistant.assistant_service import (
    AssistantService,
    IAssistantService,
    ExplanationEngineService,
    IExplanationEngineService,
    TraceVisualizationService,
    ITraceVisualizationService,
)

__all__ = [
    # Base
    "ServiceBase",
    "IService",
    "ServiceStatus",
    # Reasoning
    "ReasoningService",
    "IReasoningService",
    # Memory
    "WorkingMemoryService",
    "IWorkingMemoryService",
    "SemanticMemoryService",
    "ISemanticMemoryService",
    "EpisodicMemoryService",
    "IEpisodicMemoryService",
    "MemoryConsolidationService",
    "IMemoryConsolidationService",
    # World Model
    "WorldModelService",
    "IWorldModelService",
    "KnowledgeGraphService",
    "IKnowledgeGraphService",
    "SemanticQueryService",
    "ISemanticQueryService",
    "ConstraintValidationService",
    "IConstraintValidationService",
    "PatternMatchingService",
    "IPatternMatchingService",
    # Planning
    "PlanningService",
    "IPlanningService",
    "HTNPlanningService",
    "IHTNPlanningService",
    "GraphPlanningService",
    "IGraphPlanningService",
    "ConstraintPlanningService",
    "IConstraintPlanningService",
    # Decision
    "DecisionService",
    "IDecisionService",
    "UtilityDecisionService",
    "IUtilityDecisionService",
    "PolicyEngineService",
    "IPolicyEngineService",
    "RiskAssessmentService",
    "IRiskAssessmentService",
    # Learning
    "LearningService",
    "ILearningService",
    "ExperienceLearningService",
    "IExperienceLearningService",
    "HeuristicLearningService",
    "IHeuristicLearningService",
    "PolicyLearningService",
    "IPolicyLearningService",
    # Meta-Cognition
    "MetaCognitionService",
    "IMetaCognitionService",
    "ReflectionService",
    "IReflectionService",
    "ConfidenceEstimationService",
    "IConfidenceEstimationService",
    # Assistant
    "AssistantService",
    "IAssistantService",
    "ExplanationEngineService",
    "IExplanationEngineService",
    "TraceVisualizationService",
    "ITraceVisualizationService",
]
