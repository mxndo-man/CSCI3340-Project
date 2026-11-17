FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

WORKDIR /app 

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

# ensure it copies from the cache
ENV UV_LINK_MODE=copy

ENV UV_NO_DEV=1


RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY . /app

RUN uv sync --frozen 

EXPOSE 8000

ENTRYPOINT []

ENV PATH="/app/.venv/bin:$PATH"


CMD ["python","manage.py", "runserver" , "0.0.0.0:8000"]

