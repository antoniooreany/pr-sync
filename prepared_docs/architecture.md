# Архитектура Automation Toolkit (pr-sync)

## 1. Общая архитектура и компоненты

```mermaid
flowchart LR
    subgraph DevEnvironment["Dev Environment (Windows + IDE)"]
        IDE[IDE]
        AgentCLI[Antigravity / AI Agent]
    end

    subgraph AutomationToolkit["Automation Toolkit"]
        Constitution[prepared_docs/constitution.md]
        Spec[specs/001-automation-toolkit/spec.md]
        
        subgraph PRSync["pr-sync package"]
            CLI[toolkit.cli]
            GitAPI[toolkit.git_api]
            GHAPI[toolkit.gh_api]
            PRBody[toolkit.pr_body]
            Invariants[toolkit.invariants]
            LLMAPI[toolkit.llm_api (v1.1+)]
        end
    end

    subgraph Repo["Target GitHub Repo"]
        Git[git repo]
        GH[GitHub (gh CLI)]
        PR[Pull Request]
    end

    IDE --> CLI

    CLI --> GitAPI
    CLI --> GHAPI
    CLI --> Invariants
    CLI --> PRBody

    GitAPI --> Git
    GHAPI --> GH

    PRBody --> PR

    Constitution --> Spec
    Spec --> PRSync

    LLMAPI -.->|v1.1+| PRBody
```

## 2. Структура классов и модулей

```mermaid
classDiagram
    class CLI {
        +main()
    }
    class GitAPI {
        +get_current_branch()
        +get_diff(base, head)
        +get_commits(base, head)
        +get_changed_files(base, head)
    }
    class GitHubAPI {
        +check_auth()
        +find_open_pr(base, head)
        +create_pr(title, body, base, head)
        +update_pr(number, title, body)
    }
    class PRBody {
        +render_pr_body(diff, commits, base, head, changed_files)
    }
    class Invariants {
        +check_no_empty_diff_action(diff, strict)
    }

    CLI --> GitAPI
    CLI --> Invariants
    CLI --> PRBody
    CLI --> GitHubAPI
```
