"""
BaseAgent - Foundation class for all AI agents.

Provides common functionality for agent identification and prompt loading.
Prompts are loaded from .agents/prompts/{agent-name}/core.yaml.
"""

from dataclasses import dataclass, field
from src.agents.prompts.loader import load_agent_prompt


@dataclass
class BaseAgent:
    """
    Base class for all agents in the orchestration system.

    Attributes:
        id: Unique identifier for the agent (e.g., "spec-analyst")
        name: Human-readable name (e.g., "Spec Analyst")
        prompt_path: Directory name under .agents/prompts/
        description: Brief description of the agent's role
    """

    id: str
    name: str
    prompt_path: str
    description: str = field(default="")

    def load_prompt(self) -> str:
        """
        Load the agent's prompt content from YAML.

        Reads role from .agents/prompts/{prompt_path}/core.yaml.

        Returns:
            The prompt content as a string

        Raises:
            FileNotFoundError: If prompt file doesn't exist
        """
        return load_agent_prompt(self.prompt_path)
