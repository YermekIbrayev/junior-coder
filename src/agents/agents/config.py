"""
Agent Configuration - Constants for agent execution.

Single Responsibility: Centralize agent and LLM configuration.
"""

# LLM service configuration
LLM_BASE_URL = "http://192.168.51.22:8080"
DEFAULT_MODEL = "gpt-oss"  # Default model for agent execution
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
LLM_TIMEOUT = 120.0  # seconds

__all__ = [
    "LLM_BASE_URL",
    "DEFAULT_MODEL",
    "DEFAULT_TEMPERATURE",
    "DEFAULT_MAX_TOKENS",
    "LLM_TIMEOUT",
]
