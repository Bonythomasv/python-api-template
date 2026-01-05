Here’s a reformatted and modified version of the README file, with clearer instructions for developers on how to build, test, lint, and deploy the code:

---

# Example Repo for Make Python DevEx

This repository contains a simple Python® project setup using the Make Python DevEx system, as described and built by Colin Dean. For more details, read the [Make Python DevEx blog post](https://tech.target.com/blog/make-python-devex).

## Quickstart

Follow these steps to set up the project and get started:

### Prerequisites

- Ensure you have [Homebrew](https://brew.sh) installed on your system.
- Make sure the `brew` command is available (`which brew`).

### Clone the Repository

You can clone the repository using either of the following commands:

```bash
# Using GitHub CLI
gh repo clone target/python-api-template

# Or using Git
git clone https://github.com/target/make-python-devex.git
```

### Install Dependencies

Run the following commands to install the necessary dependencies:

```bash
# Install dependencies
make deps

# Run test
make test

# Run test
make build

or

# to install dependencies, check the code, run tests, and build the distributable
make deps check test build

```

### Running the API Server

To run the API server, use one of the following methods:

```bash
# Using uvicorn directly
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using the script entry point
poetry run python-api-template
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs (in development mode)
- ReDoc: http://localhost:8000/redoc (in development mode)

### Building and Running Docker Images

To build and run the Docker image, use the following commands:

```bash
# Build the Docker image
docker build -t python-api-template:latest .

# Run the Docker container
docker run -p 8000:8000 python-api-template:latest
```

### Project Structure

The project uses a modern `src/` layout:

```
python-api-template/
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── main.py            # FastAPI application entry point
│   └── core/              # Core utilities and configuration
│       ├── __init__.py
│       ├── config.py      # Environment configuration
│       ├── constants.py    # Application constants
│       ├── enhanced_logging.py  # Structured JSON logging
│       └── exceptions.py   # Custom exception classes
├── tests/                 # Test files
├── build/                 # Build artifacts
├── dist/                  # Distribution packages
├── reports/               # Security and analysis reports
├── pyproject.toml         # Poetry configuration
└── Makefile               # Build automation
```

### Running the Application

After building the project, you can run the app:

```bash
# Run the app using the script entry point
poetry run python-api-template

# Or run directly with uvicorn
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Available Make Tasks

Run `make help` to see a list of available tasks in the Makefile.

#### Security Scanning

The project includes comprehensive security scanning capabilities:

```bash
# Run security vulnerability scan
make check-security

# Generate Software Bill of Materials (SBOM)
make generate-sbom

# Run comprehensive security audit
make security-audit

# Scan Docker image for vulnerabilities
make scan-image IMAGE_NAME=myimage IMAGE_TAG=mytag

# Update Trivy vulnerability database
make update-trivy-db
```

Security reports are saved to the `reports/` directory:
- `reports/trivy-vulnerabilities.json` - JSON vulnerability report
- `reports/trivy-vulnerabilities-table.txt` - Human-readable vulnerability table
- `reports/sbom-cyclonedx.json` - SBOM in CycloneDX format
- `reports/sbom-spdx.json` - SBOM in SPDX format

**Note**: The `make build` command automatically runs vulnerability checks and will fail if CRITICAL/HIGH/MEDIUM vulnerabilities are found.

### Dependency Setup

1. Run `make deps` until it succeeds, following any instructions provided during the process.
2. After dependencies are installed, run the following to check the code, run tests, and build the distributable:

```bash
make check test build
```

---

## Legal Notices

- See the [LICENSE](LICENSE.md) file for licensing information.
- "Python" and the Python logos are trademarks or registered trademarks of the Python Software Foundation, used by Target [with permission](https://www.python.org/psf/trademarks/#how-to-use-the-trademarks) from the Foundation.

---

This format makes it easier for developers to follow step-by-step instructions for setting up, testing, linting, building, and deploying the project.

Comparison between poetry and raw python

| Feature                | Poetry                          | Raw Python                       |
|------------------------|----------------------------------|----------------------------------|
| **Dependency Management** | Automatic resolution & locking | Manual (`requirements.txt`)      |
| **Virtual Environment**   | Auto-created & managed         | Manual setup (`venv`)            |
| **Packaging**             | Simplified (`poetry build`)    | Manual (`setup.py` or `wheel`)   |
| **Reproducibility**       | `poetry.lock` ensures it       | Requires manual pinning          |

Poetry:
	•	Combines multiple tools into a single CLI.
	•	Examples:
	•	poetry install: Installs dependencies and sets up the virtual environment.
	•	poetry run <command>: Runs a command inside the project’s virtual environment.
	•	poetry build: Builds a Python package.
	•	poetry publish: Publishes the package to PyPI.
Raw Python:
	•	Requires chaining multiple tools:
	•	python -m venv .venv
	•	source .venv/bin/activate
	•	pip install -r requirements.txt
	•	python setup.py sdist bdist_wheel

Comparison between poetry and makefile


| Feature                | Makefile                        | Poetry                          |
|------------------------|----------------------------------|----------------------------------|
| **Purpose**             | General-purpose task automation tool | Python-specific dependency and packaging manager |
| **Dependency Management** | Requires external tools (e.g., pip, poetry) | Built-in dependency management with locking |
| **Task Automation**     | Highly flexible, supports any type of task | Limited to Python-related tasks |
| **Ease of Use**         | Requires manual scripting       | Simplified CLI for Python tasks |
| **Virtual Environment** | Needs manual setup (`venv`)     | Automatically created and managed |
| **Packaging**           | Not designed for Python packaging | Simplified (`poetry build`)     |
| **Reproducibility**     | Relies on external tools and scripts | Ensured via `poetry.lock`       |
| **Multi-Language Support** | Yes, supports any language or tool | No, Python-specific            |


A Complete Example

We’ve launched a complete example project at https://github.com/target/make-python-devex. The only prerequisites match our standard macOS development environment: Homebrew. Run make install-homebrew after cloning this repo and follow prompts, or follow the install instructions at Homebrew’s website.
Once these files are in place, you’ll
run make deps until it exits successfully, following prompts with each failure
run make deps check test build ARTIFACT_VERSION=0.0.1 to see all deps installed, checks and test pass, and produce a build in the dist directory.
run poetry run example-make-python-devex to actually see what the program does.


# Why Use the Make Python DevEx Project Structure?

Here are 5-6 reasons why this project structure is more beneficial compared to a simple raw Python project structure:

---

## 1. Improved Developer Experience

The **Make Python DevEx** project structure is designed with a focus on enhancing the developer experience by:

- Streamlining repetitive tasks with `Makefile` commands.
- Providing intuitive, documented commands like `make deps`, `make test`, and `make build` that abstract away complex workflows.

---

## 2. Consistent Dependency Management

- By integrating **Poetry**, the project ensures consistent dependency management with a `pyproject.toml` file and a `poetry.lock` file.
- This eliminates the manual maintenance of `requirements.txt` files, reduces conflicts, and ensures reproducibility across environments.

---

## 3. Simplified Task Automation

- The `Makefile` serves as a one-stop-shop for automating common project tasks like testing, linting, building, and deployment.
- Developers don’t need to memorize or manually run multiple complex commands, which reduces cognitive overhead.

---

## 4. Enhanced Reproducibility

- With `poetry.lock`, all dependencies and their versions are locked, ensuring that the same versions are installed across all environments.
- This consistency is difficult to achieve with raw Python projects unless managed manually.

---

## 5. Standardized Project Structure

- The **Make Python DevEx** structure enforces a standardized layout, making it easier for new developers to onboard.
- Features like the `dist/` directory for builds and predefined `Makefile` targets create a predictable and organized workflow.

---

## 6. Cross-Environment Compatibility

- This structure is designed to work seamlessly in local development, CI/CD pipelines, and production environments.
- The use of `Makefile` and **Poetry** allows the project to adapt to various platforms and tools without significant changes to the workflow.

---

## Bonus: Extensible and Scalable

- The structure is easily extendable to include more tools and features as the project grows (e.g., integrating Docker for containerization or CI pipelines).
- It’s suitable for both small and large teams, as it enforces consistency and best practices.

---

## Conclusion

By combining **Poetry**, `Makefile`, and well-defined processes, the **Make Python DevEx** structure provides a robust, scalable, and developer-friendly foundation for Python projects that outshines the simplicity of raw Python projects.

## Security Features

This template includes comprehensive security features:

- **Vulnerability Scanning**: Automated Trivy scanning for dependencies and filesystem
- **SBOM Generation**: Software Bill of Materials in CycloneDX and SPDX formats
- **Build-time Checks**: Automatic vulnerability checks during build process
- **Structured Logging**: JSON-formatted logs with ECS (Elastic Common Schema) format
- **Input Validation**: Request validation with detailed error messages
- **CORS Configuration**: Configurable Cross-Origin Resource Sharing settings

## Development Features

- **Type Checking**: MyPy integration with comprehensive type stubs
- **Code Formatting**: Black and Ruff for consistent code style
- **Testing**: Pytest with coverage reporting and multiple output formats
- **Async Support**: Full async/await support with strict asyncio mode
- **Environment Management**: Flexible environment variable configuration
- **Error Handling**: Custom exception classes with structured error responses
