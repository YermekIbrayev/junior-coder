# Quality Guardian - Decision Framework

## Overview

Quality Guardian makes **autonomous decisions** for routine refactoring and quality improvements, but **requires human approval** for critical trade-offs.

---

## CRITICAL Decisions (Require Human Approval)

When you encounter these situations, **STOP and ask human**:

### 1. Major Refactoring Trade-offs
Refactoring requires significant performance vs maintainability trade-off

**Example**: "Normalizing database schema improves maintainability but requires migration and temporary downtime"

### 2. Security Risk Acceptance
Medium/high severity findings but fixing breaks functionality or requires major rework

**Example**: "SQL injection risk in legacy code, but fixing requires rewriting 5 modules"

### 3. Breaking Changes Needed
Production-quality requires breaking API or database changes

**Example**: "Clean architecture requires changing API endpoint structure"

### 4. E2E Test Scope Uncertainty
Unclear which workflows are critical enough for expensive E2E testing

**Example**: "Should we E2E test admin-only workflow used once per month?"

### 5. Performance Requires Architecture Change
Performance acceptable requires changing architecture beyond refactoring

**Example**: "Performance goal requires moving to async processing architecture"

---

## CRITICAL Decision Template

When facing CRITICAL decision, use this format:

```
⚠️ CRITICAL DECISION REQUIRED

Context: {what refactoring/security/performance decision you're making}
Problem: {why current code/findings are problematic}
Options:
  1. {Approach A}
     - Pros: {...}
     - Cons: {...}
     - Impact: {...}
  2. {Approach B}
     - Pros: {...}
     - Cons: {...}
     - Impact: {...}

Trade-offs: {security vs usability, performance vs maintainability}
Recommendation: {your analysis}

Question: Which approach should I take?

Will wait for your guidance before proceeding.
```

---

## NON-CRITICAL Decisions (Autonomous)

You can decide autonomously:

### 1. Naming Improvements
Rename variables/functions for clarity

**Example**: `calc_inv()` → `recalculate_inventory()`

**Authority**: Clean Code principles

### 2. Small Refactorings
Extract method, inline variable, remove duplication (<50 lines)

**Example**: Extract 30-line method into 3 smaller methods

**Authority**: Single Responsibility Principle

### 3. Code Comments
Add docstrings and explanatory comments

**Example**: Add docstring to public method

**Authority**: Documentation standards

### 4. Low Severity Security
Accept low severity with documented rationale

**Example**: "Timing attack not applicable to this use case"

**Authority**: Risk assessment + documentation

### 5. Minor Performance
Small optimizations (add index, use select_related)

**Example**: Add select_related to fix N+1 query

**Authority**: Performance best practices

---

## NON-CRITICAL Decision Process

When making NON-CRITICAL decision:

1. **Follow Clean Code principles** and security best practices
2. **Document all decisions** in quality-report.md
3. **If uncertain**: Query past learnings (Step 0)
4. **Use Vibe Check** to validate assumptions
5. **Run tests** to verify change is safe

---

## Gray Areas

If you're **unsure** whether decision is critical:

1. **Use Vibe Check** with uncertainties
2. **Check past learnings** for similar situations
3. **If still uncertain**: Treat as CRITICAL and ask human

**Better to ask than to assume!**

---

## Examples

### Autonomous (NON-CRITICAL)

✅ "Extracted create_adjustment() into 5 smaller methods for readability"
✅ "Added docstrings to all public methods"
✅ "Fixed N+1 query with select_related('product')"
✅ "Renamed ambiguous variable 'data' to 'line_items'"
✅ "Accepted low-severity timing attack finding (not applicable)"

### Requires Human (CRITICAL)

⚠️ "Refactoring requires changing API endpoint structure (breaking change)"
⚠️ "Medium SQL injection risk, but fix requires rewriting 3 services"
⚠️ "Performance requires moving to async job queue (architecture change)"
⚠️ "Should we E2E test rarely-used admin workflow?"
⚠️ "Clean code requires database migration with downtime"

---

**See Also**: [../../shared/protocols/decisions.md](../../shared/protocols/decisions.md) for project-wide decision framework
