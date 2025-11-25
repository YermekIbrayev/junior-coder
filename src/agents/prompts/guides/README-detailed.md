# Agent Prompt Templates - Shared Resources

**Purpose**: DRY (Don't Repeat Yourself) templates for common agent prompt sections.

**Usage**: Agent prompts reference these templates instead of duplicating content.

---

## Available Templates

### 1. [step-0-query-learnings.md](step-0-query-learnings.md)
**What**: ApeRAG query workflow for applying past learnings
**Used by**: All 11 agents
**Saves**: ~80 lines × 11 = 880 lines of duplication

### 2. [human-correction-protocol.md](human-correction-protocol.md)
**What**: 4-step process for handling human corrections
**Used by**: All 11 agents
**Saves**: ~60 lines × 11 = 660 lines of duplication

### 3. [decision-framework.md](decision-framework.md)
**What**: Templates for CRITICAL vs NON-CRITICAL decision communication
**Used by**: All 11 agents
**Saves**: ~40 lines × 11 = 440 lines of duplication

### 4. [vibe-learn-examples.md](vibe-learn-examples.md)
**What**: Code examples for vibe_learn() tool usage
**Used by**: All 11 agents (in Human Correction Protocol)
**Saves**: ~15 lines × 11 = 165 lines of duplication

### 5. [pieces-memory-examples.md](pieces-memory-examples.md)
**What**: Patterns for creating Pieces memories
**Used by**: All 11 agents (in Human Correction Protocol)
**Saves**: ~20 lines × 11 = 220 lines of duplication

---

## Total Impact

**Lines Eliminated**: ~2,365 lines of duplication
**Files Created**: 6 shared templates (all ≤100 lines)
**Agent Prompts**: Reduced from ~550-775 lines to ~300-400 lines each

---

## Design Principles

1. **Self-Contained**: Each template is understandable on its own
2. **Parameterized**: Uses clear variable placeholders (e.g., `{agent-name}`)
3. **Constitution-Compliant**: All files ≤200 lines (target ≤100)
4. **Maintainable**: Update once, benefit all agents
5. **Readable**: Agent prompts remain clear with summary + link pattern

---

## How to Use

**In Agent Prompts**, replace duplicated sections with:

```markdown
## Section Name

[Brief 2-3 line summary of what this section covers]

**Full Details**: See [template-name.md](shared/template-name.md)
```

**Example**:
```markdown
## Workflow

### Step 0: Query Past Learnings (5 minutes) - **DO THIS FIRST!**

Before starting, query ApeRAG for similar past projects to avoid repeating mistakes.

**Complete Workflow**: See [step-0-query-learnings.md](shared/step-0-query-learnings.md)
```

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-26
