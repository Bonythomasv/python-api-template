# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to ensure Python runs in an unbuffered mode and doesn't create .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
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

# Install Python dependencies
RUN pip install --no-cache-dir poetry \
    && poetry install --no-dev

# Expose the port if the application runs on a specific one
EXPOSE 8000

# Define the default command to run your application
# CMD ["python3", "-m", "example"]
CMD ["poetry", "run", "uvicorn", "example:app", "--reload", "--host", "0.0.0.0"]
