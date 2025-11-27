"""
YAML and Markdown Prompt Loader.

Loads prompts from src/agents/prompts/ YAML and markdown files.
Single Responsibility: Load and provide access to prompt content.

Folder structure:
  src/agents/prompts/
  ├── INDEX.yaml              # Master index
  ├── classifications/        # Classification prompts
  │   └── intent.yaml
  └── {agent-name}/          # Agent prompts
      └── core.yaml or core.md
"""

from pathlib import Path
from typing import Optional
import yaml

# Path to prompts directory (same directory as this loader)
PROMPTS_YAML_PATH = Path(__file__).parent
# Alias for backwards compatibility
PROMPTS_DIR = PROMPTS_YAML_PATH


def load_yaml_prompt(file_path: str, prompt_key: str) -> dict:
    """
    Load a specific prompt from a YAML file.

    Args:
        file_path: Relative path to YAML file (e.g., "classifications/intent.yaml")
        prompt_key: Key of the prompt within the file (e.g., "classification")

    Returns:
        Dictionary containing prompt data with at least 'content' key.

    Raises:
        FileNotFoundError: If the YAML file doesn't exist.
        KeyError: If the prompt_key doesn't exist in the file.
    """
    full_path = PROMPTS_YAML_PATH / file_path

    if not full_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {full_path}")

    with open(full_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if "prompts" not in data:
        raise KeyError(f"No 'prompts' section in {file_path}")

    if prompt_key not in data["prompts"]:
        raise KeyError(f"Prompt '{prompt_key}' not found in {file_path}")

    return data["prompts"][prompt_key]


def get_prompt_content(file_path: str, prompt_key: str) -> str:
    """
    Get the content string from a prompt.

    Convenience function that extracts just the content field.

    Args:
        file_path: Relative path to YAML file (e.g., "classifications/intent.yaml")
        prompt_key: Key of the prompt within the file (e.g., "classification")

    Returns:
        The prompt content as a string.
    """
    prompt = load_yaml_prompt(file_path, prompt_key)
    return prompt["content"]


def load_agent_prompt(agent_name: str, filename: Optional[str] = None) -> str:
    """
    Load an agent's core prompt from YAML or markdown.

    Agents have prompts in src/agents/prompts/{agent-name}/.
    Tries core.md first, then core.yaml.

    Args:
        agent_name: Name of the agent (e.g., "spec-analyst", "test-architect")
        filename: Optional specific filename to load

    Returns:
        The agent's prompt as a string.

    Raises:
        FileNotFoundError: If the agent's prompt file doesn't exist.
    """
    prompt_dir = PROMPTS_YAML_PATH / agent_name

    # If specific filename provided, use it directly
    if filename:
        prompt_file = prompt_dir / filename
        if not prompt_file.exists():
            raise FileNotFoundError(
                f"Prompt file not found: {prompt_file}. "
                f"Create {agent_name}/{filename} in src/agents/prompts/"
            )
        return prompt_file.read_text(encoding="utf-8")

    # Try .md first (preferred), then .yaml
    for ext_file in ["core.md", "core.yaml"]:
        prompt_file = prompt_dir / ext_file
        if prompt_file.exists():
            if ext_file.endswith(".yaml"):
                # For YAML files, return the 'role' field
                with open(prompt_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                return data.get("role", "")
            else:
                return prompt_file.read_text(encoding="utf-8")

    raise FileNotFoundError(
        f"Agent prompt not found in: {prompt_dir}. "
        f"Create {agent_name}/core.md or core.yaml in src/agents/prompts/"
    )


def get_prompt_path(prompt_path: str) -> Path:
    """
    Get the full path to an agent's prompt directory.

    Args:
        prompt_path: Directory name under prompts/

    Returns:
        Path to the prompt directory
    """
    return PROMPTS_DIR / prompt_path


__all__ = [
    "PROMPTS_YAML_PATH",
    "PROMPTS_DIR",
    "load_yaml_prompt",
    "get_prompt_content",
    "load_agent_prompt",
    "get_prompt_path",
]
