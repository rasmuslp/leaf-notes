# Base definition
FROM python:3.9.6-slim as base
WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Builder
FROM base as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \ 
        git \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv "$VIRTUAL_ENV"
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y Jetson.GPIO \
    && find "$VIRTUAL_ENV" -type d -name __pycache__ -prune -exec rm -rf '{}' \; \
    && find "$VIRTUAL_ENV" -type d -name .git -prune -exec rm -rf '{}' \; \
    && rm -rf "$VIRTUAL_ENV"/src/waveshare-epd/Arduino \
    && rm -rf "$VIRTUAL_ENV"/src/waveshare-epd/RaspberryPi_JetsonNano/c \
    && rm -rf "$VIRTUAL_ENV"/src/waveshare-epd/RaspberryPi_JetsonNano/python/examples \
    && rm -rf "$VIRTUAL_ENV"/src/waveshare-epd/RaspberryPi_JetsonNano/python/pic \
    && rm -rf "$VIRTUAL_ENV"/src/waveshare-epd/RaspberryPi_JetsonNano/python/readme* \
    && rm -rf "$VIRTUAL_ENV"/src/waveshare-epd/STM32

# Runner
FROM base as runner

COPY --from=builder /usr/src/app/.venv /usr/src/app/.venv

# COPY . .