"""
Git access layer.
"""
import subprocess

def get_current_branch() -> str:
    """Return the current git branch."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git error: {e.stderr.strip() if e.stderr else 'Unknown error'}") from e
    except FileNotFoundError:
        raise RuntimeError("Git executable not found in PATH")

def get_diff(base: str, head: str) -> str:
    """Return the diff between base and head branches."""
    try:
        result = subprocess.run(
            ["git", "diff", f"{base}..{head}"],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git diff error: {e.stderr.strip() if e.stderr else 'Unknown error'}") from e
    except FileNotFoundError:
        raise RuntimeError("Git executable not found in PATH")
