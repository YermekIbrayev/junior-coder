# Knowledge Curator - Workflow

## 5-Step Curation Process

### Step 1: Collect All Retrospective Artifacts (5 minutes)

**Input Directory**: `.specify/retrospectives/{feature-name}/`

**Expected Files**:

1. **Individual Retrospectives** (7 files):
   - `spec-analyst-retrospective.md`
   - `spec-clarifier-retrospective.md`
   - `test-architect-retrospective.md`
   - `code-planner-retrospective.md`
   - `alignment-analyzer-retrospective.md`
   - `implementation-specialist-retrospective.md`
   - `quality-guardian-retrospective.md`

2. **Aggregated Reports** (2 files):
   - `synthesis-report.md`
   - `system-improvements.md`

**Actions**:
- Verify all files exist
- Query Pieces for any missing context
- Create output directory: `.specify/retrospectives/{feature-name}/yaml/`

---

### Step 2: Convert Retrospectives to YAML (20 minutes)

**For Each Retrospective File**, create corresponding YAML.

**See**: [yaml-schemas.md](yaml-schemas.md) for complete schemas and templates

**Conversion Process**:
1. Read each markdown file
2. Extract structured data (tools, ratings, patterns, recommendations)
3. Convert to YAML using schema templates
4. Save to `.specify/retrospectives/{feature-name}/yaml/`

**Key Sections to Extract**:
- Tools used (with ratings 1-10)
- Patterns observed (with replicability)
- What worked / didn't work
- Lessons learned
- Recommendations (with priority)
- Progressive learning metrics
- Output artifacts
- Handoff quality

---

### Step 3: Upload to ApeRAG (10 minutes)

**See**: [aperag-integration.md](aperag-integration.md) for complete upload process

**ApeRAG Collection**: `smartstocker-retrospectives`

**Upload Process**:

1. **Create or Select Collection**:
   ```
   Use ApeRAG: search_collection or create_collection
   Collection name: "smartstocker-retrospectives"
   Description: "Agent system retrospectives and learnings"
   ```

2. **Upload YAML Files**:
   ```
   For each YAML file:
   - Upload to ApeRAG collection
   - Tag with: feature_name, agent_id, report_type, date
   - Set metadata: {feature, agent, tools_used, patterns}
   ```

3. **Verify Upload**:
   ```
   Query ApeRAG: "Show all retrospectives for feature {feature-name}"
   Expected: 9 documents uploaded
   ```

---

### Step 4: Create Graph Relationships (15 minutes)

**See**: [aperag-integration.md](aperag-integration.md) for relationship details

**Relationship Types**:

1. **Feature → Agents**: Links feature to all agents used
2. **Agent → Tools**: Links agent to tools with ratings
3. **Agent → Patterns**: Links agent to patterns observed
4. **Feature → Recommendations**: Links feature to system recommendations
5. **Tool → Effectiveness**: Aggregated tool ratings across features

**Implementation**:
- Use ApeRAG graph API to create nodes and relationships
- Ensure bidirectional relationships
- Add metadata to edges (ratings, dates, impact)

---

### Step 5: Enable Cross-Feature Queries (5 minutes)

**Test Queries**:

1. **Tool Effectiveness Across Features**:
   ```
   Query: "What's the average rating for Sequential Thinking across all features?"
   Expected: Aggregated rating with feature breakdown
   ```

2. **Pattern Replicability**:
   ```
   Query: "Which patterns have been observed in multiple features?"
   Expected: Patterns with replicability="high" across ≥2 features
   ```

3. **Agent Performance**:
   ```
   Query: "Which agent took the longest on average?"
   Expected: Agent execution times aggregated
   ```

4. **Recommendation Tracking**:
   ```
   Query: "What P0 recommendations have been implemented?"
   Expected: Recommendations with status="implemented"
   ```

**Validation**:
- Run all test queries
- Verify results match expected outputs
- Fix any missing relationships or data

---

## Example Execution

**User Input**:
```
Run /agent:curator for feature "email-validation"
```

**Agent Response**:
```
I'm the Knowledge Curator. I'll convert retrospectives to YAML and upload to ApeRAG.

Step 1: Collecting retrospective files...
✅ 7 individual retrospectives found
✅ synthesis-report.md found
✅ system-improvements.md found

Step 2: Converting to YAML...
✅ 9 YAML files created

Step 3: Uploading to ApeRAG...
✅ 9 documents uploaded to collection 'smartstocker-retrospectives'

Step 4: Creating graph relationships...
✅ 24 relationships created

Step 5: Validating cross-feature queries...
✅ 4/4 test queries passed

Knowledge curation complete!
```

---

**See Also**:
- [yaml-schemas.md](yaml-schemas.md) - Complete YAML templates
- [aperag-integration.md](aperag-integration.md) - ApeRAG upload and graph details
- [handoff.md](handoff.md) - Validation and completion checklist
