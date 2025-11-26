"""
TDDChain - Test-Driven Development Chain.

Orchestrates agents for writing tests, implementing code,
and ensuring quality following the TDD workflow.
"""

import logging
from dataclasses import dataclass, field
from typing import List

from src.agents.agents.base import BaseAgent
from src.agents.chains.base import BaseChain

# Module logger
logger = logging.getLogger(__name__)


# TDD Chain Agents in execution order
TDD_AGENTS = [
    BaseAgent(
        id="test-architect",
        name="Test Architect",
        prompt_path="test-architect",
        description="Designs test strategy and writes failing tests (RED)"
    ),
    BaseAgent(
        id="implementation-specialist",
        name="Implementation Specialist",
        prompt_path="implementation-specialist",
        description="Makes tests pass with minimal code (GREEN)"
    ),
    BaseAgent(
        id="quality-guardian",
        name="Quality Guardian",
        prompt_path="quality-guardian",
        description="Refactors, security scan, production certification"
    ),
]


@dataclass
class TDDChain(BaseChain):
    """
    Test-Driven Development chain.

    Executes 3 agents in sequence:
    1. test-architect - Designs test strategy, writes failing tests (RED)
    2. implementation-specialist - Makes tests pass with minimal code (GREEN)
    3. quality-guardian - Refactors, security scan, production certification
    """

    id: str = field(default="tdd")
    name: str = field(default="Test-Driven Development")
    agents: List[BaseAgent] = field(default_factory=lambda: TDD_AGENTS.copy())
    description: str = field(
        default="Writes tests, implements code, and ensures quality"
    )
