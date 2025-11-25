# Implementation Specialist - TDD Discipline

**Purpose**: TDD RED-GREEN-REFACTOR workflow and implementation best practices.

---

## TDD GREEN Phase Discipline

**You are in the GREEN phase**: Write minimal code to make tests pass. **NO REFACTORING YET!**

### Workflow

1. **Run Test (RED)**: Execute failing test to see failure message
2. **Write Minimal Code (GREEN)**: Write ONLY enough code to pass the test
3. **Verify Pass**: Run test again, confirm it passes
4. **Repeat**: Move to next failing test
5. **Document**: Record RED→GREEN cycle in implementation-notes.md

### Key Principles

❌ **DON'T**:
- Refactor (that's Quality Guardian's job)
- Add "nice to have" features beyond tests
- Optimize prematurely
- Write code before seeing test fail

✅ **DO**:
- Make tests pass with minimal code
- Follow architecture plan exactly
- Use Clean Code principles from the start
- Document each RED-GREEN cycle

---

## Best Practices

### 1. Use Sequential Thinking for Complex Logic

```javascript
// When implementing complex business logic:
Sequential Thinking:
1. Understand test expectation
2. Identify minimal code needed
3. Implement
4. Verify pass
5. Move to next test
```

### 2. Vibe Check When Stuck

Run vibe_check when:
- Tests keep failing after 3 attempts
- Uncertain about approach
- Architecture seems incorrect

### 3. Find Patterns with Serena

```javascript
// Before writing new code, find similar patterns:
Serena: find_symbol "Service" depth=1
// Analyze existing service layer implementations
```

### 4. Search Solutions with Octocode

```javascript
// When stuck on Django/framework-specific issue:
Octocode: search "django select_for_update concurrent access"
// Find proven patterns from similar codebases
```

### 5. Run Tests Frequently with IDE

- After each code change: Run specific test
- After completing module: Run full test suite
- Before handoff: Run all tests + coverage

---

## Red-Green-Refactor Documentation

**Requirement**: Document ≥2 complete RED-GREEN cycles in implementation-notes.md

### Example Format

```markdown
## Red-Green-Refactor Example 1: Create Adjustment Service

### RED
```
test_create_adjustment_locks_invoice FAILED
AssertionError: Expected select_for_update() call
```

### GREEN (Minimal Code)
```python
def create_adjustment(invoice_id, amount):
    invoice = Invoice.objects.select_for_update().get(id=invoice_id)
    return AdjustmentInvoice.objects.create(
        original_invoice=invoice,
        amount=amount
    )
```

### Result
✅ test_create_adjustment_locks_invoice PASSED
```

---

## Common Patterns

### Service Layer Implementation
- Business logic in services.py (not views.py)
- Use @transaction.atomic for data modifications
- Use select_for_update() for concurrent access

### Django Patterns
- QuerySets: Use select_related(), prefetch_related() (avoid N+1)
- Transactions: Wrap multi-step operations in @transaction.atomic
- Validation: In serializers (DRF) or forms (Django)

### Test Patterns
- FactoryBoy: Generate test data
- Fixtures: Common setup (e.g., authenticated user)
- Parametrize: Test multiple inputs with single test

---

**See Also**:
- [patterns.md](patterns.md) - Common mistakes and solutions
- [../../shared/protocols/human-correction.md](../../shared/protocols/human-correction.md) - If corrected by human
- [core.md](core.md) - Back to role and tools
