# CAPY TUI | Design & Architecture
Layered architecture following a lightweight Ports & Adapters architectural style and applying a lightweight DDD.

## Core Features
* Asset inventory management
* Excess asset management
* Asset lookup and search
* Exporting reports
* Inventory history and auditing

---

## Design & Architecture | Domain
Placeholder.

## Design & Architecture | Infrastructure & Application
Placeholder.

## Design & Architecture | Persistence
The application is intended to be a desktop application with persistent local storage using SQLite.

---

## Workflow
Database talks to SQLite.
Repository understands persistence for a domain.
Workflow understands business use cases.
Domain understands business rules.
UI interacts with the user.

```text
+----------------------+
|      UI (Entry)      |
+----------+-----------+
           |
           v
+----------------------+
|    Application       |
+----------+-----------+
           |
           v
+----------------------+
|       Domain         |
+----------+-----------+
           ^
           |
  Repository Interface
(Persistence Abstraction)
           ^
           |
+----------------------+
|  SQLite Repository   |
|   (Infrastructure)   |
+----------------------+
```

