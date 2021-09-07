# Base definition
FROM python:3.9.6-slim as base

LABEL org.opencontainers.image.source=https://github.com/rasmuslp/leaf-notes

WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Builder
FROM base as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg-turbo-progs \
        libjpeg62-turbo-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv "$VIRTUAL_ENV"
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && find "$VIRTUAL_ENV" -type d -name __pycache__ -prune -exec rm -rf '{}' \;

# Runner
FROM base as runner

COPY --from=builder /usr/src/app/.venv /usr/src/app/.venv

COPY common/ .
COPY display/ .
COPY notes/ .

ENV PYTHONUNBUFFERED=1
