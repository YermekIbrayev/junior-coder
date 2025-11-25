# Spec Clarifier - Best Practices

## Common Ambiguity Patterns

### Vague Verbs

❌ **BAD**: "Should handle"
✅ **GOOD**: "Must validate and reject with error message: '{message}'"

❌ **BAD**: "Can support"
✅ **GOOD**: "Allows users to..." (specific action)

❌ **BAD**: "Might need"
✅ **GOOD**: "Required when..." (clear condition)

**Your Question**: "What specific action should the system take when {condition}?"

---

### Missing Boundaries

❌ **BAD**: "Large invoices"
✅ **GOOD**: "Invoices with >100 line items"

❌ **BAD**: "Recent data"
✅ **GOOD**: "Data from last 30 days"

❌ **BAD**: "Frequent updates"
✅ **GOOD**: "Updates occurring >10/minute"

**Your Question**: "What is the specific numeric threshold for {vague term}?"

---

### Implicit Assumptions

❌ **BAD**: "Users can edit"
✅ **GOOD**: "Users with 'Admin' or 'Resolver' roles can edit"

❌ **BAD**: "System validates"
✅ **GOOD**: "System validates on save with rules: {list}"

❌ **BAD**: "Data is saved"
✅ **GOOD**: "Data is saved to PostgreSQL with transaction isolation level..."

**Your Question**: "Which user roles can {action}?" or "What specific validation rules apply?"

---

### Contradictions

**Pattern**: Two requirements conflict

**Example**:
- Requirement A: "Invoices are immutable after approval"
- Requirement B: "Allow editing invoices anytime"

**Your Question**: "Requirements A and B contradict. Which takes precedence? Or should adjustments be separate documents?"

---

### Missing Error Paths

**Pattern**: Spec describes only happy path

**Example**: "User creates adjustment for invoice"

**Your Questions**:
- "What happens when invoice is not approved?"
- "What happens when user lacks permission?"
- "What happens when invoice is already adjusted?"
- "What happens when inventory already shipped?"

---

### Undefined Terms

**Pattern**: Spec uses domain terms without definition

**Example**: "Create credit note for adjustment"

**Your Question**: "Is 'credit note' a specific document type in the system? What are its properties?"

---

## Best Practices

### 1. Use Sequential Thinking for Systematic Analysis

**Process**:
1. Read spec section by section
2. Mark every vague term
3. List all implicit assumptions
4. Check for contradictions
5. Identify missing edge cases
6. Formulate questions

**Don't**: Read spec once and hope to catch everything

---

### 2. Run Vibe Check Proactively

**Use Vibe Check to expose**:
- Hidden assumptions
- Unstated constraints
- Implicit knowledge

**Example**:
```
Goal: Clarify invoice adjustment spec
Uncertainties:
- "Spec assumes adjustments don't affect inventory - is this valid?"
- "What if user tries to adjust same invoice twice?"
```

---

### 3. Use Octocode to Generate Recommended Options

**CRITICAL**: Every question MUST have a recommended option backed by Octocode research.

**Process**:
1. **Identify ambiguity** from spec analysis
2. **Research with Octocode**:
   ```javascript
   githubSearchCode({
     keywordsToSearch: ["{relevant", "keywords}"],
     stars: ">100",
     extension: "py"  // or relevant language
   })
   ```
3. **Analyze findings**:
   - What's the MOST common approach? (70%+ = strong recommendation)
   - What are 2-3 viable alternatives?
   - What evidence supports each?

4. **Formulate options**:
   - Option A: Alternative approach #1
   - Option B: Alternative approach #2
   - Option C: Most common approach ⭐ **Recommended**
   - Option D: Other (custom)

**Example - GOOD**:
```markdown
**Question**: Should adjustments modify original invoice or create separate document?

Octocode findings: 80% use separate documents (django-warehouse, inventory-pro, stock-manager)

Options:
A) Modify original invoice directly
B) Create new invoice version (versioning)
C) Create separate adjustment document ⭐ **Recommended**
D) Other (please specify)

Why C is recommended: 80% of production systems preserve immutability with
separate adjustment documents. Aligns with SmartStocker architecture.
```

**Example - BAD**:
```markdown
Options:
A) Approach 1
B) Approach 2
C) Approach 3 ⭐ **Recommended**  // NO EVIDENCE!
D) Other

Why C is recommended: It seems better  // VAGUE!
```

**Red Flags**:
- ❌ Recommended option without Octocode research
- ❌ "Seems better" or "feels right" justifications
- ❌ Options that don't represent real-world alternatives
- ❌ Missing percentage/evidence from code search

**See**: [octocode-use-cases.md](../../shared/tools/octocode-use-cases.md) for detailed examples

---

### 4. Prioritize Questions

**HIGH**: Blockers - cannot implement without answer
**MEDIUM**: Important but workarounds exist
**LOW**: Nice-to-know, can assume reasonable default

**Focus on HIGH first**.

---

### 5. Use SMART Question Format

**Specific**: Concrete scenario, not generic
**Measurable**: Can verify the answer
**Actionable**: Leads to clear spec update
**Relevant**: Impacts implementation
**Time-sensitive**: Blocking questions first

---

### 6. Validate Questions Before Asking

**Check**:
- "Is this truly ambiguous or am I overthinking?"
- "Can I infer answer from context?"
- "Will answer meaningfully improve spec?"

**Remove** questions that fail these checks.

---

### 7. Update spec.md Clearly

**Mark clarifications**:
```markdown
[CLARIFIED: 2025-10-26] {Updated requirement}
```

**Be specific** in updates - don't just add vague answers.

---

## Common Mistakes

❌ **Answering questions yourself**
- Ask stakeholders, don't assume
- Use Vibe Check to identify assumptions, not to answer them

❌ **Nitpicking trivial details**
- Focus on implementation-blocking ambiguities
- Don't ask about variable naming or UI colors

❌ **Asking too many questions**
- Prioritize! Group related questions
- HIGH priority should be <5 questions

❌ **Not using Vibe Check**
- Hidden assumptions are your enemy
- Vibe Check exposes them

❌ **Skipping Octocode validation**
- Production systems show proven approaches
- Learn from successful implementations

❌ **Vague questions**
- "How should this work?" is too generic
- "What should happen when user submits invoice with duplicate product IDs?" is specific

---

## Ambiguity Detection Checklist

Use this checklist when analyzing spec:

**Verbs**:
- [ ] All action verbs are specific (not "should", "might", "can")
- [ ] All validation verbs have clear rules
- [ ] All error handling verbs have defined behaviors

**Boundaries**:
- [ ] All numeric thresholds are defined (not "large", "small", "many")
- [ ] All time limits are specified (not "recent", "soon", "old")
- [ ] All frequency terms are quantified (not "often", "rarely", "frequent")

**Assumptions**:
- [ ] All user roles are explicitly stated
- [ ] All permissions are defined
- [ ] All data storage locations are specified
- [ ] All validation rules are listed

**Completeness**:
- [ ] Error paths are defined for all operations
- [ ] Edge cases are addressed
- [ ] Contradictions are resolved
- [ ] All requirements have acceptance criteria

**If ANY checkbox is unchecked**: Create clarifying question

---

**See Also**: [workflow.md](workflow.md) for detailed clarification process
