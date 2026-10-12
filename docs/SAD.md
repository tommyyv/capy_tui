# CAPY TUI | Design & Architecture
Modular, layered, and lightweight port & adapters architecture and domain-driven design. I personally thought and like
of the space station analogy to learn, understand, design, and implement the codebase around these concepts.

## Core Features and more
- Scan assets into a data table
- Import assets
- Export an asset list for generating reports
- Asset lookup and search

---

## Design & Architecture | Domain
Entities and rules. Space station bridge; everything must follow the protocols, regulations, and compliance mandated.
This means that ships must follow strict standards before permitted to dock and/or interact with the station's core
systems.

## Design & Architecture | Application & Infrastructure | Ports & Adapters
Application services coordinate data flow logic throughout the application, while the infrastructure consists of system
representations, such as databases, message queues, etc., used by the application.

Adapters implement port interfaces. The space station, docking nodes, and ships/probes. Ships/probes must have the
correct adapters to dock onto the space station's docking node. Adapters are either driven or driving. These terms are
relative to the space station's probes or ships, meaning the probes search for resources/services (outbound), while
ships delivers resources/services to the space station (inbound).

- Driving adapters (inbound) = ships deliver resources/services
- Driven adapters (outbound) = probes search for resources/services

Adapters (implementations = ships (driving) or probes (driven)):
- UI (driving) -> delivers a service
- SQLite adapter (driven) -> requires a SQLite or PostgreSQL service

Ports (interfaces/protocols = space station's dock node):
- Repository -> defines what ships/probes must follow to dock

## Design & Architecture | Workflow
```text
p = port = docking node
a = adapter = ship (driving) or probe (driven)

                                 +-------------------------------+
                                 |Application & Infrastructure   |
                                 |(space station)                |
+----------+                     |                               |                          +-----------------+
|UI (ship) a-delivers--inbound-->p                               p<--outbound--searches for-a Database (probe)|
+----------+                     |       +-------------+         |                          +-----------------+
                                 |       |   Domain    |         |
                                 |       |   (bridge)  |         |
                                 |       +-------------+         |
                                 |                               |
                                 |                               |
                                 +-------------------------------+
```

---
