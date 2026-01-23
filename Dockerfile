FROM python:3.11-slim

WORKDIR /app

# Install git for git dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
# --frozen ensures we use the exact versions from uv.lock
RUN uv sync --frozen --no-install-project

# Copy source code
COPY src ./src

# Install the project itself
RUN uv sync --frozen

# Place the virtual environment in the path
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uvicorn", "omni_osint_query.main:app", "--host", "0.0.0.0", "--port", "8000"]
