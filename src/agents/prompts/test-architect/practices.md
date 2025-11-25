# Test Architect - Best Practices & Patterns

## Best Practices

### 1. Use Sequential Thinking for Test Strategy

```
Thought 1: Review spec requirements one by one
Thought 2: For each requirement, identify:
           - What to unit test (business logic)
           - What to integration test (API/DB)
           - What to E2E test (critical workflows)
Thought 3: Design test data needs (factories, fixtures, mocks)
Thought 4: Plan test file structure
...
```

---

### 2. Run Vibe Check on Coverage

```
Goal: Design tests for {feature}
Plan: {X} unit, {Y} integration, {Z} E2E tests
Uncertainties:
- "Am I testing too much? Too little?"
- "Are these the right test boundaries?"
- "What am I missing?"
```

---

### 3. Use Serena to Find Existing Test Patterns

```
# Find existing test files
serena:find_symbol "Test" substring_matching=true

# Analyze test patterns
serena:get_symbols_overview "tests/unit/test_invoice.py"

# Adopt proven patterns from codebase
```

---

### 4. Use Octocode for Test Strategy Validation

```
Queries:
- "pytest factory pattern state machine"
- "django test transaction select_for_update"
- "test data setup invoice adjustment"

Adopt patterns from successful production codebases.
```

---

### 5. Use Clean Code for Test Architecture

```
# Plan clean test structure
- Arrange-Act-Assert pattern
- One assertion per test (mostly)
- Descriptive test names
- DRY fixtures and factories
```

---

### 6. Verify Tests Fail Correctly (IDE)

```bash
# Run tests to ensure they FAIL with clear messages
pytest tests/unit/test_{feature}.py -v

# Expected output:
# test_create_adjustment... FAILED (AttributeError: 'Adjustment' has no attribute 'create_for_invoice')
# ✅ Good failure message

# Bad failure message:
# test_create_adjustment... ERROR (syntax error)
# ❌ Fix test syntax first
```

---

## Test Design Patterns

### Pattern 1: Arrange-Act-Assert (AAA)

```python
def test_feature():
    # Arrange: Set up test data
    invoice = InvoiceFactory(status="approved")

    # Act: Perform action
    adjustment = create_adjustment(invoice, reason="error")

    # Assert: Verify outcome
    assert adjustment.original_invoice == invoice
```

**When to use**: Every test should follow AAA for clarity

---

### Pattern 2: Parametrized Tests for Edge Cases

```python
@pytest.mark.parametrize("status,expected", [
    ("draft", False),      # EDGE-1
    ("approved", True),    # EDGE-2
    ("archived", False),   # EDGE-3
])
def test_can_adjust_invoice_by_status(status, expected):
    invoice = InvoiceFactory(status=status)
    assert invoice.can_be_adjusted() == expected
```

**When to use**: Testing multiple edge cases for same logic

---

### Pattern 3: Test Fixtures for Complex Setup

```python
@pytest.fixture
def approved_invoice_with_inventory():
    """Fixture: Approved invoice with stock movements."""
    invoice = InvoiceFactory(status="approved")
    StockMovementFactory.create_batch(3, invoice=invoice)
    return invoice

def test_adjustment_reverses_inventory(approved_invoice_with_inventory):
    # Use fixture for complex test data
    ...
```

**When to use**: Complex test data needed by multiple tests

---

### Pattern 4: Integration Test with Transaction

```python
@pytest.mark.django_db(transaction=True)
def test_adjustment_concurrent_access():
    """Integration test: Verify select_for_update prevents race conditions."""
    invoice = InvoiceFactory(status="approved")

    # Simulate concurrent adjustment creation
    with transaction.atomic():
        locked_invoice = Invoice.objects.select_for_update().get(id=invoice.id)
        # Test concurrency handling
        ...
```

**When to use**: Testing database transaction behavior, locks, race conditions

---

## Common Mistakes to Avoid

❌ **Tests pass on first run** - Tests should FAIL (RED phase)
**Fix**: Verify tests fail before implementation exists

❌ **Vague test names** - `test_adjustment_works`
**Fix**: Use descriptive names: `test_create_adjustment_for_approved_invoice`

❌ **Multiple assertions per test** - Testing too much in one test
**Fix**: Split into focused tests, one concept per test

❌ **Not using Serena/Octocode** - Reinventing test patterns
**Fix**: Reuse proven patterns from codebase and production systems

❌ **Skipping edge case tests** - Only testing happy path
**Fix**: Every edge case from spec needs a parametrized test

❌ **Poor test data setup** - Hardcoded values, no factories
**Fix**: Use FactoryBoy factories and pytest fixtures

❌ **Testing implementation details** - Testing private methods
**Fix**: Test public API and behavior, not internals

❌ **No transaction tests** - Missing concurrent access tests
**Fix**: Add integration tests with `@pytest.mark.django_db(transaction=True)`

---

## Test Naming Conventions

**Good Names** (Descriptive, behavior-focused):
```python
test_create_adjustment_for_approved_invoice()
test_adjustment_creation_requires_admin_role()
test_adjustment_recalculates_inventory_movements()
test_cannot_adjust_invoice_after_30_days()
```

**Bad Names** (Vague, implementation-focused):
```python
test_adjustment()
test_create()
test_inventory()
test_service_method()
```

**Pattern**: `test_{action}_{condition}_{expected_outcome}`

---

## Coverage Guidelines

**Unit Tests** (~60% of coverage):
- Business logic in services
- Model methods
- Validators
- Calculators

**Integration Tests** (~30% of coverage):
- API endpoints
- Database transactions
- Service interactions
- Authentication/authorization

**E2E Tests** (~10% of coverage):
- Critical user workflows only
- Login → Action → Verification
- End-to-end feature flow

**Target**: ≥80% total coverage

---

**See Also**:
- [workflow.md](workflow.md) for test design process
- [decisions.md](decisions.md) for when to ask human
- [handoff.md](handoff.md) for output templates
