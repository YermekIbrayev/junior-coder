# Vibe Check Guardian - Best Practices

## Common Assumption Patterns

### Pattern 1: Implicit Business Logic

**Example**: "Users can edit invoices"

**Vibe Check Questions**:
- Which user roles can edit?
- Can they edit at any time?
- What if invoice is approved?
- What if inventory already shipped?

**Lesson**: Always make role-based access explicit

---

### Pattern 2: Technology Assumptions

**Example**: "We'll use WebSockets for real-time updates"

**Vibe Check Questions**:
- Have we validated browser support?
- What's the fallback for old browsers?
- What's the server-side cost?
- Have we load-tested?

**Lesson**: Validate technology choices with research/prototyping

---

### Pattern 3: Data Migration Blindness

**Example**: "Add new field to User model"

**Vibe Check Questions**:
- What happens to existing users?
- Default value strategy?
- Migration rollback plan?
- Database size impact?

**Lesson**: Always consider existing data when changing models

---

### Pattern 4: Edge Case Tunnel Vision

**Example**: "Test happy path thoroughly"

**Vibe Check Questions**:
- What about error paths?
- What about null/empty inputs?
- What about concurrent access?
- What about rate limits?

**Lesson**: Edge cases often reveal critical bugs

---

## Mistake Categories (vibe_learn)

### Complex Solution Bias

**Symptom**: Agent proposes elaborate architecture for simple feature

**Example**: Using event sourcing for basic CRUD

**Prevention**: Challenge with "What's the simplest solution that could work?"

---

### Feature Creep

**Symptom**: Spec includes features not in original request

**Example**: User asked for email validation, spec includes password reset

**Prevention**: Validate each requirement against original user request

---

### Premature Implementation

**Symptom**: Agent starts coding before spec/tests/architecture complete

**Example**: Implementation Specialist before Alignment Analyzer approval

**Prevention**: Enforce gate sequence (Spec → Tests → Plan → Analyze → Implement)

---

### Misalignment

**Symptom**: Spec, tests, and architecture tell different stories

**Example**: Spec says "soft delete", tests check hard delete, architecture has no delete

**Prevention**: Run Alignment Analyzer before implementation

---

### Overtooling

**Symptom**: Agent uses unnecessary or wrong MCPs

**Example**: Using Exa AI when Octocode is more appropriate

**Prevention**: Challenge tool selection with "Why this tool instead of X?"

---

## Example Vibe Check Reports

### Example 1: Spec Validation

**Context**: Spec Analyst created spec for "invoice adjustment" feature

**Vibe Check Output**:
```
Critical Assumptions:
1. Assumption: "Adjustments are separate documents"
   - Implicit (not stated in spec)
   - Risk: If wrong, database schema will need complete redesign
   - Validation: Ask human stakeholder

Blind Spots:
1. Missing: What happens to inventory when invoice adjusted?
   - Impact: Could create inventory discrepancies
   - Recommendation: Add requirement for inventory recalculation

Alternative Approaches:
1. Modify original invoice (with audit log) vs separate document
   - Current spec assumes separate
   - Should validate with stakeholder
```

---

### Example 2: Architecture Validation

**Context**: Code Planner designed architecture for "real-time dashboard"

**Vibe Check Output**:
```
Critical Assumptions:
1. Assumption: "WebSockets will scale to 1000 concurrent users"
   - Explicit (stated in architecture.md)
   - Risk: If wrong, dashboard won't work at scale
   - Validation: Load test prototype

Cascading Errors:
1. If WebSocket assumption wrong → Must redesign → Delays launch by 2 weeks
   - Prevention: Validate with prototype BEFORE full implementation
```

---

## When NOT to Use Vibe Check

❌ **Trivial Decisions**: Variable naming, file organization
❌ **After Validation**: Don't re-validate same assumption twice
❌ **Implementation Details**: Let Implementation Specialist handle

✅ **Critical Decisions**: Architecture, technology, business logic
✅ **Before Gates**: Before Alignment Analyzer, before Quality Guardian
✅ **When Stuck**: Breaking through analysis paralysis

---

**See Also**:
- [workflow.md](workflow.md) for validation process
- [handoff.md](handoff.md) for report template
