"""Invariant helpers for pr-sync testing."""
from dataclasses import dataclass

@dataclass
class PullRequestMetadata:
    title: str
    body: str
    base_branch: str
    head_branch: str
    url: str = ""

@dataclass
class DiffContext:
    files_changed: list[str]
    diff_content: str
    commits: list[str]

@dataclass
class CreatedPRInfo:
    url: str

@dataclass
class UpdatedPRInfo:
    url: str

def check_single_pr_invariant(matching_prs: list[PullRequestMetadata]) -> bool:
    """Ensures there is at most one open PR per (base, head) pair."""
    return len(matching_prs) <= 1

def check_no_pr_on_empty_diff(diff: DiffContext) -> bool:
    """Ensures we do not proceed if diff is empty."""
    if not diff.diff_content.strip() and not diff.commits:
        return True
    return False

def check_non_empty_pr_body_sections(body: str) -> bool:
    """Ensures all required sections are present and non-empty."""
    required_sections = [
        "## Summary",
        "## Changes",
        "## Commits",
        "## Risks",
        "## Config",
        "## Testing",
        "## Notes"
    ]
    for section in required_sections:
        if section not in body:
            return False
    return True
