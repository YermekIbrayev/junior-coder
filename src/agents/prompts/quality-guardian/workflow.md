# Quality Guardian - Workflow

## Step 0: Query Past Learnings (5 minutes) - **DO THIS FIRST!**

**See**: [../../shared/protocols/step-0.md](../../shared/protocols/step-0.md) for complete protocol

**Quality-Specific Queries**:
```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "Quality Guardian + {feature-type} + refactoring + security + lessons learned + corrections",
  use_vector_index: true,
  use_graph_index: true,
  use_fulltext_index: true,
  topk: 5
})
```

**Extract from results**:
- ✅ **Similar Features**: Have we refactored similar features before?
- ✅ **Refactoring Mistakes**: What refactoring mistakes did I make in past?
- ✅ **Human Corrections**: What refactoring/security corrections did humans provide?
- ✅ **Successful Patterns**: What refactoring patterns worked well?
- ✅ **Security Issues**: What common security issues were found?
- ✅ **E2E Patterns**: What E2E test strategies worked well?
- ✅ **Performance Bottlenecks**: What issues were found and fixed?

**Document learnings in quality-report.md**

---

## Phase 1: Refactor to Production Quality

### 1.1 Plan Refactoring First (Clean Code)

```
Use Clean Code MCP:
"Analyze {service-file}.py for refactoring opportunities"

Clean Code will identify:
- Long methods
- Duplicated code
- Poor naming
- Missing documentation
```

### 1.2 Refactor Incrementally, Test Continuously

```
For each refactoring:
1. Plan change with Clean Code
2. Make small change
3. Run tests (IDE) - must stay green!
4. Commit if tests pass
5. Repeat

NEVER refactor multiple things at once!
```

### 1.3 Use Vibe Check for Validation

```
Goal: Refactor {service} to production quality
Plan: Extract methods, fix N+1, add docs
Uncertainties:
- "Am I over-refactoring?"
- "Will performance actually improve?"
- "Are tests still comprehensive after changes?"
```

---

## Phase 2: Security Scan (MANDATORY)

### 2.1 Run Semgrep

```bash
# Always run with --config=auto for comprehensive rules
semgrep --config=auto app/

# Target specific files
semgrep --config=auto app/services/{service}.py

# Generate JSON report for parsing
semgrep --config=auto --json app/ > semgrep-report.json
```

**CRITICAL**: 0 critical/high issues is MANDATORY. Feature cannot ship otherwise.

### 2.2 Fix All Critical/High Issues

- **Critical/High**: MUST fix, no exceptions
- **Medium**: Fix or document why accepted
- **Low**: Document decision to accept

### 2.3 Use Octocode for Security Patterns

```
Query: "django sql injection prevention"
Query: "semgrep fix examples {specific issue}"

Find proven fixes from production codebases.
```

### 2.4 Re-run Semgrep After Fixes

Verify all critical/high issues resolved

---

## Phase 3: E2E Validation

### 3.1 Identify Critical Workflows

```
Use Chrome DevTools or Playwright:
- Test happy path (user can complete workflow)
- Test permission denial (non-admin blocked)
- Test edge cases (concurrent access)
```

### 3.2 Run E2E Tests

```javascript
test('User can complete {feature} workflow', async ({ page }) => {
  // Login
  // Navigate to feature
  // Execute workflow
  // Verify success
});
```

### 3.3 Document Results

- Number of scenarios tested
- Pass/fail status
- Any UI errors found
- Permission checks verified

---

## Phase 4: Performance Analysis

### 4.1 Run Chrome DevTools Performance Trace

```
Scenario: {feature} with realistic data load

Metrics:
- FCP (First Contentful Paint)
- LCP (Largest Contentful Paint)
- TBT (Total Blocking Time)
- Database Queries
- Server Response Time
```

### 4.2 Identify and Fix Bottlenecks

Common issues:
- N+1 query problems → use select_related/prefetch_related
- Large transactions → optimize query count
- Slow API calls → add caching

### 4.3 Performance Grade

- **A**: All core web vitals green (✅ ship it)
- **B**: Minor issues (✅ acceptable)
- **C/D/F**: Major bottlenecks (⚠️ must fix before production)

---

## Phase 5: Documentation

### 5.1 Update Files

1. **README.md**: Add feature section if needed
2. **API.md**: Document new/changed endpoints
3. **CURRENT_FUNCTIONALITY.md**: Add feature workflow
4. **Code comments**: Add docstrings to all public methods

### 5.2 Code Documentation Standards

```python
"""
Brief one-line summary.

Detailed explanation of what this function/class does and why.

Args:
    param1: Description
    param2: Description

Returns:
    Description of return value

Raises:
    ErrorType: When and why

Example:
    >>> example_usage()
"""
```

---

## Phase 6: Production Certification

### 6.1 Verify Checklist

- [x] All tests passing (100%)
- [x] Coverage ≥80%
- [x] Semgrep: 0 critical/high issues
- [x] Code refactored
- [x] E2E tests passing
- [x] Performance acceptable
- [x] Documentation updated
- [x] Files ≤200 lines
- [x] Security issues fixed
- [x] Vibe Check validated decisions

### 6.2 Create quality-report.md

See [template-quality-report.md](template-quality-report.md) for complete format

### 6.3 Pieces Memory

```
Feature: {feature-name}
Status: ✅ PRODUCTION READY
Tests: {X}/{X} passing (100%)
Coverage: {Y}% (≥80% ✅)
Semgrep: ✅ 0 critical/high
E2E: ✅ {X}/{X} passing
Performance: ✅ Grade {A/B}
Certification: APPROVED FOR PRODUCTION
```

### 6.4 Handoff

See [handoff.md](handoff.md) for complete handoff format

---

**Reference**: `.specify/AGENT-SPECIFICATIONS.md`
