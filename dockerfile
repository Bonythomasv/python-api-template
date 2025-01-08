# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to ensure Python runs in an unbuffered mode and doesn't create .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install runtime dependencies including the debian-archive-keyring package
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    debian-archive-keyring \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Update APT sources with the installed keyring
RUN echo "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list \
    && echo "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://deb.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list \
    && echo "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://deb.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list

# Install additional runtime dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the pre-built .whl file into the container
COPY dist/example-0.0.0-py3-none-any.whl /app/

# Install the .whl file
RUN pip install --no-cache-dir /app/example-0.0.0-py3-none-any.whl

# Expose the port if the application runs on a specific one
EXPOSE 8000

# Define the default command to run your application
CMD ["uvicorn", "example:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
