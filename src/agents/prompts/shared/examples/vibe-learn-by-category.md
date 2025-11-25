# Vibe Learn Examples - By Category

**Purpose**: Full vibe_learn examples organized by mistake category.

## Complex Solution Bias

When: Chose overly complex solution when simpler approach existed

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Complex Solution Bias",
  "mistake": "Designed multi-layer caching with Redis when in-memory dict sufficient",
  "solution": "Start simple - use dict, add Redis only if performance testing proves needed",
  "context": "Feature: product-catalog, Agent: Code Planner, Decision: caching architecture"
})
```

## Feature Creep

When: Added unnecessary functionality beyond requirements

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Feature Creep",
  "mistake": "Added advanced filtering options when basic search was requested",
  "solution": "Implement only what's specified - YAGNI, wait for explicit requirement",
  "context": "Feature: product-search, Agent: Implementation Specialist, Decision: search capabilities"
})
```

## Premature Implementation

When: Implemented before full understanding

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Premature Implementation",
  "mistake": "Built full payment integration before confirming payment provider",
  "solution": "Clarify requirements first - ask CRITICAL questions before implementation",
  "context": "Feature: payment-processing, Agent: Spec Analyst, Decision: payment provider selection"
})
```

## Misalignment

When: Didn't align with project principles/patterns

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Misalignment",
  "mistake": "Modified approved invoice directly instead of creating adjustment",
  "solution": "Follow immutability principle - approved documents are locked, create adjustments",
  "context": "Feature: invoice-correction, Agent: Code Planner, Decision: data modification approach"
})
```

## Overtooling

When: Used tools unnecessarily

```javascript
vibe_learn({
  "type": "mistake",
  "category": "Overtooling",
  "mistake": "Ran Semgrep during implementation phase when Quality Guardian handles it",
  "solution": "Respect phase boundaries - Semgrep is Quality Guardian's tool, not Implementation Specialist's",
  "context": "Feature: user-auth, Agent: Implementation Specialist, Decision: security scanning timing"
})
```

---

**See Also**: [vibe-learn-by-agent.md](vibe-learn-by-agent.md) - Examples organized by agent role
**Tool Syntax**: [../tools/vibe-learn.md](../tools/vibe-learn.md)
**Templates**: [../templates/vibe-learn-ready.md](../templates/vibe-learn-ready.md)
