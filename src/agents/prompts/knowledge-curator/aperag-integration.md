# Knowledge Curator - ApeRAG Integration

## ApeRAG Collection Setup

**Collection Name**: `smartstocker-retrospectives`
**Description**: "Agent system retrospectives and learnings for cross-feature knowledge sharing"

### Create or Select Collection

```javascript
// Check if collection exists
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "test"
})

// If not exists, create
create_collection({
  title: "smartstocker-retrospectives",
  description: "Agent system retrospectives and learnings"
})
```

---

## Upload YAML Files

### Upload Process

For each of the 9 YAML files:

```javascript
upload_documents({
  collection_id: "smartstocker-retrospectives",
  source_type: "local",
  source_data: {
    file_path: ".specify/retrospectives/{feature-name}/yaml/{filename}.yaml"
  }
})
```

### Metadata Tagging

Each document should have:
- `feature_name`: e.g., "email-validation"
- `agent_id`: e.g., "spec-analyst" (for individual retrospectives)
- `report_type`: "individual" | "synthesis" | "system-improvements"
- `date`: Generation date
- `tools_used`: Array of tool names
- `patterns`: Array of pattern names

---

## Graph Relationships

### Relationship Types

#### 1. Feature → Agents

Links feature to all agents that worked on it.

```
Feature "email-validation" --[used_agent]--> Agent "Spec Analyst"
Feature "email-validation" --[used_agent]--> Agent "Test Architect"
... (all 7 agents)
```

#### 2. Agent → Tools

Links agent to tools with ratings.

```
Agent "Spec Analyst" --[used_tool]--> Tool "Sequential Thinking" {rating: 9}
Agent "Spec Analyst" --[used_tool]--> Tool "Vibe Check" {rating: 8}
... (all tools per agent)
```

#### 3. Agent → Patterns

Links agent to patterns observed.

```
Agent "Spec Analyst" --[observed_pattern]--> Pattern "Sequential + Vibe combo"
Agent "Test Architect" --[observed_pattern]--> Pattern "Sequential + Vibe combo"
... (all patterns per agent)
```

#### 4. Feature → Recommendations

Links feature to system recommendations generated.

```
Feature "email-validation" --[generated_recommendation]--> Rec "Add Octocode to Spec Analyst" {priority: "P1"}
... (all recommendations)
```

#### 5. Tool → Effectiveness

Aggregated tool ratings across features.

```
Tool "Sequential Thinking" --[effectiveness_rating]--> {average: 9.2, features: ["email-validation"]}
... (aggregated across features)
```

### Implementation

Use ApeRAG graph API:
1. Create nodes for features, agents, tools, patterns, recommendations
2. Create edges with metadata (ratings, dates, impact)
3. Ensure bidirectional relationships where appropriate

---

## Cross-Feature Queries

### Query 1: Tool Effectiveness

```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "Sequential Thinking average rating across all features",
  use_graph_index: true
})
```

**Expected**: Aggregated rating with feature breakdown

### Query 2: Pattern Replicability

```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "patterns observed in multiple features with high replicability",
  use_graph_index: true
})
```

**Expected**: Patterns appearing in ≥2 features with replicability="high"

### Query 3: Agent Performance

```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "agent execution times aggregated across features",
  use_graph_index: true
})
```

**Expected**: Average execution time per agent

### Query 4: Recommendation Tracking

```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "P0 recommendations with status implemented",
  use_fulltext_index: true
})
```

**Expected**: High-priority recommendations that have been implemented

---

## Validation Steps

### 1. Verify Upload

```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "feature:{feature-name}",
  use_fulltext_index: true
})
```

**Expected**: 9 documents (7 individual + 2 reports)

### 2. Verify Relationships

Query graph for feature connections.

**Expected**: ≥20 relationships created

### 3. Test All Queries

Run all 4 cross-feature queries.

**Expected**: All return valid results

---

## Common Issues

### Issue: Collection Not Found

**Solution**: Create collection first with `create_collection`

### Issue: Upload Fails

**Solution**: Verify file paths are absolute, YAML is valid

### Issue: Missing Relationships

**Solution**: Check all YAML files have required metadata (agent_id, tools, patterns)

### Issue: Query Returns No Results

**Solution**: Verify documents uploaded, check query syntax, ensure indexes enabled
