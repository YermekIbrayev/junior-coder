"""
SDDChain - Specification-Driven Development Chain.

Orchestrates agents for creating specifications, design documents,
and planning features following the SDD workflow.
"""

import logging
from dataclasses import dataclass, field
from typing import List

from src.agents.agents.base import BaseAgent
from src.agents.chains.base import BaseChain

# Module logger
logger = logging.getLogger(__name__)


# SDD Chain Agents in execution order
SDD_AGENTS = [
    BaseAgent(
        id="spec-analyst",
        name="Spec Analyst",
        prompt_path="spec-analyst",
        description="Analyzes requirements and creates specifications"
    ),
    BaseAgent(
        id="spec-clarifier",
        name="Spec Clarifier",
        prompt_path="spec-clarifier",
        description="Identifies ambiguities and asks clarifying questions"
    ),
    BaseAgent(
        id="code-planner",
        name="Code Planner",
        prompt_path="code-planner",
        description="Designs architecture using SOLID principles"
    ),
    BaseAgent(
        id="alignment-analyzer",
        name="Alignment Analyzer",
        prompt_path="alignment-analyzer",
        description="Verifies spec/tests/architecture alignment"
    ),
    BaseAgent(
        id="vibe-check-guardian",
        name="Vibe Check Guardian",
        prompt_path="vibe-check-guardian",
        description="Challenges assumptions and identifies blind spots"
    ),
]


@dataclass
class SDDChain(BaseChain):
    """
    Specification-Driven Development chain.

    Executes 5 agents in sequence:
    1. spec-analyst - Analyzes requirements, creates specifications
    2. spec-clarifier - Identifies ambiguities, asks clarifying questions
    3. code-planner - Designs architecture using SOLID principles
    4. alignment-analyzer - Verifies spec/tests/architecture alignment
    5. vibe-check-guardian - Challenges assumptions, identifies blind spots
    """

    id: str = field(default="sdd")
    name: str = field(default="Specification-Driven Development")
    agents: List[BaseAgent] = field(default_factory=lambda: SDD_AGENTS.copy())
    description: str = field(
        default="Creates specifications, design documents, and plans features"
    )
