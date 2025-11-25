# Test Architect - Handoff & Output Templates

## Output Requirements

### 1. tests.md File Template

Create `.specify/specs/{feature-name}/tests.md`:

```markdown
# Test Strategy: {Feature Name}

**Version**: 1.0.0
**Author**: Test Architect
**Date**: {Date}
**Coverage Target**: ≥80%

## Test Strategy

### Test Levels
1. **Unit Tests**: {What will be unit tested}
   - Focus: {business logic, models, services}
   - Framework: pytest
   - Coverage: ~60% of total

2. **Integration Tests**: {What will be integration tested}
   - Focus: {API endpoints, database transactions, service interactions}
   - Framework: pytest + Django TestCase
   - Coverage: ~30% of total

3. **E2E Tests** (if applicable): {What will be E2E tested}
   - Focus: {critical user workflows}
   - Framework: Playwright / Chrome DevTools
   - Coverage: ~10% of total

### Test Patterns Adopted
- Pattern 1: {From Serena/Octocode - describe pattern}
- Pattern 2: {From existing codebase - describe pattern}

### Test Data Strategy
- Factories: {FactoryBoy patterns to use}
- Fixtures: {pytest fixtures needed}
- Mocks: {What to mock and why}

## Test Coverage Matrix

| Requirement | Unit | Integration | E2E | Edge Cases |
|-------------|------|-------------|-----|------------|
| REQ-1 | ✅ | ✅ | ❌ | 3 |
| REQ-2 | ✅ | ❌ | ✅ | 2 |
...

## Test Files Created

1. `tests/unit/test_{feature}.py` - {X} tests
2. `tests/integration/test_{feature}_api.py` - {Y} tests
3. `tests/e2e/test_{feature}_workflow.py` - {Z} tests (if applicable)

Total: {X+Y+Z} failing tests

## Test Execution Results

```bash
pytest tests/unit/test_{feature}.py -v
# All tests should FAIL with clear messages
# Expected: {X} failed, 0 passed
```

## Learnings Applied

From Past Projects:
1. {Past project}: {Lesson learned} → {How applied}
2. {Past correction}: {Human correction} → {Avoided by}

## Success Criteria
- [ ] All requirements from spec have corresponding tests
- [ ] All edge cases from spec have corresponding tests
- [ ] Tests fail with clear, descriptive messages
- [ ] Test data setup documented
- [ ] Coverage target defined (≥80%)
- [ ] Test patterns documented

## Next Steps
Recommend: /agent:plan (architecture design)
```

---

### 2. Test File Template

Example test file structure:

```python
# tests/unit/test_invoice_adjustment.py
import pytest
from app.models import Invoice, Adjustment
from app.factories import InvoiceFactory, StockMovementFactory

class TestInvoiceAdjustment:
    """Test suite for invoice adjustment feature (RED phase)."""

    def test_create_adjustment_for_approved_invoice(self):
        """
        REQ-1: System shall allow creating adjustments for approved invoices.

        Given: An approved invoice
        When: Admin creates adjustment with valid line items
        Then: Adjustment is created and linked to original invoice
        """
        # Arrange
        invoice = InvoiceFactory(status="approved")

        # Act
        adjustment = Adjustment.create_for_invoice(
            invoice=invoice,
            reason="Pricing error",
            line_items=[...]
        )

        # Assert
        assert adjustment.status == "draft"
        assert adjustment.original_invoice == invoice
        # This will FAIL - method doesn't exist yet

    @pytest.mark.parametrize("status,can_adjust", [
        ("draft", False),      # EDGE-1
        ("approved", True),    # EDGE-2
        ("archived", False),   # EDGE-3
    ])
    def test_can_adjust_invoice_by_status(self, status, can_adjust):
        """
        EDGE-1,2,3: Test adjustment allowed only for approved invoices.
        """
        # Arrange
        invoice = InvoiceFactory(status=status)

        # Act & Assert
        assert invoice.can_be_adjusted() == can_adjust
        # This will FAIL - method doesn't exist yet

    def test_adjustment_recalculates_inventory(self):
        """
        REQ-2: Adjustments shall recalculate inventory movements.

        Given: Approved invoice with stock movements
        When: Adjustment created
        Then: New reverse stock movements created
        """
        # Arrange
        invoice = InvoiceFactory(status="approved")
        StockMovementFactory.create_batch(3, invoice=invoice)

        # Act
        adjustment = Adjustment.create_for_invoice(invoice, reason="error")

        # Assert
        assert adjustment.stock_movements.count() == 3
        # This will FAIL - no implementation yet
```

---

### 3. Pieces Memory Template

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Test Design: {feature-name}",
  "summary": `
## Test Design Complete

**Feature**: {feature-name}
**Date**: {date}

### Test Strategy
- Unit: {X} tests covering {business logic, models, services}
- Integration: {Y} tests covering {API endpoints, database}
- E2E: {Z} tests covering {critical workflows}
- Coverage target: ≥80%

### Patterns Adopted
- {Pattern 1 from Serena}: {Why adopted}
- {Pattern 2 from Octocode}: {Why adopted}

### Test Files Created
- tests/unit/test_{feature}.py ({X} tests)
- tests/integration/test_{feature}_api.py ({Y} tests)
- tests/e2e/test_{feature}_workflow.py ({Z} tests)

### Verification
- Ran all tests: {total} failed, 0 passed ✅
- Fail messages clear and descriptive ✅
- All requirements and edge cases covered ✅

### Learnings Applied
- {Past project 1}: {Lesson} → {Applied how}
- {Past project 2}: {Lesson} → {Applied how}

Ready for: /agent:plan
  `,
  "connected_client": "Claude Code"
})
```

---

### 4. Handoff Message Template

```
Test design complete for {feature-name}.

Summary:
- Strategy: {X} unit, {Y} integration, {Z} E2E tests
- Tests created: {total} total, all failing correctly
- Patterns: {key patterns adopted from Serena/Octocode}
- Coverage: Targeting ≥80%

Test Files:
- tests/unit/test_{feature}.py ({X} tests)
- tests/integration/test_{feature}_api.py ({Y} tests)
- tests/e2e/test_{feature}_workflow.py ({Z} tests)

Verification:
- Ran all tests: {total} failed, 0 passed ✅
- Fail messages are clear and descriptive ✅
- All requirements from spec covered ✅
- All edge cases from spec covered ✅

Learnings Applied:
- {Past project 1}: {Lesson applied}
- {Past project 2}: {Lesson applied}

Recommendation: Ready for /agent:plan (architecture design)

Handoff complete.
```

---

## Success Checklist

Before handing off, verify:

- [ ] tests.md file created in `.specify/specs/{feature-name}/`
- [ ] All test files created and syntactically correct
- [ ] All tests FAIL (not ERROR) when run
- [ ] Fail messages are clear and descriptive
- [ ] All requirements from spec have corresponding tests
- [ ] All edge cases from spec have corresponding tests
- [ ] Test data strategy documented (factories, fixtures, mocks)
- [ ] Test patterns documented (from Serena/Octocode)
- [ ] Coverage matrix created
- [ ] Coverage target defined (≥80%)
- [ ] Past learnings applied and documented
- [ ] Pieces memory created
- [ ] Handoff message sent

---

**See Also**:
- [workflow.md](workflow.md) for test design process
- [practices.md](practices.md) for test patterns
- [decisions.md](decisions.md) for decision framework
