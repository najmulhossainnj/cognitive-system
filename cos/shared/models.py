"""Shared Models for COS.

This module defines common data models used across the Cognitive Operating System.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Problem(BaseModel):
    """Represents a problem to be solved."""

    id: str = Field(default_factory=lambda: f"problem-{datetime.now().timestamp()}")
    description: str
    constraints: list[dict[str, Any]] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Solution(BaseModel):
    """Represents a solution to a problem."""

    id: str = Field(default_factory=lambda: f"solution-{datetime.now().timestamp()}")
    problem_id: str
    result: Any
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str = ""
    trace: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Observation(BaseModel):
    """Represents an observation."""

    id: str = Field(default_factory=lambda: f"obs-{datetime.now().timestamp()}")
    content: Any
    timestamp: datetime = Field(default_factory=datetime.now)
    source: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class Confidence(BaseModel):
    """Represents a confidence estimate."""

    score: float = Field(ge=0.0, le=1.0)
    rationale: str = ""
    factors: list[str] = Field(default_factory=list)


class MemoryItem(BaseModel):
    """Represents an item in memory."""

    id: str = Field(default_factory=lambda: f"mem-{datetime.now().timestamp()}")
    content: Any
    memory_type: str = Field(default="semantic")
    timestamp: datetime = Field(default_factory=datetime.now)
    importance: float = Field(ge=0.0, le=1.0, default=0.5)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Query(BaseModel):
    """Represents a query."""

    expression: str
    filters: dict[str, Any] = Field(default_factory=dict)
    limit: int = 100


class RetrievalCriteria(BaseModel):
    """Represents retrieval criteria."""

    memory_type: str | None = None
    time_range: tuple[datetime, datetime] | None = None
    importance_threshold: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Entity(BaseModel):
    """Represents an entity in the world model."""

    id: str = Field(default_factory=lambda: f"entity-{datetime.now().timestamp()}")
    type: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    relationships: list[str] = Field(default_factory=list)


class Relationship(BaseModel):
    """Represents a relationship between entities."""

    id: str = Field(default_factory=lambda: f"rel-{datetime.now().timestamp()}")
    source_id: str
    target_id: str
    relationship_type: str
    strength: float = Field(ge=0.0, le=1.0, default=1.0)


class Constraint(BaseModel):
    """Represents a constraint."""

    id: str = Field(default_factory=lambda: f"constraint-{datetime.now().timestamp()}")
    type: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class Pattern(BaseModel):
    """Represents a pattern."""

    id: str = Field(default_factory=lambda: f"pattern-{datetime.now().timestamp()}")
    type: str
    entities: list[str] = Field(default_factory=list)
    structure: dict[str, Any] = Field(default_factory=dict)


class Hypothesis(BaseModel):
    """Represents a hypothesis."""

    id: str = Field(default_factory=lambda: f"hyp-{datetime.now().timestamp()}")
    statement: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class Goal(BaseModel):
    """Represents a goal."""

    id: str = Field(default_factory=lambda: f"goal-{datetime.now().timestamp()}")
    objective: str
    constraints: list[Constraint] = Field(default_factory=list)
    priority: int = 0
    deadline: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Plan(BaseModel):
    """Represents a plan."""

    id: str = Field(default_factory=lambda: f"plan-{datetime.now().timestamp()}")
    goal_id: str
    tasks: list[dict[str, Any]] = Field(default_factory=list)
    dependencies: list[tuple[str, str]] = Field(default_factory=list)
    estimated_cost: float = 0.0
    risk: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class Task(BaseModel):
    """Represents a task."""

    id: str = Field(default_factory=lambda: f"task-{datetime.now().timestamp()}")
    description: str
    status: str = "pending"
    dependencies: list[str] = Field(default_factory=list)


class ResourceEstimate(BaseModel):
    """Represents a resource estimate."""

    cpu_time: float = 0.0
    memory: int = 0
    storage: int = 0
    network: int = 0
    custom: dict[str, Any] = Field(default_factory=dict)


class Decision(BaseModel):
    """Represents a decision."""

    id: str = Field(default_factory=lambda: f"decision-{datetime.now().timestamp()}")
    selected_plan_id: str
    rejected_plan_ids: list[str] = Field(default_factory=list)
    utility_score: float = 0.0
    risk_score: float = 0.0
    rationale: str = ""


class Policy(BaseModel):
    """Represents a decision policy."""

    id: str = Field(default_factory=lambda: f"policy-{datetime.now().timestamp()}")
    name: str
    rules: list[dict[str, Any]] = Field(default_factory=list)
    priority: int = 0


class Preference(BaseModel):
    """Represents a preference."""

    id: str = Field(default_factory=lambda: f"pref-{datetime.now().timestamp()}")
    name: str
    value: Any
    weight: float = 1.0


class Experience(BaseModel):
    """Represents an experience."""

    id: str = Field(default_factory=lambda: f"exp-{datetime.now().timestamp()}")
    goal: Goal
    selected_plan_id: str
    outcome: str
    success: bool
    reasoning_trace: list[dict[str, Any]] = Field(default_factory=list)
    metrics: dict[str, float] = Field(default_factory=dict)


class Dataset(BaseModel):
    """Represents a dataset for learning."""

    id: str = Field(default_factory=lambda: f"dataset-{datetime.now().timestamp()}")
    name: str
    experiences: list[Experience] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class LearningMetrics(BaseModel):
    """Represents learning metrics."""

    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    custom: dict[str, float] = Field(default_factory=dict)


class CognitiveState(BaseModel):
    """Represents cognitive state."""

    timestamp: datetime = Field(default_factory=datetime.now)
    reasoning_results: list[Solution] = Field(default_factory=list)
    memory_state: dict[str, Any] = Field(default_factory=dict)
    world_model_state: dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.5


class ReflectionReport(BaseModel):
    """Represents a reflection report."""

    id: str = Field(default_factory=lambda: f"ref-{datetime.now().timestamp()}")
    timestamp: datetime = Field(default_factory=datetime.now)
    observations: list[str] = Field(default_factory=list)
    diagnoses: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    confidence: float = 0.5


class Explanation(BaseModel):
    """Represents an explanation."""

    id: str = Field(default_factory=lambda: f"exp-{datetime.now().timestamp()}")
    content: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = 0.5
    trace: list[dict[str, Any]] = Field(default_factory=list)


class Trace(BaseModel):
    """Represents an execution trace."""

    id: str = Field(default_factory=lambda: f"trace-{datetime.now().timestamp()}")
    steps: list[dict[str, Any]] = Field(default_factory=list)
    start_time: datetime
    end_time: datetime | None = None


class Report(BaseModel):
    """Represents a report."""

    id: str = Field(default_factory=lambda: f"report-{datetime.now().timestamp()}")
    title: str
    content: str
    sections: list[dict[str, Any]] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
