# Principle I: MCP-First Architecture

**Version**: 3.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [MCP Servers Reference](../references/mcp-servers-ref.md)

---

## Guideline

Leverage MCP servers when they provide clear advantages.

---

## When to Use MCP Servers

Use MCP servers when they provide advantages in **priority order**:

### 1. Accuracy/Reliability
- Produces correct, consistent results
- Reduces human error
- Example: Semgrep MCP for security scanning vs manual review

### 2. Auditability
- Creates traceable record of actions and decisions
- Enables replay and verification
- Example: GitHub MCP for commits (traceable history)

### 3. Learning Value
- Documents process for future reference
- Builds organizational knowledge
- Example: Pieces MCP for capturing solutions

### 4. Efficiency
- Reasonably performant (<10x slower than alternative)
- Time savings justify the overhead
- Example: Exa AI MCP for code search vs manual searching

---

## When to Use Traditional Methods

Use traditional methods if MCP server is:

**Unavailable or Experiencing Issues**
- Server down or unresponsive
- Network connectivity problems
- Fallback to local tools

**Significantly Slower (>10x)**
- For time-critical operations
- When latency is unacceptable
- Example: Simple file operations via local tools

**Not Suited for the Task**
- Task doesn't benefit from MCP features
- Traditional method is simpler
- Example: Quick file edits with local editor

---

## Available MCP Servers

Complete list: [MCP Servers Reference](../references/mcp-servers-ref.md)

**Development & Planning:**
- Sequential Thinking, Clean Code, Vibe-Check

**Code Search & Documentation:**
- Serena, Exa AI, Context7, GitHub

**Quality & Security:**
- Semgrep, IDE

**Testing:**
- Chrome DevTools, IDE

**Knowledge Management:**
- Pieces, Vibe-Check

**Git Operations:**
- GitHub

---

## MCP Integration in Workflows

**Feature Development:**
1. Vibe-Check → Validate approach
2. Serena → Explore codebase (token-efficient)
3. Sequential Thinking → Break down complexity
4. Clean Code → Plan architecture
5. Serena → Navigate symbols during implementation
6. IDE → Check diagnostics
7. Semgrep → Security scan
8. Pieces → Save learnings
9. GitHub → Commit and PR

**Bug Investigation:**
1. Pieces → Query similar issues
2. Serena → Find affected symbols and references
3. Exa AI → Find solutions
4. Context7 → Check library docs
5. Sequential Thinking → Debug
6. Pieces → Save fix

**Research/Spike:**
1. Serena → Explore existing code structure
2. Exa AI → Code examples
3. Context7 → Official docs
4. GitHub → Examine source
5. Vibe-Check → Validate findings
6. Pieces → Document results

---

## Decision Matrix

| Situation | Use MCP? | Why |
|-----------|----------|-----|
| Security scanning | ✅ Yes | Accuracy, auditability, consistency |
| Semantic code navigation | ✅ Yes | Serena: Token-efficient, precise symbol finding |
| Code search for patterns | ✅ Yes | Efficiency, finds examples faster |
| Reading entire files | ❌ No | Use Serena for symbols first, then read if needed |
| Simple file read | ❌ No | Local tools faster, no added value |
| Complex problem solving | ✅ Yes | Sequential Thinking provides structure |
| Git commit | ✅ Yes | GitHub MCP provides auditability |
| Quick config edit | ❌ No | Local editor more efficient |

---

**See Also**:
- [MCP Servers Reference](../references/mcp-servers-ref.md) - Complete server list
- [Standard Feature Workflow](../workflows/standard-feature.md) - MCP integration examples
- [Research/Investigation Flow](../workflows/research.md) - MCP for research
