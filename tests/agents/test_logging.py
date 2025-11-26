"""
Tests for logging configuration and structured logging.

TDD RED Phase: These tests define expected logging behavior.
"""

import pytest
import json
import logging
from io import StringIO
from unittest.mock import patch, MagicMock


# =============================================================================
# Test: Logging Configuration
# =============================================================================

class TestLoggingSetup:
    """Test logging configuration."""

    def test_get_logger_returns_logger(self):
        """get_logger should return a logging.Logger instance."""
        from src.agents.logging_config import get_logger
        logger = get_logger("test")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_has_correct_name(self):
        """Logger name should be prefixed with src.agents."""
        from src.agents.logging_config import get_logger
        logger = get_logger("gateway")
        assert logger.name == "src.agents.gateway"

    def test_setup_logging_sets_level(self):
        """setup_logging should set the correct log level."""
        from src.agents.logging_config import setup_logging, get_logger

        setup_logging(level="DEBUG")
        logger = get_logger("test")
        assert logger.getEffectiveLevel() == logging.DEBUG

        setup_logging(level="WARNING")
        assert logging.getLogger("src.agents").level == logging.WARNING


# =============================================================================
# Test: Request Context
# =============================================================================

class TestRequestContext:
    """Test request context management."""

    def test_set_request_context(self):
        """set_request_context should store context."""
        from src.agents.logging_config import (
            set_request_context, get_request_context, clear_request_context
        )

        set_request_context(request_id="test-123", user_id="user-1")
        ctx = get_request_context()

        assert ctx["request_id"] == "test-123"
        assert ctx["user_id"] == "user-1"

        clear_request_context()

    def test_clear_request_context(self):
        """clear_request_context should reset context."""
        from src.agents.logging_config import (
            set_request_context, get_request_context, clear_request_context
        )

        set_request_context(request_id="test-123")
        clear_request_context()
        ctx = get_request_context()

        assert ctx == {}

    def test_set_request_context_filters_none(self):
        """set_request_context should not include None values."""
        from src.agents.logging_config import (
            set_request_context, get_request_context, clear_request_context
        )

        set_request_context(request_id="test-123", user_id=None)
        ctx = get_request_context()

        assert "request_id" in ctx
        assert "user_id" not in ctx

        clear_request_context()


# =============================================================================
# Test: JSON Formatter
# =============================================================================

class TestJSONFormatter:
    """Test JSON log formatting."""

    def test_json_formatter_produces_valid_json(self):
        """JSONFormatter should produce valid JSON."""
        from src.agents.logging_config import JSONFormatter, clear_request_context

        clear_request_context()

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="src.agents.gateway",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test_event",
            args=(),
            exc_info=None
        )

        output = formatter.format(record)
        parsed = json.loads(output)

        assert parsed["level"] == "INFO"
        assert parsed["event"] == "test_event"
        assert "timestamp" in parsed

    def test_json_formatter_includes_component(self):
        """JSONFormatter should include shortened component name."""
        from src.agents.logging_config import JSONFormatter, clear_request_context

        clear_request_context()

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="src.agents.orchestrator",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test_event",
            args=(),
            exc_info=None
        )

        output = formatter.format(record)
        parsed = json.loads(output)

        assert parsed["component"] == "orchestrator"

    def test_json_formatter_includes_request_context(self):
        """JSONFormatter should include request context."""
        from src.agents.logging_config import (
            JSONFormatter, set_request_context, clear_request_context
        )

        set_request_context(request_id="ctx-123", user_id="user-1")

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="src.agents.gateway",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test_event",
            args=(),
            exc_info=None
        )

        output = formatter.format(record)
        parsed = json.loads(output)

        assert parsed["request_id"] == "ctx-123"
        assert parsed["user_id"] == "user-1"

        clear_request_context()

    def test_json_formatter_includes_extra_data(self):
        """JSONFormatter should include extra data in 'data' field."""
        from src.agents.logging_config import JSONFormatter, clear_request_context

        clear_request_context()

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="src.agents.gateway",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test_event",
            args=(),
            exc_info=None
        )
        record.method = "POST"
        record.duration_ms = 150.5

        output = formatter.format(record)
        parsed = json.loads(output)

        assert parsed["data"]["method"] == "POST"
        assert parsed["data"]["duration_ms"] == 150.5


# =============================================================================
# Test: Human Readable Formatter
# =============================================================================

class TestHumanReadableFormatter:
    """Test human-readable log formatting."""

    def test_human_formatter_includes_timestamp(self):
        """HumanReadableFormatter should include timestamp."""
        from src.agents.logging_config import HumanReadableFormatter, clear_request_context

        clear_request_context()

        formatter = HumanReadableFormatter()
        record = logging.LogRecord(
            name="src.agents.gateway",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test_event",
            args=(),
            exc_info=None
        )

        output = formatter.format(record)

        # Should have timestamp format [YYYY-MM-DD HH:MM:SS]
        assert "[20" in output  # Year starts with 20
        assert "INFO" in output
        assert "gateway" in output
        assert "test_event" in output

    def test_human_formatter_includes_request_id(self):
        """HumanReadableFormatter should include truncated request_id."""
        from src.agents.logging_config import (
            HumanReadableFormatter, set_request_context, clear_request_context
        )

        set_request_context(request_id="abcd1234efgh5678")

        formatter = HumanReadableFormatter()
        record = logging.LogRecord(
            name="src.agents.gateway",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test_event",
            args=(),
            exc_info=None
        )

        output = formatter.format(record)

        # Request ID should be truncated to 8 chars
        assert "abcd1234" in output

        clear_request_context()

    def test_human_formatter_includes_extra_as_key_value(self):
        """HumanReadableFormatter should format extra as key=value."""
        from src.agents.logging_config import HumanReadableFormatter, clear_request_context

        clear_request_context()

        formatter = HumanReadableFormatter()
        record = logging.LogRecord(
            name="src.agents.gateway",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test_event",
            args=(),
            exc_info=None
        )
        record.method = "POST"
        record.status = 200

        output = formatter.format(record)

        assert "method=POST" in output
        assert "status=200" in output


# =============================================================================
# Test: Log Events
# =============================================================================

class TestLogEvents:
    """Test standard log event constants."""

    def test_log_event_constants_exist(self):
        """LogEvent should have all standard event constants."""
        from src.agents.logging_config import LogEvent

        # Request lifecycle
        assert hasattr(LogEvent, "REQUEST_RECEIVED")
        assert hasattr(LogEvent, "REQUEST_COMPLETED")

        # Intent classification
        assert hasattr(LogEvent, "INTENT_CLASSIFYING")
        assert hasattr(LogEvent, "INTENT_CLASSIFIED")

        # Chain execution
        assert hasattr(LogEvent, "CHAIN_STARTING")
        assert hasattr(LogEvent, "CHAIN_COMPLETED")

        # Agent execution
        assert hasattr(LogEvent, "AGENT_STARTING")
        assert hasattr(LogEvent, "AGENT_COMPLETED")

        # LLM calls
        assert hasattr(LogEvent, "LLM_CALLING")
        assert hasattr(LogEvent, "LLM_RESPONSE")

        # Memory operations
        assert hasattr(LogEvent, "MEMORY_RETRIEVING")
        assert hasattr(LogEvent, "MEMORY_RETRIEVED")
        assert hasattr(LogEvent, "MEMORY_STORING")


# =============================================================================
# Test: Duration Logging
# =============================================================================

class TestDurationLogging:
    """Test duration logging helper."""

    def test_log_with_duration_calculates_duration(self):
        """log_with_duration should calculate duration from start_time."""
        import time
        from src.agents.logging_config import log_with_duration, get_logger

        logger = get_logger("test")

        with patch.object(logger, "info") as mock_info:
            start = time.time() - 0.5  # 500ms ago
            log_with_duration(logger, "test_event", start, extra_key="value")

            mock_info.assert_called_once()
            call_kwargs = mock_info.call_args
            extra = call_kwargs.kwargs.get("extra", call_kwargs[1].get("extra", {}))

            assert "duration_ms" in extra
            assert extra["duration_ms"] >= 400  # At least 400ms
            assert extra["extra_key"] == "value"
