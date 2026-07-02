.PHONY: help build-dev clean format check test

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

clean: ## Remove dev Docker image and local cache artifacts
	@echo "Removing $(DEV_IMAGE) image..."
	-docker rmi $(DEV_IMAGE)
	@echo "Removing cache directories..."
	@rm -rf .pytest_cache .ruff_cache .mypy_cache
	@find . -type d -name __pycache__ -not -path './.venv/*' -print0 | xargs -0 rm -rf 2>/dev/null || true
	@echo "Clean complete."

format: build-dev ## Apply code formatting
	$(DOCKER_RUN) ./scripts/format.sh

check: build-dev ## Verify formatting and run linter
	$(DOCKER_RUN) ./scripts/format-check.sh
	$(DOCKER_RUN) ./scripts/lint.sh

test: build-dev check ## Run unit tests
	$(DOCKER_RUN) ./scripts/test.sh
