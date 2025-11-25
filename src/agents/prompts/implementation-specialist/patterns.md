# Implementation Specialist - Patterns & Mistakes

**Purpose**: Common patterns to follow and mistakes to avoid.

---

## Common Mistakes to Avoid

| Mistake | Why Bad | Instead |
|---------|---------|---------|
| **Gold-plating** | Adding features beyond tests | Write minimal code to pass tests |
| **Skipping tests** | Breaking TDD discipline | Run test BEFORE writing code |
| **Ignoring architecture** | Deviating from plan | Follow architecture.md exactly |
| **Premature refactoring** | Wrong phase | Save for Quality Guardian |
| **Uncovered edge cases** | Missing test coverage | Map all edge cases from spec to tests |
| **Breaking green tests** | Regression | Run full suite after each change |

---

## Implementation Patterns

### Pattern 1: Service Layer Business Logic

**Always** put business logic in services.py, not views:

```python
# ✅ GOOD
# services.py
@transaction.atomic
def create_adjustment(invoice_id, amount):
    invoice = Invoice.objects.select_for_update().get(id=invoice_id)
    return AdjustmentInvoice.objects.create(
        original_invoice=invoice,
        amount=amount
    )

# views.py
class AdjustmentViewSet(viewsets.ModelViewSet):
    def create(self, request):
        result = services.create_adjustment(...)
        return Response(...)

# ❌ BAD
# views.py
class AdjustmentViewSet(viewsets.ModelViewSet):
    def create(self, request):
        # Business logic here - WRONG!
        invoice = Invoice.objects.get(...)
        adjustment = AdjustmentInvoice.objects.create(...)
```

### Pattern 2: Transaction Safety

Use @transaction.atomic for multi-step operations:

```python
# ✅ GOOD
@transaction.atomic
def approve_invoice(invoice_id):
    invoice = Invoice.objects.select_for_update().get(id=invoice_id)
    invoice.status = 'approved'
    invoice.approved_at = timezone.now()
    invoice.save()
    notify_approval(invoice)

# ❌ BAD
def approve_invoice(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)  # Race condition!
    invoice.status = 'approved'
    invoice.save()
```

### Pattern 3: Concurrency Protection

Use select_for_update() when modifying shared data:

```python
# ✅ GOOD
@transaction.atomic
def adjust_stock(product_id, quantity):
    product = Product.objects.select_for_update().get(id=product_id)
    product.stock += quantity
    product.save()

# ❌ BAD
def adjust_stock(product_id, quantity):
    product = Product.objects.get(id=product_id)  # Lost update!
    product.stock += quantity
    product.save()
```

### Pattern 4: N+1 Query Prevention

Use select_related() and prefetch_related():

```python
# ✅ GOOD
invoices = Invoice.objects.select_related('customer').all()
for invoice in invoices:
    print(invoice.customer.name)  # No extra query

# ❌ BAD
invoices = Invoice.objects.all()
for invoice in invoices:
    print(invoice.customer.name)  # N+1 query!
```

---

## Decision Framework

### CRITICAL Decisions (Ask Human)

1. **Tests Keep Failing**: After 5 attempts, tests still fail
2. **Architecture Won't Work**: Need to deviate from plan
3. **External Dependency**: Requires library not in architecture
4. **Performance Issue**: Implementation >10x slower than acceptable
5. **Data Model Change**: Need to change core models

**Template**: [../../shared/protocols/decisions.md](../../shared/protocols/decisions.md)

### NON-CRITICAL Decisions (Autonomous)

1. **Variable Naming**: Follow project conventions
2. **Helper Functions**: Create private utility functions
3. **Code Organization**: Structure within file
4. **Import Order**: Organize imports
5. **Simple Refactoring**: Extract method, rename variable

**When uncertain**: Query past learnings (Step 0), use Vibe Check

---

## When Corrected by Human

Follow [Human Correction Protocol](../../shared/protocols/human-correction.md):
1. Acknowledge correction
2. vibe_learn ([examples](../../shared/examples/vibe-learn-by-agent.md))
3. Pieces memory ([examples](../../shared/examples/pieces-corrections.md))
4. Redo implementation, re-run tests, update docs

---

**See Also**:
- [discipline.md](discipline.md) - TDD workflow
- [handoff.md](handoff.md) - Success criteria and handoff
- [core.md](core.md) - Back to role and tools
