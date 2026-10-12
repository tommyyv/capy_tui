# CAPY TUI | Design & Architecture
Modular, layered, and lightweight port & adapters architecture and domain-driven design.

## Core Features
- Scan assets into a data table
- Import assets
- Export an asset list for generating reports
- Asset lookup and search

---

## Design & Architecture | Domain
Placeholder.

## Design & Architecture | Infrastructure & Application
Placeholder.

## Design & Architecture | Persistence
The application is intended to be a desktop application with persistent local storage using SQLite.

---

## Workflow
```text
+----------------------+
|      UI (Entry)      |
+----------+-----------+
           |
           v
+----------------------+
|    Application       |
|     (Services)       |
+----------+-----------+
           |
           v
+----------------------+
|       Domain         |
+----------+-----------+
           ^
           |
  Repository Interface ---------> | SQLite, Postgres, etc. (Infrastructure) |
(Persistence Abstraction)
           ^
           |
+----------------------+
|  Database Interface  |
|   (Infrastructure)   |
+----------------------+
```

