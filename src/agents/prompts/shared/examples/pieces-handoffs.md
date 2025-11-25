# Pieces Memory Examples - Agent Handoffs

**Purpose**: Full Pieces memory examples for agent-to-agent handoffs.

## Spec Analyst → Test Architect

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Feature: invoice-adjustment - Spec Complete",
  "summary": `
# Feature: invoice-adjustment - Specification Complete

## Requirements Defined
- R1: Create separate AdjustmentInvoice model (preserve immutability)
- R2: Link to original invoice via foreign key
- R3: Support debit/credit adjustments
- R4: Require approval workflow (draft → submitted → approved)
- Total: 4 functional requirements

## Edge Cases Identified
- EC1: Adjustment to already-adjusted invoice (chain)
- EC2: Concurrent adjustments to same invoice
- EC3: Adjustment amount exceeds original invoice
- Total: 3 edge cases requiring test coverage

## Assumptions Made
- A1: Adjustments cannot be modified after approval (immutable)
- A2: Original invoice remains unchanged
- A3: Business logic in service layer (not views)

## Research Performed
- Reviewed: docs/architecture/immutability-patterns.md
- Confirmed: Transaction isolation required (select_for_update)
- Pattern: Similar to inventory StockMovement (append-only)

## Ready For
Test Architect: Design test strategy (TDD, ≥80% coverage)
  `,
  "connected_client": "Claude Code"
})
```

## Test Architect → Code Planner

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Feature: invoice-adjustment - Tests Designed",
  "summary": `
# Feature: invoice-adjustment - Test Design Complete

## Test Strategy
Split: TDD (unit/service) + E2E (critical path only)

## Tests Designed
- Unit: 8 tests (model validation, state transitions)
- Service: 5 tests (business logic, transactions, concurrency)
- E2E: 2 tests (create adjustment flow, approval workflow)
- Total: 15 tests, all currently FAILING (RED phase)

## Patterns Applied
- FactoryBoy for test data
- Transactions with select_for_update for concurrency
- pytest fixtures for common setup

## Coverage Target
≥80% (constitution requirement)

## Ready For
Code Planner: Design architecture to pass these tests
  `,
  "connected_client": "Claude Code"
})
```

## Code Planner → Implementation Specialist

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Feature: invoice-adjustment - Architecture Complete",
  "summary": `
# Feature: invoice-adjustment - Architecture Validated

## Modules Designed
1. models.py: AdjustmentInvoice (links to Invoice, state machine)
2. services.py: create_adjustment(), approve_adjustment() (with transactions)
3. serializers.py: AdjustmentInvoiceSerializer
4. views.py: AdjustmentInvoiceViewSet (minimal, delegates to service)

## Patterns Applied
- Service layer pattern (business logic in services.py)
- Transaction boundary (@transaction.atomic, select_for_update)
- State machine (draft → submitted → approved)
- Immutability (no modifications after approval)

## Alignment Validated
✅ Matches: docs/architecture/service-layer-pattern.md
✅ Matches: docs/architecture/immutability-patterns.md
✅ Constitution compliant (Principle III: Immutable Architecture)

## Ready For
Implementation Specialist: TDD implementation (15 tests → GREEN)
  `,
  "connected_client": "Claude Code"
})
```

## Implementation Specialist → Quality Guardian

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Feature: invoice-adjustment - Implementation Complete",
  "summary": `
# Feature: invoice-adjustment - Implementation Complete

## Tests Status
✅ 15/15 passing (100%)
- Unit: 8/8 passing
- Service: 5/5 passing
- E2E: 2/2 passing

## Coverage
88% (≥80% ✅)

## TDD Iterations
12 red-green cycles completed

## Patterns Applied
- Service layer: Business logic in services.py
- Transactions: @transaction.atomic + select_for_update
- FactoryBoy: Test data generation
- State machine: Explicit state transitions

## Ready For
Quality Guardian: Refactor + Security scan + E2E validation
  `,
  "connected_client": "Claude Code"
})
```

## Quality Guardian → DONE

```javascript
mcp__Pieces__create_pieces_memory({
  "summary_description": "Feature: invoice-adjustment - Production Certified ✅",
  "summary": `
# Feature: invoice-adjustment - PRODUCTION READY ✅

## Status
✅ READY FOR PRODUCTION

## Refactoring Complete
- Extracted magic numbers to constants
- Improved variable naming (invoice_to_adjust → original_invoice)
- Added docstrings to service functions
- No structural changes needed (code was already clean)

## Security Validation
✅ Semgrep: 0 critical/high issues
✅ Manual review: RBAC enforcement verified
✅ Transaction safety: Concurrent access handled

## E2E Validation
✅ Critical path tested: 2/2 E2E tests passing
✅ Manual verification: Adjustment workflow complete

## Performance
✅ Grade A (no N+1 queries, select_related used)

## Feature Complete
All checkpoints passed. Ready for merge.
  `,
  "connected_client": "Claude Code"
})
```

---

**See Also**: [pieces-corrections.md](pieces-corrections.md) - Human correction memories
**Tool Syntax**: [../tools/pieces-memory.md](../tools/pieces-memory.md)
**Templates**: [../templates/pieces-memory-ready.md](../templates/pieces-memory-ready.md)
