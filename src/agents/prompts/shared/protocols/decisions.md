# Decision Framework

**Purpose**: Templates for CRITICAL vs NON-CRITICAL decisions. **Used By**: All agents

## Classification

**CRITICAL** (ask human): Architecture change, security/compliance, performance impact, external dependency, breaking change, unclear requirements

**NON-CRITICAL** (autonomous): Code organization, naming, minor refactoring, test structure, documentation style, implementation details

## CRITICAL Template

```markdown
⚠️ CRITICAL DECISION REQUIRED

Context: {what you're deciding}
Problem: {why uncertain}

Options:
  1. {Approach A} - Pros: {...} | Cons: {...}
  2. {Approach B} - Pros: {...} | Cons: {...}

Recommendation: {your analysis}
Question: Which approach?

Will wait for guidance.
```

## NON-CRITICAL Documentation

```markdown
### Decision: {Title}
**Context**: {what} | **Chosen**: {decision} | **Rationale**: {why} | **Based On**: {patterns/principles}
```

Document in agent's output artifact.

## Autonomy Metrics

| Project | Critical | Asked | Autonomous | Rate |
|---------|----------|-------|------------|------|
| 1 | 6 | 6 | 21 | 78% |
| 2 | 4 | 4 | 25 | 86% |

**Goal**: ↑ autonomy rate while maintaining quality

## When Uncertain
Vibe Check → Query past learnings → **If still uncertain → CRITICAL**

---

**Detailed Guide**: [guides/decision-framework-detailed.md](../guides/decision-framework-detailed.md) (examples by agent)
