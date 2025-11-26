"""
RetroChain - Retrospective Analysis Chain.

Orchestrates agents for reviewing, analyzing, and improving
existing code following the retrospective workflow.
"""

import logging
from dataclasses import dataclass, field
from typing import List

from src.agents.agents.base import BaseAgent
from src.agents.chains.base import BaseChain

# Module logger
logger = logging.getLogger(__name__)


# Retro Chain Agents in execution order
RETRO_AGENTS = [
    BaseAgent(
        id="knowledge-curator",
        name="Knowledge Curator",
        prompt_path="knowledge-curator",
        description="Extracts learnings from development"
    ),
    BaseAgent(
        id="synthesis-specialist",
        name="Synthesis Specialist",
        prompt_path="synthesis-specialist",
        description="Aggregates retrospectives and patterns"
    ),
    BaseAgent(
        id="system-improver",
        name="System Improver",
        prompt_path="system-improver",
        description="Recommends system improvements"
    ),
]


@dataclass
class RetroChain(BaseChain):
    """
    Retrospective Analysis chain.

    Executes 3 agents in sequence:
    1. knowledge-curator - Extracts learnings from development
    2. synthesis-specialist - Aggregates retrospectives and patterns
    3. system-improver - Recommends system improvements
    """

    id: str = field(default="retro")
    name: str = field(default="Retrospective Analysis")
    agents: List[BaseAgent] = field(default_factory=lambda: RETRO_AGENTS.copy())
    description: str = field(
        default="Reviews, analyzes, and improves existing code"
    )
