# Automation Toolkit Architecture

## pr-sync (v1.0.0)
```mermaid
classDiagram
    class CLI {
        +main()
    }
    class GitAPI {
        +get_current_branch()
        +get_diff()
    }
    class GitHubAPI {
        +find_open_pr()
        +create_pr()
    }
    class PRBody {
        +render_pr_body()
    }
    class Invariants {
        +check_no_empty_diff_action()
    }
    CLI --> GitAPI
    CLI --> Invariants
    CLI --> PRBody
    CLI --> GitHubAPI
```
*Note: `pr-sync` relies entirely on determinism. The `pr_body` module uses static templating. The `toolkit/` layer is designed to be shared with future tools (e.g., `release-sync`).*

## Cross-Repository Analysis: oracle-capacity-hunter-claude
```mermaid
classDiagram
    class CLI { +main() }
    class Config { +load_config() }
    class Finder { +run_forever() }
    class Notifier { +TelegramNotifier() }
    CLI --> Config
    CLI --> Finder
    CLI --> Notifier
    Finder --> Notifier
```
*Conclusion: The Oracle bot interacts strictly with OCI and Telegram. There is no PR generation logic (`codetodocs.py`) to extract. LLM-based PR generation for `pr-sync` must be designed as a net-new feature.*
