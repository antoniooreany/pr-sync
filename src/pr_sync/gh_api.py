"""GitHub API layer via gh CLI."""
import subprocess
import json
from .invariants import PullRequestMetadata, CreatedPRInfo, UpdatedPRInfo

class GhAuthError(Exception):
    pass

def check_gh_auth():
    """Ensure gh is available and authenticated."""
    result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise GhAuthError("gh CLI is missing or not authenticated.")

def find_open_pr(base: str, head: str) -> list[PullRequestMetadata]:
    """Find open PRs for a (base, head) pair."""
    result = subprocess.run(
        ["gh", "pr", "list", "--base", base, "--head", head, "--state", "open", "--json", "title,body,headRefName,baseRefName,url"],
        capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise Exception(f"Failed to list PRs: {result.stderr}")
    
    data = json.loads(result.stdout or "[]")
    return [
        PullRequestMetadata(
            title=pr["title"],
            body=pr["body"],
            base_branch=pr.get("baseRefName", base),
            head_branch=pr.get("headRefName", head),
            url=pr.get("url", "")
        ) for pr in data
    ]

def create_pr(metadata: PullRequestMetadata) -> CreatedPRInfo:
    """Create a new PR."""
    result = subprocess.run(
        ["gh", "pr", "create", "--base", metadata.base_branch, "--head", metadata.head_branch, "--title", metadata.title, "--body", metadata.body],
        capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise Exception(f"Failed to create PR: {result.stderr}")
    return CreatedPRInfo(url=result.stdout.strip())

def update_pr(pr_number_or_url: str, metadata: PullRequestMetadata) -> UpdatedPRInfo:
    """Update an existing PR."""
    result = subprocess.run(
        ["gh", "pr", "edit", pr_number_or_url, "--title", metadata.title, "--body", metadata.body],
        capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise Exception(f"Failed to update PR: {result.stderr}")
    return UpdatedPRInfo(url=result.stdout.strip())
