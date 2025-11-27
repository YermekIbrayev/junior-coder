"""
Tests for YAML prompt loader - TDD approach.

Tests the prompt loading functionality from .agents/prompts/ YAML files.
Folder structure:
  .agents/prompts/
  ├── INDEX.yaml
  ├── classifications/
  │   └── intent.yaml
  └── {agent-name}/
      └── core.yaml
"""

import pytest
from pathlib import Path


# ============================================================================
# T100: YAML Prompt Loader Module Tests
# ============================================================================

class TestPromptLoaderExists:
    """Test that prompt loader module exists."""

    def test_loader_module_exists(self):
        """loader.py module must exist in src/agents/prompts/."""
        from src.agents.prompts import loader
        assert loader is not None

    def test_load_yaml_prompt_function_exists(self):
        """load_yaml_prompt function must exist."""
        from src.agents.prompts.loader import load_yaml_prompt
        assert callable(load_yaml_prompt)

    def test_get_prompt_content_function_exists(self):
        """get_prompt_content function must exist."""
        from src.agents.prompts.loader import get_prompt_content
        assert callable(get_prompt_content)

    def test_load_agent_prompt_function_exists(self):
        """load_agent_prompt function must exist for agent prompts."""
        from src.agents.prompts.loader import load_agent_prompt
        assert callable(load_agent_prompt)


class TestPromptLoaderPaths:
    """Test prompt loader path configuration."""

    def test_prompts_yaml_path_constant_exists(self):
        """PROMPTS_YAML_PATH constant must be defined."""
        from src.agents.prompts.loader import PROMPTS_YAML_PATH
        assert PROMPTS_YAML_PATH is not None
        assert isinstance(PROMPTS_YAML_PATH, Path)

    def test_prompts_yaml_path_points_to_agents_prompts(self):
        """PROMPTS_YAML_PATH must point to .agents/prompts/."""
        from src.agents.prompts.loader import PROMPTS_YAML_PATH
        assert PROMPTS_YAML_PATH.name == "prompts"
        assert PROMPTS_YAML_PATH.parent.name == ".agents"


# ============================================================================
# T101: Folder Structure Tests
# ============================================================================

class TestFolderStructure:
    """Test that folder structure is correct."""

    def test_index_yaml_at_root(self):
        """INDEX.yaml must exist at .agents/prompts/ root."""
        from src.agents.prompts.loader import PROMPTS_YAML_PATH
        index_path = PROMPTS_YAML_PATH / "INDEX.yaml"
        assert index_path.exists(), f"Missing: {index_path}"

    def test_classifications_folder_exists(self):
        """classifications/ folder must exist."""
        from src.agents.prompts.loader import PROMPTS_YAML_PATH
        classifications_path = PROMPTS_YAML_PATH / "classifications"
        assert classifications_path.exists(), f"Missing: {classifications_path}"
        assert classifications_path.is_dir()

    def test_intent_yaml_in_classifications(self):
        """intent.yaml must exist in classifications/."""
        from src.agents.prompts.loader import PROMPTS_YAML_PATH
        intent_path = PROMPTS_YAML_PATH / "classifications" / "intent.yaml"
        assert intent_path.exists(), f"Missing: {intent_path}"

    def test_no_yaml_files_at_root_except_index(self):
        """Only INDEX.yaml should be at root, others in subfolders."""
        from src.agents.prompts.loader import PROMPTS_YAML_PATH
        root_yaml_files = list(PROMPTS_YAML_PATH.glob("*.yaml"))
        yaml_names = [f.name for f in root_yaml_files]
        assert yaml_names == ["INDEX.yaml"], f"Unexpected files at root: {yaml_names}"


# ============================================================================
# T102: Classification Prompts Tests
# ============================================================================

class TestClassificationPrompts:
    """Test classification prompts loading."""

    def test_load_classification_prompt(self):
        """Must load classification prompt from classifications/intent.yaml."""
        from src.agents.prompts.loader import load_yaml_prompt
        result = load_yaml_prompt("classifications/intent.yaml", "classification")
        assert isinstance(result, dict)
        assert "content" in result

    def test_classification_content_has_intent_keywords(self):
        """Classification prompt must contain intent keywords."""
        from src.agents.prompts.loader import get_prompt_content
        result = get_prompt_content("classifications/intent.yaml", "classification")
        assert "intent" in result.lower()
        assert "classify" in result.lower() or "classifier" in result.lower()

    def test_load_clarifying_question(self):
        """Must load clarifying question from classifications/intent.yaml."""
        from src.agents.prompts.loader import get_prompt_content
        result = get_prompt_content("classifications/intent.yaml", "clarifying_question")
        assert "clarify" in result.lower() or "help" in result.lower()

    def test_classification_has_config(self):
        """Classification prompt should have config section."""
        from src.agents.prompts.loader import load_yaml_prompt
        result = load_yaml_prompt("classifications/intent.yaml", "classification")
        assert "config" in result
        assert "temperature" in result["config"]


# ============================================================================
# T103: Agent Prompts Tests
# ============================================================================

class TestAgentPrompts:
    """Test agent prompt loading."""

    def test_spec_analyst_folder_exists(self):
        """spec-analyst/ folder must exist."""
        from src.agents.prompts.loader import PROMPTS_YAML_PATH
        path = PROMPTS_YAML_PATH / "spec-analyst"
        assert path.exists(), f"Missing: {path}"

    def test_spec_analyst_core_yaml_exists(self):
        """spec-analyst/core.yaml must exist."""
        from src.agents.prompts.loader import PROMPTS_YAML_PATH
        path = PROMPTS_YAML_PATH / "spec-analyst" / "core.yaml"
        assert path.exists(), f"Missing: {path}"

    def test_load_agent_prompt_returns_string(self):
        """load_agent_prompt must return prompt content string."""
        from src.agents.prompts.loader import load_agent_prompt
        result = load_agent_prompt("spec-analyst")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_load_agent_prompt_contains_role(self):
        """Agent prompt must contain role description."""
        from src.agents.prompts.loader import load_agent_prompt
        result = load_agent_prompt("spec-analyst")
        assert "spec" in result.lower() or "analyst" in result.lower()

    def test_test_architect_prompt_exists(self):
        """test-architect agent prompt must exist."""
        from src.agents.prompts.loader import load_agent_prompt
        result = load_agent_prompt("test-architect")
        assert isinstance(result, str)
        assert len(result) > 0


# ============================================================================
# T104: Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Test error handling in prompt loader."""

    def test_load_yaml_prompt_raises_on_missing_file(self):
        """load_yaml_prompt must raise FileNotFoundError for missing file."""
        from src.agents.prompts.loader import load_yaml_prompt
        with pytest.raises(FileNotFoundError):
            load_yaml_prompt("nonexistent/file.yaml", "any")

    def test_load_yaml_prompt_raises_on_missing_key(self):
        """load_yaml_prompt must raise KeyError for missing prompt key."""
        from src.agents.prompts.loader import load_yaml_prompt
        with pytest.raises(KeyError):
            load_yaml_prompt("classifications/intent.yaml", "nonexistent_key")

    def test_load_agent_prompt_raises_on_missing_agent(self):
        """load_agent_prompt must raise FileNotFoundError for missing agent."""
        from src.agents.prompts.loader import load_agent_prompt
        with pytest.raises(FileNotFoundError):
            load_agent_prompt("nonexistent-agent")


# ============================================================================
# T105: Integration with Constants Tests
# ============================================================================

class TestConstantsIntegration:
    """Test that constants.py uses YAML prompts."""

    def test_classification_prompt_loaded_from_yaml(self):
        """CLASSIFICATION_PROMPT in constants should match YAML."""
        from src.agents.orchestrator.constants import CLASSIFICATION_PROMPT
        from src.agents.prompts.loader import get_prompt_content
        yaml_content = get_prompt_content("classifications/intent.yaml", "classification")
        assert CLASSIFICATION_PROMPT == yaml_content

    def test_clarifying_question_loaded_from_yaml(self):
        """CLARIFYING_QUESTION in constants should match YAML."""
        from src.agents.orchestrator.constants import CLARIFYING_QUESTION
        from src.agents.prompts.loader import get_prompt_content
        yaml_content = get_prompt_content("classifications/intent.yaml", "clarifying_question")
        assert CLARIFYING_QUESTION == yaml_content


# ============================================================================
# T106: BaseAgent Integration Tests
# ============================================================================

class TestBaseAgentIntegration:
    """Test that BaseAgent loads prompts from YAML."""

    def test_base_agent_loads_from_yaml(self):
        """BaseAgent.load_prompt() must load from .agents/prompts/."""
        from src.agents.agents.base import BaseAgent
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        prompt = agent.load_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_base_agent_prompt_matches_yaml(self):
        """BaseAgent prompt must match YAML file content."""
        from src.agents.agents.base import BaseAgent
        from src.agents.prompts.loader import load_agent_prompt

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        agent_prompt = agent.load_prompt()
        yaml_prompt = load_agent_prompt("spec-analyst")
        assert agent_prompt == yaml_prompt
