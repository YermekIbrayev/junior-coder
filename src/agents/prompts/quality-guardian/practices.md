# Quality Guardian - Best Practices

## Refactoring Practices

### 1. Plan Before Refactoring

**Use Clean Code MCP** to analyze code and identify opportunities:
- Long methods (>20 lines)
- Duplicated code
- Poor naming
- Missing documentation
- Complex conditionals

**Document refactoring plan** before making changes

### 2. Small, Incremental Changes

```
✅ DO: One refactoring at a time
❌ DON'T: Combine multiple refactorings

Process:
1. Make ONE small change
2. Run tests
3. Commit if green
4. Repeat
```

### 3. Keep Tests Green

**NEVER** commit broken tests during refactoring

If tests fail:
- Revert change
- Analyze why
- Fix tests or adjust approach

### 4. Focus on Readability

**Priority**: Readability > Cleverness

Refactor for:
- Clear intent
- Self-documenting code
- Reduced cognitive load
- Future maintainability

---

## Security Practices

### 1. Semgrep is MANDATORY

**Zero tolerance** for critical/high issues

```bash
semgrep --config=auto app/
```

**Before production**:
- Critical: 0 (MUST)
- High: 0 (MUST)
- Medium: Document acceptance
- Low: Document acceptance

### 2. Fix Don't Suppress

**Always** fix security issues, don't suppress findings

Exception: False positives with documented justification

### 3. Use Proven Patterns

Query Octocode for security fixes:
- "django csrf protection"
- "sql injection prevention"
- "secure authentication patterns"

### 4. Re-scan After Fixes

**Always** re-run Semgrep after security fixes to verify resolution

---

## E2E Testing Practices

### 1. Test Critical Paths

Focus on workflows users actually use:
- Happy path (complete workflow)
- Permission denials
- Concurrent access
- Edge cases

### 2. Use Real Data

Test with realistic data volumes:
- 50+ items for performance validation
- Multiple concurrent users
- Large datasets

### 3. Validate UI and Backend

Check both:
- UI displays correctly
- Backend state is correct
- Errors handled gracefully

---

## Performance Practices

### 1. Profile Before Optimizing

Use Chrome DevTools to identify real bottlenecks

Don't guess - measure!

### 2. Fix N+1 Queries

Common Django issue:
```python
# ❌ BAD (N+1 queries)
for item in items:
    product = Product.objects.get(id=item.product_id)

# ✅ GOOD (1 query)
for item in items.select_related('product'):
    product = item.product
```

### 3. Add Database Indexes

For frequently queried fields:
- Foreign keys
- Status fields
- Created/modified dates

---

## Common Mistakes

❌ **Skipping Semgrep** - MANDATORY, cannot ship without 0 critical/high

❌ **Breaking tests during refactoring** - Run tests after EVERY change

❌ **Over-refactoring** - Refactor for readability, not perfection

❌ **Ignoring performance** - Check with Chrome DevTools

❌ **Poor documentation** - Add comprehensive docstrings

❌ **Accepting security issues** - Fix ALL critical/high, justify medium/low

❌ **Combining changes** - One refactoring at a time

❌ **Premature optimization** - Profile first, optimize second

---

## Decision Heuristics

**When uncertain**, ask:
1. "Does this improve readability?" (if not, skip)
2. "Will tests stay green?" (if no, reconsider)
3. "Is this the simplest solution?" (complexity is a smell)
4. "Am I fixing real issues or theoretical ones?" (focus on real)

**Use Vibe Check** to validate refactoring decisions

---

**See Also**: [decisions.md](decisions.md) for critical vs non-critical framework
