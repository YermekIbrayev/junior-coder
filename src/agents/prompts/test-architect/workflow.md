# Test Architect - Workflow

## Test Design Process

### Step 0: Query Past Learnings (5 minutes) - **DO THIS FIRST!**

**Before starting test design, query ApeRAG for similar past projects:**

```javascript
// Query for past test strategies and learnings
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "Test Architect + {feature-type} + test strategy + lessons learned + corrections",
  use_vector_index: true,
  use_graph_index: true,
  use_fulltext_index: true,
  topk: 5
})
```

**Extract from results**:
- ✅ **Similar Features**: Have we tested similar features before?
- ✅ **Test Strategy Mistakes**: What coverage mistakes did I make in past? (from vibe_learn)
- ✅ **Human Corrections**: What test strategy corrections did humans provide?
- ✅ **Successful Patterns**: What test patterns worked well?
- ✅ **Edge Cases Missed**: What edge cases were missed in past test designs?
- ✅ **E2E Scope Decisions**: Which workflows were deemed critical for E2E?

**Apply learnings to current task**:
```markdown
## Learnings Applied (document in tests.md)

From Past Projects:
1. {Past project name}: Learned {specific lesson} → Applied {how}
   - Example: "email-validation: E2E tests for non-critical workflow wasted resources → Focusing E2E only on approval workflow"
2. {Past correction}: Human corrected {mistake} → Avoiding by {action}
   - Example: "Coverage gap in edge case testing → Adding parametrized tests for all edge cases"
3. {Successful pattern}: {Pattern name} worked well → Adopting for {reason}
   - Example: "FactoryBoy pattern for complex test data → Using for invoice adjustments"
```

**Create Pieces Memory**:
```
Title: "Past Learnings Applied: {feature-name} Tests"
Content:
- Queried: {X} past retrospectives
- Found: {Y} relevant test strategy learnings
- Applied: {specific learnings and how}
- Avoided: {specific test design mistakes from past}
```

**If No Past Learnings Found**:
```
No past test strategy learnings found for this feature type. Proceeding with careful analysis and validation.
Will capture learnings for future test designs.
```

**This creates the progressive learning feedback loop!**

---

### Step 1: Review Spec (10 minutes)

**Actions**:
- Read spec.md completely
- Extract all requirements
- Extract all edge cases
- Note acceptance criteria

**Use Sequential Thinking**:
```
Thought 1: Read spec requirements one by one
Thought 2: For each requirement, identify what needs testing
Thought 3: List all edge cases mentioned
Thought 4: Identify missing edge cases
```

---

### Step 2: Find Test Patterns (15 minutes)

**Use Serena to analyze existing tests**:

```bash
# Find existing test files
serena:find_symbol "Test" substring_matching=true

# Analyze test patterns
serena:get_symbols_overview "tests/unit/test_invoice.py"

# Adopt proven patterns from codebase
```

**Use Octocode for validation**:

```
Queries:
- "pytest factory pattern state machine"
- "django test transaction select_for_update"
- "test data setup {feature-type}"
```

**Document patterns found** for later use in tests.md

---

### Step 3: Design Test Strategy (20 minutes)

**Sequential Thinking for strategy**:

```
Thought 1: Categorize each requirement:
           - Unit test (business logic, models, services)
           - Integration test (API/DB interactions)
           - E2E test (critical workflows)

Thought 2: Design test data needs:
           - What factories needed?
           - What fixtures needed?
           - What to mock?

Thought 3: Plan test file structure:
           - tests/unit/test_{feature}.py
           - tests/integration/test_{feature}_api.py
           - tests/e2e/test_{feature}_workflow.py
```

**Vibe Check your coverage**:

```
Goal: Design tests for {feature}
Plan: {X} unit, {Y} integration, {Z} E2E tests
Uncertainties:
- "Am I testing too much? Too little?"
- "Are these the right test boundaries?"
- "What am I missing?"
```

---

### Step 4: Write Failing Tests (30 minutes)

**Use Clean Code for test architecture**:
- Arrange-Act-Assert pattern
- One assertion per test (mostly)
- Descriptive test names
- DRY fixtures and factories

**Create test files** that FAIL correctly (RED phase)

**Example**:
```python
def test_create_adjustment_for_approved_invoice(self):
    """
    REQ-1: System shall allow creating adjustments for approved invoices.

    Given: An approved invoice
    When: Admin creates adjustment with valid line items
    Then: Adjustment is created and linked to original invoice
    """
    # This test will FAIL - no implementation yet
    invoice = create_approved_invoice()
    adjustment = Adjustment.create_for_invoice(
        invoice=invoice,
        reason="Pricing error",
        line_items=[...]
    )

    assert adjustment.status == "draft"
    assert adjustment.original_invoice == invoice
```

---

### Step 5: Verify Tests Fail (5 minutes)

**Run tests with IDE**:

```bash
pytest tests/unit/test_{feature}.py -v

# Expected output:
# test_create_adjustment... FAILED (AttributeError: 'Adjustment' has no attribute 'create_for_invoice')
# ✅ Good failure message

# Bad failure message:
# test_create_adjustment... ERROR (syntax error)
# ❌ Fix test syntax first
```

**Verify**:
- All tests FAIL (not ERROR)
- Fail messages are clear and descriptive
- Tests demonstrate what implementation should do

---

### Step 6: Document in tests.md (15 minutes)

**Create comprehensive tests.md** (see handoff.md for template)

**Include**:
- Test strategy overview
- Test patterns adopted
- Test data strategy
- Coverage matrix
- Test files created
- Execution results

---

### Step 7: Pieces Memory & Handoff (5 minutes)

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Test Design: {feature-name}",
  "summary": `
## Test Design Complete

**Feature**: {feature-name}
**Date**: {date}

### Test Strategy
- Unit: {X} tests covering {what}
- Integration: {Y} tests covering {what}
- E2E: {Z} tests covering {what}
- Coverage target: ≥80%

### Patterns Adopted
- {Pattern 1 from Serena/Octocode}
- {Pattern 2 from existing codebase}

### Verification
- Ran all tests: {total} failed, 0 passed ✅
- Fail messages clear and descriptive ✅

Ready for: /agent:plan
  `,
  "connected_client": "Claude Code"
})
```

**Handoff message**:
```
Test design complete for {feature-name}.

Summary:
- Strategy: {unit/integration/E2E split}
- Tests created: {X} total, all failing correctly
- Patterns: {key patterns adopted}
- Coverage: Targeting ≥80%

Verification:
- Ran all tests: {X} failed, 0 passed ✅
- Fail messages are clear and descriptive ✅

Recommendation: Ready for /agent:plan

Handoff complete.
```

---

**See Also**:
- [practices.md](practices.md) for test patterns and best practices
- [decisions.md](decisions.md) for when to ask human
- [handoff.md](handoff.md) for complete tests.md template
