# Variables
DOCKER_COMPOSE=docker-compose

.PHONY: start
start: ## start containers
	@ ($(DOCKER_COMPOSE) up -d)

.PHONY: stop
stop: ## stop containers
	@ ($(DOCKER_COMPOSE) down)