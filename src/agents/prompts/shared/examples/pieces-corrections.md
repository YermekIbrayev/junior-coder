# Pieces Memory Examples - Human Corrections

**Purpose**: Full Pieces memory examples for documenting human corrections.

## Correction Template Structure

```markdown
## Correction Details
- Agent: {agent} | Feature: {feature} | Decision: {decision}
- My Approach: {what I did wrong}
- Correction: {human's guidance}
- Lesson: {key takeaway}
- Apply To: {when to apply this lesson}
- Keywords: {searchable terms for Step 0}
```

## Example: Immutability Principle

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Correction: Invoice Adjustment Immutability",
  "summary": `
## Correction Details
- Agent: Spec Analyst | Feature: invoice-adjustment | Decision: adjustment handling
- My Approach: Modify original invoice directly to adjust values
- Correction: Use separate AdjustmentInvoice model - approved documents are IMMUTABLE
- Lesson: Always preserve immutability for approved/locked documents
- Apply To: Any feature modifying approved documents (invoices, purchase orders, etc.)
- Keywords: invoice, adjustment, immutability, approved, state machine, locked documents
  `,
  "connected_client": "Claude Code"
})
```

## Example: YAGNI Principle

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Correction: Caching Over-Engineering",
  "summary": `
## Correction Details
- Agent: Code Planner | Feature: product-lookup | Decision: caching strategy
- My Approach: Designed multi-tier caching with Redis and in-memory layer
- Correction: Start with simple in-memory dict - add Redis only if performance testing proves needed
- Lesson: YAGNI - You Aren't Gonna Need It. Start simple, optimize when proven necessary
- Apply To: Any performance optimization decision - measure first, then optimize
- Keywords: caching, YAGNI, over-engineering, premature optimization, Redis, performance
  `,
  "connected_client": "Claude Code"
})
```

## Example: TDD Discipline

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Correction: Premature Implementation",
  "summary": `
## Correction Details
- Agent: Implementation Specialist | Feature: email-validation | Decision: validation scope
- My Approach: Implemented comprehensive email validation before tests defined edge cases
- Correction: Follow TDD strictly - write MINIMAL code to pass tests (GREEN phase discipline)
- Lesson: RED → GREEN → REFACTOR. Don't implement beyond what tests require
- Apply To: Any implementation phase - resist urge to add "nice to have" code
- Keywords: TDD, GREEN phase, premature implementation, minimal code, test-driven
  `,
  "connected_client": "Claude Code"
})
```

## Example: Tool Phase Boundaries

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Correction: Semgrep Usage Timing",
  "summary": `
## Correction Details
- Agent: Implementation Specialist | Feature: user-authentication | Decision: security scanning
- My Approach: Ran Semgrep during implementation phase to check for security issues
- Correction: Semgrep is Quality Guardian's tool - respect phase boundaries, don't jump ahead
- Lesson: Each agent has specific tools and responsibilities - don't use tools from future phases
- Apply To: Any tool usage - check which phase/agent owns the tool
- Keywords: Semgrep, phase boundaries, tool restrictions, Quality Guardian, Implementation Specialist
  `,
  "connected_client": "Claude Code"
})
```

## Example: E2E Test Scope

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Correction: E2E Test Over-Coverage",
  "summary": `
## Correction Details
- Agent: Test Architect | Feature: order-workflow | Decision: E2E test coverage
- My Approach: Designed E2E tests for every workflow path including edge cases
- Correction: E2E tests only for CRITICAL journeys (login, checkout, approval) - unit tests for edge cases
- Lesson: E2E tests are expensive - focus on happy paths and critical failures only
- Apply To: Any E2E test design - identify critical journeys first
- Keywords: E2E tests, test strategy, critical path, happy path, test pyramid, expensive tests
  `,
  "connected_client": "Claude Code"
})
```

---

**See Also**: [pieces-handoffs.md](pieces-handoffs.md) - Agent handoff memories
**Tool Syntax**: [../tools/pieces-memory.md](../tools/pieces-memory.md)
**Templates**: [../templates/pieces-memory-ready.md](../templates/pieces-memory-ready.md)
**Reference**: [../protocols/human-correction.md](../protocols/human-correction.md) - Step 3
