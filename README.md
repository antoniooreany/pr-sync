# Automation Toolkit: pr-sync

`pr-sync` is a smart, general-purpose CLI tool designed to automate Pull Request metadata generation. It analyzes your local git changes and commits to generate high-quality PR titles, descriptions, and labels.

It supports local AI models via **Ollama** as well as cloud models like **Anthropic Claude** and **Google Gemini** with automated resilient fallback routing.

---

## Features

- **🧠 Smart PR Summaries**: Generates structured markdown descriptions including *Smart Summary* (changes logically grouped into Features, Bug Fixes, Chores) and *Risk Analysis* using local or cloud LLMs.
- **🏷️ Automated Label Application**: Infers `type:*` and `area:*` labels from changed file paths and automatically applies them on GitHub.
- **⏳ Execution Timers**: Displays precise duration measurements for both LLM calls and the overall process.
- **🎨 Premium CLI Interface**: Clear step-by-step progress logging with emojis and encoding safety for Windows consoles.
- **🔄 Robust Fallback**: Gracefully degrades to a clean static fallback template if no LLMs are configured or available.
- **💬 GitHub Actions Integration**: Trigger updates directly on GitHub by commenting `[review-pr]` on any open Pull Request.

---

## Installation

Install in editable mode inside your python environment:

```powershell
pip install -e .
```

Ensure you have the [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated:

```powershell
gh auth status
```

---

## Local Usage

Run `pr` (or `pr.exe` on Windows) from the root of any git repository:

```powershell
pr --base develop
```

### Specifying LLM Models

The tool checks for LLM configurations in the following priority order:

1. **Ollama (Local)**: Set the `OLLAMA_MODEL` environment variable (e.g., `qwen2.5-coder:1.5b`).
2. **Anthropic Claude**: Set the `ANTHROPIC_API_KEY` environment variable.
3. **Google Gemini**: Set the `GEMINI_API_KEY` environment variable.

#### Quick Model Overrides

You can override the model on the fly using the `--model` flag:

```powershell
# Run with a fast local 1.5B model
pr --model qwen2.5-coder:1.5b

# Run with a heavier local 7B model
pr --model qwen2.5-coder:7b
```

---

## Configuring Environment Variables on Windows

To set a global environment variable permanently:

```powershell
[Environment]::SetEnvironmentVariable("OLLAMA_MODEL", "qwen2.5-coder:1.5b", "User")
```
*Note: Restart your terminal window after running this command to load the new variable.*

For temporary use in the current session:

```powershell
$env:OLLAMA_MODEL = "qwen2.5-coder:1.5b"
```

---

## GitHub Actions Workflow (`docs-assistant.yml`)

You can set up `pr-sync` to run automatically on GitHub whenever a team member comments `[review-pr]` on a Pull Request.

Create `.github/workflows/docs-assistant.yml` in your repository:

```yaml
name: docs-assistant

on:
  issue_comment:
    types: [created]

jobs:
  review-pr:
    if: >
      github.event.issue.pull_request &&
      contains(github.event.comment.body, '[review-pr]')
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Checkout PR branch
        run: gh pr checkout ${{ github.event.issue.number }}
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install pr-sync
        run: pip install -e .

      - name: Run pr-sync to update PR
        run: pr-sync --base ${{ github.event.issue.pull_request.base.ref || 'develop' }}
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OLLAMA_MODEL: ""
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}

      - name: Acknowledge in comment
        run: |
          gh pr comment ${{ github.event.issue.number }} \
            --body "✅ **docs-assistant** updated this PR's title, body, and labels."
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Architecture & Specifications

For more details on specifications, check the internal documentation:
- [Code-to-Docs Contract](.specify/contracts/code-to-docs.md)
- [Code-to-Docs Constraints](.specify/contracts/code-to-docs-constraints.md)
- [Architecture Diagram](docs/architecture-pr-sync.md)
