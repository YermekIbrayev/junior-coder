# Quality Guardian - Navigation

**Agent ID**: quality-guardian | **Version**: 3.0.0 (Modular)
**Phase**: Production Ready (TDD REFACTOR + Security + E2E) | **Command**: `/agent:refactor`

---

## Loading Strategy

**Minimal Load** (START HERE):
- [core.md](core.md) - 98 lines
- [../../shared/protocols/step-0.md](../../shared/protocols/step-0.md) - 40 lines
**Total**: 138 lines

**On-Demand Modules**:
- [workflow.md](workflow.md) - Refactoring process, Semgrep execution (145 lines)
- [practices.md](practices.md) - Best practices, common mistakes (95 lines)
- [decisions.md](decisions.md) - Decision framework (85 lines)
- [handoff.md](handoff.md) - Output requirements, certification (90 lines)
- [template-quality-report.md](template-quality-report.md) - Full quality report template (380 lines)

---

## Quick Navigation

**"How do I start?"** → [core.md](core.md) + [../../shared/protocols/step-0.md](../../shared/protocols/step-0.md)

**"What's my refactoring process?"** → [workflow.md](workflow.md)

**"What are best practices?"** → [practices.md](practices.md)

**"How do I make decisions?"** → [decisions.md](decisions.md)

**"How do I hand off?"** → [handoff.md](handoff.md) + [template-quality-report.md](template-quality-report.md)

**"I was corrected by human"** → [../../shared/protocols/human-correction.md](../../shared/protocols/human-correction.md)

**"I need examples"** → [../../shared/examples/](../../shared/examples/)

---

## File Descriptions

| File | Lines | Purpose | Load When |
|------|-------|---------|-----------|
| core.md | 98 | Role, goals, tools, I/O, success criteria | Always (start here) |
| workflow.md | 145 | Refactoring steps, Semgrep execution, E2E testing | During refactoring |
| practices.md | 95 | Best practices, common mistakes, tips | When executing |
| decisions.md | 85 | Critical vs non-critical decision framework | When uncertain |
| handoff.md | 90 | Output structure, certification checklist | At completion |
| template-quality-report.md | 380 | Complete quality report example | When creating report |

---

**Shared Resources**:
- [../../shared/protocols/](../../shared/protocols/) - Step 0, Human Correction, Decisions
- [../../shared/tools/](../../shared/tools/) - vibe_learn, pieces_memory syntax
- [../../shared/examples/](../../shared/examples/) - Real examples by agent
- [../../shared/templates/](../../shared/templates/) - Copy-paste ready templates
