"""
BaseAgent - Foundation class for all AI agents.

Provides common functionality for agent identification and prompt loading.
"""

from dataclasses import dataclass, field
from pathlib import Path


# Base path for agent prompts
PROMPTS_BASE_PATH = Path(__file__).parent.parent / "prompts"


def load_prompt_file(file_path: Path) -> str:
    """
    Load content from a prompt file.

    Args:
        file_path: Path to the prompt markdown file

    Returns:
        Content of the file as string

    Raises:
        FileNotFoundError: If the file does not exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    return file_path.read_text(encoding="utf-8")


@dataclass
class BaseAgent:
    """
    Base class for all agents in the orchestration system.

    Attributes:
        id: Unique identifier for the agent (e.g., "spec-analyst")
        name: Human-readable name (e.g., "Spec Analyst")
        prompt_path: Directory name under src/agents/prompts/
        description: Brief description of the agent's role
    """

    id: str
    name: str
    prompt_path: str
    description: str = field(default="")

    def load_prompt(self) -> str:
        """
        Load the agent's prompt content.

        Reads core.md from the agent's prompt directory.

        Returns:
            The prompt content as a string

        Raises:
            FileNotFoundError: If prompt directory or core.md doesn't exist
        """
        prompt_dir = PROMPTS_BASE_PATH / self.prompt_path

        if not prompt_dir.exists():
            raise FileNotFoundError(
                f"Prompt directory not found: {prompt_dir}"
            )

        core_file = prompt_dir / "core.md"
        if not core_file.exists():
            raise FileNotFoundError(
                f"core.md not found in: {prompt_dir}"
            )

        return load_prompt_file(core_file)
