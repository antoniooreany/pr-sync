import sys
import argparse
from toolkit.git_api import get_current_branch, get_diff, get_commits, get_changed_files
from toolkit.gh_api import check_auth, find_open_pr, create_pr, update_pr
from toolkit.pr_body import render_pr_body
from toolkit.invariants import check_no_empty_diff_action

def main():
    try:
        parser = argparse.ArgumentParser(description="PR Sync CLI")
        parser.add_argument("--base", default="develop", help="Base branch")
        args, _ = parser.parse_known_args()

        if not check_auth():
            print("GitHub CLI is not authenticated.")
            return 2

        base = args.base
        head = get_current_branch()
        diff = get_diff(base, head)
        
        if not diff.strip():
            # if empty diff, do not take action
            if not check_no_empty_diff_action(diff.strip(), True):
                print("Empty diff, no action taken.")
                return 0

        commits = get_commits(base, head)
        changed_files = get_changed_files(base, head)
        
        body = render_pr_body(diff, commits, base=base, head=head, changed_files=changed_files)
        title = f"Auto PR: {head}"
        
        pr = find_open_pr(base, head)
        if pr:
            update_pr(pr['number'], title, body)
            print(f"Updated PR #{pr['number']} for {head}")
        else:
            create_pr(title, body, base, head)
            print(f"Created PR for {head}")
            
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
