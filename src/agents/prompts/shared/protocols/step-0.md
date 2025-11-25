# Step 0: Query Past Learnings

**Purpose**: Query ApeRAG to avoid repeating mistakes. **DO THIS FIRST!**

**Used By**: All agents

## Workflow (5 min)

### 1. Query ApeRAG
```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "{agent-name} + {feature-type} + lessons + corrections",
  use_vector_index: true, use_graph_index: true, use_fulltext_index: true, topk: 5
})
```

### 2. Extract
- ✅ Similar features? Past mistakes? Human corrections? Successful patterns?

### 3. Apply
Document in your output artifact:
```markdown
## Learnings Applied
1. {Past project}: {Lesson} → Applied {how}
2. {Correction}: {Mistake} → Avoiding by {action}
```

### 4. Create Pieces Memory
Template: [pieces-memory-examples.md](pieces-memory-examples.md#step-0-learnings-applied)

### 5. If No Results
```
No past learnings found. Proceeding carefully. Will capture for future.
```

## Progressive Learning Metrics

| Metric | P1 | P2 | P3 | Trend |
|--------|-----|-----|-----|-------|
| Human Interventions | 8 | 5 | 3 | ✅ ↓ |
| Questions Asked | 12 | 8 | 5 | ✅ ↓ |
| Autonomy Rate | 85% | 90% | 94% | ✅ ↑ |

## Success
- [ ] Queried ApeRAG
- [ ] Extracted insights (if found)
- [ ] Documented application
- [ ] Created Pieces memory

---

**Detailed Guide**: [guides/step-0-detailed.md](../guides/step-0-detailed.md) (examples, troubleshooting)
