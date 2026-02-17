# Task Scheduler (Django)

This repository contains the **original Django-based implementation** of a task scheduling application.

It represents the **starting point** of the project, before later experiments with service separation and alternative architectures.

The application is designed to be run locally using **Docker Compose** and focuses primarily on backend functionality.

---

## Overview

The project is structured as a Django application backed by PostgreSQL and Redis, with NGINX acting as a reverse proxy and static file server.

Multiple logical components (authentication, calendar functionality, email handling) exist within the same codebase and runtime environment.

---

## Architecture (current state)

The system consists of:

* Django application(s) served via **Gunicorn**
* PostgreSQL databases
* Redis
* NGINX reverse proxy

All components are started and managed together using **Docker Compose**.

---

## Services (Docker Compose)

### Django services

The project runs multiple Django-based services, each started with Gunicorn and exposed internally.

Each service is configured with its own database connection and URL prefix.

### Databases

PostgreSQL 16 is used.

Separate database containers exist for different parts of the application.

### Redis

A Redis instance is available and exposed on port `6379`.

### NGINX

NGINX:

* routes requests to Django services
* serves static files from a shared volume

It is exposed on port **4000**.

---

## Running the project

### Requirements

* Docker
* Docker Compose
* Make

There is **no supported non-Docker setup**.

---

## Makefile

The `Makefile` is the primary interface for working with the project.

### Common commands

```bash
make start        # start containers
make stop         # stop containers and remove volumes
make restart      # restart containers
make status       # show container status
make build        # build images
make build-clean  # build images without cache
make logs         # follow logs
```

### Shell access

```bash
make shell_app    # open a shell in the backend container
make shell_db     # open a psql session for the database
```

### Django management

```bash
make migration    # create migrations
make migrate      # apply migrations
make test         # run Django tests
```

---

## Static files

Static files are written to a shared Docker volume and served by NGINX.

This avoids serving static assets directly from Django.

---

## Environment

The Makefile expects a `.env` file to be present.

Environment variables are used by Docker Compose and the Django services.

---

## Project context

This repository is the **original django version** of the Task Scheduler project.

Later iterations explore:

* separating functionality into independent services
* different composition strategies
* alternative architectural approaches

Those later experiments live in separate repositories and should be treated as follow-ups, not prerequisites.

---

## Current scope

* Local development only
* Docker Compose–based runtime
* No production deployment configuration
* No CI/CD pipeline

This repository documents a working baseline rather than a finished product.


# Task-scheduler-django
Version of my Task Scheduler project made in Django

Features:
- User Registration and Authentication: Secure user authentication and registration system.
- Task Creation: Users can create tasks with attributes such as title, description, priority, and due date.
- Task Scheduling: Set specific dates and times for tasks.
- Email Notifications: Send scheduled email notifications to users reminding them of upcoming tasks.
- Task Management Dashboard: View and manage all created tasks in a user-friendly interface.
