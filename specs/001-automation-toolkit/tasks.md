# Tasks: Automation Toolkit

**Linked Spec**: `specs/001-automation-toolkit/spec.md`

## Phase 1: Setup (Shared Infrastructure)
*Purpose: Project initialization and basic structure*
- [ ] T001 Create package skeleton (`__init__.py`, `cli.py`, `git_api.py`, `gh_api.py`, `pr_body.py`, `invariants.py`) under `src/toolkit/` and scripts entry point (`pyproject.toml`)
- [ ] T002 [P] Implement invariant helpers in `src/toolkit/invariants.py` for testing

## Phase 2: Foundational (Blocking Prerequisites)
*Purpose: Core infrastructure that MUST be complete before ANY user story can be implemented*
⚠️ CRITICAL: No user story work can begin until this phase is complete
- [ ] T003 Implement git access layer (`get_current_branch`, `get_diff`) in `src/toolkit/git_api.py` and pass empty diff unit tests
- [ ] T004 Implement GitHub interaction (`find_open_pr`, `create_pr`, `update_pr`) in `src/toolkit/gh_api.py` with auth checks and mocked subprocess tests
*Checkpoint: Foundation ready - user story implementation can now begin*

## Phase 3: User Story 1 - PR Automation with pr-sync (Priority: P1) 🎯 MVP
*Goal: Automatically standardize and generate PR metadata (body, titles) based on code diffs*
*Independent Test: Can be fully tested by running pr-sync against a test branch with changes.*
- [ ] T005 [P] [US1] Write test mapping specs (`test_pr_body.py`, `test_cli.py`, `test_invariants.py`) ensuring each invariant has an enforcing test
- [ ] T006 [US1] Implement PR body generation (`render_pr_body`) in `src/toolkit/pr_body.py` with required sections (Summary, Changes, Commits, Risks, Config, Testing, Notes)
- [ ] T007 [US1] Enforce invariants and exit codes in `src/toolkit/cli.py` (`main()`) to handle empty diffs, ambiguity, missing gh auth
*Checkpoint: At this point, User Story 1 should be fully functional and testable independently*

## Phase 4: Polish & Cross-Cutting Concerns
*Purpose: Improvements that affect multiple user stories*
- [ ] T008 [P] Sync docs and CLI contract in `docs/pr-sync-specification.md` and `specs/001-automation-toolkit/contracts/cli_contract.md`
- [ ] T009 [P] Update quickstart scenarios in `specs/001-automation-toolkit/quickstart.md`
