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

# Install uv
RUN pip install uv

# Set UV environment variables for Docker
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_CACHE_DIR=/tmp/uv-cache

COPY pyproject.toml uv.lock ./
# Install dependencies using uv with explicit system interpreter
RUN uv sync --frozen --no-dev --python /usr/local/bin/python3

COPY . ${APP_ROOT}

# Ensure no conflicting virtual environment exists and clean up cache
RUN rm -rf .venv && rm -rf /tmp/uv-cache

RUN uv run python manage.py collectstatic --noinput
# Expose the port that the app runs on
EXPOSE 8000

CMD ["uv", "run", "gunicorn", "-c", "gunicorn.conf.py", "config.wsgi:application"]
