# Base definition
FROM python:3.11.9-alpine AS base

WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Builder
FROM base AS builder

RUN apk add --update --no-cache \
    build-base python3-dev \
    freetype-dev jpeg-dev zlib-dev musl-dev \
    libffi-dev openssl-dev

RUN python -m venv "$VIRTUAL_ENV"
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && find "$VIRTUAL_ENV" -type d -name __pycache__ -prune -exec rm -rf '{}' \;

### Runner
FROM base AS runner

RUN apk add --update --no-cache freetype libjpeg

COPY --from=builder /usr/src/app/.venv /usr/src/app/.venv

COPY common/ common/
COPY display/ display/
COPY notes/ notes/

ENV PYTHONUNBUFFERED=1
