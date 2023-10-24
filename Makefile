up:
	@docker-compose -f ./.build/docker-compose.yml up -d
	@docker images -q -f dangling=true | xargs docker rmi -f

up-build:
	@docker-compose -f ./.build/docker-compose.yml up -d --build
	@docker images -q -f dangling=true | xargs docker rmi -f

down:
	@docker-compose -f ./.build/docker-compose.yml down

down-v:
	@docker-compose -f ./.build/docker-compose.yml down -v

shell:
	@docker-compose -f ./.build/docker-compose.yml exec web python manage.py shell_plus

bash:
	@docker-compose -f ./.build/docker-compose.yml exec web bash

# If the first argument is "logs"...
ifeq (logs,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "logs"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
logs:
	@docker-compose -f ./.build/docker-compose.yml logs -f $(RUN_ARGS)

# If the first argument is "test"...
ifeq (logs,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "test"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
test:
	@docker-compose -f ./.build/docker-compose.yml run -e PYTHONDONTWRITEBYTECODE=1 --rm web python manage.py test
validate:
	@docker-compose -f ./.build/docker-compose.yml run -e PRE_COMMIT_HOME=/tmp --rm web pre-commit run --all-files -c .pre-commit-config.yaml

# Sphinx documentation rules

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .docs/
BUILDDIR      = .docs/_build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile


%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
