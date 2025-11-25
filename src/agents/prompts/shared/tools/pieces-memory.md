# Pieces Memory - Tool Syntax

**Purpose**: Create long-term memories for handoffs, learnings, and corrections.

## Function Signature

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "{Brief 1-line summary}",
  "summary": "{Detailed markdown content}",
  "connected_client": "Claude Code"
})
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `summary_description` | Yes | Brief 1-line summary (searchable title) |
| `summary` | Yes | Detailed markdown content (full context) |
| `connected_client` | Yes | Always "Claude Code" |
| `files` | Optional | Array of absolute file paths |
| `project` | Optional | Absolute path to project root |
| `externalLinks` | Optional | Array of relevant URLs |

## Common Use Cases

### 1. Agent Handoff
After completing phase, document what was done and pass to next agent.

### 2. Human Correction
After vibe_learn, create searchable memory for Step 0 queries.

### 3. Step 0 Learnings Applied
Document which past learnings were applied to avoid mistakes.

## When to Use

- **End of Phase**: Create handoff memory before passing to next agent
- **After Correction**: Create searchable memory after vibe_learn (Step 3)
- **After Step 0**: Document which learnings were applied

---

**Examples**: [../examples/pieces-handoffs.md](../examples/pieces-handoffs.md), [../examples/pieces-corrections.md](../examples/pieces-corrections.md)
**Templates**: [../templates/pieces-memory-ready.md](../templates/pieces-memory-ready.md)
**Reference**: [../protocols/human-correction.md](../protocols/human-correction.md) - Step 3
