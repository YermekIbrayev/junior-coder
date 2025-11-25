# Human Correction Protocol

**Purpose**: Standard 4-step process for handling human corrections during agent execution.

**Used By**: All agents

**Goal**: Capture corrections so they become queryable learnings for future projects.

---

## When to Use

Human provides correction or guidance during your work, such as:
- Correcting a decision you made
- Providing clarification on requirements
- Suggesting a different approach
- Pointing out a mistake

---

## 4-Step Protocol

### Step 1: Acknowledge

Show understanding by restating the correction:

```markdown
Thank you for the correction. I understand that {restate correction in your own words}.
```

**Example**:
```
Thank you for the correction. I understand that invoice adjustments should be
separate documents (AdjustmentInvoice model) rather than modifications to the
original invoice, to preserve immutability.
```

---

### Step 2: Record with vibe_learn

Capture the mistake for progressive learning:

```javascript
vibe_learn({
  "type": "mistake",
  "category": "{select from categories below}",
  "mistake": "{what I did wrong - be specific}",
  "solution": "{human's correction - exact guidance}",
  "context": "Feature: {feature-name}, Agent: {agent-name}, Decision: {what I was deciding}"
})
```

**Correction Categories**:
- **Complex Solution Bias**: Chose complex solution when simple one would suffice
- **Feature Creep**: Added functionality beyond requirements
- **Premature Implementation**: Implemented before full understanding
- **Misalignment**: Didn't align with project principles or patterns
- **Overtooling**: Used tools unnecessarily
- **Other**: Other mistake types

**Example**:
```javascript
vibe_learn({
  "type": "mistake",
  "category": "Misalignment",
  "mistake": "Specified invoice adjustment as modification to original invoice instead of separate adjustment document",
  "solution": "Use separate AdjustmentInvoice model to preserve immutability principle",
  "context": "Feature: invoice-adjustment, Agent: Spec Analyst, Decision: adjustment implementation approach"
})
```

---

### Step 3: Update Pieces Memory

Create detailed memory for future query:

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Human Correction: {brief topic}",
  "summary": `
## Correction Details
- **Agent**: {agent-name}
- **Feature**: {feature-name}
- **Decision Point**: {what I was deciding/implementing/testing}
- **My Approach**: {what I did wrong}
- **Human Correction**: {what I should do instead}
- **Lesson Learned**: {how to avoid this in future}
- **Apply To**: Always check this before {similar decisions}

## Future Application
- Query this memory in Step 0 when working on similar features
- Keywords: {relevant keywords for future search}
  `,
  "connected_client": "Claude Code"
})
```

**Example**:
```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Human Correction: Invoice Adjustment Immutability",
  "summary": `
## Correction Details
- **Agent**: Spec Analyst
- **Feature**: invoice-adjustment
- **Decision Point**: How to handle adjustments to approved invoices
- **My Approach**: Specified modification to original invoice
- **Human Correction**: Use separate AdjustmentInvoice model
- **Lesson Learned**: Always preserve immutability for approved documents
- **Apply To**: Any feature involving modifications to approved/locked documents

## Future Application
- Query this memory in Step 0 when specifying document modification features
- Keywords: invoice, adjustment, immutability, approved documents, state machine
  `,
  "connected_client": "Claude Code"
})
```

---

### Step 4: Apply Correction Immediately

Take agent-specific action:

**Spec Analyst**:
- Redo the spec section with corrected approach
- Update spec.md
- Document in "Assumptions" section why correction was needed

**Test Architect**:
- Redo the test strategy with corrected approach
- Update tests.md and test files
- Re-run tests to verify they fail correctly

**Code Planner**:
- Redo architecture with corrected approach
- Update architecture.md
- Document architectural decision rationale

**Implementation Specialist**:
- Redo implementation with corrected approach
- Re-run tests to verify they pass
- Update implementation-notes.md with correction

**Quality Guardian**:
- Redo refactoring/security fix/E2E test with corrected approach
- Re-run tests to verify they still pass
- Update quality-report.md with correction
- Re-run Semgrep if security-related

---

## Why This Matters

**This ensures corrections are captured and queryable in future projects!**

Progressive Learning Loop:
1. Human corrects mistake → Captured via vibe_learn + Pieces
2. Future agent queries in Step 0 → Finds past correction
3. Future agent applies learning → Avoids repeating mistake
4. Human interventions decrease over time → System learns!

---

## Success Criteria

✅ Acknowledged correction by restating understanding
✅ Recorded mistake via vibe_learn (with category)
✅ Created Pieces memory with detailed context
✅ Applied correction to current work immediately
✅ Verified correction works (tests pass, docs updated, etc.)

---

**Reference**: This protocol is used by all agents when receiving human guidance.
