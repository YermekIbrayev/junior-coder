# Vibe Learn - Copy-Paste Templates

**Purpose**: Ready-to-use vibe_learn templates - just fill in the blanks.

## Universal Template

```javascript
vibe_learn({
  "type": "mistake",
  "category": "{Complex Solution Bias|Feature Creep|Premature Implementation|Misalignment|Overtooling|Other}",
  "mistake": "{WHAT_I_DID_WRONG - be specific}",
  "solution": "{HUMAN_CORRECTION - exact words}",
  "context": "Feature: {FEATURE_NAME}, Agent: {AGENT_NAME}, Decision: {DECISION_CONTEXT}"
})
```

## By Agent Templates

### Spec Analyst
```javascript
vibe_learn({
  "type": "mistake",
  "category": "{Misalignment|Premature Implementation}",
  "mistake": "Specified {WRONG_APPROACH} instead of {CORRECT_APPROACH}",
  "solution": "{HUMAN_GUIDANCE}",
  "context": "Feature: {FEATURE}, Agent: Spec Analyst, Decision: {WHAT_WAS_BEING_DECIDED}"
})
```

### Test Architect
```javascript
vibe_learn({
  "type": "mistake",
  "category": "{Feature Creep|Complex Solution Bias}",
  "mistake": "Designed {WRONG_TEST_STRATEGY}",
  "solution": "{HUMAN_GUIDANCE}",
  "context": "Feature: {FEATURE}, Agent: Test Architect, Decision: {TEST_SCOPE_OR_STRATEGY}"
})
```

### Code Planner
```javascript
vibe_learn({
  "type": "mistake",
  "category": "{Complex Solution Bias|Misalignment}",
  "mistake": "Designed {WRONG_ARCHITECTURE}",
  "solution": "{HUMAN_GUIDANCE}",
  "context": "Feature: {FEATURE}, Agent: Code Planner, Decision: {ARCHITECTURE_DECISION}"
})
```

### Implementation Specialist
```javascript
vibe_learn({
  "type": "mistake",
  "category": "{Premature Implementation|Feature Creep}",
  "mistake": "Implemented {WRONG_CODE}",
  "solution": "{HUMAN_GUIDANCE}",
  "context": "Feature: {FEATURE}, Agent: Implementation Specialist, Decision: {IMPLEMENTATION_SCOPE}"
})
```

### Quality Guardian
```javascript
vibe_learn({
  "type": "mistake",
  "category": "{Overtooling|Complex Solution Bias}",
  "mistake": "Refactored {WRONG_REFACTORING}",
  "solution": "{HUMAN_GUIDANCE}",
  "context": "Feature: {FEATURE}, Agent: Quality Guardian, Decision: {REFACTORING_SCOPE}"
})
```

---

**Reference**: [../protocols/human-correction.md](../protocols/human-correction.md) - Step 2
**Tool Syntax**: [../tools/vibe-learn.md](../tools/vibe-learn.md)
**Examples**: [../examples/vibe-learn-by-agent.md](../examples/vibe-learn-by-agent.md), [../examples/vibe-learn-by-category.md](../examples/vibe-learn-by-category.md)
