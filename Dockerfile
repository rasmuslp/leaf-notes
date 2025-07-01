# Base definition
FROM python:3.11.13-slim-bookworm AS base

WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Builder
FROM base AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv "$VIRTUAL_ENV"
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && find "$VIRTUAL_ENV" -type d -name __pycache__ -prune -exec rm -rf '{}' \;

# Runner
FROM base AS runner

COPY --from=builder /usr/src/app/.venv /usr/src/app/.venv

COPY common/ common/
COPY display/ display/
COPY notes/ notes/

ENV PYTHONUNBUFFERED=1
