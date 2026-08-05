# Data Model: Automation Toolkit

Since the toolkit is a set of CLI wrappers around `gh` and Git, it is largely stateless. However, key data entities processed during execution include:

## Entity: PullRequestMetadata
Represents the data required to create or update a PR.
- `title` (String): The PR title.
- `body` (String): The generated Markdown body containing Summary, Changes, Commits, Risks, Config, Testing, Notes.
- `base_branch` (String): The target branch (e.g., `main` or `develop`).
- `head_branch` (String): The source branch with changes.

## Entity: DiffContext
Input for the documentation engine to generate descriptions.
- `files_changed` (List[String]): Files modified in the branch.
- `diff_content` (String): The raw diff output.
- `commits` (List[String]): Commit messages in the branch.
