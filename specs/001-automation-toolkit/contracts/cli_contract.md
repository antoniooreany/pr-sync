# CLI Contract: `pr-sync`

The `pr-sync` tool provides a command-line interface for PR automation.

## Command: `pr-sync`

**Description**: Creates or updates a single GitHub PR for the current branch against a base branch.

**Arguments/Options**:
- `--base` (optional, string): The base branch to target. Defaults to the repository's default branch.
- `--head` (optional, string): The head branch. Defaults to the current active branch.
- `--dry-run` (optional, flag): If set, prints the generated PR title and body to stdout without interacting with GitHub.

**Exit Codes**:
- `0`: Success (PR created or updated).
- `1`: Error (e.g., no diff, `gh` CLI not authenticated, generation failed).
