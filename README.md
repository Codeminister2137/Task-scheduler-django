# Task-scheduler-django
Version of my Task Scheduler project made in Django
```mermaid
---
title: Entity Relationship diagram for database
---
erDiagram
    USER||--o{ TASK : plans
    TASK ||--|{ NOTIFICATION : contains
```
