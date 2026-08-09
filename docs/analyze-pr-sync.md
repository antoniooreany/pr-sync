# Анализ и Архитектура `pr-sync` (SDD Analyze Report)

## 1. Ретроспектива и риски LLM
Проект `pr-sync` достиг версии MVP (v1.0.0). Базовый функционал автогенерации PR из коммитов реализован и протестирован (21/21).

**Риски LLM-генерации (v1.1+):**
- **Идемпотентность:** Повторный вызов генерации перезапишет ручные правки в PR.
- **Недетерминированность:** Текст может отличаться байт-в-байт при тех же вводных данных.
- **Трата ресурсов:** Настройка генерации PR съела больше времени, чем должна была сэкономить.

**Вывод:** Разработка LLM-модуля заморожена. Фокус смещен на эксплуатацию инструмента `pr-sync` в том виде, в каком он есть сейчас.

## 2. Архитектура интеграции: `pr-sync` и `oracle-capacity-hunter-claude`

Ниже представлена диаграмма, описывающая структуру проектов и то, как `pr-sync` выступает генерализированным модулем.

```mermaid
classDiagram
    %% oracle-capacity-hunter-claude structure
    namespace OracleCapacityHunterClaude {
        class CLI_Oracle {
            <<Entry Point>>
            src/capacity_hunter/cli.py
        }
        class Finder {
            src/capacity_hunter/finder.py
        }
        class Notifier {
            src/capacity_hunter/notifier.py
        }
        class Config_Oracle {
            src/capacity_hunter/config.py
        }
        class Scripts_Deprecated {
            <<Deprecated / Extracted>>
            scripts/pr.ps1
            scripts/code_to_docs.py
        }
    }

    CLI_Oracle --> Finder : uses
    CLI_Oracle --> Notifier : uses
    CLI_Oracle --> Config_Oracle : reads

    %% pr-sync structure
    namespace PR_Sync_Toolkit {
        class CLI_Toolkit {
            <<Entry Point: pr-sync>>
            src/toolkit/cli.py
        }
        class GitAPI {
            src/toolkit/git_api.py
        }
        class GitHubAPI {
            src/toolkit/gh_api.py
        }
        class PRBody_Generator {
            src/toolkit/pr_body.py
        }
        class Invariants_Checker {
            src/toolkit/invariants.py
        }
    }

    CLI_Toolkit --> GitAPI : fetches repo state
    CLI_Toolkit --> GitHubAPI : manages PRs
    CLI_Toolkit --> PRBody_Generator : formats text
    CLI_Toolkit --> Invariants_Checker : validates actions

    %% Relationships and Extraction
    Scripts_Deprecated ..|> CLI_Toolkit : Generalized & Replaced by
    
    note for Scripts_Deprecated "Логика автогенерации PR полностью вынесена\nв глобальный инструмент pr-sync"
```
