FROM python:3.11-slim-buster

ENV POETRY_VERSION "~=1.5.1"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apt-get update && \
  apt-get install --no-install-recommends -y postgresql postgresql-contrib python-psycopg2 libpq-dev gcc musl-dev libc-dev libffi-dev libssl-dev cargo wget make wait-for-it curl git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/app

COPY start.sh poetry.lock pyproject.toml ./
COPY alembic.ini /etc/chat/alembic.ini
COPY chat /srv/app/chat

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install

EXPOSE 8080

CMD ["/bin/bash", "start.sh"]

ENV TZ="UTC"
