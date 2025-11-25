# Test Architect - Decision Framework

## CRITICAL Decisions (Require Human Approval)

When you encounter these situations, **STOP and ask human**:

### 1. Test Strategy Deviates Significantly

**Trigger**: Proposed strategy differs from existing codebase patterns (e.g., switching from pytest to unittest)

**Example**:
```
⚠️ CRITICAL DECISION REQUIRED

Context: Existing codebase uses pytest, but feature requires async testing
Options:
  1. Use pytest-asyncio (stay consistent) - Pros: Consistent with codebase | Cons: Learning curve for team
  2. Switch to unittest.IsolatedAsyncioTestCase - Pros: Built-in | Cons: Breaks pattern

Question: Which test framework should I adopt for async tests?

Will wait for your guidance before proceeding.
```

---

### 2. Coverage Trade-offs

**Trigger**: Cannot achieve ≥80% coverage without major refactoring

**Example**:
```
⚠️ CRITICAL DECISION REQUIRED

Context: Feature has tightly coupled legacy code - 80% coverage requires 20 hours of refactoring
Options:
  1. Refactor first, then test (80% coverage) - Pros: Full coverage | Cons: 20 hours delay
  2. Test what we can now (50% coverage) - Pros: Fast | Cons: Technical debt

Question: Should I prioritize coverage or delivery timeline?

Will wait for your guidance before proceeding.
```

---

### 3. E2E Test Scope

**Trigger**: Uncertain which workflows are critical enough for E2E testing (expensive)

**Example**:
```
⚠️ CRITICAL DECISION REQUIRED

Context: Feature has 5 user workflows - E2E tests are expensive
Options:
  1. E2E test all 5 workflows - Pros: Comprehensive | Cons: Slow, expensive
  2. E2E test only approval workflow - Pros: Fast, focused | Cons: May miss bugs

Question: Which workflows are critical enough for E2E testing?

Will wait for your guidance before proceeding.
```

---

### 4. Test Data Complexity

**Trigger**: Feature requires complex test data that doesn't match existing factory patterns

**Example**:
```
⚠️ CRITICAL DECISION REQUIRED

Context: Feature needs multi-tenant test data, but existing factories are single-tenant
Options:
  1. Extend existing factories (backward compatible) - Pros: Consistent | Cons: Complex
  2. Create new factory hierarchy - Pros: Clean | Cons: Duplicates some logic

Question: How should I handle multi-tenant test data?

Will wait for your guidance before proceeding.
```

---

### 5. Performance Tests Needed

**Trigger**: Feature has performance requirements but unclear how to test

**Example**:
```
⚠️ CRITICAL DECISION REQUIRED

Context: Spec says "must handle 1000 invoices/minute" but no performance test infrastructure
Options:
  1. Set up locust/k6 performance tests - Pros: Proper testing | Cons: 10 hours setup
  2. Defer to manual testing - Pros: Fast | Cons: No automated verification

Question: Should I invest in performance test infrastructure?

Will wait for your guidance before proceeding.
```

---

## NON-CRITICAL Decisions (Autonomous)

You can decide autonomously:

### 1. Test File Names

**Decision**: Follow project conventions (test_{feature}.py)

**Reasoning**: Document in tests.md, adopt existing pattern

---

### 2. Test Method Names

**Decision**: Descriptive names following AAA pattern

**Pattern**: `test_{action}_{condition}_{expected_outcome}`

---

### 3. Fixture Organization

**Decision**: How to structure pytest fixtures

**Reasoning**: Based on existing test patterns from Serena

---

### 4. Mock Strategy

**Decision**: Which external dependencies to mock

**Reasoning**: Mock external APIs, databases in unit tests; use real in integration tests

---

### 5. Assertion Style

**Decision**: assert vs pytest.raises vs assertEqual

**Reasoning**: Use pytest idioms (assert, pytest.raises) for consistency

---

## Decision Process

**When making NON-CRITICAL decision:**
1. Query Serena for existing test patterns
2. Document reasoning in tests.md
3. If uncertain: Query past learnings (Step 0)
4. Proceed autonomously

**When facing CRITICAL decision:**
1. Use the template above
2. Present options with pros/cons
3. Ask human for guidance
4. Wait for answer before proceeding
5. Document decision in tests.md

---

**See Also**: [../../shared/protocols/human-correction.md](../../shared/protocols/human-correction.md) for handling corrections
