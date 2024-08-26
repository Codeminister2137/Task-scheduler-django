FROM python:3.10.12-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./



RUN poetry install
COPY . /app

RUN chmod 600 .my_pgpass
RUN chmod 0640 .pg_service.conf
