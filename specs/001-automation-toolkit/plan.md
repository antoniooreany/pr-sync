# Implementation Plan: Automation Toolkit

**Branch**: `001-automation-toolkit` | **Date**: 2026-08-05 | **Spec**: [specs/001-automation-toolkit/spec.md](spec.md)

**Input**: Feature specification from `specs/001-automation-toolkit/spec.md`

## Summary

The Automation Toolkit provides a suite of CLI tools starting with `pr-sync` to standardise PR generation across repositories. It will be implemented in Python and interact with GitHub using the `gh` CLI rather than direct API calls, integrating existing logic from `code_to_docs.py` to ensure zero logic duplication.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `gh` CLI (must be installed system-wide). No complex third-party dependencies expected except possibly `pytest` for testing.

**Storage**: N/A (Stateless CLI logic operating on git repository).

**Testing**: `pytest`

**Target Platform**: Any OS with Python and `gh` CLI available.

**Project Type**: CLI Toolkit

**Performance Goals**: N/A (Dependent on GitHub API rate limits via `gh`).

**Constraints**: Strict adherence to GitHub CLI usage for v1; no other VCS support.

**Scale/Scope**: Solo developer/small teams across multiple internal repositories.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Language**: English required. (Pass)
- **Gitflow**: Using proper branch names. (Pass)
- **Safe-by-default**: Tools are non-destructive (e.g. `pr-sync --dry-run` available, no force-pushes). (Pass)
- **No duplication**: Will re-use `code_to_docs.py`. (Pass)

## Project Structure

### Documentation (this feature)

```text
specs/001-automation-toolkit/
├── plan.md              
├── research.md          
├── data-model.md        
├── quickstart.md        
├── contracts/cli_contract.md
└── tasks.md             
```

### Source Code (repository root)

```text
src/
└── toolkit/
    ├── __init__.py
    ├── cli.py               # Main CLI orchestrator
    ├── commands/
    │   ├── __init__.py
    │   └── pr_sync.py       # pr-sync command logic
    └── engines/
        ├── __init__.py
        └── docs_engine.py   # Refactored code_to_docs.py

tests/
├── integration/
│   └── test_pr_sync.py
└── unit/
    └── test_docs_engine.py
```

**Structure Decision**: A single Python package `toolkit` that exposes various commands. Existing logic from `oracle-capacity-hunter-claude` will be ported into the `engines/` subdirectory.

## Complexity Tracking

None required. No constitution violations.
