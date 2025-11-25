# Step 0: Query Past Learnings

**Purpose**: Query ApeRAG knowledge graph to apply learnings from past projects before starting work.

**Used By**: All agents (Spec Analyst, Test Architect, Code Planner, Implementation Specialist, Quality Guardian, etc.)

**When to Use**: **DO THIS FIRST** - Before starting your agent's primary task.

---

## Why This Matters

This creates the **progressive learning feedback loop**:
- Avoid repeating past mistakes
- Apply successful patterns from previous features
- Reduce human interventions over time
- Increase decision autonomy with each project

---

## Workflow

### 1. Query ApeRAG (2 minutes)

```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "{agent-name} + {feature-type} + lessons learned + corrections + {phase-specific-keywords}",
  use_vector_index: true,
  use_graph_index: true,
  use_fulltext_index: true,
  topk: 5
})
```

**Variable Substitutions**:
- `{agent-name}`: Your agent name (e.g., "Spec Analyst", "Implementation Specialist")
- `{feature-type}`: Feature category (e.g., "invoice", "validation", "workflow")
- `{phase-specific-keywords}`: Keywords relevant to your phase
  - Spec Analyst: "requirements", "edge cases", "assumptions"
  - Test Architect: "test strategy", "coverage", "TDD"
  - Implementation Specialist: "implementation", "patterns", "TDD green phase"
  - Quality Guardian: "refactoring", "security", "Semgrep"

### 2. Extract Learnings (2 minutes)

From query results, extract:

✅ **Similar Features**: Have we worked on similar features before?
✅ **Past Mistakes**: What mistakes did this agent make? (from vibe_learn)
✅ **Human Corrections**: What corrections did humans provide?
✅ **Successful Patterns**: What approaches worked well?
✅ **Agent-Specific Insights**:
   - Spec Analyst: Edge cases missed, assumption failures
   - Test Architect: Coverage gaps, test strategy errors
   - Implementation Specialist: Implementation mistakes, test failures
   - Quality Guardian: Refactoring mistakes, security issues

### 3. Apply Learnings (1 minute)

Document how you'll apply learnings to current task:

```markdown
## Learnings Applied (document in your output artifact)

From Past Projects:
1. {Past project name}: Learned {specific lesson} → Applied {how}
   - Example: "email-validation: E2E tests for non-critical workflow wasted resources → Focusing E2E only on approval workflow"

2. {Past correction}: Human corrected {mistake} → Avoiding by {action}
   - Example: "invoice-adjustment: Specified modification instead of separate document → Using separate AdjustmentInvoice model"

3. {Successful pattern}: {Pattern from past} → Adopted for {reason}
   - Example: "Service layer pattern for business logic → Using for adjustment logic"
```

### 4. Create Pieces Memory

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Past Learnings Applied: {feature-name} {phase}",
  "summary": `
## Step 0 Learnings Applied

- Agent: {agent-name}
- Feature: {feature-name}
- Queried: {X} past retrospectives
- Found: {Y} relevant learnings
- Applied: {specific learnings and how}
- Avoided: {specific mistakes from past}

## Impact
- Expected to reduce human interventions by {N}
- Expected to avoid {specific past mistakes}
  `,
  "connected_client": "Claude Code"
})
```

### 5. Handle No Results

If no past learnings found:

```markdown
No past learnings found for this feature type. Proceeding with careful analysis and validation.
Will capture learnings for future projects via vibe_learn and Pieces memories.
```

---

## Progressive Learning Metrics

Each project should show improvement:

| Metric | Project 1 | Project 2 | Project 3 | Trend |
|--------|-----------|-----------|-----------|-------|
| Human Interventions | 8 | 5 | 3 | ✅ Decreasing |
| Questions Asked | 12 | 8 | 5 | ✅ Decreasing |
| Autonomy Rate | 85% | 90% | 94% | ✅ Increasing |
| Learnings Applied | 0 | 8 | 12 | ✅ Increasing |

---

## Success Criteria

✅ Queried ApeRAG for past learnings (even if no results)
✅ Extracted relevant insights (if found)
✅ Documented how learnings will be applied
✅ Created Pieces memory with Step 0 summary
✅ Ready to proceed with agent's primary task

---

**Reference**: This template is used by all agents in their "Workflow" section.
