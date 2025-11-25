# Knowledge Curator - Handoff Protocol

## Pre-Completion Validation

Before marking complete, verify:

### 1. YAML Files Created (9 total)

```bash
ls .specify/retrospectives/{feature-name}/yaml/
```

**Expected**:
- 7 individual agent retrospectives (.yaml)
- 1 synthesis-report.yaml
- 1 system-improvements.yaml

**Total**: 9 YAML files

### 2. YAML Schema Compliance

Each YAML file must have:
- All required fields (feature_name, agent_id, tools_used, etc.)
- Valid YAML syntax (proper indentation, no syntax errors)
- All 1-10 ratings preserved from markdown
- All text descriptions and evidence

### 3. ApeRAG Upload Confirmed

```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "feature:{feature-name}"
})
```

**Expected**: 9 documents found

### 4. Graph Relationships Created

**Expected**: ≥20 relationships
- Feature → Agents (7 relationships)
- Agents → Tools (10+ relationships)
- Agents → Patterns (variable)
- Feature → Recommendations (variable)

### 5. Cross-Feature Queries Passing

Run all 4 test queries:
- ✅ Tool effectiveness query
- ✅ Pattern replicability query
- ✅ Agent performance query
- ✅ Recommendation tracking query

---

## Output Artifacts

### 1. YAML Directory

**Location**: `.specify/retrospectives/{feature-name}/yaml/`

**Contents**: 9 YAML files (verified above)

### 2. ApeRAG Collection

**Collection**: `smartstocker-retrospectives`
**Documents**: 9 uploaded
**Relationships**: ≥20 created

### 3. Pieces Memory

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Knowledge Curated: {feature-name}",
  "summary": `
## Knowledge Curation Complete

**Feature**: {feature-name}
**Date**: {date}

### Artifacts Created
- YAML Files: 9 (7 individual + 2 reports)
- ApeRAG Upload: ✅ All uploaded
- Graph Relationships: {count} created
- Test Queries: ✅ 4/4 passing

### Collection
- Name: smartstocker-retrospectives
- Total Documents: {total-count} (including previous features)

### Future Learning
✅ Cross-feature learning enabled
✅ Future agents can query this feature's learnings
✅ Progressive improvement tracking active

Retrospective cycle complete.
  `,
  "connected_client": "Claude Code"
})
```

---

## Completion Message

```
Knowledge curation complete for "{feature-name}".

Summary:
- YAML Files: 9 created and validated
- ApeRAG Upload: ✅ All 9 documents uploaded to 'smartstocker-retrospectives'
- Graph Relationships: {count} created (feature → agents → tools → patterns)
- Cross-Feature Queries: ✅ 4/4 test queries passing

Knowledge Graph Status:
✅ Future features can query past learnings
✅ Tool effectiveness trends trackable
✅ Pattern replicability validated
✅ Recommendation implementation trackable

Retrospective cycle complete. Feature knowledge is now part of the learning system.
```

---

## Quality Checklist

Use this checklist before marking complete:

- [ ] ✅ 9 YAML files created (7 individual + 2 reports)
- [ ] ✅ All YAML files follow schema (tools, patterns, recommendations)
- [ ] ✅ All 1-10 ratings preserved from markdown
- [ ] ✅ All files uploaded to ApeRAG (`smartstocker-retrospectives` collection)
- [ ] ✅ ≥20 graph relationships created
- [ ] ✅ Test queries return expected results (4/4 queries)
- [ ] ✅ Pieces memory created with summary
- [ ] ✅ Future features can query this feature's learnings

**If any item fails**: Fix before marking complete.

---

## Next Steps (Optional)

After knowledge curation, the retrospective cycle is complete.

**Optional Activities**:
- Review system improvements recommendations
- Implement high-priority (P0/P1) recommendations
- Plan for next feature with learnings applied

**Knowledge Graph Growth**:
- Each feature adds to collective knowledge
- Cross-feature patterns become visible
- System continuously improves over time

---

**Handoff Complete**: Knowledge curator work is done. Feature knowledge is preserved and queryable.
