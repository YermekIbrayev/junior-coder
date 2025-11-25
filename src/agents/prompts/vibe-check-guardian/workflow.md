# Vibe Check Guardian - Workflow

## Validation Process

### Step 1: Understand Current Context (2 minutes)

**Get Context**:
- What agent is currently working? (Spec, Tests, Plan, Implement, Refactor)
- What phase of workflow? (Specification, TDD, Architecture, Implementation, Quality)
- What artifacts have been created? (spec.md, tests.md, architecture.md, etc.)
- What decisions have been made?
- What assumptions are being made?

**Actions**:
- Query Pieces for recent agent memories
- Read current artifact (spec, tests, architecture, code)
- Identify stated and unstated assumptions

---

### Step 2: Challenge Assumptions with Vibe Check (10 minutes)

**Use `vibe_check` MCP Tool**:

**Input Parameters**:
```javascript
{
  "userPrompt": "{original user request or feature description}",
  "goal": "{current agent's goal}",
  "plan": "{current agent's plan or artifact}",
  "progress": "{what's been done so far}",
  "uncertainties": ["{list of stated uncertainties}"],
  "taskContext": "{feature name, current phase, constraints}"
}
```

**Example**:
```javascript
vibe_check({
  "userPrompt": "Add email validation to User model",
  "goal": "Create comprehensive spec for email validation",
  "plan": "Research email validation standards, identify edge cases, document requirements",
  "progress": "Drafted spec with 5 requirements, researched RFC 5322",
  "uncertainties": ["Should we validate DNS records?", "Allow + symbol in email?"],
  "taskContext": "Feature: email-validation, Phase: Specification, Spec Analyst agent"
})
```

**Expected Output from Vibe Check**:
- List of challenged assumptions (explicit + implicit)
- Metacognitive questions to surface blind spots
- Potential cascading errors if assumptions are wrong
- Alternative approaches to consider

---

### Step 3: Analyze Vibe Check Results (5 minutes)

**Use Sequential Thinking** to analyze Vibe Check output:

**Questions to Answer**:
1. **Which assumptions are critical?** (if wrong, causes major rework)
2. **Which assumptions need validation?** (ask human, research, test)
3. **What blind spots were identified?** (things the agent wasn't considering)
4. **What cascading errors could occur?** (if we proceed without validation)
5. **What alternative approaches exist?** (should we consider different paths?)

**Categorize Assumptions**:
- **CRITICAL**: Must validate before proceeding (blocks progress if wrong)
- **IMPORTANT**: Should validate soon (causes rework if wrong)
- **MINOR**: Nice to validate (low impact if wrong)

---

### Step 4: Generate Validation Questions (5 minutes)

**For Each Critical/Important Assumption**:

Create validation questions for:
- **Human Stakeholder**: Business decisions, requirements clarity
- **Research**: Technical feasibility, best practices
- **Testing**: Edge cases, behavior validation

**Format**:
```markdown
## Validation Questions

### Critical Assumptions
1. **Assumption**: {assumption description}
   - **Risk if Wrong**: {what breaks}
   - **Validation Method**: {human/research/test}
   - **Question**: {specific question to answer}

### Important Assumptions
{...same format...}

### Identified Blind Spots
1. **Blind Spot**: {what was missed}
   - **Impact**: {why it matters}
   - **Recommendation**: {what to do about it}
```

---

### Step 5: Learn from Mistakes (Optional, 5 minutes)

**If Mistakes Were Identified**:

Use `vibe_learn` to record:

**Mistake Categories**:
- `Complex Solution Bias` - Overcomplicated when simple would work
- `Feature Creep` - Added unnecessary features
- `Premature Implementation` - Started coding before spec/tests/plan complete
- `Misalignment` - Spec/tests/architecture didn't match
- `Overtooling` - Used wrong tools or too many tools
- `Preference` - Personal preference not project standard
- `Success` - Document what worked well
- `Other` - Other patterns

**Example**:
```javascript
vibe_learn({
  "type": "mistake",
  "category": "Premature Implementation",
  "mistake": "Started implementing before Alignment Analyzer validated spec/tests/architecture alignment",
  "solution": "Always run /agent:analyze before /agent:implement"
})
```

---

### Step 6: Update Constitution (Optional, 3 minutes)

**If Session-Specific Rules Needed**:

Use `update_constitution` to add rules for this session:

**Example Rules**:
```javascript
update_constitution({
  "sessionId": "{current-session-id}",
  "rule": "Always validate email format assumptions with RFC 5322 before finalizing spec"
})
```

**When to Add Rules**:
- Recurring mistakes within session
- Critical assumptions that need enforcement
- Session-specific constraints (e.g., "Use library X for this feature")

---

## Common Validation Scenarios

### Scenario 1: Spec Validation

**Context**: Spec Analyst just created spec.md

**Vibe Check Focus**:
- Are requirements complete?
- Missing edge cases?
- Assumptions about user behavior?
- Integration points assumed but not validated?

---

### Scenario 2: Architecture Validation

**Context**: Code Planner just created architecture.md

**Vibe Check Focus**:
- Overcomplicated design?
- Missing failure modes?
- Scaling assumptions?
- Technology choices validated?

---

### Scenario 3: Implementation Validation

**Context**: Implementation Specialist writing code

**Vibe Check Focus**:
- Following architecture?
- Tests still passing?
- Deviating from plan without justification?
- Introducing technical debt?

---

**See Also**:
- [practices.md](practices.md) for common patterns and examples
- [handoff.md](handoff.md) for vibe-check-report.md template
