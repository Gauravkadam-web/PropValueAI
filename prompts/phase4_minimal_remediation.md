# PropValueAI — Phase 4 Minimal Remediation Only

Project: `D:\PropValueAI`

Implement only the approved Phase 4 audit remediations listed below. The existing architecture is approved and must remain unchanged.

## Mandatory restrictions

- Read `AGENTS.md`, `docs/architecture.md`, `docs/api-contracts.md`, `prompts/phase4.md`, and the independent audit report first.
- Inspect current source code before changing anything.
- Do not redesign or refactor the architecture.
- Do not change the ML module, training pipeline, inference API, model artifacts, or dataset.
- Do not modify unrelated files.
- Do not commit, push, reset, stash, or discard changes.
- Preserve all existing user work and the exact mandatory disclaimer.
- Do not start Phase 5.
- If a proposed fix requires an architectural change, stop and report the reason instead.

## Fix 1 — CORS configuration

Inspect `SecurityConfig.java`.

Replace the unsafe or invalid wildcard fallback behavior with a secure configuration consistent with the approved architecture.

Requirements:
- Read allowed origins from environment-driven application configuration.
- Do not use a permissive wildcard fallback for credentialed browser requests in production.
- Ensure allowed origins and credentials are configured consistently.
- Keep local development configuration documented and separate from production.
- Do not introduce hardcoded production domains.
- Add or update focused tests for allowed and rejected origins if feasible.

Do not blindly substitute `allowedOriginPatterns("*")` as a shortcut.

## Fix 2 — Deterministic pagination

Inspect `PredictionHistoryService.java` and existing repository methods.

Where prediction history is sorted by creation timestamp descending, use a deterministic secondary sort by ID descending.

Requirements:
- Apply consistently to user history and administrative history.
- Preserve existing pagination behavior and response format.
- Do not modify unrelated query or entity logic.

## Fix 3 — API contract documentation

Inspect the actual controllers and `docs/api-contracts.md`.

Update only the outdated endpoint references so documentation matches the implemented API paths, including the `/api/v1/` prefix where appropriate.

Requirements:
- Verify endpoint paths against actual controller mappings.
- Do not rename endpoints or change request/response contracts merely to match old documentation.
- Preserve the approved API behavior.

## Fix 4 — Clarify the no-guest-prediction decision

Inspect `prompts/phase4.md` and related Phase 4 documentation.

Clarify superseded planning text that discusses guest predictions or nullable prediction ownership.

The final rule must be explicit:
- Authentication is mandatory for every prediction.
- Guest predictions are prohibited.
- Every persisted prediction belongs to an authenticated user.
- The database ownership constraint remains enforced.

Do not rewrite the entire planning document or change the approved architecture.

## Fix 5 — Record-ID ownership test

Extend the existing `PredictionControllerTest.java`.

Add a test where authenticated User A attempts to access a prediction owned by User B using:

`GET /api/v1/predictions/{id}`

Verify that the response does not reveal User B's record. Use the application's established authorization convention (403 or 404) and verify the actual expected behavior from the service/controller implementation.

Also verify that the owner can access their own record if that case is not already covered.

Do not weaken authorization to make tests pass.

## Fix 6 — Test and report

Run:
1. Backend test suite: `mvn test` from `backend/`.
2. ML regression suite: `.\.venv\Scripts\pytest.exe ml/tests/ -v` from the repository root, if feasible.

Report actual results and any environmental blockers.

Inspect:
- `git status --short`
- `git diff --check`
- `git diff --stat`
- Full diff of every modified tracked file
- Direct contents of changed or newly created files that do not appear in ordinary `git diff`

Do not claim all tests passed unless you ran them and observed the result.

## Final report

Provide:
- Each finding fixed and the exact file changed
- Any finding intentionally left unchanged, with reason
- Actual backend and ML test results
- Confirmation that architecture, ML modules, model artifacts, and API behavior were not unnecessarily changed
- Confirmation that no commit or push occurred
- Remaining concerns

Stop after reporting. Do not begin Phase 5.
