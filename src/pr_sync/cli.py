"""CLI entry point for pr-sync."""
import argparse
import sys
from datetime import datetime

from . import git_api
from . import gh_api
from . import pr_body
from . import invariants

def main():
    parser = argparse.ArgumentParser(description="PR Automation Toolkit - pr-sync")
    parser.add_argument("--base", default="develop", help="Base branch")
    parser.add_argument("--head", help="Head branch (defaults to current branch)")
    parser.add_argument("--title", help="Optional PR title")
    parser.add_argument("--dry-run", action="store_true", help="Print output without modifying GitHub")
    args = parser.parse_args()

    # Resolve branches
    base = args.base
    head = args.head or git_api.get_current_branch()
    
    if not head:
        print("Error: Could not determine current branch.", file=sys.stderr)
        sys.exit(1)

    # Authentication check
    try:
        gh_api.check_gh_auth()
    except gh_api.GhAuthError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    # Get diff
    diff = git_api.get_diff(base, head)
    if invariants.check_no_pr_on_empty_diff(diff):
        print("no changes between base and head, no PR created or updated", file=sys.stderr)
        sys.exit(1)

    # Render body
    timestamp = datetime.now().isoformat()
    body = pr_body.render_pr_body(diff, base, head, timestamp)
    title = args.title or f"Sync {head} into {base}"

    metadata = invariants.PullRequestMetadata(
        title=title,
        body=body,
        base_branch=base,
        head_branch=head
    )

    if args.dry_run:
        print("--- DRY RUN ---")
        print(f"Title: {title}")
        print(f"Base: {base}")
        print(f"Head: {head}")
        print("Body:")
        print(body)
        sys.exit(0)

    # Find existing PRs
    try:
        prs = gh_api.find_open_pr(base, head)
    except Exception as e:
        print(f"Error finding PRs: {e}", file=sys.stderr)
        sys.exit(1)
        
    if len(prs) == 0:
        # Create new
        try:
            info = gh_api.create_pr(metadata)
            print(f"Created PR: {info.url}")
        except Exception as e:
            print(f"Error creating PR: {e}", file=sys.stderr)
            sys.exit(1)
    elif len(prs) == 1:
        # Update existing
        try:
            info = gh_api.update_pr(prs[0].url, metadata)
            print(f"Updated PR: {info.url}")
        except Exception as e:
            print(f"Error updating PR: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Ambiguous
        print("Ambiguity: more than 1 open PR found for this base/head pair. No changes made.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
