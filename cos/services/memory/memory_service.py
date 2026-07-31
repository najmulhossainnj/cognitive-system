"""Memory Service Interfaces.

This module defines interfaces for memory services.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.services.base import IService

if TYPE_CHECKING:
    from cos.shared.models import Query, RetrievalCriteria


class IWorkingMemoryService(IService):
    """Working Memory Service interface.

    Provides transient cognitive workspace.

    See SERVICE-200 for full specification.
    """

    async def create_workspace(self) -> str:
        """Create a workspace.

        Returns:
            Workspace ID
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def destroy_workspace(self, workspace_id: str) -> None:
        """Destroy a workspace.

        Args:
            workspace_id: Workspace to destroy
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def store_fact(self, workspace_id: str, fact: dict[str, Any]) -> None:
        """Store a fact in workspace.

        Args:
            workspace_id: Workspace ID
            fact: Fact to store
        """
        raise NotImplementedError("Will be implemented in Phase 4")

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
        raise NotImplementedError("Will be implemented in Phase 4")

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
        raise NotImplementedError("Will be implemented in Phase 4")

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
        raise NotImplementedError("Will be implemented in Phase 4")

    async def snapshot(self, workspace_id: str) -> str:
        """Create workspace snapshot.

        Args:
            workspace_id: Workspace ID

        Returns:
            Snapshot ID
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def restore(self, workspace_id: str, snapshot_id: str) -> None:
        """Restore from snapshot.

        Args:
            workspace_id: Workspace ID
            snapshot_id: Snapshot to restore
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def clear(self, workspace_id: str) -> None:
        """Clear workspace.

        Args:
            workspace_id: Workspace ID
        """
        raise NotImplementedError("Will be implemented in Phase 4")


class ISemanticMemoryService(IService):
    """Semantic Memory Service interface.

    Provides persistent conceptual knowledge.

    See SERVICE-210 for full specification.
    """

    async def store_concept(self, concept: dict[str, Any]) -> str:
        """Store a concept.

        Args:
            concept: Concept to store

        Returns:
            Concept ID
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def retrieve_concept(self, concept_id: str) -> dict[str, Any] | None:
        """Retrieve a concept.

        Args:
            concept_id: Concept ID

        Returns:
            Concept or None
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def search_concepts(self, query: Query) -> list[dict[str, Any]]:
        """Search concepts.

        Args:
            query: Search query

        Returns:
            Matching concepts
        """
        raise NotImplementedError("Will be implemented in Phase 4")

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
        raise NotImplementedError("Will be implemented in Phase 4")


class IEpisodicMemoryService(IService):
    """Episodic Memory Service interface.

    Provides historical execution experiences.

    See SERVICE-220 for full specification.
    """

    async def record_episode(self, episode: dict[str, Any]) -> str:
        """Record an episode.

        Args:
            episode: Episode to record

        Returns:
            Episode ID
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def retrieve_episodes(
        self,
        criteria: RetrievalCriteria,
    ) -> list[dict[str, Any]]:
        """Retrieve episodes.

        Args:
            criteria: Retrieval criteria

        Returns:
            Matching episodes
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def get_episode(self, episode_id: str) -> dict[str, Any] | None:
        """Get an episode.

        Args:
            episode_id: Episode ID

        Returns:
            Episode or None
        """
        raise NotImplementedError("Will be implemented in Phase 4")


class IMemoryConsolidationService(IService):
    """Memory Consolidation Service interface.

    Consolidates memories for improved organization.

    See SERVICE-230 for full specification.
    """

    async def consolidate(self) -> dict[str, Any]:
        """Consolidate memory.

        Returns:
            Consolidation results
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def analyze_importance(self) -> list[str]:
        """Analyze memory importance.

        Returns:
            List of memory IDs to retain
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def prune_old_memories(self, threshold: float) -> int:
        """Prune old memories.

        Args:
            threshold: Importance threshold

        Returns:
            Number of memories pruned
        """
        raise NotImplementedError("Will be implemented in Phase 4")
