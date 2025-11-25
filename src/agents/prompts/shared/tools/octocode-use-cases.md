# Octocode - GitHub Code Search Use Cases

**Version**: 1.0.0 | **Last Updated**: 2025-10-27

Learn from millions of repositories before writing code. Find architecture patterns, implementation strategies, and edge cases from production systems.

---

## What is Octocode?

**Octocode** is a GitHub MCP server that lets you search, explore, and read code from public repositories to inform your design and implementation decisions.

**Philosophy**: Don't guess—research how successful projects solve similar problems.

---

## Available Tools

### 1. githubSearchRepositories
**Purpose**: Find repositories by keywords, topics, or filters

**Best For**: Discovering projects similar to your feature

**Example**:
```javascript
mcp__octocode__githubSearchRepositories({
  queries: [{
    researchGoal: "Find Django warehouse management systems",
    topicsToSearch: ["django", "inventory", "warehouse"],
    stars: ">100",
    limit: 5
  }]
})
```

---

### 2. githubViewRepoStructure
**Purpose**: Explore folder/file structure of a repository

**Best For**: Understanding project organization and architecture

**Example**:
```javascript
mcp__octocode__githubViewRepoStructure({
  queries: [{
    owner: "django",
    repo: "django",
    branch: "main",
    path: "django/db",
    depth: 2
  }]
})
```

---

### 3. githubSearchCode
**Purpose**: Search code by patterns, language, or specific symbols

**Best For**: Finding specific implementation patterns

**Example**:
```javascript
mcp__octocode__githubSearchCode({
  queries: [{
    keywordsToSearch: ["select_for_update", "transaction.atomic"],
    extension: "py",
    match: "file",
    limit: 10
  }]
})
```

---

### 4. githubGetFileContent
**Purpose**: Read file contents from a repository

**Best For**: Studying implementation details

**Example**:
```javascript
mcp__octocode__githubGetFileContent({
  queries: [{
    owner: "django",
    repo: "django",
    path: "django/db/transaction.py",
    startLine: 100,
    endLine: 150
  }]
})
```

---

## Use Cases by Agent

### Spec Analyst (Research Phase)

**When**: Researching industry patterns before writing spec

**Use Cases**:
- Find how successful projects define similar features
- Research industry-standard workflows
- Validate requirements against real implementations

**Example Query**:
```
"How do warehouse systems handle invoice approval workflows?"
→ Search repos with topics: ["invoice", "approval", "workflow"]
→ Find state machine patterns
```

---

### Spec Clarifier (Validation Phase)

**When**: Resolving ambiguities and generating question options

**Use Cases**:
- **Generate Recommended Options**: Find how most projects solve ambiguity
- Discover edge cases from real code
- Validate assumptions with working examples

**Example Query**:
```
Ambiguity: "Should adjustments modify original invoice or create separate document?"
→ Search: "invoice adjustment" + "credit note"
→ Find: 80% use separate documents
→ Recommend: Option C) Create separate adjustment document ⭐
```

**CRITICAL**: Always use Octocode to inform the **recommended option** when asking clarifying questions.

---

### Code Planner (Architecture Phase)

**When**: Designing system architecture and interfaces

**Use Cases**:
- Research Django service layer patterns
- Find React TypeScript component patterns
- Study state machine implementations
- Explore RBAC (Role-Based Access Control) patterns
- Find database transaction patterns

**Example Query**:
```
"How do Django projects structure service layers?"
→ Search code: "class.*Service" in Python files
→ Review patterns for transaction handling
→ Adopt best practices in plan.md
```

---

### Implementation Specialist (Coding Phase)

**When**: Writing code and need specific implementation patterns

**Use Cases**:
- Find library usage examples
- Research error handling approaches
- Study input validation patterns
- Explore testing strategies

**Example Query**:
```
"How to use select_for_update() with F() expressions?"
→ Search: "select_for_update F(" extension:py
→ Find working examples
→ Apply pattern to implementation
```

---

### Test Architect (Testing Phase)

**When**: Designing test strategy and writing tests

**Use Cases**:
- Find service layer test patterns
- Research React Testing Library best practices
- Study integration test approaches
- Explore mock/fixture strategies

**Example Query**:
```
"How do projects test Django services with transactions?"
→ Search: "TestCase" + "transaction.atomic" + "service"
→ Review test isolation patterns
→ Design test strategy
```

---

## Query Best Practices

### 1. Start Broad, Then Narrow
```
Step 1: Search repositories by topic
Step 2: View repository structure
Step 3: Search code within repo
Step 4: Read specific files
```

### 2. Use Filters Effectively
- **stars: ">1000"** → Well-maintained projects
- **updated: ">=2024-01-01"** → Active development
- **extension: "py"** → Language-specific
- **match: "file"** → Search in content vs. path

### 3. Research Before Recommending
For Spec Clarifier questions, ALWAYS research with Octocode BEFORE recommending an option:
```
1. Identify ambiguity
2. Query Octocode for how others solved it
3. Analyze top 3-5 examples
4. Formulate recommended option based on majority pattern
5. Explain "why recommended" with evidence
```

---

## Integration with .agents Workflow

All agents can use Octocode, but these are primary users:

| Agent | Primary Use | Frequency |
|-------|-------------|-----------|
| Spec Analyst | Feature research | Every spec |
| Spec Clarifier | **Option recommendations** | Every question |
| Code Planner | Architecture patterns | Every plan |
| Implementation Specialist | Implementation examples | As needed |
| Test Architect | Test patterns | Every test strategy |

---

## Example: Full Clarification Flow with Octocode

**Ambiguity**: "What happens if inventory has already been shipped when adjustment is created?"

**Octocode Research**:
```javascript
githubSearchCode({
  keywordsToSearch: ["inventory", "shipped", "adjustment"],
  extension: "py"
})
```

**Findings**: 3 common patterns found:
- 70% prevent adjustment if shipped
- 20% allow with warning flag
- 10% create reverse shipment

**Question Presented**:
```
**Question 1 of 3** (Priority: HIGH)

What should happen if an invoice adjustment is attempted after inventory has been shipped?

**Please choose one:**
A) Block the adjustment entirely (prevent data inconsistency)
B) Allow adjustment but flag for manual reconciliation
C) Prevent adjustment and require reverse shipment process ⭐ **Recommended**
D) Other (please specify)

**Why C is recommended:** 70% of warehouse systems (Django-based) prevent
adjustments post-shipment and require explicit reverse shipment workflows for
auditability. Found in: django-warehouse, inventory-pro, stock-manager.
```

---

## References

- Octocode MCP: `npx octocode-mcp@latest`
- GitHub Code Search Syntax: https://docs.github.com/en/search-github/searching-on-github
- SmartStocker Constitution: `/.specify/templates/constitution/INDEX.md`

---

**Next Steps**: Use Octocode in [spec-clarifier workflow](../../agents/spec-clarifier/workflow.md)
