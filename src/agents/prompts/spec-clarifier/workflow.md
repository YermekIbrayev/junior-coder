# Spec Clarifier - Workflow

## Clarification Process

### Step 1: Read spec.md (5 minutes)

**Actions**:
- Read entire specification from Spec Analyst
- Note initial impressions of unclear areas
- Identify sections that seem vague or incomplete

---

### Step 2: Sequential Thinking - Systematic Scan (15 minutes)

**Use Sequential Thinking** to analyze systematically:

```
Thought 1: Read spec.md section by section
Thought 2: Identify vague terms (e.g., "should", "might", "handle")
Thought 3: Check for contradictions between sections
Thought 4: List missing edge cases
Thought 5: Formulate questions for each ambiguity
```

**Look for**:
- Vague verbs ("should handle", "can support", "might need")
- Missing boundaries ("large", "recent", "frequent")
- Implicit assumptions (unstated roles, validations, storage)
- Contradictions between requirements
- Missing error paths

---

### Step 3: Vibe Check - Expose Assumptions (10 minutes)

**Run Vibe Check**:

```
Goal: Clarify spec for {feature}
Plan: Read spec, identify ambiguities, ask questions
Uncertainties:
- "Spec assumes {X}, but is it valid?"
- "Requirement says {Y}, but what about {edge case}?"
- "Is {term} clearly defined?"
```

**Let Vibe Check challenge**:
- Hidden assumptions
- Implicit constraints
- Undefined terms

---

### Step 4: Octocode Validation (10 minutes)

**Query Octocode**:

```
"How do successful projects handle {similar feature}?"
```

**Compare their approaches** to spot gaps in current spec:
- Do they handle edge cases we're missing?
- Do they have constraints we haven't considered?
- Do they clarify ambiguities we have?

---

### Step 5: Identify & Research First Question (10 minutes)

**Prioritize questions** by impact:
- HIGH: Blockers (cannot proceed without answer)
- MEDIUM: Important (workarounds exist)
- LOW: Nice-to-know (can assume reasonable default)

**Select the highest priority ambiguity.**

**Research with Octocode**:
```javascript
mcp__octocode__githubSearchCode({
  queries: [{
    researchGoal: "Find how successful projects handle {ambiguity}",
    keywordsToSearch: ["{relevant", "keywords}"],
    stars: ">100",
    limit: 5
  }]
})
```

**Analyze findings**:
- What's the most common approach? (This becomes recommended option)
- What alternatives exist? (Options A, B)
- What evidence supports recommendation?

---

### Step 6: Present Interactive Question (Variable - per question)

**Present ONE question at a time** in this format:

```markdown
---
**Question {N} of {Total}** (Priority: {HIGH/MEDIUM/LOW})

{Clear question text with context}

**Please choose one:**
A) {Option 1 - brief description}
B) {Option 2 - brief description}
C) {Option 3 - brief description} ⭐ **Recommended**
D) Other (please specify)

**Why C is recommended:** {1-2 sentences explaining Octocode research findings}
Found in: {repo examples if applicable}

**Context**: {Why this is ambiguous and needs clarification}
**Impact**: {What happens if not clarified}
---
```

**Wait for user answer** before proceeding.

**CRITICAL Rules**:
- Always provide exactly 3 preset options (A, B, C)
- Always mark ONE as recommended (⭐) based on Octocode research
- Always include option D for custom answer
- Always explain why the recommended option is best

---

### Step 7: Process Answer & Update Spec (5 minutes per question)

**Immediately after receiving answer**:

1. **Record the choice** (A/B/C/D and any custom text)
2. **Update spec.md** with the clarification:
   ```markdown
   ## Before
   Requirement 3.1: System should allow adjustments after approval

   ## After
   Requirement 3.1: System allows Admin and Resolver users to create adjustment
   documents (credit/debit notes) for approved invoices within 30 days of approval.
   [CLARIFIED: 2025-10-27 - Answer: Option C]
   ```

3. **Check for follow-up questions** the answer might raise
4. **If more questions exist**, return to Step 5
5. **If all questions answered**, proceed to Step 8

---

### Step 8: Final Validation (10 minutes)

**After all questions answered**:

**Vibe Check**:
```
Goal: Ensure spec is now unambiguous
Questions:
- "Are there any remaining contradictions?"
- "Can implementation begin without further clarification?"
- "Are all edge cases addressed?"
```

**Review spec.md**:
- All ambiguities marked with `[CLARIFIED: date]`
- No contradictions between requirements
- Clear acceptance criteria
- All edge cases documented

---

### Step 9: Pieces Memory (5 minutes)

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Spec Clarification: {feature-name}",
  "summary": `
## Clarification Complete

**Feature**: {feature-name}
**Date**: {date}

### Ambiguities Resolved
- {Ambiguity 1}: {Resolution}
- {Ambiguity 2}: {Resolution}
- ...

### Questions Asked: {count}
- HIGH priority: {count}
- MEDIUM priority: {count}
- LOW priority: {count}

### Spec Updates
{Summary of changes to spec.md}

### Remaining Uncertainties
{If any, or "None"}

Ready for: /agent:tests
  `,
  "connected_client": "Claude Code"
})
```

---

### Step 10: Handoff (5 minutes)

```
Clarification complete for {feature-name}.

Ambiguities Resolved:
- {List key clarifications}

Spec Updates:
- {What changed in spec.md}

Remaining Uncertainties:
- {Any unresolved items, or "None"}

Recommendation: Ready for /agent:tests

Handoff complete.
```

---

## Example: Interactive Clarification Flow

**Input Spec**: "Add ability to adjust invoices after approval"

### Steps 1-4: Analysis

**Sequential Thinking** identifies 3 ambiguities:
1. "Adjust" is vague (HIGH priority)
2. "After approval" has no time limit (HIGH priority)
3. Missing edge case: inventory already shipped (MEDIUM priority)

**Vibe Check** exposes assumptions:
- Adjustments might be separate documents
- Role permissions unclear

**Octocode** research findings:
- 80% of warehouse systems use separate adjustment documents
- 70% have 30-day time limits
- 65% prevent adjustments post-shipment

---

### Step 5-7: Interactive Questions (ONE AT A TIME)

**Question 1 of 3** (Priority: HIGH)

Does "adjust invoice" mean creating a separate adjustment document or modifying the original invoice?

**Please choose one:**
A) Modify the original invoice directly (mutable approach)
B) Create a new version of the invoice (versioning approach)
C) Create a separate adjustment document (credit/debit note) ⭐ **Recommended**
D) Other (please specify)

**Why C is recommended:** 80% of production warehouse systems (django-warehouse, inventory-pro, stock-manager) use separate adjustment documents to preserve immutability and maintain audit trails. This aligns with SmartStocker's immutable architecture principle.

**Context**: Spec says "adjust" but doesn't clarify if this modifies existing data
**Impact**: Determines database schema and audit trail implementation

---

**USER ANSWERS: C**

**Spec updated immediately**:
```markdown
Requirement 3.1: System allows creation of separate adjustment documents
(credit notes for reductions, debit notes for additions) linked to approved invoices.
Original invoices remain immutable.
[CLARIFIED: 2025-10-27 - Answer: Option C]
```

---

**Question 2 of 3** (Priority: HIGH)

Are there time limits on when adjustments can be created after invoice approval?

**Please choose one:**
A) No limit - adjustments can be created anytime
B) 30-day limit from approval date ⭐ **Recommended**
C) Only before month-end close
D) Other (please specify)

**Why B is recommended:** 70% of systems enforce 30-day limits to balance flexibility with accounting close processes. Found in: django-erp, warehouse-manager, stock-control.

**Context**: "After approval" is unbounded
**Impact**: Affects business rules and validation logic

---

**USER ANSWERS: B**

**Spec updated**. Proceeds to Question 3...

---

### Step 8-10: Finalization

After all 3 questions answered, perform Final Validation, create Pieces memory, hand off to Test Architect.

---

**See Also**: [practices.md](practices.md) for common ambiguity patterns to watch for
