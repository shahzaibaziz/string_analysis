.PHONY: help format check test

DEV_IMAGE := string_analysis-dev
DOCKER_RUN := docker run --rm -e STRING_ANALYSIS_USE_PATH=1 -v "$(CURDIR):/app" -w /app $(DEV_IMAGE)

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

build-dev: ## Build dev/CI Docker image if not already built
	@if ! docker image inspect $(DEV_IMAGE) >/dev/null 2>&1; then \
		echo "Building $(DEV_IMAGE)..."; \
		docker build -f dockerfile.dev -t $(DEV_IMAGE) .; \
	else \
		echo "$(DEV_IMAGE) already built"; \
	fi


format: build-dev ## Apply code formatting
	$(DOCKER_RUN) ./scripts/format.sh

check: format ## Verify formatting and run linter
	$(DOCKER_RUN) ./scripts/format-check.sh
	$(DOCKER_RUN) ./scripts/lint.sh

test: check ## Run unit tests
	$(DOCKER_RUN) ./scripts/test.sh
