FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .
ENTRYPOINT ["uv", "run", "granian", "--interface", "asgi", "--host", "0.0.0.0", "--port", "8000", "main:app"]
