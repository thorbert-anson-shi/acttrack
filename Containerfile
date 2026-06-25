FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .
ENTRYPOINT ["uv", "run", "granian", "--interface", "asgi", "--host", "::", "--port", "8000", "main:app"]
