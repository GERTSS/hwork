FROM python:3.12.3-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    mkdir -p /root/.local/share/pypoetry && \
    pip install poetry
    
ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry --version

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-root --no-interaction --no-ansi --no-cache

COPY . .

EXPOSE 8000

CMD ["sh", "-c", \
"python manage.py makemigrations && \
python manage.py migrate && \
python manage.py create_orders && \
python manage.py create_products && \
gunicorn --bind 0.0.0.0:8000 config.wsgi""]
