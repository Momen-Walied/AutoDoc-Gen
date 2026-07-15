# AutoDoc-Gen: Dynamic Tech Documentation & Architecture Generator

A production-grade system that ingests a public GitHub repository URL, clones and chunks the codebase, runs a CrewAI multi-agent pipeline to generate architecture documentation and Mermaid.js C4 diagrams, and exposes a FastAPI gateway backed by Temporal.io workflows.

## Architecture Highlights

- **FastAPI** — thin, async HTTP gateway.
- **Temporal.io** — durable workflow orchestration with retries, state preservation, and Human-in-the-Loop signals.
- **CrewAI + LiteLLM** — multi-agent AI layer with Tiered LLM Routing.
- **PostgreSQL** — metadata and state persistence.
- **Amazon S3** — generated Markdown/Mermaid artifact storage.
- **Langtrace** — LLM call observability (tokens, latency, cost).

## Documentation

- [`docs/project_infra.md`](docs/project_infra.md) — system architecture, clean-code guidelines, design patterns, and folder structure.
- [`docs/implementation_phases.md`](docs/implementation_phases.md) — phased implementation plan with acceptance criteria.

## Quick Start

```bash
# 1. Install uv (https://docs.astral.sh/uv/)
# 2. Create the virtual environment with Python 3.12
uv venv --python 3.12 .venv

# 3. Install dependencies
uv sync --extra dev

# 4. Copy environment variables
cp .env.example .env
# Edit .env with your provider keys and endpoints

# 5. Run database migrations
uv run alembic upgrade head

# 6. Start Temporal (if not using Docker Compose)
./scripts/start_temporal.sh

# 7. Start the API
uv run uvicorn src.api.main:create_app --factory --reload

# 8. In another shell, start the Temporal worker
uv run python -m src.workflows.worker
```

## Development

```bash
# Type checking
uv run mypy --strict src

# Linting
uv run ruff check .

# Tests
uv run pytest

# Tests with coverage
uv run pytest --cov=src --cov-report=term-missing
```

## License

MIT
