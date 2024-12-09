include .env
# Variables
DOCKER_COMPOSE=docker-compose
DATABASE=db
BACKEND=web


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
	@ ($(DOCKER_COMPOSE) exec $(BACKEND) /bin/bash)

.PHONY: shell_db
shell_db: ## open database console
	@ ($(DOCKER_COMPOSE) exec $(DATABASE) psql -U ${POSTGRES_USER} ${POSTGRES_DB})

.PHONY: migration
migration: ## create migration
	@ ($(DOCKER_COMPOSE) exec -it $(BACKEND) python manage.py makemigrations)

.PHONY: migrate
migrate: ## migrate database
	@ ($(DOCKER_COMPOSE) exec -it $(BACKEND) python manage.py migrate)


.PHONY: test
test: # run tests
	@ ($(DOCKER_COMPOSE) exec -it $(BACKEND) poetry run python manage.py test)

.PHONY: build-test
build-test: build test # build and run tests

.PHONY: stop-build-test
stop-build-test: stop build test # build and run tests

.PHONY: rebuild
rebuild: stop build start # rebuild and run
