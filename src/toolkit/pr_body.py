def render_pr_body(diff: str, commits: list) -> str:
    """Render the standard PR body."""
    commits_str = "\n".join(f"- {c}" for c in commits) if commits else "- None"
    
    return f"""## Summary
Auto-generated PR based on diff.

## Changes
- Updated files

## Commits
{commits_str}

## Risks
- Low

## Config
- None

## Testing
- Automated

## Notes
- None
"""
