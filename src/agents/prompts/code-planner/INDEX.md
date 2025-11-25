# Code Planner - Navigation

**Agent ID**: code-planner | **Version**: 3.0.0 (Modular)
**Phase**: Architecture Design (SOLID) | **Command**: `/agent:plan`

---

## Loading Strategy

**Minimal Load** (START HERE):
- [core.md](core.md) - 95 lines
- [../../shared/protocols/step-0.md](../../shared/protocols/step-0.md) - 40 lines
**Total**: 135 lines

**On-Demand Modules**:
- [workflow.md](workflow.md) - Architecture design process (140 lines)
- [practices.md](practices.md) - SOLID principles, best practices (120 lines)
- [decisions.md](decisions.md) - Decision framework (85 lines)
- [handoff.md](handoff.md) - Output template, success criteria (90 lines)

---

## Quick Navigation

**"How do I start?"** → [core.md](core.md) + [../../shared/protocols/step-0.md](../../shared/protocols/step-0.md)

**"What's my design process?"** → [workflow.md](workflow.md)

**"How do I apply SOLID?"** → [practices.md](practices.md)

**"How do I make decisions?"** → [decisions.md](decisions.md)

**"How do I hand off?"** → [handoff.md](handoff.md)

**"I was corrected by human"** → [../../shared/protocols/human-correction.md](../../shared/protocols/human-correction.md)

---

## File Descriptions

| File | Lines | Purpose | Load When |
|------|-------|---------|-----------|
| core.md | 95 | Role, goals, tools, I/O | Always (start here) |
| workflow.md | 140 | Architecture design steps | During design |
| practices.md | 120 | SOLID principles, patterns | When designing |
| decisions.md | 85 | Critical vs non-critical framework | When uncertain |
| handoff.md | 90 | architecture.md template, success criteria | At completion |

---

**Shared Resources**:
- [../../shared/protocols/](../../shared/protocols/) - Step 0, Human Correction, Decisions
- [../../shared/tools/](../../shared/tools/) - vibe_learn, pieces_memory syntax
- [../../shared/examples/](../../shared/examples/) - Real examples
