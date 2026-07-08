-include .env
# Variables
DOCKER_COMPOSE=docker-compose
AUTH_DATABASE=auth-db
CALENDAR_DATABASE=calendar-db
EMAIL_DATABASE=email-db
AUTH_SERVICE=auth-service
CALENDAR_SERVICE=calendar-service
EMAIL_SERVICE=email-service


.PHONY: start
start: ## start containers
	@ ($(DOCKER_COMPOSE) up -d)

.PHONY: stop
stop: ## stop containers
	@ ($(DOCKER_COMPOSE) down -v)

.PHONY: restart
restart: stop start ## restart containers

.PHONY: status
status: ## display containers status
	@ ($(DOCKER_COMPOSE) ps)

.PHONY: build
build: ## build image
	@ ($(DOCKER_COMPOSE) build)

.PHONY: build-clean
build-clean: ## build image without cache
	@ ($(DOCKER_COMPOSE) build --no-cache)

.PHONY: logs
logs: ## access logs
	@ ($(DOCKER_COMPOSE) logs -f)

.PHONY: shell_app
shell_app: ## start app
	@ ($(DOCKER_COMPOSE) exec $(AUTH_SERVICE) /bin/bash)

.PHONY: shell_db
shell_db: ## open database console
	@ ($(DOCKER_COMPOSE) exec $(AUTH_DATABASE) psql -U $${POSTGRES_USER:-postgres} $${POSTGRES_DB:-postgres})

.PHONY: migration
migration: ## create migration
	@ ($(DOCKER_COMPOSE) exec -it $(AUTH_SERVICE) python manage.py makemigrations)
	@ ($(DOCKER_COMPOSE) exec -it $(CALENDAR_SERVICE) python manage.py makemigrations)
	@ ($(DOCKER_COMPOSE) exec -it $(EMAIL_SERVICE) python manage.py makemigrations)

.PHONY: migrate
migrate: ## migrate database
	@ ($(DOCKER_COMPOSE) exec -it $(AUTH_SERVICE) python manage.py migrate)
	@ ($(DOCKER_COMPOSE) exec -it $(CALENDAR_SERVICE) python manage.py migrate)
	@ ($(DOCKER_COMPOSE) exec -it $(EMAIL_SERVICE) python manage.py migrate)


.PHONY: test
test: # run tests
	@ ($(DOCKER_COMPOSE) exec -T $(AUTH_SERVICE) python manage.py test)
	@ ($(DOCKER_COMPOSE) exec -T $(CALENDAR_SERVICE) python manage.py test)
	@ ($(DOCKER_COMPOSE) exec -T $(EMAIL_SERVICE) python manage.py test)

.PHONY: coverage
coverage: # run tests with coverage
	@ ($(DOCKER_COMPOSE) exec -T $(AUTH_SERVICE) coverage run --source=auth_app manage.py test)
	@ ($(DOCKER_COMPOSE) exec -T $(AUTH_SERVICE) coverage report --omit='*/tests/*')
	@ ($(DOCKER_COMPOSE) exec -T $(CALENDAR_SERVICE) coverage run --source=calendar_app manage.py test)
	@ ($(DOCKER_COMPOSE) exec -T $(CALENDAR_SERVICE) coverage report --omit='*/tests/*')
	@ ($(DOCKER_COMPOSE) exec -T $(EMAIL_SERVICE) coverage run --source=email_app manage.py test)
	@ ($(DOCKER_COMPOSE) exec -T $(EMAIL_SERVICE) coverage report --omit='*/tests/*')

.PHONY: build-test
build-test: build test # build and run tests

.PHONY: stop-build-test
stop-build-test: stop build test # build and run tests

.PHONY: rebuild
rebuild: stop build start # rebuild and run
