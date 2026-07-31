"""Model Provider Manager - Central routing and management for AI providers.

This module provides the ModelProviderManager that coordinates multiple
model providers, handles routing, failover, and health monitoring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from cos.infrastructure.model_provider.base import (
    InferenceRequest,
    InferenceResponse,
    ModelProvider,
    ModelCapability,
    ProviderCapability,
    ProviderStatus,
)


class RoutingStrategy(Enum):
    """Provider routing strategies."""
    LATENCY = "latency"
    COST = "cost"
    CAPABILITY = "capability"
    ROUND_ROBIN = "round_robin"
    FAILOVER = "failover"


@dataclass
class ProviderMetrics:
    """Metrics for a provider."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency_ms: float = 0.0
    last_request: datetime | None = None
    last_success: datetime | None = None
    last_failure: datetime | None = None


@dataclass
class ManagerConfig:
    """Configuration for the provider manager."""
    default_strategy: RoutingStrategy = RoutingStrategy.LATENCY
    failover_enabled: bool = True
    health_check_interval: float = 60.0
    max_retries: int = 3
    retry_delay_ms: float = 100.0


class ModelProviderManager:
    """Manages multiple model providers with routing and failover.
    
    This class provides a unified interface for accessing AI models
    across multiple providers, handling:
    - Provider registration
    - Request routing
    - Automatic failover
    - Health monitoring
    - Cost optimization
    """

    def __init__(self, config: ManagerConfig | None = None) -> None:
        """Initialize the provider manager.
        
        Args:
            config: Manager configuration
        """
        self._config = config or ManagerConfig()
        self._providers: dict[str, ModelProvider] = {}
        self._provider_order: list[str] = []  # For round-robin
        self._current_index: int = 0
        self._metrics: dict[str, ProviderMetrics] = {}
        self._preferred_provider: str | None = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the manager."""
        # Register default providers
        self._register_default_providers()
        self._initialized = True

    def _register_default_providers(self) -> None:
        """Register default providers."""
        from cos.infrastructure.model_provider.openai_client import OpenAIProvider
        from cos.infrastructure.model_provider.anthropic_client import AnthropicProvider
        
        self.register_provider(OpenAIProvider())
        self.register_provider(AnthropicProvider())

    async def shutdown(self) -> None:
        """Shutdown all providers."""
        for provider in self._providers.values():
            await provider.shutdown()
        self._providers.clear()
        self._initialized = False

    def register_provider(self, provider: ModelProvider) -> None:
        """Register a model provider.
        
        Args:
            provider: The provider to register
        """
        self._providers[provider.provider_name] = provider
        self._metrics[provider.provider_name] = ProviderMetrics()
        if provider.provider_name not in self._provider_order:
            self._provider_order.append(provider.provider_name)

    def unregister_provider(self, provider_name: str) -> bool:
        """Unregister a provider.
        
        Args:
            provider_name: Name of the provider to remove
            
        Returns:
            True if provider was removed
        """
        if provider_name in self._providers:
            del self._providers[provider_name]
            del self._metrics[provider_name]
            self._provider_order.remove(provider_name)
            return True
        return False

    def get_provider(self, name: str) -> ModelProvider | None:
        """Get a specific provider.
        
        Args:
            name: Provider name
            
        Returns:
            Provider or None
        """
        return self._providers.get(name)

    def list_providers(self) -> list[str]:
        """List all registered provider names.
        
        Returns:
            List of provider names
        """
        return list(self._providers.keys())

    def set_preferred_provider(self, name: str) -> None:
        """Set the preferred provider.
        
        Args:
            name: Provider name
        """
        if name in self._providers:
            self._preferred_provider = name

    async def invoke(
        self,
        request: InferenceRequest,
        provider_name: str | None = None,
        strategy: RoutingStrategy | None = None,
    ) -> InferenceResponse:
        """Invoke a model with automatic provider selection.
        
        Args:
            request: The inference request
            provider_name: Specific provider to use (optional)
            strategy: Routing strategy to use (optional)
            
        Returns:
            Inference response
        """
        if not self._initialized:
            await self.initialize()
        
        # Select provider
        if provider_name and provider_name in self._providers:
            selected = provider_name
        else:
            selected = await self._select_provider(strategy or self._config.default_strategy)
        
        if not selected:
            return InferenceResponse(
                content="",
                model="none",
                provider="none",
                error="No available providers",
            )
        
        # Execute with failover
        return await self._execute_with_failover(request, selected)

    async def _select_provider(self, strategy: RoutingStrategy) -> str | None:
        """Select a provider based on strategy.
        
        Args:
            strategy: Routing strategy
            
        Returns:
            Selected provider name or None
        """
        available = self._get_available_providers()
        if not available:
            return None
        
        # Use preferred if available
        if self._preferred_provider and self._preferred_provider in available:
            return self._preferred_provider
        
        if strategy == RoutingStrategy.LATENCY:
            return self._select_by_latency(available)
        elif strategy == RoutingStrategy.COST:
            return self._select_by_capability(available)
        elif strategy == RoutingStrategy.ROUND_ROBIN:
            return self._select_round_robin(available)
        else:
            return available[0] if available else None

    def _get_available_providers(self) -> list[str]:
        """Get list of available provider names.
        
        Returns:
            List of available provider names
        """
        return [
            name for name, provider in self._providers.items()
            if provider.health.status in (ProviderStatus.AVAILABLE, ProviderStatus.DEGRADED)
        ]

    def _select_by_latency(self, available: list[str]) -> str:
        """Select provider with best latency.
        
        Args:
            available: Available provider names
            
        Returns:
            Selected provider name
        """
        best = None
        best_latency = float('inf')
        
        for name in available:
            health = self._providers[name].health
            if health.latency_ms and health.latency_ms < best_latency:
                best_latency = health.latency_ms
                best = name
        
        return best or available[0]

    def _select_by_capability(self, available: list[str]) -> str:
        """Select provider by capability (prefer cost-effective).
        
        Args:
            available: Available provider names
            
        Returns:
            Selected provider name
        """
        # Prefer OpenAI for cost-effectiveness
        if "openai" in available:
            return "openai"
        return available[0]

    def _select_round_robin(self, available: list[str]) -> str:
        """Select provider using round-robin.
        
        Args:
            available: Available provider names
            
        Returns:
            Selected provider name
        """
        # Find index in available list
        while self._current_index < len(self._provider_order):
            provider = self._provider_order[self._current_index]
            self._current_index = (self._current_index + 1) % len(self._provider_order)
            if provider in available:
                return provider
        
        # Fallback to first available
        self._current_index = 1
        return available[0]

    async def _execute_with_failover(
        self,
        request: InferenceRequest,
        primary: str,
    ) -> InferenceResponse:
        """Execute request with automatic failover.
        
        Args:
            request: The inference request
            primary: Primary provider name
            
        Returns:
            Inference response
        """
        last_error: str | None = None
        providers_tried: list[str] = []
        
        for attempt in range(self._config.max_retries):
            provider = self._providers.get(primary)
            if not provider:
                break
            
            providers_tried.append(primary)
            metrics = self._metrics[primary]
            metrics.total_requests += 1
            
            try:
                response = await provider.invoke(request)
                
                if response.error:
                    metrics.failed_requests += 1
                    metrics.last_failure = datetime.now()
                    last_error = response.error
                else:
                    metrics.successful_requests += 1
                    metrics.last_success = datetime.now()
                    if response.latency_ms:
                        metrics.total_latency_ms += response.latency_ms
                    return response
                    
            except Exception as e:
                metrics.failed_requests += 1
                metrics.last_failure = datetime.now()
                last_error = str(e)
            
            # Try failover if enabled
            if self._config.failover_enabled and attempt < self._config.max_retries - 1:
                secondary = self._get_next_provider(primary, providers_tried)
                if secondary:
                    primary = secondary
        
        # All attempts failed
        return InferenceResponse(
            content="",
            model="none",
            provider=";".join(providers_tried),
            error=f"All providers failed. Last error: {last_error}",
        )

    def _get_next_provider(
        self,
        current: str,
        tried: list[str],
    ) -> str | None:
        """Get next available provider for failover.
        
        Args:
            current: Current provider name
            tried: List of already tried providers
            
        Returns:
            Next provider name or None
        """
        available = self._get_available_providers()
        for name in available:
            if name != current and name not in tried:
                return name
        return None

    async def health_check_all(self) -> dict[str, Any]:
        """Check health of all providers.
        
        Returns:
            Health status for all providers
        """
        results = {}
        for name, provider in self._providers.items():
            health = await provider.health_check()
            results[name] = {
                "status": health.status.value,
                "latency_ms": health.latency_ms,
                "last_check": health.last_check.isoformat(),
                "error_count": health.error_count,
            }
        return results

    def get_metrics(self, provider_name: str | None = None) -> dict[str, Any]:
        """Get metrics for providers.
        
        Args:
            provider_name: Specific provider or None for all
            
        Returns:
            Provider metrics
        """
        if provider_name:
            if provider_name in self._metrics:
                return self._metrics[provider_name].__dict__
            return {}
        
        return {
            name: {
                "total_requests": m.total_requests,
                "successful_requests": m.successful_requests,
                "failed_requests": m.failed_requests,
                "avg_latency_ms": m.total_latency_ms / m.total_requests if m.total_requests > 0 else 0,
                "last_request": m.last_request.isoformat() if m.last_request else None,
            }
            for name, m in self._metrics.items()
        }

    def get_capabilities(self) -> dict[str, ProviderCapability]:
        """Get capabilities of all providers.
        
        Returns:
            Provider capabilities by name
        """
        import asyncio
        capabilities = {}
        for name, provider in self._providers.items():
            try:
                caps = asyncio.create_task(provider.get_capabilities())
                # Note: In production, use proper async handling
                capabilities[name] = caps
            except Exception:
                pass
        return capabilities


# Singleton instance for convenience
_manager: ModelProviderManager | None = None


def get_provider_manager() -> ModelProviderManager:
    """Get the global provider manager instance.
    
    Returns:
        Provider manager singleton
    """
    global _manager
    if _manager is None:
        _manager = ModelProviderManager()
    return _manager
