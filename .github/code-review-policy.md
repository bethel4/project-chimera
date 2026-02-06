# AI Code Review Policy (Project Chimera)

## Prime Directive: Spec Alignment
- Any non-trivial code change MUST reference a requirement in `specs/`:
  - Mention the spec file + section in PR description or code comments.
- Reject changes that add features not described in specs.

## Architecture Compliance (Non-Negotiable)
- External interactions MUST go through MCP (no direct API calls).
- Planner-Worker-Judge pattern is mandatory for orchestration logic.
- Python-first, use pydantic for schemas.
- Personas must come from SOUL.md (not embedded in code).

## Security Requirements
- No secrets in code or logs:
  - Wallet keys, seed phrases, API tokens, private keys.
- Coinbase/AgentKit logic must include budget governance hooks.
- Prefer least privilege and environment-based configuration.

## Testing Requirements
- TDD: tests should exist before implementation.
- New behavior requires tests.
- If tests/lint/typecheck fail, PR must not merge.

## Observability & Traceability
- Code should be traceable to specs and produce meaningful logs without leaking secrets.
