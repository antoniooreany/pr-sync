# Phase 0: Research & Technical Decisions

## Decision 1: GitHub API Integration
- **Decision**: Use `subprocess` to call `gh` CLI commands directly, leveraging `--json` flags where structured data is needed.
- **Rationale**: The specification explicitly constraints v1 to "GitHub only, via the gh CLI" and forbids direct API usage. The `gh` CLI handles authentication, pagination, and provides robust JSON output capabilities.
- **Alternatives considered**: PyGithub or direct REST API requests were rejected due to the strict `gh` CLI constraint in the specs.

## Decision 2: Documentation Engine Integration
- **Decision**: Extract `code_to_docs.py` into a reusable internal module within the toolkit (e.g., `src/toolkit/docs_engine.py`).
- **Rationale**: The user's goal is to prevent duplication across repositories. By creating a unified python CLI package that bundles the engine, other tools in the toolkit (like `doc-sync` or `pr-sync`) can simply import and invoke it.
- **Alternatives considered**: Keeping it as a loose script, which violates the "Reuse over reimplementation" principle and complicates sharing across the toolkit.
