# Task Scheduler Django

This repository contains a Docker Compose based Django baseline for a task
scheduler project. It is currently split into three Django services:

- `auth-service`
- `calendar-service`
- `email-service`

Each service has its own PostgreSQL container. Redis and NGINX are also defined
in Compose.

## Current State

This is a backend-only local development project. The implemented application
code is small:

- `auth_app` currently uses Django's built-in auth models and exposes only the
  Django admin URL.
- `calendar_app` defines a `Notification` model with `scheduled_for` and
  `task_id` fields.
- `email_app` defines `Email` and `EmailEvent` models, event tracking signals,
  and a Celery task function for sending created email events.

There is no implemented task CRUD API, registration flow, dashboard, or
frontend in this repository at the moment. Those features are listed as planned
work below.

## Runtime

The supported runtime is Docker Compose. The services are built from:

- `auth_service/Dockerfile`
- `calendar_service/Dockerfile`
- `email_service/Dockerfile`

The Compose stack includes:

- `auth-db`, `calendar-db`, `email-db`: PostgreSQL 16 containers
- `auth-service`, `calendar-service`, `email-service`: Django/Gunicorn services
- `redis`: Redis on host port `6379`
- `nginx`: reverse proxy on host port `4000`

NGINX routes:

- `/auth/` to `auth-service`
- `/calendar/` to `calendar-service`
- `/email/` to `email-service`

Each Django service currently exposes only `/admin/` through its URL
configuration.

## Requirements

- Docker
- Docker Compose
- Make, optional but recommended for the commands below

There is no maintained non-Docker setup documented for this project.

## Commands

Start the stack:

```bash
make start
```

Stop the stack and remove volumes:

```bash
make stop
```

Build images:

```bash
make build
```

Apply migrations for all three Django services:

```bash
make migrate
```

Run tests for all three Django services:

```bash
make test
```

Run coverage for all three Django services:

```bash
make coverage
```

Equivalent direct Docker Compose test commands:

```bash
docker-compose exec -T auth-service python manage.py test
docker-compose exec -T calendar-service python manage.py test
docker-compose exec -T email-service python manage.py test
```

## Environment

The Compose file defines the database host/name/password values used by the
services. A `.env` file is optional for the Makefile; `.env.example` is present
as a placeholder for local environment values.

## Static Files

All Django services mount the shared `static` Docker volume at
`/var/www/static`. NGINX currently defines static aliases for `/auth/static` and
`/calendar/static`.

## Tests and Coverage

Tests are run inside the service containers. Coverage is installed in each
service image and can be run with:

```bash
make coverage
```

Current coverage intentionally focuses on implemented model, signal, and task
behavior rather than placeholder views.

## Planned Features

The following features are part of the intended task scheduler product but are
not implemented in the current codebase:

- User registration and authentication flows beyond Django's built-in admin
  auth.
- Task creation with fields such as title, description, priority, due date, and
  scheduled time.
- Task scheduling logic for specific dates and times.
- Email notifications that remind users about upcoming tasks.
- Task management dashboard for viewing and managing created tasks.
- Public REST API endpoints for task and user workflows.
- Frontend interface for the dashboard and user workflows.

## Scope

This repository is a local development baseline. It does not currently include:

- production deployment configuration
- CI/CD configuration
- the planned user-facing product features listed above
