"""
Tests for BaseAgent class.

TDD Phase: RED - These tests should FAIL until BaseAgent is implemented.
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
        """load_prompt() must load core.md content from prompt_path."""
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )
        result = agent.load_prompt()
        # core.md contains role definition
        assert "Spec Analyst" in result or "spec-analyst" in result.lower()

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


class TestBaseAgentPromptLoader:
    """Test prompt loader utility function."""

    def test_load_prompt_file_reads_index(self):
        """Prompt loader must read INDEX.md to understand module structure."""
        from src.agents.agents.base import load_prompt_file

        # INDEX.md exists for spec-analyst
        prompts_dir = Path("src/agents/prompts/spec-analyst")
        content = load_prompt_file(prompts_dir / "INDEX.md")
        assert "INDEX" in content or "Navigation" in content

    def test_load_prompt_file_reads_core(self):
        """Prompt loader must be able to read core.md."""
        from src.agents.agents.base import load_prompt_file

        prompts_dir = Path("src/agents/prompts/spec-analyst")
        content = load_prompt_file(prompts_dir / "core.md")
        assert "Role" in content or "Agent" in content

    def test_load_prompt_file_raises_for_missing(self):
        """Prompt loader must raise FileNotFoundError for missing files."""
        from src.agents.agents.base import load_prompt_file

        with pytest.raises(FileNotFoundError):
            load_prompt_file(Path("nonexistent/file.md"))


class TestPromptLoaderIndexNavigation:
    """Test prompt loader INDEX.md-based navigation per research.md decision."""

    def test_index_md_contains_loading_strategy(self):
        """INDEX.md must contain loading strategy guidance."""
        from src.agents.agents.base import load_prompt_file

        prompts_dir = Path("src/agents/prompts/spec-analyst")
        content = load_prompt_file(prompts_dir / "INDEX.md")
        # INDEX.md should have loading instructions
        assert "Load" in content or "core.md" in content

    def test_index_md_lists_available_modules(self):
        """INDEX.md must list available modules for the agent."""
        from src.agents.agents.base import load_prompt_file

        prompts_dir = Path("src/agents/prompts/spec-analyst")
        content = load_prompt_file(prompts_dir / "INDEX.md")
        # Should reference core.md as minimum
        assert "core" in content.lower()

    def test_prompt_loader_handles_different_agents(self):
        """Prompt loader should work for multiple agent prompt directories."""
        from src.agents.agents.base import load_prompt_file

        # Test with different agents that have prompts
        agents_with_prompts = [
            "spec-analyst",
            "spec-clarifier",
            "code-planner",
            "test-architect"
        ]

        for agent_name in agents_with_prompts:
            prompts_dir = Path(f"src/agents/prompts/{agent_name}")
            core_content = load_prompt_file(prompts_dir / "core.md")
            assert len(core_content) > 0, f"core.md empty for {agent_name}"

    def test_load_prompt_returns_utf8_content(self):
        """Prompt loader must handle UTF-8 encoded content."""
        from src.agents.agents.base import load_prompt_file

        prompts_dir = Path("src/agents/prompts/spec-analyst")
        content = load_prompt_file(prompts_dir / "core.md")
        # Should be able to encode/decode as UTF-8
        assert content == content.encode("utf-8").decode("utf-8")

    def test_base_agent_load_prompt_uses_prompts_base_path(self):
        """BaseAgent.load_prompt() must use PROMPTS_BASE_PATH constant."""
        from src.agents.agents.base import BaseAgent, PROMPTS_BASE_PATH

        assert PROMPTS_BASE_PATH.exists()
        assert "prompts" in str(PROMPTS_BASE_PATH)

        # Verify agent can load from the base path
        agent = BaseAgent(
            id="test-architect",
            name="Test Architect",
            prompt_path="test-architect"
        )
        prompt = agent.load_prompt()
        assert len(prompt) > 0
