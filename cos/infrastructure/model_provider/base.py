"""Base Model Provider - Abstract interfaces for AI model providers.

This module defines the vendor-neutral interfaces that all model providers
must implement to ensure portability and interoperability.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ModelCapability(Enum):
    """Supported model capabilities."""
    TEXT_GENERATION = "text_generation"
    EMBEDDINGS = "embeddings"
    IMAGE_UNDERSTANDING = "image_understanding"
    SPEECH_RECOGNITION = "speech_recognition"
    TOOL_CALLING = "tool_calling"
    STRUCTURED_OUTPUT = "structured_output"
    REASONING = "reasoning"


class ProviderStatus(Enum):
    """Provider status."""
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    RATE_LIMITED = "rate_limited"


@dataclass
class ModelConfig:
    """Configuration for a model."""
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: list[str] | None = None
    timeout: float = 60.0


@dataclass
class InferenceRequest:
    """Request for model inference."""
    prompt: str | list[dict[str, Any]]
    model_config: ModelConfig | None = None
    system_prompt: str | None = None
    messages: list[dict[str, str]] | None = None
    stream: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class InferenceResponse:
    """Response from model inference."""
    content: str
    model: str
    provider: str
    usage: dict[str, int] | None = None
    latency_ms: float = 0.0
    finish_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass 
class ProviderCapability:
    """Capabilities of a provider."""
    provider_name: str
    supported_models: list[str]
    capabilities: list[ModelCapability]
    max_concurrency: int = 10
    rate_limit_rpm: int | None = None
    rate_limit_tpm: int | None = None
    supports_streaming: bool = True


@dataclass
class HealthStatus:
    """Health status of a provider."""
    status: ProviderStatus
    latency_ms: float | None = None
    last_check: datetime = field(default_factory=datetime.now)
    error_count: int = 0
    total_requests: int = 0


class ModelProvider(ABC):
    """Abstract base class for AI model providers.
    
    All model providers must implement this interface to ensure
    vendor independence and portability.
    """

    def __init__(self, provider_name: str) -> None:
        """Initialize the provider.
        
        Args:
            provider_name: Unique name for this provider
        """
        self._provider_name = provider_name
        self._initialized = False
        self._health = HealthStatus(status=ProviderStatus.UNAVAILABLE)

    @property
    def provider_name(self) -> str:
        """Get the provider name."""
        return self._provider_name

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized."""
        return self._initialized

    @property
    def health(self) -> HealthStatus:
        """Get provider health status."""
        return self._health

    @abstractmethod
    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        """Initialize the provider with configuration.
        
        Args:
            config: Provider-specific configuration (API keys, endpoints, etc.)
        """
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the provider gracefully."""
        pass

    @abstractmethod
    async def invoke(self, request: InferenceRequest) -> InferenceResponse:
        """Perform inference request.
        
        Args:
            request: The inference request
            
        Returns:
            Inference response from the model
        """
        pass

    @abstractmethod
    async def get_capabilities(self) -> ProviderCapability:
        """Get provider capabilities.
        
        Returns:
            Provider capabilities including supported models and features
        """
        pass

    @abstractmethod
    async def health_check(self) -> HealthStatus:
        """Check provider health.
        
        Returns:
            Current health status
        """
        pass

    async def stream(self, request: InferenceRequest) -> list[InferenceResponse]:
        """Perform streaming inference.
        
        Default implementation collects all chunks into responses.
        Override for true streaming support.
        
        Args:
            request: The inference request
            
        Returns:
            List of response chunks
        """
        if not self._supports_streaming():
            # Fall back to non-streaming
            response = await self.invoke(request)
            return [response]
        
        # Collect streamed chunks
        chunks: list[InferenceResponse] = []
        full_content = ""
        
        async for chunk in self._stream_chunks(request):
            full_content += chunk.content
            chunks.append(chunk)
        
        # Return aggregated response
        if chunks:
            final = chunks[-1].model_copy()
            final.content = full_content
            return chunks + [final]
        
        return []

    @abstractmethod
    async def _stream_chunks(self, request: InferenceRequest):
        """Internal streaming implementation.
        
        Args:
            request: The inference request
            
        Yields:
            Response chunks
        """
        pass

    def _supports_streaming(self) -> bool:
        """Check if streaming is supported."""
        return True

    def _update_health(self, status: ProviderStatus, latency_ms: float | None = None) -> None:
        """Update health status.
        
        Args:
            status: New status
            latency_ms: Optional latency measurement
        """
        self._health = HealthStatus(
            status=status,
            latency_ms=latency_ms,
            last_check=datetime.now(),
            error_count=self._health.error_count,
            total_requests=self._health.total_requests + 1,
        )

    def _record_error(self) -> None:
        """Record an error for health tracking."""
        self._health.error_count += 1
        if self._health.error_count >= 5:
            self._health.status = ProviderStatus.DEGRADED
