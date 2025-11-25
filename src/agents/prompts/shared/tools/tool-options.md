# Tool Options - Configuration Check

**Purpose**: Template for agents to check and adapt to tool configuration

---

## Configuration Format

Tool options are set in `.agents/config/agents.json`:

```json
{
  "toolOptions": {
    "serena": true/false,
    "pieces": true/false,
    "aperag": true/false
  }
}
```

---

## Agent Behavior Template

### Check Configuration

At the start of your workflow, acknowledge tool configuration:

```markdown
## Tool Configuration (from agents.json)

✅ Serena: {enabled/disabled}
✅ Pieces: {enabled/disabled}
✅ ApeRAG: {enabled/disabled}

{If any disabled: "Adapting workflow based on configuration"}
```

---

## Conditional Workflows

### When Serena Disabled

**Instead of**: `mcp__serena__find_symbol`, `mcp__serena__get_symbols_overview`

**Use**: Basic file operations via Read tool

**Impact**: More token usage, less precise navigation

---

### When Pieces Disabled

**Instead of**: `mcp__Pieces__create_pieces_memory`

**Use**: Document key decisions in notes files

**Impact**: No searchable memory for future agents, must rely on file-based notes

**Example**:
```markdown
## Key Decisions (Pieces memory disabled)

**Decision**: Used service layer pattern
**Rationale**: Encapsulates business logic
**Files**: services/adjustment_service.py
```

---

### When ApeRAG Disabled

**Instead of**: `mcp__aperag-mcp__search_collection`, knowledge graph queries

**Skip**: Knowledge curation workflows

**Impact**: No knowledge graph updates, manual documentation only

---

## Runtime Override Example

User can override configuration in prompt:

```
Tool configuration for this session:
- serena: false (troubleshooting, use Read tool)
- pieces: true (keep memories)
- aperag: true (enabled)
```

**Agent Response**:
```markdown
✅ Acknowledged tool configuration
- Serena: disabled (using basic file operations)
- Pieces: enabled
- ApeRAG: enabled

Proceeding with adapted workflow...
```

---

## Default Behavior

**If toolOptions missing**: Assume all tools enabled (backward compatible)

**If individual key missing**: Assume enabled (fail-safe to full functionality)

---

## References

- [../../config/TOOL-OPTIONS.md](../../config/TOOL-OPTIONS.md) - Complete configuration guide
- [../../config/agents.json](../../config/agents.json) - Configuration file
