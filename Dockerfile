# Dockerfile
FROM python:3.13-slim

ARG DOCKER_USER_UID=1000
ENV DOCKER_USER_NAME=${DOCKER_USER_NAME:-dev}
ENV DOCKER_WSGI_WORKERS=${DOCKER_WSGI_WORKERS:-3}
ENV DOCKER_WSGI_APPLICATION=${DOCKER_WSGI_APPLICATION:-core.wsgi:application}
ARG STATIC_FILES_DIR=staticfiles
ARG WWW_USER_ID=33
ENV STATIC_FILES_DIR=${STATIC_FILES_DIR}
ENV WWW_USER_ID=${WWW_USER_ID}
ENV DOCKER_USER_UID=${DOCKER_USER_UID}


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
# Create www-data user if it doesn't exist
RUN if ! id -u www-data >/dev/null 2>&1; then \
        useradd -r -u ${WWW_USER_ID} www-data; \
    fi
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install Python dependencies
COPY . /app/
RUN mkdir -p /app/${STATIC_FILES_DIR}

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN chown ${DOCKER_USER_NAME} /usr/local/bin/docker-entrypoint.sh
RUN chown ${DOCKER_USER_NAME}  /app
RUN chown ${WWW_USER_ID}:${DOCKER_USER_NAME} /app/${STATIC_FILES_DIR}
RUN chmod 775 /app/${STATIC_FILES_DIR}
    # Expose port
EXPOSE 8000

USER ${DOCKER_USER_NAME}

WORKDIR /app

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
# Default command (can be overridden in compose)
CMD gunicorn --bind 0.0.0.0:8000 --workers ${DOCKER_WSGI_WORKERS} ${DOCKER_WSGI_APPLICATION}