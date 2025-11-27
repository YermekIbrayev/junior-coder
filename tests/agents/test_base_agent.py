"""
Tests for BaseAgent class.

TDD Phase: GREEN - BaseAgent loads prompts from .agents/prompts/{agent}/core.yaml
"""

import pytest
from pathlib import Path


class TestBaseAgentFields:
    """Test BaseAgent has required fields: id, name, prompt_path."""

    def test_base_agent_has_id_field(self):
        """BaseAgent must have an 'id' field."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        assert agent.id == "spec-analyst"

    def test_base_agent_has_name_field(self):
        """BaseAgent must have a 'name' field."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        assert agent.name == "Spec Analyst"

    def test_base_agent_has_prompt_path_field(self):
        """BaseAgent must have a 'prompt_path' field."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        assert agent.prompt_path == "spec-analyst"

    def test_base_agent_has_description_field(self):
        """BaseAgent must have an optional 'description' field."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst",
            description="Analyzes specifications"
        )
        assert agent.description == "Analyzes specifications"

    def test_base_agent_description_defaults_to_empty(self):
        """BaseAgent description should default to empty string."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        assert agent.description == ""


class TestBaseAgentLoadPrompt:
    """Test BaseAgent.load_prompt() method."""

    def test_load_prompt_returns_string(self):
        """load_prompt() must return a string."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        result = agent.load_prompt()
        assert isinstance(result, str)

    def test_load_prompt_returns_non_empty(self):
        """load_prompt() must return non-empty content for valid prompt_path."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        result = agent.load_prompt()
        assert len(result) > 0

    def test_load_prompt_includes_core_content(self):
        """load_prompt() must load core.yaml content from prompt_path."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        result = agent.load_prompt()
        # core.yaml contains role definition
        assert "Spec Analyst" in result or "spec" in result.lower()

    def test_load_prompt_with_invalid_path_raises_error(self):
        """load_prompt() must raise FileNotFoundError for invalid prompt_path."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="nonexistent",
            name="Nonexistent Agent",
            prompt_path="nonexistent-agent"
        )
        with pytest.raises(FileNotFoundError):
            agent.load_prompt()


class TestBaseAgentYamlPromptLoader:
    """Test BaseAgent loads prompts from YAML files."""

    def test_load_prompt_uses_yaml_loader(self):
        """BaseAgent.load_prompt() must use YAML loader from .agents/prompts/."""
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

    def test_load_prompt_loads_from_agents_prompts(self):
        """BaseAgent.load_prompt() must load from .agents/prompts/{path}/core.md or core.yaml."""
        from src.agents.agents.base import BaseAgent
        from src.agents.prompts.loader import PROMPTS_DIR

        agent = BaseAgent(
            id="test-architect",
            name="Test Architect",
            prompt_path="test-architect"
        )
        prompt = agent.load_prompt()
        assert len(prompt) > 0

        # Verify a prompt file exists (either .md or .yaml)
        md_file = PROMPTS_DIR / "test-architect" / "core.md"
        yaml_file = PROMPTS_DIR / "test-architect" / "core.yaml"
        assert md_file.exists() or yaml_file.exists()

    def test_load_prompt_handles_different_agents(self):
        """load_prompt() should work for multiple agents."""
        from src.agents.agents.base import BaseAgent

        agents = [
            ("spec-analyst", "Spec Analyst"),
            ("test-architect", "Test Architect"),
            ("code-planner", "Code Planner"),
            ("implementation-specialist", "Implementation Specialist"),
        ]

        for agent_id, agent_name in agents:
            agent = BaseAgent(
                id=agent_id,
                name=agent_name,
                prompt_path=agent_id
            )
            prompt = agent.load_prompt()
            assert len(prompt) > 0, f"Prompt empty for {agent_id}"

    def test_load_prompt_returns_utf8_content(self):
        """Prompt loader must handle UTF-8 encoded content."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        content = agent.load_prompt()
        # Should be able to encode/decode as UTF-8
        assert content == content.encode("utf-8").decode("utf-8")
