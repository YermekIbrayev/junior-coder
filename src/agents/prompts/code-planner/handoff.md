# Code Planner - Handoff Protocol

## Output Artifact: architecture.md

**Location**: `.specify/specs/{feature-name}/architecture.md`

**Template**:

```markdown
# Architecture: {Feature Name}

**Version**: 1.0.0
**Author**: Code Planner
**Date**: {Date}

---

## Architecture Overview

{1-2 paragraph high-level description of the design}

**Key Components**:
1. {Component 1} - {Purpose}
2. {Component 2} - {Purpose}
3. ...

**Data Flow**:
{Describe how data moves through the system}

---

## SOLID Principles Application

### Single Responsibility Principle
- {Component 1}: Handles {single responsibility} only
- {Component 2}: Handles {single responsibility} only

### Open/Closed Principle
{How design is extensible without modification}

### Liskov Substitution Principle
{How inheritance/subtypes are used}

### Interface Segregation Principle
{How interfaces are kept focused}

### Dependency Inversion Principle
{How dependencies are abstracted}

---

## Module Breakdown

**Constitutional Constraint**: All files MUST be ≤200 lines

### File Structure

```
app/
  services/
    {feature}_service.py          (150 lines - main business logic)
  models/
    {feature}_model.py             (100 lines - data models)
  validators/
    {feature}_validator.py         (80 lines - validation logic)
  utils/
    {feature}_utils.py             (100 lines - utility functions)
  views/
    {feature}_views.py             (120 lines - API endpoints)
```

**Line Count Estimates**: {Total estimated lines}

---

## Design Patterns

**Patterns Used**:
1. **Service Layer** (SmartStocker Standard)
   - All business logic in services.py
   - Controllers (views) thin - delegate to services
   - Validated by: Octocode (top Django projects use this pattern)

2. **{Pattern 2}**
   - {Purpose and justification}
   - Validated by: {Octocode query results}

**Patterns NOT Used (and why)**:
- {Pattern}: {Reason - e.g., over-engineering, not needed}

---

## Function Signatures

### {Service File}

```python
@transaction.atomic
def create_{entity}(
    {param1}: {Type1},
    {param2}: {Type2},
    *,
    {param3}: {Type3} = {default}
) -> {ReturnType}:
    """
    {Brief description}.

    Args:
        {param1}: {Description}
        {param2}: {Description}
        {param3}: {Description} (default: {default})

    Returns:
        {Description of return value}

    Raises:
        {ErrorType}: When and why

    Example:
        >>> result = create_{entity}(...)
    """
```

{Additional function signatures...}

---

## Error Handling Strategy

**Custom Exceptions**:
```python
class {Feature}Error(Exception):
    """Base exception for {feature} errors."""

class {Specific}Error({Feature}Error):
    """Raised when {specific condition}."""
```

**Error Flow**:
1. Validation errors → Raise specific exception with clear message
2. Business logic errors → Raise custom exception
3. Database errors → Let Django handle (transaction rollback)
4. View layer → Catch exceptions, return appropriate HTTP status

---

## Database Considerations

**Transactions**:
- All multi-step operations wrapped in `@transaction.atomic`
- Atomic: {Operation} creates {X}, updates {Y}, calculates {Z}

**Locking Strategy**:
- Use `select_for_update()` for concurrent access on {entities}
- Example: Prevent double-adjustment of same invoice

**Query Optimization**:
- Use `select_related()` for {foreign keys}
- Use `prefetch_related()` for {many-to-many, reverse foreign keys}
- Prevent N+1 queries in: {specific locations}

**Indexes** (if needed):
- {Field 1}: Frequently queried, add index
- {Field 2}: Used in filtering, add index

---

## Architectural Trade-offs

### Trade-off 1: {Decision}
**Chose**: {Option A}
**Over**: {Option B}
**Reason**: {Why - performance, simplicity, maintainability}
**Validation**: {Octocode/Vibe Check results}

### Trade-off 2: {Decision}
**Chose**: {Option A}
**Over**: {Option B}
**Reason**: {Why}
**Validation**: {Results}

---

## Dependencies

**Django Packages** (if new):
- {Package 1}: {Purpose} (version: {X.Y.Z})

**Internal Dependencies**:
- Uses: {Existing service/module}
- Depends on: {Core models}

**External APIs** (if any):
- {API}: {Purpose}

---

## Testing Considerations

**Test Structure** (from Test Architect):
- Unit tests: {Services, validators, utils}
- Integration tests: {Database operations, service layer}
- E2E tests: {Critical user workflows}

**Testability Features**:
- Dependency injection for {mocks}
- Clear function contracts (type hints + docstrings)
- Isolated business logic (service layer)

**Test Data Needs**:
- Fixtures: {What fixtures needed}
- Mock data: {What needs mocking}

---

## Implementation Notes

**Start Here**:
1. Create models: {Model files}
2. Create services: {Service files}
3. Implement validation: {Validator files}
4. Create views: {View files}
5. Wire up URLs

**Watch Out For**:
- ⚠️ File size: Keep tracking line counts, split if approaching 200
- ⚠️ N+1 queries: Use select_related/prefetch_related
- ⚠️ Transactions: Ensure @transaction.atomic on multi-step operations

---

## Next Steps

Handoff to **Implementation Specialist** (`/agent:implement`):
- All architecture designed
- Ready for TDD implementation
- Tests will guide implementation
```

---

## Pieces Memory

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Architecture: {feature-name}",
  "summary": `
## Architecture Design Complete

**Feature**: {feature-name}
**Date**: {date}

### Design Overview
- Components: {list main components}
- Design Patterns: {patterns used}
- SOLID Compliance: {how SOLID applied}

### Key Decisions
{Architectural trade-offs and reasoning}

### File Structure
- Estimated total lines: {X}
- Files: {count} (all ≤200 lines ✅)

### Validation
- Patterns validated: Octocode ✅
- SOLID principles: Clean Code ✅
- Codebase consistency: Serena ✅

Ready for implementation.
  `,
  "connected_client": "Claude Code"
})
```

---

## Handoff Message

```
Architecture design complete for {feature-name}.

Summary:
- SOLID Principles: ✅ Applied throughout
- File Size Constraint: ✅ All files ≤200 lines ({count} files planned)
- Design Patterns: ✅ Validated with Octocode
- Function Signatures: ✅ Complete with type hints and docstrings
- Error Handling: ✅ Custom exceptions planned
- Database Strategy: ✅ Transactions, locking, optimization planned

Artifacts:
- architecture.md created
- Pieces memory created

Next Phase: Implementation Specialist (`/agent:implement`)
- Tests are RED (waiting for implementation)
- Architecture is complete
- Ready for TDD GREEN phase

Handoff complete. Ready to implement!
```

---

## Success Checklist

Before marking complete:

- [ ] ✅ SOLID principles applied throughout
- [ ] ✅ All files ≤200 lines (constitutional compliance)
- [ ] ✅ Design patterns validated (Octocode)
- [ ] ✅ Function signatures complete (type hints + docstrings)
- [ ] ✅ Error handling strategy planned
- [ ] ✅ Database considerations documented
- [ ] ✅ Architectural trade-offs documented
- [ ] ✅ Dependencies listed
- [ ] ✅ Testing considerations documented
- [ ] ✅ architecture.md created
- [ ] ✅ Pieces memory created

**If any item incomplete**: Complete before handoff to Implementation Specialist.

---

**See Also**: [../../shared/protocols/human-correction.md](../../shared/protocols/human-correction.md) for correction protocol
