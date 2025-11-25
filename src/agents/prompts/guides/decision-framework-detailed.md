# Decision Framework

**Purpose**: Templates for communicating CRITICAL vs NON-CRITICAL decisions to humans.

**Used By**: All agents

---

## Decision Classification

### CRITICAL Decisions (Require Human Approval)

Decisions that significantly impact:
- Architecture or system design
- Security or compliance
- Performance or scalability
- External dependencies
- Breaking changes
- Unclear requirements

**Action**: **STOP and ask human** before proceeding.

### NON-CRITICAL Decisions (Autonomous)

Decisions within established patterns:
- Code organization and naming
- Minor refactorings
- Test structure
- Documentation style
- Implementation details within architecture

**Action**: Decide autonomously, document rationale.

---

## CRITICAL Decision Template

When facing a CRITICAL decision, use this template:

```markdown
⚠️ CRITICAL DECISION REQUIRED

Context: {what you're trying to decide/implement/test}
Problem: {why current approach isn't working or is uncertain}
[Optional] Attempts: {what you've tried so far, if applicable}

Options:
  1. {Approach A}
     - Pros: {...}
     - Cons: {...}
     [Optional] - Impact: {...}

  2. {Approach B}
     - Pros: {...}
     - Cons: {...}
     [Optional] - Impact: {...}

  [If applicable] 3. {Alternative approach, e.g., "Revise architecture/tests"}
     - Requires: {what would need to change}
     - Impact: {downstream effects}

[Optional] Trade-offs: {key trade-offs between options}
Recommendation: {your analysis and preferred option with rationale}

Question: Which approach should I take?

Will wait for your guidance before proceeding.
```

---

## NON-CRITICAL Decision Documentation

When making NON-CRITICAL decisions autonomously:

```markdown
### Decision: {Brief title}

**Context**: {What you needed to decide}
**Options Considered**: {Brief list}
**Chosen**: {What you decided}
**Rationale**: {Why this choice}
**Based On**: {Existing patterns from Serena/Octocode, or principles}
```

**Where to Document**:
- Spec Analyst: In spec.md "Assumptions" section
- Test Architect: In tests.md "Test Strategy" section
- Code Planner: In architecture.md "Design Decisions" section
- Implementation Specialist: In implementation-notes.md
- Quality Guardian: In quality-report.md

---

## Examples

### CRITICAL Decision Example

```markdown
⚠️ CRITICAL DECISION REQUIRED

Context: Implementing invoice adjustment feature
Problem: Tests keep failing after 5 implementation attempts due to complex concurrency handling

Options:
  1. Continue with select_for_update() approach
     - Pros: Handles concurrency correctly
     - Cons: Complex implementation, tests brittle
     - Impact: May need 2 more hours to debug

  2. Use simpler pessimistic locking
     - Pros: Easier to implement and test
     - Cons: Lower concurrency, potential performance impact
     - Impact: May slow down under high load (>100 concurrent users)

  3. Revise architecture to avoid concurrency altogether
     - Requires: Returning to Code Planner phase
     - Impact: 4-6 hour delay but cleaner solution

Recommendation: Option 2 (simpler locking) for v1, then optimize in v2 if needed

Question: Which approach should I take, or should I escalate to another agent?

Will wait for your guidance before proceeding.
```

### NON-CRITICAL Decision Example

```markdown
### Decision: Test Fixture Organization

**Context**: Needed to structure pytest fixtures for invoice tests
**Options Considered**: Inline fixtures vs conftest.py vs factory pattern
**Chosen**: Factory pattern using FactoryBoy
**Rationale**: Consistent with existing codebase patterns (found via Serena)
**Based On**: Existing InvoiceFactory pattern in tests/factories.py
```

---

## Decision Autonomy Metrics

Track decision-making progress:

| Project | Critical Decisions | Asked Human | Autonomous | Autonomy Rate |
|---------|-------------------|-------------|------------|---------------|
| 1       | 6                 | 6           | 21         | 78% (21/27)   |
| 2       | 4                 | 4           | 25         | 86% (25/29)   |
| 3       | 3                 | 3           | 28         | 90% (28/31)   |

**Goal**: Increase autonomy rate over time while maintaining quality.

---

## When Uncertain

If uncertain whether a decision is CRITICAL or NON-CRITICAL:
1. Run Vibe Check to validate assumptions
2. Query past learnings (Step 0) for similar decisions
3. **If still uncertain → Treat as CRITICAL** (safer to ask)

---

**Reference**: This framework is used by all agents in their "Decision Framework" sections.
