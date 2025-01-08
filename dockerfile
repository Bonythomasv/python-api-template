# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to ensure Python runs in an unbuffered mode and doesn't create .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the pre-built .whl file into the container
COPY dist/example-0.0.0-py3-none-any.whl /app/

# Install the .whl file
RUN pip install --no-cache-dir /app/example-0.0.0-py3-none-any.whl

# Expose the port if the application runs on a specific one
EXPOSE 8000

# Define the default command to run your application
CMD ["uvicorn", "example:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
