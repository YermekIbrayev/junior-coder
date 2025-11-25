# Human Correction Protocol

**Purpose**: Capture corrections for progressive learning. **Used By**: All agents

## 4-Step Process

### 1. Acknowledge
"Thank you. I understand that {restate correction}."

### 2. vibe_learn
```javascript
vibe_learn({
  "type": "mistake",
  "category": "{Complex Solution Bias|Feature Creep|Premature Implementation|Misalignment|Overtooling|Other}",
  "mistake": "{what I did wrong}",
  "solution": "{human's correction}",
  "context": "Feature: {feature}, Agent: {agent}, Decision: {decision}"
})
```

### 3. Pieces Memory
```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Correction: {topic}",
  "summary": "Agent: {agent}\nFeature: {feature}\nMy Approach: {wrong}\nCorrection: {right}\nLesson: {lesson}\nKeywords: {keywords}",
  "connected_client": "Claude Code"
})
```

### 4. Apply
Redo work with correction → Re-run tests/validation → Update output artifact

## Why
Human corrects → Captured (vibe_learn + Pieces) → Future agent queries (Step 0) → Avoids mistake → Interventions ↓

## Success
- [ ] Acknowledged
- [ ] vibe_learn (with category)
- [ ] Pieces memory
- [ ] Applied + verified

---

**Examples**: [vibe-learn-examples.md](vibe-learn-examples.md), [pieces-memory-examples.md](pieces-memory-examples.md)
**Detailed Guide**: [guides/human-correction-detailed.md](../guides/human-correction-detailed.md)
