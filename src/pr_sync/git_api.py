"""Git API layer."""
import subprocess
from .invariants import DiffContext

def run_git_command(args: list[str]) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(["git"] + args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()

def get_current_branch() -> str:
    """Get the current active branch."""
    return run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])

def get_diff(base: str, head: str) -> DiffContext:
    """Get diff context between base and head."""
    # List of changed files
    files_changed_out = run_git_command(["diff", "--name-only", f"{base}...{head}"])
    files_changed = [f for f in files_changed_out.splitlines() if f]

    # Raw diff text
    diff_content = run_git_command(["diff", f"{base}...{head}"])

    # List of commits
    commits_out = run_git_command(["log", "--format=%H %s", f"{base}...{head}"])
    commits = [c for c in commits_out.splitlines() if c]

    return DiffContext(
        files_changed=files_changed,
        diff_content=diff_content,
        commits=commits
    )
