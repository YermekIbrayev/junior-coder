# Vibe Learn - Tool Syntax

**Purpose**: Capture mistakes using vibe_learn for pattern recognition and learning.

## Function Signature

```javascript
vibe_learn({
  "type": "mistake",
  "category": "{category}",
  "mistake": "{what I did wrong - specific}",
  "solution": "{human's correction - exact}",
  "context": "Feature: {feature}, Agent: {agent}, Decision: {decision}"
})
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | Yes | Always "mistake" for error capture |
| `category` | Yes | One of the categories below |
| `mistake` | Yes | Specific description of what went wrong |
| `solution` | Yes | Human's exact correction/guidance |
| `context` | Optional | Feature, agent, and decision context |

## Categories

| Category | When to Use |
|----------|-------------|
| `Complex Solution Bias` | Chose overly complex solution when simpler existed |
| `Feature Creep` | Added unnecessary functionality beyond requirements |
| `Premature Implementation` | Implemented before full understanding |
| `Misalignment` | Didn't align with project principles/patterns |
| `Overtooling` | Used tools unnecessarily |
| `Other` | Other mistake types |

## When to Use

**Step 2 of Human Correction Protocol**: After human provides correction, immediately capture the learning.

**Success Criteria**:
- [ ] Correct syntax (all required fields)
- [ ] Appropriate category selected
- [ ] Specific mistake (not vague)
- [ ] Human's exact guidance in "solution"
- [ ] Full context provided

---

**Examples**: [examples/vibe-learn-by-agent.md](../examples/vibe-learn-by-agent.md), [examples/vibe-learn-by-category.md](../examples/vibe-learn-by-category.md)
**Templates**: [templates/vibe-learn-ready.md](../templates/vibe-learn-ready.md)
**Reference**: [protocols/human-correction.md](../protocols/human-correction.md) - Step 2
