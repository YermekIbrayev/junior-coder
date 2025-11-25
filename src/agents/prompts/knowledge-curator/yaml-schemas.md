# Knowledge Curator - YAML Schemas

## Individual Retrospective Schema

```yaml
# {agent-name}-retrospective.yaml
feature_name: "email-validation"
agent_name: "Spec Analyst"
agent_id: "spec-analyst"
execution_date: "2025-10-25"
execution_time_hours: 0.5

tools_used:
  - name: "Sequential Thinking"
    rating: 9
    how_used: "Broke down complex user requirements systematically"
    impact: "Identified 5 edge cases that weren't obvious from initial request"

  - name: "Vibe Check"
    rating: 8
    how_used: "Validated assumptions about email validation standards"
    impact: "Caught assumption that all emails need DNS verification"

  - name: "Context7"
    rating: 9
    how_used: "Researched email validation libraries and standards"
    impact: "Found RFC 5322 spec and industry best practices"

patterns_observed:
  - name: "Sequential Thinking + Vibe Check combination"
    description: "Using both tools together improved requirement thoroughness"
    evidence: "Spec had 0 ambiguities vs typical 2-3"
    replicability: "high"

  - name: "Early Octocode validation"
    description: "Checking production patterns before spec finalization"
    evidence: "Aligned our approach with 15 successful production systems"
    replicability: "high"

what_worked:
  - item: "Sequential Thinking for requirement breakdown"
    rating: 9
    evidence: "Identified 8 requirements from 2-sentence user request"

  - item: "Vibe Check for assumption validation"
    rating: 8
    evidence: "Caught 3 implicit assumptions early"

what_didnt_work:
  - item: "Initial research was too broad"
    rating: 4
    impact: "Spent 10 minutes on irrelevant libraries"
    solution: "Use Octocode for targeted production pattern search first"

lessons_learned:
  - lesson: "Start with Octocode to find proven patterns"
    confidence: "high"
    applicability: "all features"

  - lesson: "Vibe Check should be used proactively, not reactively"
    confidence: "medium"
    applicability: "spec phase"

recommendations:
  - recommendation: "Add Octocode to spec analyst workflow (before Context7)"
    priority: "P0"
    impact: "high"
    effort: "low"

output_artifacts:
  - name: "spec.md"
    location: ".specify/specs/email-validation/spec.md"
    quality_score: 9
    completeness: "100%"

handoff_quality:
  - to_agent: "Spec Clarifier"
    rating: 9
    pieces_memory_created: true
    context_clarity: "high"

progressive_learning_metrics:
  human_interventions:
    corrections_provided: 2
    guidance_requested: 1
    total_interventions: 3

  decision_breakdown:
    critical_decisions_made: 1
    critical_decisions_asked: 1
    non_critical_autonomous: 5
    decision_autonomy_rate: 0.83

  questions_asked:
    clarification_questions: 3
    validation_questions: 1
    total_questions: 4

  past_learnings_applied:
    learnings_queried: 5
    learnings_applied: 3
    learnings_avoided_mistakes: 2

  corrections_captured:
    vibe_learn_entries: 2
    pieces_memories_created: 2
    correction_categories:
      - "Complex Solution Bias"
      - "Misalignment"

metadata:
  constitution_compliant: true
  file_size_limits_met: true
  semgrep_applicable: false
```

---

## Synthesis Report Schema

```yaml
# synthesis-report.yaml
feature_name: "email-validation"
report_type: "synthesis"
generated_date: "2025-10-25"
total_development_time_hours: 3.5

agents_used:
  - agent_id: "spec-analyst"
    execution_time_hours: 0.5
    status: "completed"
    output: "spec.md"

  - agent_id: "spec-clarifier"
    execution_time_hours: 0.2
    status: "completed"
    output: "spec.md (updated)"

  # ... (all 7 agents)

tool_effectiveness:
  - tool_name: "Sequential Thinking"
    average_rating: 9.2
    used_by_agents: ["spec-analyst", "test-architect", "code-planner", "alignment-analyzer", "implementation-specialist", "quality-guardian"]
    top_insight: "Enabled systematic problem-solving across all phases"

  - tool_name: "Vibe Check"
    average_rating: 8.8
    used_by_agents: ["spec-analyst", "test-architect", "code-planner", "alignment-analyzer", "implementation-specialist", "quality-guardian"]
    top_insight: "Caught assumptions early, preventing late-stage rewrites"

  # ... (all tools)

cross_agent_patterns:
  - pattern_name: "Sequential Thinking + Vibe Check combination"
    observed_by_agents: ["spec-analyst", "test-architect", "code-planner"]
    description: "Using both tools together for systematic + assumption-validated analysis"
    impact: "positive"
    replicability: "high"

  # ... (all patterns)

key_takeaways:
  what_worked_well:
    - takeaway: "Alignment Analyzer prevented costly rewrites"
      evidence: "Caught 3 spec gaps before implementation"
      impact: "saved 2 hours"

    # ... (all successes)

  what_needs_improvement:
    - takeaway: "Spec Clarifier could be more proactive"
      evidence: "Generated only 2 questions vs expected 5-7"
      impact: "minor ambiguities remained"

    # ... (all improvements)

recommendations:
  - recommendation: "Enhance Spec Clarifier prompt for more proactive questioning"
    priority: "P1"
    impact: "medium"
    effort: "low"

  # ... (all recommendations)

progressive_learning_aggregated:
  total_human_interventions: 8
  total_corrections_provided: 5
  total_guidance_requested: 3

  decision_autonomy:
    total_critical_decisions: 4
    total_critical_asked_human: 4
    total_autonomous_decisions: 23
    overall_autonomy_rate: 0.85

  questions_summary:
    total_questions_asked: 12
    by_agent:
      - agent: "Spec Analyst"
        questions: 4
      - agent: "Test Architect"
        questions: 2
      # ... (all agents)

  learnings_applied_summary:
    total_learnings_queried: 15
    total_learnings_applied: 8
    total_mistakes_avoided: 5
    learning_effectiveness_rate: 0.53

  corrections_summary:
    total_vibe_learn_entries: 5
    total_pieces_memories: 5
    top_correction_categories:
      - category: "Complex Solution Bias"
        count: 2
      - category: "Misalignment"
        count: 1

  comparison_to_project_n_minus_1:
    previous_project: null
    human_interventions_delta: null
    questions_asked_delta: null
    autonomy_rate_delta: null
```

---

## System Improvements Schema

```yaml
# system-improvements.yaml
feature_name: "email-validation"
report_type: "system-improvements"
generated_date: "2025-10-25"
based_on: "synthesis-report.md"

correlations:
  - type: "tool_usage_to_quality"
    correlation: "Sequential Thinking usage correlated with 0 alignment gaps"
    evidence: "Features using Sequential Thinking had 40% fewer gaps"
    confidence: "high"
    validation: "Vibe Check + Octocode confirmed"

  - type: "workflow_step_to_speed"
    correlation: "Alignment Analyzer ROI was 13x"
    evidence: "15min investment prevented 2hrs of rework"
    confidence: "high"
    validation: "Quantitative data from timeline"

  # ... (all correlations)

system_optimizations:
  workflow_optimizations:
    - name: "Skip Spec Clarifier for simple features"
      current_state: "All features go through Spec Clarifier"
      proposed_change: "Skip for features with <5 requirements"
      expected_benefit: "Save 10 minutes per simple feature"
      validation: "Vibe Check + Octocode validated"
      implementation: "Add conditional logic to workflow docs"
      priority: "P2"

  tool_enhancements:
    - name: "Add Octocode to Spec Analyst"
      current_state: "Spec Analyst uses Context7/Ref first"
      proposed_change: "Use Octocode before Context7"
      expected_benefit: "Align with proven patterns earlier"
      validation: "Octocode shows top teams do this"
      implementation: "Update spec-analyst.md prompt"
      priority: "P1"

  agent_refinements:
    - name: "Enhance Quality Guardian with pre-flight checklist"
      current_issue: "Semgrep findings sometimes miss context"
      proposed_solution: "Add pre-flight security checklist"
      expected_benefit: "Catch common issues before scan"
      validation: "Vibe Check confirmed"
      implementation: "Update quality-guardian.md prompt"
      priority: "P0"

prioritized_recommendations:
  p0_high_impact_low_effort:
    - recommendation: "Add pre-flight checklist to Quality Guardian"
      impact: "high"
      effort: "low"
      action: "Update quality-guardian.md prompt"
      owner: "System Admin"

  p1_high_impact_medium_effort:
    - recommendation: "Add Octocode to Spec Analyst"
      impact: "high"
      effort: "medium"
      action: "Update spec-analyst.md and tool matrix"
      owner: "System Admin"

  # ... (all prioritized recommendations)

implementation_plan:
  immediate_next_feature:
    - action: "Add pre-flight checklist to Quality Guardian"
      status: "pending"

  short_term_2_3_features:
    - action: "Add Octocode to Spec Analyst"
      status: "pending"

  # ... (all implementation steps)

progressive_learning_tracking:
  project_sequence_number: 1
  previous_project_name: null

  metrics_trend:
    human_interventions:
      current: 8
      previous: null
      delta: null
      trend: null

    questions_asked:
      current: 12
      previous: null
      delta: null
      trend: null

    autonomy_rate:
      current: 0.85
      previous: null
      delta: null
      trend: null

  learning_velocity:
    mistakes_repeated: 0
    new_mistakes_made: 5
    learnings_effectiveness: 0.53

  progressive_learning_health:
    score: 7.5
    assessment: "good_start"
    evidence:
      - "All agents using Step 0"
      - "Human corrections being captured"
      - "85% autonomy rate is healthy"
    concerns:
      - "First project, no trend data yet"
```

---

## Conversion Tips

**Preserve All Data**:
- All 1-10 ratings must be preserved
- All text evidence and descriptions
- All metadata (dates, times, priorities)

**Structure Matters**:
- Follow indentation strictly (2 spaces)
- Use arrays `[]` for lists
- Use objects `{}` for nested data
- Quote strings with special characters

**Validate YAML**:
- Check syntax before saving
- Ensure all required fields present
- Verify nested structure matches schema
