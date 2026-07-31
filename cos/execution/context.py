"""Cognitive Context Interface.

This module defines the interface for the Cognitive Context.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.core.capabilities.assistant_capability import IAssistantCapability
    from cos.core.capabilities.decision_capability import IDecisionCapability
    from cos.core.capabilities.learning_capability import ILearningCapability
    from cos.core.capabilities.memory_capability import IMemoryCapability
    from cos.core.capabilities.meta_cognition_capability import IMetaCognitionCapability
    from cos.core.capabilities.planning_capability import IPlanningCapability
    from cos.core.capabilities.reasoning_capability import IReasoningCapability
    from cos.core.capabilities.world_model_capability import IWorldModelCapability


class ICognitiveContext:
    """Cognitive Context provides access to all cognitive capabilities.

    This is the primary interface through which applications access
    cognitive functionality.

    See COS-CORE-004 for full specification.
    """

    @property
    def cognition(self) -> ICognition:
        """Get cognitive capabilities.

        Returns:
            Cognition interface
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    @property
    def session_id(self) -> str:
        """Get session ID.

        Returns:
            Current session ID
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    @property
    def execution_id(self) -> str:
        """Get execution ID.

        Returns:
            Current execution ID
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def create_context(self) -> ICognitiveContext:
        """Create a new cognitive context.

        Returns:
            New context
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def destroy_context(self) -> None:
        """Destroy this context."""
        raise NotImplementedError("Will be implemented in Phase 3")

    async def get_state(self) -> dict[str, Any]:
        """Get context state.

        Returns:
            Current state
        """
        raise NotImplementedError("Will be implemented in Phase 3")


class ICognition:
    """ICognition provides access to all cognitive capabilities.

    This interface provides a unified view of all cognitive services.
    """

    @property
    def reasoning(self) -> IReasoningCapability:
        """Get reasoning capability.

        Returns:
            Reasoning capability
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    @property
    def memory(self) -> IMemoryCapability:
        """Get memory capability.

        Returns:
            Memory capability
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    @property
    def world(self) -> IWorldModelCapability:
        """Get world model capability.

        Returns:
            World model capability
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    @property
    def planning(self) -> IPlanningCapability:
        """Get planning capability.

        Returns:
            Planning capability
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    @property
    def decision(self) -> IDecisionCapability:
        """Get decision capability.

        Returns:
            Decision capability
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    @property
    def learning(self) -> ILearningCapability:
        """Get learning capability.

        Returns:
            Learning capability
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    @property
    def meta(self) -> IMetaCognitionCapability:
        """Get meta-cognition capability.

        Returns:
            Meta-cognition capability
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    @property
    def assistant(self) -> IAssistantCapability:
        """Get assistant capability.

        Returns:
            Assistant capability
        """
        raise NotImplementedError("Will be implemented in Phase 3")
