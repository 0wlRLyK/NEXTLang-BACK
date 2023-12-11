DOCKER_COMPOSE_FILE = ./.build/docker-compose.yml
PROD_DOCKER_COMPOSE_FILE = ./.build/prod.docker-compose.yml

prod:
	$(eval DOCKER_COMPOSE_FILE=$(PROD_DOCKER_COMPOSE_FILE))

dev:
	$(eval DOCKER_COMPOSE_FILE=$(DOCKER_COMPOSE_FILE))

up:
	@docker-compose -f $(DOCKER_COMPOSE_FILE) up -d
	@docker images -q -f dangling=true | xargs docker rmi -f

up-build:
	@docker-compose -f $(DOCKER_COMPOSE_FILE) up -d --build
	@docker images -q -f dangling=true | xargs docker rmi -f

down:
	@docker-compose -f $(DOCKER_COMPOSE_FILE) down

down-v:
	@docker-compose -f $(DOCKER_COMPOSE_FILE) down -v

shell:
	@docker-compose -f $(DOCKER_COMPOSE_FILE) exec web python manage.py shell

bash:
	@docker-compose -f $(DOCKER_COMPOSE_FILE) exec web bash

# If the first argument is "logs"...
ifeq (logs,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "logs"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
logs:
	@docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f $(RUN_ARGS)

# If the first argument is "test"...
ifeq (logs,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "test"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
test:
	@docker-compose -f $(DOCKER_COMPOSE_FILE) run -e PYTHONDONTWRITEBYTECODE=1 --rm web python manage.py test
validate:
	@docker-compose -f $(DOCKER_COMPOSE_FILE) run -e PRE_COMMIT_HOME=/tmp --rm web pre-commit run --all-files -c .pre-commit-config.yaml

# Sphinx documentation rules

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .docs/
BUILDDIR      = .docs/_build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile
.PHONY: prod dev up up-build down down-v

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
