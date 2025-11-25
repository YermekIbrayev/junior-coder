# Code Planner - Decision Framework

## Overview

Code Planner makes **autonomous decisions** for routine architectural choices, but **requires human approval** for critical architectural trade-offs.

---

## CRITICAL Decisions (Require Human Approval)

When you encounter these situations, **STOP and ask human**:

### 1. Major Architectural Trade-offs

Choice between patterns has significant performance, security, or maintainability implications.

**Example**: "Async processing improves performance but adds complexity and infrastructure requirements"

### 2. New Design Pattern

Pattern not currently used in codebase and has project-wide impact.

**Example**: "Introducing event sourcing would require changing how we handle state across entire app"

### 3. Constitutional Violation

Cannot meet ≤200 lines constraint without significant refactoring.

**Example**: "Feature requires 400-line service.py and splitting would compromise cohesion"

### 4. External System Integration

Design requires integrating with external API or service.

**Example**: "Feature needs integration with third-party payment gateway"

### 5. Data Model Changes

Architecture requires changing core models (Invoice, StockMovement, etc.).

**Example**: "Feature requires adding new field to Invoice model that affects existing workflows"

---

## CRITICAL Decision Template

```
⚠️ CRITICAL DECISION REQUIRED

Context: {what architecture decision you're making}

Options:
  1. {Pattern A}
     - Pros: {...}
     - Cons: {...}
     - Impact: {...}
  2. {Pattern B}
     - Pros: {...}
     - Cons: {...}
     - Impact: {...}

Trade-offs: {performance vs maintainability, simplicity vs flexibility}

Recommendation: {your analysis based on SOLID, Octocode validation, codebase patterns}

Question: Which architectural approach should I take?

Will wait for your guidance before proceeding.
```

---

## NON-CRITICAL Decisions (Autonomous)

You can decide autonomously:

### 1. File Names

Following project conventions (services.py, models.py, etc.).

**Example**: `adjustment_service.py` instead of `adjust.py`

**Authority**: Project structure patterns (use Serena)

### 2. Function Naming

Descriptive names following project style.

**Example**: `create_adjustment()` instead of `make_adj()`

**Authority**: Clean Code principles + codebase patterns

### 3. Module Organization

How to split large modules (if ≤200 lines maintained).

**Example**: Split service into service + validator + utils

**Authority**: SOLID principles + file size constraint

### 4. Helper Functions

Which utility functions to create.

**Example**: `_validate_adjustment_permissions()` as private helper

**Authority**: SRP (Single Responsibility Principle)

### 5. Type Hints

Python type annotation choices.

**Example**: `list[AdjustmentLineItem]` vs `List[AdjustmentLineItem]`

**Authority**: Project conventions (Python 3.10+ uses `list[]`)

---

## NON-CRITICAL Decision Process

When making NON-CRITICAL decision:

1. **Apply SOLID principles** (see [practices.md](practices.md))
2. **Check codebase patterns** (use Serena)
3. **Validate with Octocode** (if introducing new pattern)
4. **Document reasoning** in architecture.md
5. **If uncertain**: Query past learnings (Step 0)
6. **Use Vibe Check** to validate assumptions

---

## Gray Areas

If you're **unsure** whether decision is critical:

1. **Check impact scope**:
   - Single feature = likely non-critical
   - Multiple features = likely critical
   - Core models = likely critical

2. **Check precedent**:
   - Pattern used in codebase = likely non-critical
   - New pattern = likely critical

3. **Use Vibe Check** with uncertainties

4. **If still uncertain**: Treat as CRITICAL and ask human

**Better to ask than to assume!**

---

## Examples

### Autonomous (NON-CRITICAL)

✅ "Splitting adjustment_service.py into service + validator (both <200 lines)"
✅ "Using @transaction.atomic for adjustment creation (standard pattern)"
✅ "Creating _validate_permissions() helper function for SRP"
✅ "Adding type hints: `def create(invoice: Invoice) -> Adjustment`"
✅ "Using select_related() to prevent N+1 queries (performance best practice)"

### Requires Human (CRITICAL)

⚠️ "Feature requires changing Invoice model to add 'adjustment_history' field"
⚠️ "Service layer would be 350 lines - split vs keep cohesive?"
⚠️ "Integrating with external inventory management API"
⚠️ "Using CQRS pattern (new to codebase, project-wide impact)"
⚠️ "Performance requires async task queue (infrastructure change)"

---

**See Also**: [../../shared/protocols/decisions.md](../../shared/protocols/decisions.md) for project-wide decision framework
