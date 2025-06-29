FROM --platform=linux/amd64 python:3.13-slim-bookworm

# Install system dependencies for PostGIS, psycopg2, and other potential needs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    geos-bin \
    libgeos-dev \
    proj-bin \
    libproj-dev \
    # Clean up apt lists to reduce image size
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV APP_ROOT=/app
WORKDIR ${APP_ROOT}

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
# Ensure psycopg2-binary is in your pyproject.toml
# Add it using: poetry add psycopg2-binary
RUN poetry install --no-interaction --no-root --no-cache

COPY . ${APP_ROOT}

RUN python manage.py collectstatic --noinput
# Expose the port that the app runs on
EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "config.wsgi:application"]
