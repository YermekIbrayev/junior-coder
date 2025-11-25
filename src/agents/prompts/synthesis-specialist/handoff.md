# Synthesis Specialist - Handoff & Output Template

## File: synthesis-report.md

**Location**: `.specify/retrospectives/{feature-name}/synthesis-report.md`

**Template**:

```markdown
# Synthesis Report: {Feature Name}

**Date**: {YYYY-MM-DD}
**Feature**: {feature-name}
**Total Development Time**: {hours}

---

## Development Timeline

### Overview
- **Started**: {timestamp}
- **Completed**: {timestamp}
- **Total Time**: {hours}
- **Agents Used**: 7

### Agent Execution Timeline

| Agent | Duration | Output | Status |
|-------|----------|--------|--------|
| Spec Analyst | {time} | spec.md | ✅ |
| Spec Clarifier | {time} | spec.md updated | ✅ |
| Test Architect | {time} | tests.md, failing tests | ✅ |
| Code Planner | {time} | architecture.md | ✅ |
| Alignment Analyzer | {time} | alignment-report.md | ✅ APPROVED |
| Implementation Specialist | {time} | Working code | ✅ 100% tests pass |
| Quality Guardian | {time} | Production code | ✅ Semgrep 0 critical |

---

## Tool Effectiveness Analysis

### Ratings Summary (10-point scale)

| Tool | Avg Rating | Used By | Top Insight |
|------|------------|---------|-------------|
| Sequential Thinking | {avg} | {count} agents | {insight} |
| Vibe Check | {avg} | {count} agents | {insight} |
| Clean Code | {avg} | {count} agents | {insight} |
| Semgrep | {rating} | Quality Guardian | {insight} |
| Octocode | {avg} | {count} agents | {insight} |
| Serena | {avg} | {count} agents | {insight} |
| IDE | {avg} | {count} agents | {insight} |
| Context7/Ref | {avg} | {count} agents | {insight} |
| Pieces | {avg} | {count} agents | {insight} |

### Highest Rated Tools
1. **{Tool Name}** ({rating}/10): {why it worked}
2. **{Tool Name}** ({rating}/10): {why it worked}
3. **{Tool Name}** ({rating}/10): {why it worked}

### Underutilized Tools
- **{Tool Name}**: Could have been used for {use case}

---

## Progressive Learning Analysis

### Project Context
- **Project Sequence**: Project #{project_sequence_number}
- **Previous Project**: {previous_project_name or "None (first project)"}
- **Comparison Period**: Project N vs Project N-1

### Metrics Comparison

**Human Interventions**:
- **Current Project**: {total_human_interventions} interventions
- **Previous Project**: {previous_total_human_interventions or "N/A"}
- **Delta**: {delta} ({trend: "↓ improving" / "↑ regressing" / "→ stable"})
- **Analysis**: {interpretation of trend}

**Questions Asked**:
- **Current Project**: {total_questions_asked} questions
- **Previous Project**: {previous_total_questions or "N/A"}
- **Delta**: {delta} ({trend})
- **Analysis**: {Are agents asking fewer questions as they learn?}

**Decision Autonomy Rate**:
- **Current Project**: {autonomy_rate} ({X% of decisions made autonomously})
- **Previous Project**: {previous_autonomy_rate or "N/A"}
- **Delta**: {delta} ({trend})
- **Analysis**: {Are agents making more decisions autonomously?}

**Learnings Applied**:
- **Current Project**: {total_learnings_applied} learnings from ApeRAG
- **Previous Project**: {previous_learnings_applied or "N/A"}
- **Delta**: {delta} ({trend})
- **Analysis**: {Are agents successfully querying and applying past learnings?}

### Learning Velocity

**Mistakes Repeated**: {mistakes_repeated} (should be 0 if progressive learning works)
- {List any repeated mistakes from Project N-1}

**New Mistakes Made**: {new_mistakes_made}
- {Brief list of new categories of mistakes}

**Learnings Effectiveness**: {learnings_effectiveness_rate} ({X}% of queried learnings were useful)

### Progressive Learning Health Score

**Overall Score**: {score}/10

**Assessment**: {excellent / good_start / needs_improvement / not_learning}

**Evidence of Learning**:
- ✅ {Evidence point 1}
- ✅ {Evidence point 2}
- ✅ {Evidence point 3}

**Concerns**:
- ⚠️ {Concern 1}
- ⚠️ {Concern 2}

### Learning Trends Summary

{2-3 paragraph narrative analyzing whether the system is successfully learning from past projects}

**Key Indicators**:
- Human interventions: {trending down / stable / trending up}
- Questions asked: {trending down / stable / trending up}
- Autonomy rate: {trending up / stable / trending down}
- Learnings applied: {effective / moderate / ineffective}

**Recommendation**: {What should we focus on to improve progressive learning?}

---

## Cross-Agent Patterns

### Pattern 1: {Pattern Name}
- **Observed By**: {agents list}
- **Description**: {what was observed}
- **Impact**: {positive or negative}
- **Recommendation**: {how to leverage or fix}

### Pattern 2: {Pattern Name}
{...same structure...}

{Continue for all identified patterns (≥3)}

---

## Key Takeaways

### ✅ What Worked Well
1. **{Success #1}**: {description, evidence from retrospectives}
2. **{Success #2}**: {description, evidence}
3. **{Success #3}**: {description, evidence}

### ⚠️ What Needs Improvement
1. **{Pain Point #1}**: {description, evidence}
   - **Impact**: {how it affected development}
   - **Recommendation**: {how to fix}
2. **{Pain Point #2}**: {...}
3. **{Pain Point #3}**: {...}

### 🔧 Tool Insights
- **Best Tool Combinations**: {e.g., Sequential Thinking + Vibe Check for spec analysis}
- **Underutilized Tools**: {tools that could have been used more}
- **Tool Gaps**: {capabilities we wish existed}

### 📈 Process Insights
- **Workflow Optimizations**: {e.g., skip Spec Clarifier for simple features}
- **Handoff Improvements**: {e.g., Pieces memories were critical for context}
- **Quality Gate Effectiveness**: {e.g., Alignment Analyzer caught X gaps}

---

## Future Recommendations

### For Next Feature
1. **{Recommendation #1}**: {specific, actionable}
2. **{Recommendation #2}**: {...}
3. **{Recommendation #3}**: {...}

### For Agent System
1. **{System Improvement #1}**: {e.g., enhance Spec Clarifier prompt}
2. **{System Improvement #2}**: {...}

---

**Synthesis Complete**: Ready for `/agent:improve`
```

---

## Pieces Memory Template

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Synthesis Complete: {feature-name}",
  "summary": `
## Synthesis Complete

**Feature**: {feature-name}
**Date**: {date}
**Development Time**: {hours}

### Tool Effectiveness
- **Top Tool**: {tool name} ({rating}/10)
- **Most Used**: {tool name} ({count} agents)

### Key Patterns
- Pattern 1: {pattern description}
- Pattern 2: {pattern description}

### Progressive Learning
- **Score**: {score}/10 ({assessment})
- **Trend**: {improving/stable/regressing}

### Top Recommendations
1. {Recommendation 1}
2. {Recommendation 2}

Ready for: /agent:improve
  `,
  "connected_client": "Claude Code"
})
```

---

## Handoff Message Template

```
Synthesis complete for {feature-name}.

Summary:
- {X} retrospectives analyzed
- {Y} cross-agent patterns identified
- Development time: {hours}

Tool Effectiveness:
- Highest rated: {tool} ({rating}/10)
- Most useful: {insight}

Progressive Learning:
- Health score: {score}/10 ({assessment})
- Trend: {improving/stable/regressing}

Key Takeaways:
- ✅ {What worked}
- ⚠️ {What needs improvement}

Recommendation: {Top recommendation}

synthesis-report.md created. Next: /agent:improve

Handoff complete.
```

---

**See Also**:
- [workflow.md](workflow.md) for synthesis process
- [practices.md](practices.md) for quality checks
