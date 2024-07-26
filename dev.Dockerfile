FROM python:3.11.9

WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv "$VIRTUAL_ENV"
COPY requirements.txt ./
COPY dev-requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r dev-requirements.txt
