# Phase 3: Validation & Documentation

**Part of**: [Standard Feature Workflow](../standard-feature.md)

**Purpose**: Ensure quality standards met and knowledge captured.

---

## Steps

**9. Validate** - Run quality gates
- Run all applicable [quality gates](../../principles/05-quality-gates.md#54-quality-gates-by-work-type)
- Production: ALL gates
- Infrastructure: Relaxed gates
- Experimental: Minimal gates

**10. Test UI** (if applicable) - Browser testing
- Use Chrome DevTools MCP
- Verify UI functionality
- Test user flows

**11. Log** (if complex) - Complete execution log
- If using 4-document planning
- Record actual execution
- Note deviations from plan
- See [Planning: Complex](../../principles/04-planning.md#complex-11-steps-4-hours)

**12. Document** - Update docs
- Per [documentation decision tree](../../principles/07-documentation.md#documentation-decision-tree)
- README if new directory
- API docs if public API
- ADR if architectural decision

**13. Learn** - Save insights
- Use Pieces MCP: `create_pieces_memory`
- Important decisions
- Complex problems solved
- Patterns discovered

---

## Prerequisites

- Refactored code from Phase 2

---

## Deliverables

- ✅ All quality gates passed
- ✅ UI tested (if applicable)
- ✅ Documentation updated
- ✅ Learnings saved to Pieces
- ✅ Ready to commit

---

**Previous Phase**: [Phase 2: Implementation & Testing](phase2-implementation.md)

**Next Phase**: [Phase 4: Review & Completion](phase4-completion.md)

**See Also**:
- [Principle V: Quality Gates](../../principles/05-quality-gates.md)
- [Principle VII: Documentation](../../principles/07-documentation.md)
- [Principle VI: Knowledge Management](../../principles/06-knowledge.md)
- [Chrome DevTools MCP](../../../../docs/mcp/testing.md)
- [Pieces MCP](../../../../docs/mcp/ai-assistance.md)
