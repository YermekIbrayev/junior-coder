# Code Planner - Best Practices

## SOLID Principles

### Single Responsibility Principle (SRP)

**Principle**: A class/function should have one, and only one, reason to change.

**Application**:
- ✅ `create_adjustment_service.py` - handles adjustment creation only
- ✅ `adjustment_validator.py` - validation only
- ❌ `adjustment_manager.py` - does creation + validation + inventory + emails (violates SRP)

**Test**: Can you name it easily? If not, probably violates SRP.

---

### Open/Closed Principle (OCP)

**Principle**: Software entities should be open for extension, closed for modification.

**Application**:
```python
# ✅ GOOD: Extensible without modifying
class NotificationService:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def notify(self, user, message):
        self.strategy.send(user, message)

# Add new notification method by creating new strategy, not modifying existing code

# ❌ BAD: Must modify for new notification types
class NotificationService:
    def notify(self, user, message, type):
        if type == "email":
            send_email(user, message)
        elif type == "sms":  # Requires modification to add new type
            send_sms(user, message)
```

---

### Liskov Substitution Principle (LSP)

**Principle**: Objects of a superclass should be replaceable with objects of a subclass without breaking the application.

**Application**:
```python
# ✅ GOOD: Subtypes behave consistently
class Document:
    def approve(self):
        self.status = "approved"

class Invoice(Document):
    def approve(self):
        super().approve()
        recalculate_inventory()  # Additional behavior, doesn't break contract

# ❌ BAD: Subtype changes behavior unexpectedly
class ReadOnlyDocument(Document):
    def approve(self):
        raise NotImplementedError()  # Breaks LSP - unexpected behavior
```

---

### Interface Segregation Principle (ISP)

**Principle**: No client should be forced to depend on methods it does not use.

**Application**:
```python
# ✅ GOOD: Many small interfaces
class Printable:
    def print(self): pass

class Exportable:
    def export(self): pass

class Report(Printable, Exportable):  # Only implements what it needs
    pass

# ❌ BAD: Fat interface
class DocumentOperations:
    def print(self): pass
    def export(self): pass
    def email(self): pass
    def archive(self): pass
    # Invoice might not need email/archive but forced to implement
```

---

### Dependency Inversion Principle (DIP)

**Principle**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Application**:
```python
# ✅ GOOD: Depends on abstraction
class AdjustmentService:
    def __init__(self, inventory_manager: InventoryManagerInterface):
        self.inventory_manager = inventory_manager

# ❌ BAD: Depends on concrete implementation
class AdjustmentService:
    def __init__(self):
        self.inventory_manager = StockMovementManager()  # Tightly coupled
```

---

## File Size Management

### Constitutional Constraint: ≤200 Lines

**Strategies**:

#### 1. Split by Responsibility

```python
# BEFORE (280 lines - TOO LARGE)
# adjustment_service.py

# AFTER (3 files, each <200 lines)
# adjustment_service.py (150 lines - main logic)
# adjustment_validator.py (80 lines - validation)
# adjustment_calculator.py (70 lines - calculations)
```

#### 2. Extract Utilities

```python
# Move reusable functions to utils/
# adjustment_utils.py (100 lines)
# - format_adjustment_reason()
# - calculate_adjustment_impact()
```

#### 3. Use Composition

```python
# Instead of one large class
class AdjustmentManager:  # 300 lines - TOO LARGE
    def validate(self): pass
    def create(self): pass
    def notify(self): pass
    # ...

# Split into smaller classes
class AdjustmentValidator:  # 80 lines
class AdjustmentCreator:    # 100 lines
class AdjustmentNotifier:   # 60 lines

# Compose in service
class AdjustmentService:    # 100 lines
    def __init__(self):
        self.validator = AdjustmentValidator()
        self.creator = AdjustmentCreator()
        self.notifier = AdjustmentNotifier()
```

---

## Design Pattern Selection

### When to Use Patterns

**Service Layer** (SmartStocker Standard):
- Use for ALL business logic
- ✅ Testable
- ✅ Reusable
- ✅ Transaction management

**Factory Pattern**:
- Complex object creation
- Multiple construction paths
- Example: `InvoiceFactory.create(type="adjustment")`

**Strategy Pattern**:
- Interchangeable algorithms
- Example: `NotificationStrategy` (email, SMS, push)

**Decorator Pattern**:
- Add functionality without modification
- Example: `@transaction.atomic`, `@permission_required`

### When NOT to Use Patterns

❌ **Premature abstraction**: Don't create patterns "just in case"
❌ **Over-engineering**: KISS (Keep It Simple, Stupid)
❌ **Not validated**: Always check Octocode for production examples

---

## Function Signature Best Practices

### Type Hints (Required)

```python
# ✅ GOOD
def create_adjustment(
    invoice: Invoice,
    reason: str,
    line_items: list[AdjustmentLineItem],
    user: User
) -> Adjustment:
    pass

# ❌ BAD
def create_adjustment(invoice, reason, line_items, user):
    pass
```

### Docstrings (Required)

```python
"""
Brief one-line summary.

Detailed explanation of what this does and why.

Args:
    invoice: Invoice to adjust (must be approved)
    reason: Justification for adjustment
    line_items: Products/quantities to adjust
    user: User creating adjustment

Returns:
    Created adjustment in draft status

Raises:
    InvoiceNotAdjustableError: If invoice not approved
    PermissionError: If user lacks permission

Example:
    >>> adj = create_adjustment(invoice, "Pricing error", items, user)
"""
```

### Error Handling

```python
# ✅ GOOD: Specific exceptions
class InvoiceNotAdjustableError(Exception):
    """Raised when trying to adjust non-approved invoice."""

def create_adjustment(invoice, ...):
    if invoice.status != "approved":
        raise InvoiceNotAdjustableError(f"Invoice {invoice.id} not approved")

# ❌ BAD: Generic exceptions
def create_adjustment(invoice, ...):
    if invoice.status != "approved":
        raise ValueError("Bad status")  # Too generic
```

---

## Database Best Practices

### Transactions

```python
# ✅ GOOD: Atomic operations
from django.db import transaction

@transaction.atomic
def create_adjustment(invoice, ...):
    adjustment = Adjustment.objects.create(...)
    recalculate_inventory(adjustment)
    # All-or-nothing
```

### Locking

```python
# ✅ GOOD: Prevent concurrent modifications
invoice = Invoice.objects.select_for_update().get(id=invoice_id)
```

### Query Optimization

```python
# ✅ GOOD: Prevent N+1
line_items = adjustment.line_items.select_related('product').all()

# ❌ BAD: N+1 queries
for item in adjustment.line_items.all():
    product = item.product  # Additional query per item
```

---

## Common Architecture Mistakes

❌ **God classes**: One class doing everything (violates SRP)
❌ **Tight coupling**: Direct dependencies instead of abstractions (violates DIP)
❌ **No error handling**: Missing exception planning
❌ **Ignoring ≤200 lines**: Not planning file splits
❌ **Premature optimization**: Optimizing before measuring
❌ **No pattern validation**: Not checking Octocode for proven patterns

---

**See Also**:
- [workflow.md](workflow.md) - Architecture design process
- [decisions.md](decisions.md) - Decision framework
- [handoff.md](handoff.md) - architecture.md template
