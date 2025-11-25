# Phase 2: Implementation & Testing

**Part of**: [Standard Feature Workflow](../standard-feature.md)

**Purpose**: Write code following TDD cycle with incremental validation.

---

## Steps

**5. Test (RED)** - Write failing tests
- Demonstrate requirement through test
- Test must fail for right reason
- See [Principle II: TDD](../../principles/02-tdd.md)

**6. Approve (if needed)** - Get approval for tests
- New patterns/critical paths: Approval required
- Routine tests: Fast-track
- Via User or Vibe-Check MCP
- See [TDD Approval Process](../../principles/02-tdd.md#approval-process)

**7. Implement (GREEN)** - Write minimal code
- Use Serena to navigate symbols during implementation
- Just enough to pass test
- No extra features
- Keep it simple

**8. Refactor** - Improve quality
- While keeping tests green
- Reduce [complexity](../../glossary.md#complex-logic) ≤10
- Improve readability

**Repeat 5-8** until feature complete

---

## Prerequisites

- Validated plan from Phase 1

---

## Deliverables

- ✅ All tests passing (GREEN)
- ✅ Code refactored for quality
- ✅ Complexity ≤10 per function
- ✅ Ready for quality gates

---

## Note

- Use Serena MCP for code navigation, Sequential Thinking for complex logic
- If spec gaps found: Return to Phase 1 per [Iteration Protocol](../../principles/03-spec-driven.md#specification-iteration-protocol)

---

**Previous Phase**: [Phase 1: Planning & Specification](phase1-planning.md)

**Next Phase**: [Phase 3: Validation & Documentation](phase3-validation.md)

**See Also**:
- [Principle II: TDD](../../principles/02-tdd.md)
- [TDD Quick Reference](../../references/tdd-quick-ref.md)
- [Sequential Thinking MCP](../../references/mcp-servers-ref.md)
- [Serena MCP](../../../../docs/mcp/code-navigation.md)
