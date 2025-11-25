# Phase 4: Review & Completion

**Part of**: [Standard Feature Workflow](../standard-feature.md)

**Purpose**: Finalize changes and verify consistency.

---

## Steps

**14. Commit** - Use GitHub MCP
- Only after all gates pass
- Follow [commit message format](../../cicd.md#commit-message-format)
- Include spec/plan references if applicable

**15. Create PR** - Submit for review
- Via GitHub MCP
- Clear description
- Link to spec/plan

**16. Code Review** - Peer review
- Per [team size requirements](../../team-adaptations.md)
- Solo: Self-review + Vibe-Check
- Small: 1 approver
- Large: 2+ approvers

**17. Analyze** - Consistency check
- Use `/speckit.analyze`
- Verify cross-artifact consistency
- Ensure spec matches implementation

---

## Prerequisites

- Quality-validated code from Phase 3

---

## Deliverables

- ✅ Code committed to repository
- ✅ PR created and reviewed
- ✅ Spec-kit analysis passed
- ✅ Feature complete

---

**Previous Phase**: [Phase 3: Validation & Documentation](phase3-validation.md)

**See Also**:
- [GitHub MCP](../../references/mcp-servers-ref.md)
- [CI/CD & Automation](../../cicd.md)
- [Team Adaptations](../../team-adaptations.md)
- [Governance](../../governance.md)
