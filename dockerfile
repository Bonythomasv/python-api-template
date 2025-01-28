# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables to ensure Python runs in an unbuffered mode and doesn't create .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1

# Set the working directory in the container
WORKDIR /app

# Copy the pre-built .whl file into the container
COPY dist/*.whl /app/

# Install the pre-built .whl file dynamically
RUN pip install --no-cache-dir --root-user-action=ignore --progress-bar off /app/*.whl

# Debug Python version (optional)
RUN python --version && pip --version

# Expose the port if the application runs on a specific one
EXPOSE 8000

# Define the default command to run your application
CMD ["uvicorn", "python_api_template:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
