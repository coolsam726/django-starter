# Dockerfile
FROM python:3.13-slim

ENV DOCKER_USER_UID=${DOCKER_USER_UID:-1000}
ENV DOCKER_USER_NAME=${DOCKER_USER_NAME:-dev}
ENV DOCKER_WSGI_WORKERS=${DOCKER_WSGI_WORKERS:-3}
ENV DOCKER_WSGI_APPLICATION=${DOCKER_WSGI_APPLICATION:-core.wsgi:application}
ENV STATIC_FILES_DIR=${STATIC_FILES_DIR:-staticfiles}


# Install system dependencies for psycopg2 and build tools
RUN apt-get update && \
    apt-get install -y gcc libpq-dev

# Install Node and npm
RUN apt-get install -y curl gnupg && \
    curl -sL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

RUN useradd -m -r -u ${DOCKER_USER_UID} ${DOCKER_USER_NAME} && \
    mkdir -p /app && \
    chown -R ${DOCKER_USER_NAME} /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install Python dependencies
COPY . /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Make static files directory if it doesn't exist
RUN mkdir -p /app/${STATIC_FILES_DIR}

RUN python manage.py collectstatic --no-input

# Change ownership of the app directory
RUN chown -R ${DOCKER_USER_NAME} /app && \
    chmod -R 775 /app

# Expose port
EXPOSE 8000

USER ${DOCKER_USER_NAME}

# Default command (can be overridden in compose)
CMD gunicorn --bind 0.0.0.0:8000 --workers ${DOCKER_WSGI_WORKERS} ${DOCKER_WSGI_APPLICATION}