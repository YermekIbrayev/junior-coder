# Pieces Memory - Copy-Paste Templates

**Purpose**: Ready-to-use Pieces memory templates - just fill in the blanks.

## Agent Handoff Template

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Feature: {FEATURE_NAME} - {PHASE} Complete",
  "summary": `
# Feature: {FEATURE_NAME} - {PHASE_NAME} Complete

{PHASE_SPECIFIC_CONTENT - see agent templates below}

## Ready For
{NEXT_AGENT}: {WHAT_THEY_SHOULD_DO}
  `,
  "connected_client": "Claude Code"
})
```

## Agent-Specific Handoff Templates

### Spec Analyst → Test Architect
```javascript
{
  "summary_description": "Feature: {FEATURE} - Spec Complete",
  "summary": `
Requirements: {X} defined | Edge Cases: {Y} identified
Assumptions: {Z} documented | Research: {sources}
Ready For: Test Architect (design test strategy, TDD)
  `
}
```

### Test Architect → Code Planner
```javascript
{
  "summary_description": "Feature: {FEATURE} - Tests Designed",
  "summary": `
Strategy: TDD+E2E | Tests: {X} failing (RED phase)
Patterns: {list} | Coverage Target: ≥80%
Ready For: Code Planner (architecture design)
  `
}
```

### Code Planner → Implementation Specialist
```javascript
{
  "summary_description": "Feature: {FEATURE} - Architecture Complete",
  "summary": `
Modules: {X} designed | Patterns: {list}
Alignment: validated against {docs}
Ready For: Implementation Specialist (TDD implementation)
  `
}
```

### Implementation Specialist → Quality Guardian
```javascript
{
  "summary_description": "Feature: {FEATURE} - Implementation Complete",
  "summary": `
Tests: {X}/{X} passing (100%)
Coverage: {Y}% (≥80% ✅)
Patterns: {list} | Iterations: {N} red-green cycles
Ready For: Quality Guardian (refactor + security)
  `
}
```

### Quality Guardian → DONE
```javascript
{
  "summary_description": "Feature: {FEATURE} - Production Certified ✅",
  "summary": `
Status: ✅ READY FOR PRODUCTION
Refactoring: {summary}
Semgrep: ✅ 0 critical/high | E2E: ✅ {X}/{X}
Performance: ✅ Grade {A/B}
  `
}
```

## Human Correction Template

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Correction: {TOPIC}",
  "summary": `
## Correction Details
- Agent: {AGENT} | Feature: {FEATURE} | Decision: {DECISION}
- My Approach: {WHAT_I_DID_WRONG}
- Correction: {HUMAN_GUIDANCE}
- Lesson: {KEY_TAKEAWAY}
- Apply To: {WHEN_TO_APPLY}
- Keywords: {SEARCHABLE_TERMS}
  `,
  "connected_client": "Claude Code"
})
```

## Step 0 Learnings Applied Template

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Learnings Applied: {FEATURE} {PHASE}",
  "summary": `
Agent: {AGENT} | Feature: {FEATURE}
Queried: {X} retrospectives | Found: {Y} learnings
Applied: {SPECIFIC_LEARNINGS}
Avoided: {SPECIFIC_MISTAKES_FROM_PAST}
Impact: Reduced human interventions by {N}
  `,
  "connected_client": "Claude Code"
})
```

---

**Reference**: [../protocols/human-correction.md](../protocols/human-correction.md) - Step 3
**Tool Syntax**: [../tools/pieces-memory.md](../tools/pieces-memory.md)
**Examples**: [../examples/pieces-handoffs.md](../examples/pieces-handoffs.md), [../examples/pieces-corrections.md](../examples/pieces-corrections.md)
