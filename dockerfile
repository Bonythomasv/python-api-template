# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to ensure Python runs in an unbuffered mode and doesn't create .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including gnupg
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gnupg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add the missing Debian GPG keys (with checks)
RUN if [ ! -f /usr/share/keyrings/debian-archive-keyring.gpg ]; then \
      curl -fsSL https://ftp-master.debian.org/keys/archive-key-12.asc | gpg --batch --no-tty --dearmor -o /usr/share/keyrings/debian-archive-keyring.gpg; \
    fi \
    && if [ ! -f /usr/share/keyrings/debian-archive-keyring-13.gpg ]; then \
      curl -fsSL https://ftp-master.debian.org/keys/archive-key-13.asc | gpg --batch --no-tty --dearmor -o /usr/share/keyrings/debian-archive-keyring-13.gpg; \
    fi

# Update APT sources with the new GPG keys
RUN echo "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list \
    && echo "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://deb.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list \
    && echo "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://deb.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list

# Install additional packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project files to the container
COPY pyproject.toml README.md LICENSE.md Makefile .editorconfig .pre-commit-config.yaml .python-version /app/
COPY example/ /app/example/
COPY tests/ /app/tests/
COPY .github/ /app/.github/

# Install Poetry and check version
RUN pip install --no-cache-dir poetry \
    && poetry self update

# Install Python dependencies (without dev dependencies)
RUN poetry install --without dev

# Expose the port if the application runs on a specific one
EXPOSE 8000

# Define the default command to run your application
CMD ["poetry", "run", "uvicorn", "example:app", "--reload", "--host", "0.0.0.0"]
