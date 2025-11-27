"""
Prompt system for agents.

Provides YAML-based prompts for all agents and classifications.
Prompts are stored in .agents/prompts/ with folder-per-category structure.
"""

from src.agents.prompts.loader import (
    PROMPTS_YAML_PATH,
    load_yaml_prompt,
    get_prompt_content,
    load_agent_prompt,
)

__all__ = [
    "PROMPTS_YAML_PATH",
    "load_yaml_prompt",
    "get_prompt_content",
    "load_agent_prompt",
]
