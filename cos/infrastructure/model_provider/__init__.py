"""Model Provider Layer - Vendor-neutral AI model abstraction.

This module provides standardized interfaces for integrating AI models
(LLMs, embedding models, vision models) without depending on specific providers.
"""

from cos.infrastructure.model_provider.base import (
    ModelProvider,
    ModelCapability,
    ModelConfig,
    InferenceRequest,
    InferenceResponse,
    ProviderCapability,
)
from cos.infrastructure.model_provider.provider_manager import ModelProviderManager
from cos.infrastructure.model_provider.openai_client import OpenAIProvider
from cos.infrastructure.model_provider.anthropic_client import AnthropicProvider

__all__ = [
    "ModelProvider",
    "ModelCapability",
    "ModelConfig",
    "InferenceRequest",
    "InferenceResponse",
    "ProviderCapability",
    "ModelProviderManager",
    "OpenAIProvider",
    "AnthropicProvider",
]
