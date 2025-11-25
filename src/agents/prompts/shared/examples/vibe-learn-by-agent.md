# Vibe Learn Examples - By Agent

**Purpose**: Full vibe_learn examples organized by agent role.

## Spec Analyst

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Misalignment",
  "mistake": "Specified invoice adjustment as modification to original invoice instead of separate document",
  "solution": "Use separate AdjustmentInvoice model to preserve immutability principle",
  "context": "Feature: invoice-adjustment, Agent: Spec Analyst, Decision: adjustment implementation approach"
})
```

## Test Architect

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Feature Creep",
  "mistake": "Designed E2E tests for non-critical workflow paths instead of focusing on critical journeys",
  "solution": "Focus E2E on critical journeys only (login, checkout, approval flow) - YAGNI",
  "context": "Feature: order-workflow, Agent: Test Architect, Decision: E2E test scope"
})
```

## Code Planner

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Complex Solution Bias",
  "mistake": "Designed complex caching layer for simple data access pattern",
  "solution": "Use simple in-memory dict - YAGNI, add caching only if proven needed through performance testing",
  "context": "Feature: product-lookup, Agent: Code Planner, Decision: caching strategy"
})
```

## Implementation Specialist

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Premature Implementation",
  "mistake": "Implemented complex validation logic before tests defined edge cases",
  "solution": "Follow TDD strictly - write minimal code to pass tests, nothing more (GREEN phase discipline)",
  "context": "Feature: email-validation, Agent: Implementation Specialist, Decision: validation implementation scope"
})
```

## Quality Guardian

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Overtooling",
  "mistake": "Refactored working code into unnecessary abstractions during refactor phase",
  "solution": "Refactor only for readability and maintainability - YAGNI, avoid over-engineering",
  "context": "Feature: user-registration, Agent: Quality Guardian, Decision: refactoring scope"
})
```

---

**See Also**: [vibe-learn-by-category.md](vibe-learn-by-category.md) - Examples organized by mistake category
**Tool Syntax**: [../tools/vibe-learn.md](../tools/vibe-learn.md)
**Templates**: [../templates/vibe-learn-ready.md](../templates/vibe-learn-ready.md)
