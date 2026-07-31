"""Unit tests for COS package initialization."""

import pytest


def test_version_exists():
    """Test that version is defined."""
    from cos import __version__

    assert __version__ is not None


def test_imports():
    """Test that main imports work."""
    from cos import CognitiveContext, CognitiveBroker

    assert CognitiveContext is not None
    assert CognitiveBroker is not None


def test_cognitive_context_has_properties():
    """Test CognitiveContext has required properties."""
    from cos.kernel.context.cognitive_context import CognitiveContext

    ctx = object.__new__(CognitiveContext)
    assert hasattr(ctx, "kernel")
    assert hasattr(ctx, "cognition")


def test_cognitive_broker_has_capabilities():
    """Test CognitiveBroker has required capability properties."""
    from cos.broker.cognitive_broker import CognitiveBroker

    # Check that the class has these as properties (not necessarily implemented)
    broker_cls = CognitiveBroker
    assert hasattr(broker_cls, "reasoning")
    assert hasattr(broker_cls, "memory")
    assert hasattr(broker_cls, "world")
    assert hasattr(broker_cls, "meta")
    assert hasattr(broker_cls, "learning")
    assert hasattr(broker_cls, "planning")
    assert hasattr(broker_cls, "assistant")
