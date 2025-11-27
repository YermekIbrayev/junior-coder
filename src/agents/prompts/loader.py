"""
YAML Prompt Loader.

Loads prompts from src/agents/prompts/ YAML files.
Single Responsibility: Load and provide access to YAML-defined prompts.

Folder structure:
  src/agents/prompts/
  ├── INDEX.yaml              # Master index
  ├── classifications/        # Classification prompts
  │   └── intent.yaml
  └── {agent-name}/          # Agent prompts
      └── core.yaml
"""

from pathlib import Path
import yaml

# Path to YAML prompts directory (same directory as this loader)
PROMPTS_YAML_PATH = Path(__file__).parent


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


def load_agent_prompt(agent_name: str) -> str:
    """
    Load an agent's core prompt from YAML.

    Agents have prompts in src/agents/prompts/{agent-name}/core.yaml.
    Returns the 'role' field which contains the agent's identity and instructions.

    Args:
        agent_name: Name of the agent (e.g., "spec-analyst", "test-architect")

    Returns:
        The agent's role/prompt as a string.

    Raises:
        FileNotFoundError: If the agent's prompt file doesn't exist.
    """
    agent_path = PROMPTS_YAML_PATH / agent_name / "core.yaml"

    if not agent_path.exists():
        raise FileNotFoundError(f"Agent prompt not found: {agent_path}")

    with open(agent_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Return the role as the main prompt content
    return data.get("role", "")
