# Standard Feature Implementation Workflow

**Version**: 4.0.0 | **Part of**: [Constitution](../INDEX.md) > Workflows

**Related**: All principles, [Quick Fix Flow](quick-fix.md), [Research Flow](research.md)

**Diagram**: [View Standard Workflow](../diagrams/standard-workflow.mermaid)

---

## Overview

The standard workflow integrates all constitution principles into a repeatable, auditable process with 4 phases.

**Phases**:
1. 🔵 **[Planning & Specification](standard-feature/phase1-planning.md)** - Define requirements
2. 🟡 **[Implementation & Testing](standard-feature/phase2-implementation.md)** - TDD cycle
3. 🟠 **[Validation & Documentation](standard-feature/phase3-validation.md)** - Quality gates
4. 🟢 **[Review & Completion](standard-feature/phase4-completion.md)** - Finalize and merge

---

## Quick Navigation

### [Phase 1: Planning & Specification](standard-feature/phase1-planning.md)

**Steps**: Specify → Clarify → Explore (Serena) → Plan → Validate

**Deliverables**:
- ✅ Specification created and clarified
- ✅ Execution plan (if needed)
- ✅ Approach validated
- ✅ Ready to write tests

---

### [Phase 2: Implementation & Testing](standard-feature/phase2-implementation.md)

**Steps**: Test (RED) → Approve → Implement (GREEN) → Refactor → Repeat

**Deliverables**:
- ✅ All tests passing (GREEN)
- ✅ Code refactored for quality
- ✅ Complexity ≤10 per function
- ✅ Ready for quality gates

---

### [Phase 3: Validation & Documentation](standard-feature/phase3-validation.md)

**Steps**: Validate → Test UI → Log → Document → Learn

**Deliverables**:
- ✅ All quality gates passed
- ✅ UI tested (if applicable)
- ✅ Documentation updated
- ✅ Learnings saved to Pieces
- ✅ Ready to commit

---

### [Phase 4: Review & Completion](standard-feature/phase4-completion.md)

**Steps**: Commit → PR → Review → Analyze → Done

**Deliverables**:
- ✅ Code committed to repository
- ✅ PR created and reviewed
- ✅ Spec-kit analysis passed
- ✅ Feature complete

---

## Workflow Diagram Summary

```
Planning (Phase 1)
  ↓
Specify → Clarify → Explore (Serena) → Plan → Validate
  ↓
Implementation (Phase 2)
  ↓
Test (RED) → Approve → Implement (GREEN) → Refactor → Repeat
  ↓
Validation (Phase 3)
  ↓
Quality Gates → UI Test → Log → Document → Learn
  ↓
Completion (Phase 4)
  ↓
Commit → PR → Review → Analyze → Done
```

---

## Step-by-Step Navigation

| Step | Phase | Description | Details |
|------|-------|-------------|---------|
| 1-4 | [Phase 1](standard-feature/phase1-planning.md) | Planning & Specification | Define requirements |
| 5-8 | [Phase 2](standard-feature/phase2-implementation.md) | Implementation & Testing | TDD cycle |
| 9-13 | [Phase 3](standard-feature/phase3-validation.md) | Validation & Documentation | Quality gates |
| 14-17 | [Phase 4](standard-feature/phase4-completion.md) | Review & Completion | Finalize |

---

## When to Use This Workflow

**Use Standard Feature Workflow for:**
- User-facing features (requires specification)
- Features with moderate to complex implementation
- Multi-day development efforts
- Team collaboration scenarios

**Don't use for:**
- Quick fixes: Use [Quick Fix Flow](quick-fix.md) instead
- Research tasks: Use [Research/Investigation Flow](research.md) instead
- Trivial changes (<1 hour): Skip phases, just code + test + commit

---

## Key MCP Integration Points

**Phase 1 (Planning)**:
- Vibe-Check → Validate approach
- Serena → Explore codebase
- Sequential Thinking → Break down complexity
- Clean Code → Plan architecture

**Phase 2 (Implementation)**:
- Serena → Navigate code during implementation
- Sequential Thinking → Solve complex logic
- IDE → Check diagnostics

**Phase 3 (Validation)**:
- Semgrep → Security scan
- Chrome DevTools → UI testing
- Pieces → Save learnings

**Phase 4 (Completion)**:
- GitHub → Commit and PR
- Vibe-Check → Final review

---

## See Also

- [Quick Fix Flow](quick-fix.md) - For small changes (<1 hour)
- [Research/Investigation Flow](research.md) - For exploration
- All 8 Principles referenced throughout
- [Quality Gates Reference](../references/quality-gates-ref.md)
- [TDD Quick Reference](../references/tdd-quick-ref.md)
- [MCP Servers Reference](../references/mcp-servers-ref.md)

---

## File Organization

This workflow is split into multiple files following Principle VIII (Token-Efficient Architecture):

- **This file**: Navigation hub (~150 lines)
- **Phase files**: Detailed steps (~50-60 lines each)
- **Total**: 4 phase files + hub = Constitution-compliant

**Benefits**:
- Load only needed phase (75% token reduction)
- Clear phase boundaries
- Easy navigation
- Constitution-compliant file sizes
