"""Cognitive Broker - Unified cognitive facade of the Cognitive Operating System."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.services.assistant.assistant_service import (
    AssistantService,
    ExplanationEngineService,
    TraceVisualizationService,
)
from cos.services.decision.decision_service import (
    DecisionService,
    PolicyEngineService,
    RiskAssessmentService,
    UtilityDecisionService,
)
from cos.services.learning.learning_service import (
    ExperienceLearningService,
    HeuristicLearningService,
    LearningService,
    PolicyLearningService,
)
from cos.services.memory.memory_service import (
    EpisodicMemoryService,
    MemoryConsolidationService,
    SemanticMemoryService,
    WorkingMemoryService,
)
from cos.services.meta.meta_service import (
    ConfidenceEstimationService,
    MetaCognitionService,
    ReflectionService,
)
from cos.services.planning.planning_service import (
    ConstraintPlanningService,
    GraphPlanningService,
    HTNPlanningService,
    PlanningService,
)
from cos.services.reasoning.reasoning_service import ReasoningService
from cos.services.world.world_service import (
    ConstraintValidationService,
    KnowledgeGraphService,
    PatternMatchingService,
    SemanticQueryService,
    WorldModelService,
)

if TYPE_CHECKING:
    from cos.kernel.context.cognitive_context import CognitiveContext


class ReasoningCapability:
    """Reasoning capability."""

    def __init__(self, service: ReasoningService) -> None:
        """Initialize reasoning capability.

        Args:
            service: Reasoning service instance
        """
        self._service = service

    async def solve(self, problem: Any) -> dict[str, Any]:
        """Solve a reasoning task.

        Args:
            problem: Problem to solve

        Returns:
            Solution
        """
        return await self._service.solve(problem)

    async def infer(self, facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Perform inference.

        Args:
            facts: Facts to reason about

        Returns:
            Inferred conclusions
        """
        return await self._service.infer(facts)

    async def prove(self, goal: dict[str, Any]) -> dict[str, Any]:
        """Prove a goal.

        Args:
            goal: Goal to prove

        Returns:
            Proof result
        """
        return await self._service.prove(goal)

    async def explain(self, result: Any) -> str:
        """Explain a result.

        Args:
            result: Result to explain

        Returns:
            Explanation
        """
        return await self._service.explain(result)

    async def trace(self, result: Any) -> list[dict[str, Any]]:
        """Get reasoning trace.

        Args:
            result: Result to trace

        Returns:
            Reasoning trace
        """
        return await self._service.trace(result)


class MemoryCapability:
    """Memory capability."""

    def __init__(
        self,
        working: WorkingMemoryService,
        semantic: SemanticMemoryService,
        episodic: EpisodicMemoryService,
        consolidation: MemoryConsolidationService,
    ) -> None:
        """Initialize memory capability.

        Args:
            working: Working memory service
            semantic: Semantic memory service
            episodic: Episodic memory service
            consolidation: Consolidation service
        """
        self._working = working
        self._semantic = semantic
        self._episodic = episodic
        self._consolidation = consolidation
        self._current_workspace: str | None = None

    async def create_workspace(self) -> str:
        """Create a workspace.

        Returns:
            Workspace ID
        """
        workspace_id = await self._working.create_workspace()
        self._current_workspace = workspace_id
        return workspace_id

    async def store(self, item: dict[str, Any], memory_type: str = "semantic") -> None:
        """Store in memory.

        Args:
            item: Item to store
            memory_type: Type of memory (working, semantic, episodic)
        """
        if memory_type == "working":
            if not self._current_workspace:
                self._current_workspace = await self._working.create_workspace()
            await self._working.store_fact(self._current_workspace, item)
        elif memory_type == "episodic":
            await self._episodic.record_episode(item)
        else:
            await self._semantic.store_concept(item)

    async def query(self, query: Any, memory_type: str = "semantic") -> list[dict[str, Any]]:
        """Query memory.

        Args:
            query: Search query
            memory_type: Type of memory to query

        Returns:
            Query results
        """
        if memory_type == "episodic":
            return await self._episodic.retrieve_episodes(query)
        elif memory_type == "working":
            if not self._current_workspace:
                return []
            criteria = query.model_dump() if hasattr(query, "model_dump") else (
                query if isinstance(query, dict) else {}
            )
            return await self._working.retrieve_fact(self._current_workspace, criteria)
        else:
            return await self._semantic.search_concepts(query)

    async def recall(self, situation: dict[str, Any]) -> list[dict[str, Any]]:
        """Recall similar experiences.

        Args:
            situation: Situation to recall

        Returns:
            Similar experiences
        """
        experiences = await self._episodic.retrieve_episodes(situation)
        return experiences

    async def consolidate(self) -> dict[str, Any]:
        """Consolidate memories.

        Returns:
            Consolidation result
        """
        return await self._consolidation.consolidate()


class WorldCapability:
    """World model capability."""

    def __init__(
        self,
        world_model: WorldModelService,
        knowledge_graph: KnowledgeGraphService,
        semantic_query: SemanticQueryService,
        constraint_validation: ConstraintValidationService,
        pattern_matching: PatternMatchingService,
    ) -> None:
        """Initialize world capability.

        Args:
            world_model: World model service
            knowledge_graph: Knowledge graph service
            semantic_query: Semantic query service
            constraint_validation: Constraint validation service
            pattern_matching: Pattern matching service
        """
        self._world_model = world_model
        self._knowledge_graph = knowledge_graph
        self._semantic_query = semantic_query
        self._constraint_validation = constraint_validation
        self._pattern_matching = pattern_matching

    async def validate(self, hypothesis: Any) -> dict[str, Any]:
        """Validate against world model.

        Args:
            hypothesis: Hypothesis to validate

        Returns:
            Validation result
        """
        return await self._world_model.validate(hypothesis)

    async def query(self, criteria: dict[str, Any]) -> list[dict[str, Any]]:
        """Query the world model.

        Args:
            criteria: Query criteria

        Returns:
            Matching entities
        """
        return await self._world_model.query(criteria)

    async def find(self, entity_type: str) -> list[dict[str, Any]]:
        """Find entities by type.

        Args:
            entity_type: Entity type

        Returns:
            Matching entities
        """
        return await self._world_model.find(entity_type)

    async def add_entity(self, entity: Any) -> str:
        """Add an entity to the knowledge graph.

        Args:
            entity: Entity to add

        Returns:
            Entity ID
        """
        return await self._knowledge_graph.add_entity(entity)

    async def add_relationship(self, relationship: Any) -> str:
        """Add a relationship to the knowledge graph.

        Args:
            relationship: Relationship to add

        Returns:
            Relationship ID
        """
        return await self._knowledge_graph.add_relationship(relationship)

    async def traverse(self, start_id: str, path_pattern: dict[str, Any]) -> list[dict[str, Any]]:
        """Traverse the knowledge graph.

        Args:
            start_id: Starting entity
            path_pattern: Path pattern

        Returns:
            Traversed entities
        """
        return await self._knowledge_graph.traverse(start_id, path_pattern)

    async def validate_constraint(self, constraint: Any) -> bool:
        """Validate a constraint.

        Args:
            constraint: Constraint to validate

        Returns:
            True if valid
        """
        return await self._constraint_validation.validate_constraint(constraint)

    async def find_violations(self) -> list[dict[str, Any]]:
        """Find constraint violations.

        Returns:
            List of violations
        """
        return await self._constraint_validation.find_violations()


class PlanningCapability:
    """Planning capability."""

    def __init__(
        self,
        planning: PlanningService,
        htn: HTNPlanningService,
        graph: GraphPlanningService,
        constraint: ConstraintPlanningService,
    ) -> None:
        """Initialize planning capability.

        Args:
            planning: Planning service
            htn: HTN planning service
            graph: Graph planning service
            constraint: Constraint planning service
        """
        self._planning = planning
        self._htn = htn
        self._graph = graph
        self._constraint = constraint

    async def plan(self, goal: Any) -> dict[str, Any]:
        """Create a plan.

        Args:
            goal: Goal to plan for

        Returns:
            Generated plan
        """
        return await self._planning.generate(goal)

    async def decompose(self, goal: Any) -> dict[str, Any]:
        """Decompose a goal into subtasks.

        Args:
            goal: Goal to decompose

        Returns:
            Decomposition result
        """
        return await self._planning.decompose(goal)

    async def validate(self, plan: dict[str, Any]) -> bool:
        """Validate a plan.

        Args:
            plan: Plan to validate

        Returns:
            True if valid
        """
        return await self._planning.validate(plan)

    async def execute_step(self, plan_id: str) -> dict[str, Any]:
        """Execute next step in plan.

        Args:
            plan_id: Plan ID

        Returns:
            Execution result
        """
        return await self._planning.execute_step(plan_id)


class DecisionCapability:
    """Decision capability."""

    def __init__(
        self,
        decision: DecisionService,
        utility: UtilityDecisionService,
        policy: PolicyEngineService,
        risk: RiskAssessmentService,
    ) -> None:
        """Initialize decision capability.

        Args:
            decision: Decision service
            utility: Utility decision service
            policy: Policy engine service
            risk: Risk assessment service
        """
        self._decision = decision
        self._utility = utility
        self._policy = policy
        self._risk = risk

    async def decide(self, context: Any) -> dict[str, Any]:
        """Make a decision.

        Args:
            context: Decision context

        Returns:
            Decision result
        """
        return await self._decision.decide(context)

    async def assess_risk(self, option: dict[str, Any]) -> dict[str, Any]:
        """Assess risk of an option.

        Args:
            option: Option to assess

        Returns:
            Risk assessment
        """
        return await self._risk.assess(option)

    async def select_best(self, options: list[dict[str, Any]]) -> dict[str, Any]:
        """Select best option.

        Args:
            options: Options to evaluate

        Returns:
            Best option
        """
        return await self._utility.select_best(options)


class LearningCapability:
    """Learning capability."""

    def __init__(
        self,
        learning: LearningService,
        experience: ExperienceLearningService,
        heuristic: HeuristicLearningService,
        policy: PolicyLearningService,
    ) -> None:
        """Initialize learning capability.

        Args:
            learning: Learning service
            experience: Experience learning service
            heuristic: Heuristic learning service
            policy: Policy learning service
        """
        self._learning = learning
        self._experience = experience
        self._heuristic = heuristic
        self._policy = policy

    async def learn(self, experience: Any) -> dict[str, Any]:
        """Learn from experience.

        Args:
            experience: Experience to learn from

        Returns:
            Learning result
        """
        return await self._learning.learn(experience)

    async def record(
        self,
        situation: dict[str, Any],
        action: dict[str, Any],
        outcome: dict[str, Any],
    ) -> str:
        """Record an experience.

        Args:
            situation: Observed situation
            action: Action taken
            outcome: Resulting outcome

        Returns:
            Experience ID
        """
        return await self._experience.record(situation, action, outcome)

    async def recall(self, situation: dict[str, Any]) -> list[Any]:
        """Recall similar experiences.

        Args:
            situation: Situation to recall

        Returns:
            Similar experiences
        """
        return await self._learning.recall(situation)

    async def get_insights(self) -> list[str]:
        """Get learned insights.

        Returns:
            List of insights
        """
        return await self._learning.get_insights()


class MetaCapability:
    """Meta-cognition capability."""

    def __init__(
        self,
        meta: MetaCognitionService,
        reflection: ReflectionService,
        confidence: ConfidenceEstimationService,
    ) -> None:
        """Initialize meta-cognition capability.

        Args:
            meta: Meta-cognition service
            reflection: Reflection service
            confidence: Confidence estimation service
        """
        self._meta = meta
        self._reflection = reflection
        self._confidence = confidence

    async def observe(self, state: Any) -> dict[str, Any]:
        """Observe current state.

        Args:
            state: State to observe

        Returns:
            Observation result
        """
        return await self._meta.observe(state)

    async def regulate(self, observation: dict[str, Any]) -> dict[str, Any]:
        """Regulate based on observation.

        Args:
            observation: Observation to regulate

        Returns:
            Regulation action
        """
        return await self._meta.regulate(observation)

    async def monitor(self) -> dict[str, Any]:
        """Monitor meta-cognitive state.

        Returns:
            Monitoring result
        """
        return await self._meta.monitor()

    async def reflect(self, reasoning: Any) -> str:
        """Perform reflection.

        Args:
            reasoning: Reasoning to reflect on

        Returns:
            Reflection
        """
        return await self._reflection.reflect(reasoning)

    async def estimate_confidence(self, result: Any) -> dict[str, Any]:
        """Estimate confidence in result.

        Args:
            result: Result to estimate

        Returns:
            Confidence estimate
        """
        return await self._confidence.estimate(result)


class AssistantCapability:
    """Assistant capability."""

    def __init__(
        self,
        assistant: AssistantService,
        explanation: ExplanationEngineService,
        trace: TraceVisualizationService,
    ) -> None:
        """Initialize assistant capability.

        Args:
            assistant: Assistant service
            explanation: Explanation engine service
            trace: Trace visualization service
        """
        self._assistant = assistant
        self._explanation = explanation
        self._trace = trace
        self._current_session: str | None = None

    async def respond(self, query: str) -> dict[str, Any]:
        """Respond to a query.

        Args:
            query: User query

        Returns:
            Response
        """
        response = await self._assistant.respond(query, self._current_session)
        self._current_session = response.get("session_id")
        return response

    async def explain(self, result: Any, context: dict[str, Any] | None = None) -> str:
        """Explain a result.

        Args:
            result: Result to explain
            context: Additional context

        Returns:
            Explanation
        """
        return await self._explanation.explain(result, context)

    async def record_trace(self, trace_id: str, action: str, reasoning: str) -> None:
        """Record a step in a trace.

        Args:
            trace_id: Trace identifier
            action: Action taken
            reasoning: Reasoning for action
        """
        await self._trace.record_step(trace_id, action, reasoning)

    async def get_trace(self, trace_id: str) -> list[dict[str, Any]]:
        """Get a trace.

        Args:
            trace_id: Trace identifier

        Returns:
            Trace steps
        """
        return await self._trace.get_trace(trace_id)


class CognitiveBroker:
    """The unified cognitive facade of the Cognitive Operating System.

    The Cognitive Broker is the single entry point for all cognitive operations.
    Rather than exposing numerous individual methods, the Broker organizes
    cognition into capability namespaces.

    Example:
        >>> broker = CognitiveBroker()
        >>> await broker.initialize()
        >>> result = await broker.reasoning.solve(task)
        >>> memories = await broker.memory.query(query)
        >>> broker.world.validate(constraints)
    """

    def __init__(self, context: CognitiveContext | None = None) -> None:
        """Initialize the cognitive broker.

        Args:
            context: The parent cognitive context
        """
        self._context = context
        self._initialized = False

        # Service instances
        self._reasoning_service = ReasoningService()
        self._working_memory = WorkingMemoryService()
        self._semantic_memory = SemanticMemoryService()
        self._episodic_memory = EpisodicMemoryService()
        self._memory_consolidation = MemoryConsolidationService()
        self._world_model = WorldModelService()
        self._knowledge_graph = KnowledgeGraphService()
        self._semantic_query = SemanticQueryService()
        self._constraint_validation = ConstraintValidationService()
        self._pattern_matching = PatternMatchingService()
        self._planning = PlanningService()
        self._htn_planning = HTNPlanningService()
        self._graph_planning = GraphPlanningService()
        self._constraint_planning = ConstraintPlanningService()
        self._decision = DecisionService()
        self._utility_decision = UtilityDecisionService()
        self._policy_engine = PolicyEngineService()
        self._risk_assessment = RiskAssessmentService()
        self._learning = LearningService()
        self._experience_learning = ExperienceLearningService()
        self._heuristic_learning = HeuristicLearningService()
        self._policy_learning = PolicyLearningService()
        self._meta_cognition = MetaCognitionService()
        self._reflection = ReflectionService()
        self._confidence = ConfidenceEstimationService()
        self._assistant = AssistantService()
        self._explanation = ExplanationEngineService()
        self._trace = TraceVisualizationService()

        # Capability instances
        self._reasoning: ReasoningCapability | None = None
        self._memory: MemoryCapability | None = None
        self._world: WorldCapability | None = None
        self._planning_cap: PlanningCapability | None = None
        self._decision_cap: DecisionCapability | None = None
        self._learning_cap: LearningCapability | None = None
        self._meta: MetaCapability | None = None
        self._assistant_cap: AssistantCapability | None = None

    async def initialize(self) -> None:
        """Initialize all services."""
        if self._initialized:
            return

        # Initialize services
        await self._reasoning_service.initialize()

        # Create capabilities
        self._reasoning = ReasoningCapability(self._reasoning_service)
        self._memory = MemoryCapability(
            self._working_memory,
            self._semantic_memory,
            self._episodic_memory,
            self._memory_consolidation,
        )
        self._world = WorldCapability(
            self._world_model,
            self._knowledge_graph,
            self._semantic_query,
            self._constraint_validation,
            self._pattern_matching,
        )
        self._planning_cap = PlanningCapability(
            self._planning,
            self._htn_planning,
            self._graph_planning,
            self._constraint_planning,
        )
        self._decision_cap = DecisionCapability(
            self._decision,
            self._utility_decision,
            self._policy_engine,
            self._risk_assessment,
        )
        self._learning_cap = LearningCapability(
            self._learning,
            self._experience_learning,
            self._heuristic_learning,
            self._policy_learning,
        )
        self._meta = MetaCapability(
            self._meta_cognition,
            self._reflection,
            self._confidence,
        )
        self._assistant_cap = AssistantCapability(
            self._assistant,
            self._explanation,
            self._trace,
        )

        self._initialized = True

    async def shutdown(self) -> None:
        """Shutdown all services."""
        self._initialized = False

    @property
    def reasoning(self) -> ReasoningCapability:
        """Access reasoning capability."""
        if not self._initialized:
            raise RuntimeError("Broker not initialized. Call initialize() first.")
        return self._reasoning

    @property
    def memory(self) -> MemoryCapability:
        """Access memory capability."""
        if not self._initialized:
            raise RuntimeError("Broker not initialized. Call initialize() first.")
        return self._memory

    @property
    def world(self) -> WorldCapability:
        """Access world model capability."""
        if not self._initialized:
            raise RuntimeError("Broker not initialized. Call initialize() first.")
        return self._world

    @property
    def planning(self) -> PlanningCapability:
        """Access planning capability."""
        if not self._initialized:
            raise RuntimeError("Broker not initialized. Call initialize() first.")
        return self._planning_cap

    @property
    def decision(self) -> DecisionCapability:
        """Access decision capability."""
        if not self._initialized:
            raise RuntimeError("Broker not initialized. Call initialize() first.")
        return self._decision_cap

    @property
    def learning(self) -> LearningCapability:
        """Access learning capability."""
        if not self._initialized:
            raise RuntimeError("Broker not initialized. Call initialize() first.")
        return self._learning_cap

    @property
    def meta(self) -> MetaCapability:
        """Access meta-cognition capability."""
        if not self._initialized:
            raise RuntimeError("Broker not initialized. Call initialize() first.")
        return self._meta

    @property
    def assistant(self) -> AssistantCapability:
        """Access assistant capability."""
        if not self._initialized:
            raise RuntimeError("Broker not initialized. Call initialize() first.")
        return self._assistant_cap
