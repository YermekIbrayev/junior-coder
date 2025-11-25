# Synthesis Specialist - Workflow

## Synthesis Process

### Step 1: Collect Retrospectives (5 minutes)

**Input Location**: `.specify/retrospectives/{feature-name}/`

**Expected Files** (from 7 agents):
1. `spec-analyst-retrospective.md`
2. `spec-clarifier-retrospective.md` (if used)
3. `test-architect-retrospective.md`
4. `code-planner-retrospective.md`
5. `alignment-analyzer-retrospective.md`
6. `implementation-specialist-retrospective.md`
7. `quality-guardian-retrospective.md`

**Actions**:
- Use Serena to read all retrospective files
- Query Pieces for agent memories
- Verify all expected retrospectives exist

---

### Step 2: Analyze Tool Effectiveness (10 minutes)

**For Each MCP Tool**:
- Sequential Thinking: Ratings from all agents
- Vibe Check: Ratings from all agents
- Clean Code: Ratings from Test/Plan/Implement/Refactor agents
- Semgrep: Rating from Quality Guardian
- Octocode: Ratings from all research-phase agents
- IDE: Ratings from Test/Implement/Refactor agents

**Analysis Method**:
```
1. Extract 10-point ratings from each retrospective
2. Calculate average rating per tool
3. Identify highest/lowest rated tools
4. Note which agents found which tools most useful
5. Identify tool gaps or underutilization
```

**Use Sequential Thinking** to systematically analyze each tool across agents.

---

### Step 3: Identify Cross-Agent Patterns (10 minutes)

**Pattern Categories**:
- **Process Patterns**: Workflow improvements, handoff issues
- **Tool Patterns**: Common tool usage, tool combinations
- **Quality Patterns**: Testing practices, code quality habits
- **Communication Patterns**: Spec clarity, alignment issues

**Analysis Method**:
```
1. Read each retrospective's "Patterns Observed" section
2. Group similar patterns across agents
3. Identify recurring themes (≥3 agents mention)
4. Note agent-specific patterns (unique insights)
5. Validate patterns with Vibe Check
```

**Use Sequential Thinking** to group and categorize patterns systematically.

---

### Step 4: Create Development Timeline (5 minutes)

**Timeline Elements**:
- Feature start/end timestamps
- Each agent's execution time
- Total development time
- Handoff points
- Quality gate results

**Format**:
```
Feature: {feature-name}
Started: {timestamp}
Completed: {timestamp}
Total Time: {hours}

Agent Timeline:
- Spec Analyst: {time} (spec.md created)
- Spec Clarifier: {time} (ambiguities resolved)
- Test Architect: {time} (tests.md + failing tests)
- Code Planner: {time} (architecture.md)
- Alignment Analyzer: {time} (alignment-report.md - APPROVED)
- Implementation Specialist: {time} (code green)
- Quality Guardian: {time} (Semgrep ✅, E2E ✅)
```

---

### Step 5: Analyze Progressive Learning Metrics (15 minutes)

**Objective**: Compare current project with Project N-1 to assess progressive learning effectiveness.

**Process**:

#### 1. Query ApeRAG for Project N-1 Metrics (if not first project):

```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "progressive_learning_aggregated + {previous_project_name}",
  use_vector_index: true,
  use_graph_index: true,
  topk: 1
})
```

#### 2. Extract Metrics from Current Project:

Aggregate `progressive_learning_metrics` from all 7 agent retrospectives:
- `total_human_interventions` (sum across agents)
- `total_questions_asked` (sum across agents)
- `total_autonomous_decisions` (sum across agents)
- `total_learnings_applied` (sum across agents)
- `overall_autonomy_rate` (autonomous / total decisions)

#### 3. Compare with Project N-1 (if available):

Calculate deltas: `current - previous`

Determine trends:
- Human interventions: ↓ improving (fewer), → stable, ↑ regressing (more)
- Questions asked: ↓ improving (fewer), → stable, ↑ regressing (more)
- Autonomy rate: ↑ improving (higher %), → stable, ↓ regressing (lower %)
- Learnings applied: ↑ improving (more), → stable, ↓ regressing (fewer)

#### 4. Assess Learning Velocity:

**Mistakes Repeated**: Count how many Project N-1 mistakes were repeated
- Query: "vibe_learn + {current_project} + mistakes" → compare categories with N-1
- Should be 0 if progressive learning works

**New Mistakes Made**: Count unique mistake categories in current project

**Learnings Effectiveness**: `learnings_applied / learnings_queried` (%)

#### 5. Calculate Progressive Learning Health Score (0-10):

```
Score Formula:
- Human interventions trending ↓: +2 points
- Questions asked trending ↓: +2 points
- Autonomy rate trending ↑: +2 points
- Learnings applied effectively (>50%): +2 points
- Zero repeated mistakes: +2 points

Assessment:
- 9-10: "excellent" - System is learning rapidly
- 7-8: "good_start" - Positive trends, needs more data
- 5-6: "needs_improvement" - Some learning, but concerns
- 0-4: "not_learning" - No improvement or regressing
```

#### 6. Write Learning Trends Summary:

2-3 paragraph narrative analyzing:
- Is the system learning from past projects?
- Which metrics show improvement?
- What concerns exist?
- What should we focus on?

**Use Sequential Thinking** to systematically analyze metrics and calculate scores.

**Use Vibe Check** to validate learning assessment ("Is this truly improving or just variance?").

**First Project Handling**:
- If this is Project #1 (no Project N-1 data):
  - Set all "previous" values to `null`
  - Set all "delta" values to `null`
  - Set all "trend" values to `null`
  - Score: Default to 7.5/10 ("good_start")
  - Note: "First project - baseline established, need Project #2 to assess learning"

---

### Step 6: Synthesize Key Takeaways (10 minutes)

**Takeaway Categories**:
1. **What Worked Well**: Top 3 successes
2. **What Needs Improvement**: Top 3 pain points
3. **Tool Insights**: Best tool combinations, underutilized tools
4. **Process Insights**: Workflow optimizations, handoff improvements
5. **Future Recommendations**: Actionable next steps

**Synthesis Method**:
```
1. Aggregate all "What Worked" from retrospectives
2. Aggregate all "What Didn't Work" from retrospectives
3. Identify top 3-5 recurring themes
4. Validate with Vibe Check (are these real insights?)
5. Make them actionable (specific, measurable)
```

---

## Quality Checks (Run Before Handoff)

**Verify**:
- [ ] All 7 retrospectives read and analyzed
- [ ] Tool ratings calculated for all tools (averages + insights)
- [ ] ≥3 cross-agent patterns identified and documented
- [ ] Timeline complete with timestamps
- [ ] ≥5 key takeaways synthesized (3 successes, 3 improvements)
- [ ] Recommendations are specific and actionable
- [ ] synthesis-report.md follows template
- [ ] Pieces memory created

**If any verification fails**: Fix before handoff.

---

**See Also**:
- [practices.md](practices.md) for common issues and final reminders
- [handoff.md](handoff.md) for complete synthesis-report.md template
