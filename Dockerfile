FROM python:3.12.3-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libpq-dev && \
    pip install poetry psycopg

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-root --no-interaction --no-ansi --no-cache

COPY . .

EXPOSE 8000

CMD ["sh", "-c", \
"python /app/mysite/manage.py makemigrations && \
python /app/mysite/manage.py migrate && \
python /app/mysite/manage.py create_orders && \
python /app/mysite/manage.py create_products && \
gunicorn --bind 0.0.0.0:8000 config.wsgi""]