# Quality Guardian - Handoff Protocol

## Output Artifacts

### 1. Refactored Production Code

**Location**: Source code files

**Requirements**:
- ✅ All tests still passing (100%)
- ✅ Clean code principles applied
- ✅ Performance optimized
- ✅ Security issues fixed (0 critical/high)
- ✅ Files ≤200 lines (constitutional compliance)

### 2. quality-report.md

**Location**: `.specify/specs/{feature-name}/quality-report.md`

**Sections** (see [template-quality-report.md](template-quality-report.md) for full example):
- Executive Summary
- Refactoring (before/after examples)
- Security Scan (Semgrep results)
- E2E Testing (scenarios and results)
- Performance Analysis (metrics and fixes)
- Documentation Updates
- Test Verification
- Production Certification Checklist
- Recommendations
- Next Steps

### 3. Pieces Memory (Production Certification)

**Tool**: `mcp__Pieces__create_pieces_memory`

**Format**:
```markdown
## Production Certification: {feature-name}

**Status**: ✅ PRODUCTION READY
**Date**: {Date}
**Agent**: Quality Guardian

### Metrics
- Tests: {X}/{X} passing (100%)
- Coverage: {Y}% (≥80% ✅)
- Semgrep: ✅ 0 critical/high issues
- E2E: ✅ {X}/{X} scenarios passing
- Performance: ✅ Grade {A/B}

### Refactoring Summary
{Brief summary of refactorings applied}

### Security
{Semgrep findings and fixes}

### Performance
{Performance improvements}

### Certification
✅ APPROVED FOR PRODUCTION

Ready to ship to production.
```

### 4. Explicit Handoff Message

**To**: User/Team

**Format**:
```
Production certification complete for {feature-name}.

Summary:
- Refactoring: {X} improvements applied, tests still passing
- Semgrep: ✅ 0 critical/high issues (MANDATORY check passed)
- E2E: ✅ {X}/{X} scenarios passing
- Performance: ✅ Grade {A/B} (all core web vitals green)
- Coverage: {Y}% (≥80% ✅)

Certification: ✅ **PRODUCTION READY**

Next Steps:
1. Deploy to production
2. Optional: Create retrospectives for future learning

Handoff complete. Feature ready to ship!
```

---

## Production Certification Checklist

Use this checklist before granting certification:

- [ ] ✅ All tests passing (100%)
- [ ] ✅ Coverage ≥80%
- [ ] ✅ Semgrep: 0 critical/high issues (MANDATORY)
- [ ] ✅ Code refactored (Clean Code principles applied)
- [ ] ✅ E2E tests passing (critical workflows verified)
- [ ] ✅ Performance acceptable (Grade A/B)
- [ ] ✅ Documentation updated (README, API, CURRENT_FUNCTIONALITY)
- [ ] ✅ Files ≤200 lines (constitutional compliance)
- [ ] ✅ Security issues fixed (all critical/high resolved)
- [ ] ✅ Vibe Check validated refactoring decisions

**Status**:
- ✅ **PRODUCTION READY** - All criteria met, approved for deployment
- ⚠️ **CONDITIONAL** - Some items need attention (specify which)
- ❌ **NOT READY** - Blocking issues found (specify blockers)

---

## Handoff to Next Agent (Optional)

If user requests retrospectives:

### Individual Retrospectives
Not applicable - Quality Guardian is final production phase

### System Retrospectives

**Synthesis Specialist** (`/agent:synthesis`):
- Consolidate learnings from all agents
- Identify patterns and anti-patterns
- Create reusable templates

**System Improver** (`/agent:improve`):
- Suggest process improvements
- Identify bottlenecks in workflow
- Recommend agent enhancements

**Knowledge Curator** (`/agent:curator`):
- Organize and index all artifacts
- Create searchable knowledge graph
- Ensure future discoverability

---

## Human Correction Protocol

**If human provides correction during your work:**

See [../../shared/protocols/human-correction.md](../../shared/protocols/human-correction.md) for complete protocol

**Quick Summary**:
1. Acknowledge correction
2. Record with vibe_learn
3. Update Pieces memory
4. Apply correction immediately
5. Re-run affected phases (tests/Semgrep/E2E)

---

**See Also**:
- [template-quality-report.md](template-quality-report.md) - Complete report template
- [../../shared/templates/pieces-memory-ready.md](../../shared/templates/pieces-memory-ready.md) - Pieces memory format
- [../../shared/templates/vibe-learn-ready.md](../../shared/templates/vibe-learn-ready.md) - vibe_learn syntax
