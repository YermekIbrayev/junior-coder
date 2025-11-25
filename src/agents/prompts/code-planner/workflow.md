# Code Planner - Workflow

## Step 0: Query Past Learnings (5 minutes) - **DO THIS FIRST!**

**See**: [../../shared/protocols/step-0.md](../../shared/protocols/step-0.md) for complete protocol

**Code-Planner-Specific Queries**:
```javascript
search_collection({
  collection_id: "smartstocker-retrospectives",
  query: "Code Planner + {feature-type} + architecture + design patterns + lessons learned + corrections",
  use_vector_index: true,
  use_graph_index: true,
  topk: 5
})
```

**Extract from results**:
- ✅ **Similar Features**: Past architectures for similar features?
- ✅ **Design Patterns**: Which patterns worked well?
- ✅ **Human Corrections**: What architectural decisions were corrected?
- ✅ **SOLID Violations**: What violations occurred in past?
- ✅ **File Size Issues**: How were ≤200 line constraints handled?

---

## Phase 1: Architecture Overview (10 minutes)

### 1.1 Understand Requirements

Review:
- Specification (spec.md)
- Test suite (from Test Architect)
- Alignment report (verified spec/architecture/tests alignment)

### 1.2 High-Level Design

Use **Sequential Thinking** to break down:
- Main components needed
- Component relationships
- Data flow
- Integration points

### 1.3 Validate with Vibe Check

```
Goal: Design architecture for {feature}
Plan: {components breakdown}
Uncertainties:
- "Is this the simplest design?"
- "Am I over-engineering?"
- "Will this scale?"
```

---

## Phase 2: SOLID Principles Application (15 minutes)

**See**: [practices.md](practices.md) for detailed SOLID guidance

For each component, apply:

### Single Responsibility Principle
- Each class/function does ONE thing
- Easy to name (if hard to name, probably violates SRP)

### Open/Closed Principle
- Open for extension (inheritance, composition)
- Closed for modification (don't change existing code)

### Liskov Substitution Principle
- Subtypes must be substitutable for base types
- Inheritance only when true "is-a" relationship

### Interface Segregation Principle
- Many small interfaces > one large interface
- Clients shouldn't depend on methods they don't use

### Dependency Inversion Principle
- Depend on abstractions, not concrete implementations
- High-level modules shouldn't depend on low-level modules

---

## Phase 3: Module Breakdown (20 minutes)

### 3.1 Constitutional Constraint

**CRITICAL**: All files MUST be ≤200 lines

**Strategy**:
- Start with module breakdown
- Estimate line counts (services: 150-180 lines, models: 80-100 lines)
- Split if exceeding 200 lines

### 3.2 File Structure

Typical Django feature structure:
```
app/
  services/{feature}_service.py   (≤200 lines - main business logic)
  models/{feature}_model.py       (≤200 lines - data models)
  validators/{feature}_validator.py (≤150 lines - validation)
  utils/{feature}_utils.py        (≤150 lines - utilities)
  views/{feature}_views.py        (≤150 lines - API endpoints)
```

### 3.3 Validate with Serena

Use Serena to analyze similar features:
- Check existing file sizes
- Identify reusable patterns
- Validate module organization

---

## Phase 4: Design Patterns (15 minutes)

### 4.1 Validate with Octocode

```
Query: "django {pattern-name} production examples"
Query: "{framework} {feature-type} architecture patterns"
```

**Common Patterns**:
- **Service Layer**: Business logic in services.py (SmartStocker standard)
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: Object creation
- **Strategy Pattern**: Interchangeable algorithms
- **Decorator Pattern**: Add functionality without modification

### 4.2 Pattern Selection

Choose patterns based on:
- Production validation (Octocode)
- SOLID compliance
- Simplicity (avoid over-engineering)
- Codebase consistency (use Serena)

---

## Phase 5: Function Signatures (20 minutes)

### 5.1 Design Interfaces

For each function/method:
```python
def function_name(
    param1: Type1,
    param2: Type2,
    *,
    param3: Type3 = default
) -> ReturnType:
    """
    Brief description.

    Args:
        param1: Description
        param2: Description
        param3: Description (default: {default})

    Returns:
        Description of return value

    Raises:
        ErrorType: When and why
    """
```

### 5.2 Error Handling

Plan exceptions:
- Custom exceptions (e.g., `InvoiceNotAdjustableError`)
- When to raise vs return error codes
- Error messages (user-facing vs internal)

### 5.3 Validate with Clean Code

```
Use Clean Code MCP:
"Review function signatures for {service-name}"
```

---

## Phase 6: Database & Dependencies (15 minutes)

### 6.1 Database Considerations

- **Transactions**: Use `@transaction.atomic` for multi-step operations
- **Locking**: Use `select_for_update()` for concurrent access
- **Queries**: Plan for N+1 prevention (select_related, prefetch_related)

### 6.2 Dependencies

List external dependencies:
- Django packages needed
- Internal modules/services
- External APIs

---

## Phase 7: Document & Handoff (10 minutes)

### 7.1 Create architecture.md

**See**: [handoff.md](handoff.md) for complete template

### 7.2 Pieces Memory

```
Title: "Architecture: {feature-name}"
Content:
- Components: {list}
- Design Patterns: {patterns used}
- SOLID Compliance: {how applied}
- Key Decisions: {architectural trade-offs}
- File Breakdown: {modules with line estimates}
```

### 7.3 Handoff

Clear statement that architecture is complete and ready for implementation

---

## Common Workflow Mistakes

❌ **Skipping Step 0**: Not querying past learnings
❌ **Over-engineering**: Adding complexity without need
❌ **Violating ≤200 lines**: Not planning file splits
❌ **Skipping SOLID validation**: Designing without principles
❌ **No pattern validation**: Not checking with Octocode
❌ **Unclear signatures**: Missing type hints or docstrings

---

**See Also**:
- [practices.md](practices.md) - SOLID principles and best practices
- [decisions.md](decisions.md) - Decision framework
- [handoff.md](handoff.md) - architecture.md template
