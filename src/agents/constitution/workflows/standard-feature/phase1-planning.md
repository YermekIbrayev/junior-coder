# Phase 1: Planning & Specification

**Part of**: [Standard Feature Workflow](../standard-feature.md)

**Purpose**: Define requirements and validate approach before coding.

---

## Steps

**1. Specify** - Create feature spec
- Use `/speckit.specify`
- Define [required elements](../../principles/03-spec-driven.md#required-specification-elements)
- See [Principle III](../../principles/03-spec-driven.md)

**2. Clarify** - Identify gaps
- Use `/speckit.clarify`
- Address ambiguities
- Iterate until clear

**2.5. Explore** - Use Serena MCP for semantic code navigation
- Get symbols overview of related files
- Find existing patterns and references
- Token-efficient exploration (avoid reading entire files)

**3. Plan** - Create execution plan
- Create `.plans/` based on [complexity](../../principles/04-planning.md#graduated-planning-levels)
- Trivial: no plan needed
- Simple: 1 file
- Moderate: 2 files
- Complex: 4 files

**4. Validate** - Vibe-Check approach
- Use Vibe-Check MCP
- Catch assumptions
- Validate soundness

---

## Prerequisites

- Feature request or requirement identified

---

## Deliverables

- ✅ Specification created and clarified
- ✅ Execution plan (if needed)
- ✅ Approach validated
- ✅ Ready to write tests

---

**Next Phase**: [Phase 2: Implementation & Testing](phase2-implementation.md)

**See Also**:
- [Principle III: Specification-Driven](../../principles/03-spec-driven.md)
- [Principle IV: Planning](../../principles/04-planning.md)
- [Vibe-Check MCP](../../references/mcp-servers-ref.md)
- [Serena MCP](../../../../docs/mcp/code-navigation.md)
