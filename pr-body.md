## Summary

Refined Phase 2 tasks for the Automation Toolkit to include explicit "Done when" criteria for the git and GitHub access layers.

## Changes

- Updated `specs/001-automation-toolkit/tasks.md`:
  - Added detailed "Done when" checklists for T003 (git access layer) and T004 (GitHub interaction layer).
  - Linked the behavior of `get_current_branch` and `get_diff` to the contracts in `spec.md`.
  - Defined clear expectations for gh_api functions (find_open_pr, create_pr, update_pr) and their interaction with gh and auth checks.
- Kept Phase 1, Phase 3, and Phase 4 task structure intact while making Phase 2 more verifiable.

## Risks

- Minimal: only documentation/spec-level changes, no runtime behavior modifications.
- Potential misalignment if future implementation of git_api/gh_api diverges from these new "Done when" criteria; this will require updating either the spec or the implementation to stay in sync.

## Testing

- No automated tests were added or modified in this PR.
- Verified that:
  - specs/001-automation-toolkit/tasks.md renders correctly as Markdown.
  - The new checklists for T003 and T004 are consistent with the current specs/001-automation-toolkit/spec.md.
