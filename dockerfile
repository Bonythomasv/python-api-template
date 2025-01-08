# Use Python 3.13 as the base image
FROM python:3.13-slim

# Set environment variables to reduce threading
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONTHREADDEBUG=1
ENV PYTHONNOUSERSITE=1
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1

# Set the working directory in the container
WORKDIR /app

# Upgrade pip, setuptools, and wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Debug threading
RUN python -c "import threading; print(f'Max threads: {threading.active_count()}')"

# Copy the pre-built .whl file into the container
COPY dist/example-0.0.0-py3-none-any.whl /app/

# Install the .whl file with reduced threading
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver --progress-bar off --no-build-isolation /app/example-0.0.0-py3-none-any.whl

# Expose the port if the application runs on a specific one
EXPOSE 8000

# Define the default command to run your application
CMD ["uvicorn", "example:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
