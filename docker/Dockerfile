FROM python:3.10.12-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry


COPY . .

RUN poetry install
ENTRYPOINT ["poetry", "run", "python", "manage.py", "runserver", "localhost:8000"]