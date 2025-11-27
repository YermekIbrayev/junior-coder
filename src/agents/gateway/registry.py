"""
Agent Registry - Available agents and their descriptions.

Single Responsibility: Agent metadata only.
"""

AGENTS = {
    # Orchestrator (main entry point)
    "orchestrator": "Routes to appropriate flow (SDD/TDD/Retro)",

    # Agent Chains (workflow orchestration)
    "sdd": "Specification-Driven Development chain (5 agents)",
    "tdd": "Test-Driven Development chain (3 agents)",
    "retro": "Retrospective Analysis chain (3 agents)",

    # Individual Agents
    "spec-analyst": "Analyzes requirements, creates specifications",
    "spec-clarifier": "Identifies ambiguities, asks clarifying questions",
    "test-architect": "Designs test strategy, writes failing tests (RED)",
    "code-planner": "Designs architecture using SOLID principles",
    "alignment-analyzer": "Verifies spec/tests/architecture alignment",
    "implementation-specialist": "Makes tests pass (GREEN)",
    "quality-guardian": "Refactors, security scan, production certification",
    "knowledge-curator": "Extracts learnings from development",
    "synthesis-specialist": "Aggregates retrospectives",
    "system-improver": "Recommends system improvements",
    "vibe-check-guardian": "Challenges assumptions, identifies blind spots",

    # Tool Agents
    "indexer": "Indexes codebase structure, enables architecture search",
}

__all__ = ["AGENTS"]
