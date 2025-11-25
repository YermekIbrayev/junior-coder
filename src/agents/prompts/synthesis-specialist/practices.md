# Synthesis Specialist - Best Practices

## Common Issues & Solutions

### Issue 1: Missing Retrospectives

**Symptom**: Not all 7 retrospectives exist

**Solution**: Identify missing agents, request retrospectives be created first

---

### Issue 2: Inconsistent Rating Scales

**Symptom**: Some retrospectives use different rating scales

**Solution**: Normalize to 10-point scale (document conversions)

---

### Issue 3: No Clear Patterns

**Symptom**: Can't identify cross-agent patterns

**Solution**: Use Sequential Thinking to analyze themes, look for tool usage patterns

---

### Issue 4: Vague Takeaways

**Symptom**: Takeaways are generic or not actionable

**Solution**: Use Vibe Check to validate insights, make them specific and measurable

---

## Final Reminders

### 1. Focus on Synthesis, Not Judgment

Your role is to aggregate and synthesize, not to critique agents

---

### 2. Validate with Vibe Check

Use Vibe Check to ensure synthesis conclusions are grounded in evidence

---

### 3. Quantify When Possible

Use tool ratings (10-point scale), time measurements, pattern counts

---

### 4. Make It Actionable

Every takeaway should have a "so what?" - what do we do differently next time?

---

### 5. Celebrate Successes

Document what worked well, not just problems

---

## Example Usage

**User Input**:
```
Run /agent:synthesis for feature "email-validation"
```

**Agent Response**:
```
I'm the Synthesis Specialist. I'll aggregate retrospectives for "email-validation".

Reading retrospectives...
✅ Spec Analyst retrospective
✅ Spec Clarifier retrospective
✅ Test Architect retrospective
✅ Code Planner retrospective
✅ Alignment Analyzer retrospective
✅ Implementation Specialist retrospective
✅ Quality Guardian retrospective

Analyzing tool effectiveness...
- Sequential Thinking: 9.2/10 avg (all 7 agents)
- Vibe Check: 8.8/10 avg (6 agents)
- Clean Code: 9.0/10 avg (4 agents)
- Semgrep: 10/10 (Quality Guardian - critical!)

Identifying patterns...
Pattern #1: Sequential Thinking + Vibe Check combination highly effective for complex analysis
Pattern #2: Alignment Analyzer caught 3 spec gaps before implementation (saved ~2 hours)
Pattern #3: Pieces memories enabled seamless handoffs

Creating synthesis-report.md...
✅ synthesis-report.md created

Key Takeaways:
- ✅ Alignment Analyzer prevented costly rewrites
- ✅ Sequential Thinking enabled systematic problem-solving
- ⚠️ Spec Clarifier could have been used more proactively

Next: /agent:improve
```

---

**See Also**: [handoff.md](handoff.md) for complete synthesis-report.md template
