"""Telemetry - Observability infrastructure for COS."""

from __future__ import annotations

from typing import Any


class ITelemetry:
    """Telemetry service for collecting and reporting system metrics.

    The telemetry service is responsible for:
    - Collecting timing information
    - Recording resource usage
    - Emitting trace events
    - Generating diagnostic metadata
    """

    async def record_timing(self, name: str, duration_ms: float) -> None:
        """Record timing information.

        Args:
            name: Metric name
            duration_ms: Duration in milliseconds
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    async def record_metric(self, name: str, value: Any) -> None:
        """Record a metric value.

        Args:
            name: Metric name
            value: Metric value
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    async def emit_trace(self, trace_id: str, span_id: str, data: dict[str, Any]) -> None:
        """Emit a trace span.

        Args:
            trace_id: Trace identifier
            span_id: Span identifier
            data: Trace data
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    async def get_metrics(self) -> dict[str, Any]:
        """Get all collected metrics.

        Returns:
            Dictionary of metrics
        """
        raise NotImplementedError("Will be implemented in Phase 2")
