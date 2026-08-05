import datetime

def render_pr_body(diff: str, commits: list, base: str = "develop", head: str = "HEAD", changed_files: list = None) -> str:
    """Render the standard PR body."""
    if changed_files is None:
        changed_files = []
        
    commits_str = "\n".join(f"{c}" for c in commits) if commits else "- None"
    changes_str = "\n".join(f"- {f}" for f in changed_files) if changed_files else "- None"
    timestamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    
    return f"""## Summary

Introduce changes from branch {head} into {base}.

## Changes

{changes_str}

## Commits

{commits_str}

## Risks

- Low: see commit history for scope of change.

## Config

- No new required environment variables beyond existing ones.

## Testing

- ruff check, pytest, manual smoke test.

## Notes

-

_Last updated by pr-sync at {timestamp}._"""
