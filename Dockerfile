# Base definition
FROM python:3.9.6-slim-buster as base

LABEL org.opencontainers.image.source=https://github.com/rasmuslp/leaf-notes

WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Builder
FROM base as builder

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install \
	build-essential \
    cmake \
    ghostscript \
    git \
    libffi-dev \
    libfreetype6-dev \
    libfribidi-dev \
    libharfbuzz-dev \
    libjpeg-turbo-progs \
    libjpeg62-turbo-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    netpbm \
    python3-dev \
    python3-numpy \
    python3-pyqt5 \
    python3-scipy \
    python3-setuptools \
    python3-tk \
    sudo \
    tcl8.6-dev \
    tk8.6-dev \
    virtualenv \
    wget \
    xvfb \
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

COPY common/ common/
COPY display/ display/
COPY notes/ notes/

ENV PYTHONUNBUFFERED=1
