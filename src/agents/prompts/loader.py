"""
Prompt Loader - Loads agent prompts from markdown files.

Prompts are stored in src/agents/prompts/{agent-name}/core.md
"""

from pathlib import Path
from typing import Optional


# Base directory for prompts
PROMPTS_DIR = Path(__file__).parent
# Backwards compatibility alias
PROMPTS_YAML_PATH = PROMPTS_DIR


def load_agent_prompt(prompt_path: str, filename: Optional[str] = None) -> str:
    """
    Load an agent's prompt from its directory.

    Args:
        prompt_path: Directory name under prompts/ (e.g., "spec-analyst")
        filename: Prompt file name. If None, tries core.md then core.yaml

    Returns:
        The prompt content as a string

    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    prompt_dir = PROMPTS_DIR / prompt_path

    # If specific filename provided, use it directly
    if filename:
        prompt_file = prompt_dir / filename
        if not prompt_file.exists():
            raise FileNotFoundError(
                f"Prompt file not found: {prompt_file}. "
                f"Create {prompt_path}/{filename} in src/agents/prompts/"
            )
        return prompt_file.read_text(encoding="utf-8")

    # Try multiple extensions in order of preference
    for ext_file in ["core.md", "core.yaml"]:
        prompt_file = prompt_dir / ext_file
        if prompt_file.exists():
            return prompt_file.read_text(encoding="utf-8")

    raise FileNotFoundError(
        f"Prompt file not found in: {prompt_dir}. "
        f"Create {prompt_path}/core.md or core.yaml in src/agents/prompts/"
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


def get_prompt_content(file_path: str, key: str) -> str:
    """
    Load prompt content from a YAML file by key.

    Used for loading specific prompts from structured YAML files,
    like classifications/intent.yaml.

    Args:
        file_path: Path to YAML file relative to prompts dir
                   (e.g., "classifications/intent.yaml")
        key: Key to extract from the YAML file (e.g., "classification")

    Returns:
        Prompt content as string

    Raises:
        FileNotFoundError: If YAML file doesn't exist
        KeyError: If key not found in YAML
    """
    import yaml

    prompt_file = PROMPTS_DIR / file_path
    if not prompt_file.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_file}. "
            f"Create {file_path} in src/agents/prompts/"
        )

    content = prompt_file.read_text(encoding="utf-8")
    data = yaml.safe_load(content)

    if key not in data:
        raise KeyError(
            f"Key '{key}' not found in {file_path}. "
            f"Available keys: {list(data.keys())}"
        )

    return data[key]


__all__ = [
    "load_agent_prompt",
    "get_prompt_path",
    "get_prompt_content",
    "PROMPTS_DIR",
    "PROMPTS_YAML_PATH",
]
