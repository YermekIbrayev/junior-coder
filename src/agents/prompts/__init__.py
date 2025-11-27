"""
Prompt system for agents.

Provides YAML-based prompts for all agents and classifications.
Prompts are stored in src/agents/prompts/ with folder-per-category structure.
"""

from src.agents.prompts.loader import (
    PROMPTS_YAML_PATH,
    PROMPTS_DIR,
    load_yaml_prompt,
    get_prompt_content,
    load_agent_prompt,
    get_prompt_path,
)

__all__ = [
    "PROMPTS_YAML_PATH",
    "PROMPTS_DIR",
    "load_yaml_prompt",
    "get_prompt_content",
    "load_agent_prompt",
    "get_prompt_path",
]
