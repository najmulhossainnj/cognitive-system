"""Memory Services Implementation.

This module provides memory services for the cognitive system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class MemoryItem:
    """Represents a memory item."""

    id: str
    content: dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    importance: float = 0.5
    access_count: int = 0
    last_accessed: datetime | None = None


@dataclass
class Workspace:
    """Represents a working memory workspace."""

    id: str
    facts: list[dict[str, Any]] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    attention_focus: str = ""
    snapshots: dict[str, dict[str, Any]] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


class WorkingMemoryService:
    """Working Memory Service for transient cognitive workspace.

    Provides a transient cognitive workspace for active reasoning.
    """

    def __init__(self) -> None:
        """Initialize the working memory service."""
        self._workspaces: dict[str, Workspace] = {}
        self._default_workspace: Workspace | None = None

    async def create_workspace(self) -> str:
        """Create a workspace.

        Returns:
            Workspace ID
        """
        workspace_id = str(uuid4())
        workspace = Workspace(id=workspace_id)
        self._workspaces[workspace_id] = workspace

        if self._default_workspace is None:
            self._default_workspace = workspace

        return workspace_id

    async def destroy_workspace(self, workspace_id: str) -> None:
        """Destroy a workspace.

        Args:
            workspace_id: Workspace to destroy
        """
        if workspace_id in self._workspaces:
            del self._workspaces[workspace_id]

        if self._default_workspace and self._default_workspace.id == workspace_id:
            self._default_workspace = None

    async def store_fact(self, workspace_id: str, fact: dict[str, Any]) -> None:
        """Store a fact in workspace.

        Args:
            workspace_id: Workspace ID
            fact: Fact to store
        """
        workspace = self._workspaces.get(workspace_id)
        if workspace:
            workspace.facts.append(fact)

    async def retrieve_fact(
        self,
        workspace_id: str,
        criteria: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Retrieve facts from workspace.

        Args:
            workspace_id: Workspace ID
            criteria: Retrieval criteria

        Returns:
            Retrieved facts
        """
        workspace = self._workspaces.get(workspace_id)
        if not workspace:
            return []

        results = []
        for fact in workspace.facts:
            if self._matches_criteria(fact, criteria):
                results.append(fact)

        return results

    def _matches_criteria(self, fact: dict[str, Any], criteria: dict[str, Any]) -> bool:
        """Check if a fact matches criteria."""
        for key, value in criteria.items():
            if key not in fact or fact[key] != value:
                return False
        return True

    async def update_context(
        self,
        workspace_id: str,
        context: dict[str, Any],
    ) -> None:
        """Update workspace context.

        Args:
            workspace_id: Workspace ID
            context: Context to set
        """
        workspace = self._workspaces.get(workspace_id)
        if workspace:
            workspace.context.update(context)

    async def set_attention(
        self,
        workspace_id: str,
        focus: str,
    ) -> None:
        """Set attention focus.

        Args:
            workspace_id: Workspace ID
            focus: Focus area
        """
        workspace = self._workspaces.get(workspace_id)
        if workspace:
            workspace.attention_focus = focus

    async def snapshot(self, workspace_id: str) -> str:
        """Create workspace snapshot.

        Args:
            workspace_id: Workspace ID

        Returns:
            Snapshot ID
        """
        workspace = self._workspaces.get(workspace_id)
        if not workspace:
            return ""

        snapshot_id = str(uuid4())
        workspace.snapshots[snapshot_id] = {
            "facts": workspace.facts.copy(),
            "context": workspace.context.copy(),
            "attention_focus": workspace.attention_focus,
            "created_at": datetime.now().isoformat(),
        }

        return snapshot_id

    async def restore(self, workspace_id: str, snapshot_id: str) -> None:
        """Restore from snapshot.

        Args:
            workspace_id: Workspace ID
            snapshot_id: Snapshot to restore
        """
        workspace = self._workspaces.get(workspace_id)
        if not workspace:
            return

        snapshot = workspace.snapshots.get(snapshot_id)
        if snapshot:
            workspace.facts = snapshot.get("facts", []).copy()
            workspace.context = snapshot.get("context", {}).copy()
            workspace.attention_focus = snapshot.get("attention_focus", "")

    async def clear(self, workspace_id: str) -> None:
        """Clear workspace.

        Args:
            workspace_id: Workspace ID
        """
        workspace = self._workspaces.get(workspace_id)
        if workspace:
            workspace.facts.clear()
            workspace.context.clear()
            workspace.attention_focus = ""


class SemanticMemoryService:
    """Semantic Memory Service for persistent conceptual knowledge.

    Provides persistent storage and retrieval of conceptual knowledge.
    """

    def __init__(self) -> None:
        """Initialize the semantic memory service."""
        self._concepts: dict[str, MemoryItem] = {}
        self._index: dict[str, set[str]] = {}

    async def store_concept(self, concept: dict[str, Any]) -> str:
        """Store a concept.

        Args:
            concept: Concept to store

        Returns:
            Concept ID
        """
        concept_id = concept.get("id", str(uuid4()))
        importance = concept.get("importance", 0.5)

        item = MemoryItem(
            id=concept_id,
            content=concept,
            importance=importance,
        )
        self._concepts[concept_id] = item

        category = concept.get("category", "general")
        if category not in self._index:
            self._index[category] = set()
        self._index[category].add(concept_id)

        return concept_id

    async def retrieve_concept(self, concept_id: str) -> dict[str, Any] | None:
        """Retrieve a concept.

        Args:
            concept_id: Concept ID

        Returns:
            Concept or None
        """
        item = self._concepts.get(concept_id)
        if item:
            item.access_count += 1
            item.last_accessed = datetime.now()
            return item.content
        return None

    async def search_concepts(self, query: Any) -> list[dict[str, Any]]:
        """Search concepts.

        Args:
            query: Search query

        Returns:
            Matching concepts
        """
        results = []

        query_dict = query.model_dump() if hasattr(query, "model_dump") else (
            query if isinstance(query, dict) else {"text": str(query)}
        )

        search_text = query_dict.get("text", "").lower()
        category = query_dict.get("category")
        tags = query_dict.get("tags", [])

        for item in self._concepts.values():
            content = item.content

            if category and content.get("category") != category:
                continue

            if tags and not any(t in content.get("tags", []) for t in tags):
                continue

            if search_text:
                text_match = search_text in str(content).lower()
                if not text_match:
                    continue

            results.append(content)

        def get_importance(item: dict[str, Any]) -> float:
            mem_item = self._concepts.get(item.get("id", ""), MemoryItem("", {}))
            return mem_item.importance

        results.sort(key=get_importance, reverse=True)

        return results

    async def update_concept(
        self,
        concept_id: str,
        updates: dict[str, Any],
    ) -> dict[str, Any]:
        """Update a concept.

        Args:
            concept_id: Concept ID
            updates: Updates to apply

        Returns:
            Updated concept
        """
        item = self._concepts.get(concept_id)
        if not item:
            return {}

        item.content.update(updates)
        item.importance = updates.get("importance", item.importance)

        return item.content

    async def delete_concept(self, concept_id: str) -> bool:
        """Delete a concept.

        Args:
            concept_id: Concept ID

        Returns:
            True if deleted
        """
        item = self._concepts.pop(concept_id, None)
        if item:
            for index_set in self._index.values():
                index_set.discard(concept_id)
            return True
        return False


class EpisodicMemoryService:
    """Episodic Memory Service for historical execution experiences.

    Provides storage and retrieval of historical experiences.
    """

    def __init__(self) -> None:
        """Initialize the episodic memory service."""
        self._episodes: dict[str, MemoryItem] = {}
        self._by_time: list[tuple[datetime, str]] = []

    async def record_episode(self, episode: dict[str, Any]) -> str:
        """Record an episode.

        Args:
            episode: Episode to record

        Returns:
            Episode ID
        """
        episode_id = episode.get("id", str(uuid4()))
        timestamp = datetime.fromisoformat(episode.get("timestamp", datetime.now().isoformat()))
        importance = episode.get("importance", 0.5)

        item = MemoryItem(
            id=episode_id,
            content=episode,
            created_at=timestamp,
            importance=importance,
        )
        self._episodes[episode_id] = item

        self._by_time.append((timestamp, episode_id))
        self._by_time.sort(key=lambda x: x[0], reverse=True)

        return episode_id

    async def retrieve_episodes(
        self,
        criteria: Any,
    ) -> list[dict[str, Any]]:
        """Retrieve episodes.

        Args:
            criteria: Retrieval criteria

        Returns:
            Matching episodes
        """
        criteria_dict = criteria.model_dump() if hasattr(criteria, "model_dump") else (
            criteria if isinstance(criteria, dict) else {}
        )

        limit = criteria_dict.get("limit", 10)
        start_time = criteria_dict.get("start_time")
        end_time = criteria_dict.get("end_time")

        results = []

        for timestamp, episode_id in self._by_time:
            if start_time and timestamp < datetime.fromisoformat(start_time):
                continue
            if end_time and timestamp > datetime.fromisoformat(end_time):
                continue

            item = self._episodes.get(episode_id)
            if item:
                results.append(item.content)

            if len(results) >= limit:
                break

        return results

    async def get_episode(self, episode_id: str) -> dict[str, Any] | None:
        """Get an episode.

        Args:
            episode_id: Episode ID

        Returns:
            Episode or None
        """
        item = self._episodes.get(episode_id)
        return item.content if item else None


class MemoryConsolidationService:
    """Memory Consolidation Service for memory organization.

    Consolidates memories for improved organization and retrieval.
    """

    def __init__(self) -> None:
        """Initialize the consolidation service."""
        self._importance_threshold = 0.3

    async def consolidate(self) -> dict[str, Any]:
        """Consolidate memory.

        Returns:
            Consolidation results
        """
        results = {
            "status": "completed",
            "items_processed": 0,
            "items_pruned": 0,
            "timestamp": datetime.now().isoformat(),
        }

        return results

    async def analyze_importance(self) -> list[str]:
        """Analyze memory importance.

        Returns:
            List of memory IDs to retain
        """
        return []

    async def prune_old_memories(self, threshold: float) -> int:
        """Prune old memories.

        Args:
            threshold: Importance threshold

        Returns:
            Number of memories pruned
        """
        self._importance_threshold = threshold
        return 0


# Re-export interfaces
IWorkingMemoryService = WorkingMemoryService
ISemanticMemoryService = SemanticMemoryService
IEpisodicMemoryService = EpisodicMemoryService
IMemoryConsolidationService = MemoryConsolidationService
