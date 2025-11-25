# Vibe Check Guardian - Handoff & Output Template

## File: vibe-check-report.md

**Location**: `.specify/specs/{feature-name}/vibe-check-report.md` (if during feature development)
OR in chat (if quick validation)

**Template**:

```markdown
# Vibe Check Report: {Context}

**Date**: {YYYY-MM-DD}
**Context**: {feature-name, agent, phase}
**Triggered By**: {who/what requested vibe check}

---

## Current Context

**Agent**: {current agent name}
**Goal**: {current agent's goal}
**Progress**: {what's been done}
**Artifacts**: {spec.md, tests.md, etc.}

---

## Assumptions Challenged

### Critical Assumptions (Must Validate)

1. **Assumption**: {assumption description}
   - **Stated or Implicit**: {stated/implicit}
   - **Risk if Wrong**: {impact description}
   - **Validation Status**: {validated/pending/rejected}
   - **Recommendation**: {validate before proceeding}

2. {...}

### Important Assumptions (Should Validate)

1. **Assumption**: {assumption description}
   - **Stated or Implicit**: {stated/implicit}
   - **Risk if Wrong**: {impact description}
   - **Validation Status**: {validated/pending/rejected}
   - **Recommendation**: {validate soon}

2. {...}

---

## Blind Spots Identified

1. **Blind Spot**: {what was missed}
   - **Why Missed**: {lack of context, tunnel vision, etc.}
   - **Impact if Not Addressed**: {consequences}
   - **Recommendation**: {action to take}

2. {...}

---

## Cascading Error Risks

1. **Error Path**: {assumption → consequence 1 → consequence 2}
   - **Probability**: {high/medium/low}
   - **Impact**: {critical/major/minor}
   - **Prevention**: {how to prevent}

2. {...}

---

## Validation Questions

### For Human Stakeholder
1. {question about requirements or business logic}
2. {question about priorities or trade-offs}

### For Research
1. {question about technical feasibility}
2. {question about best practices}

### For Testing
1. {question about edge cases}
2. {question about expected behavior}

---

## Alternative Approaches

1. **Alternative**: {different approach to consider}
   - **Pros**: {advantages}
   - **Cons**: {disadvantages}
   - **Recommendation**: {consider/reject and why}

2. {...}

---

## Learnings Recorded

### Mistakes (via vibe_learn)
- {mistake recorded with vibe_learn}

### Patterns
- {pattern observed}

### Constitution Updates
- {session rule added via update_constitution}

---

**Validation Complete**: {Continue with current agent | Address critical assumptions first}
```

---

## Pieces Memory Template

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Vibe Check: {feature-name} at {phase}",
  "summary": `
## Vibe Check Complete

**Feature**: {feature-name}
**Agent**: {current agent}
**Phase**: {current phase}
**Date**: {date}

### Assumptions Challenged
- Critical: {X} assumptions (must validate)
- Important: {Y} assumptions (should validate)

### Blind Spots Identified
- {Blind spot 1}
- {Blind spot 2}

### Learnings Recorded
- {Mistake/pattern learned}

### Recommendations
- {Top recommendation}

Next: {Resume current agent | Address critical assumptions}
  `,
  "connected_client": "Claude Code"
})
```

---

## Handoff Message Template

```
Vibe Check complete for {feature-name} at {phase}.

Assumptions Challenged:
- Critical: {X} assumptions requiring immediate validation
- Important: {Y} assumptions to validate soon

Blind Spots Identified:
- {Key blind spot 1}
- {Key blind spot 2}

Cascading Error Risks:
- {High-risk error path}

Learnings Recorded:
- {Mistake/pattern captured in vibe_learn}

Recommendation: {validate critical assumptions / proceed with caution / good to proceed}

Handoff complete.
```

---

**See Also**:
- [workflow.md](workflow.md) for validation process
- [practices.md](practices.md) for common patterns
