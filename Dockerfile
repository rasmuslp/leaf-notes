FROM python:3.9.6-slim as builder

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \ 
        git \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv .venv
RUN . .venv/bin/activate
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt && pip uninstall Jetson.GPIO

###

FROM python:3.9.6-slim as runner

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/.venv /usr/src/app/.venv

# COPY . .