# Python API Template

A production-ready Python FastAPI template with comprehensive security scanning, structured logging, middleware, and modern development tooling. Built following the Make Python DevEx best practices.

## 🚀 Features

### Core Application Features

- **FastAPI Framework**: Modern, fast web framework for building APIs with automatic OpenAPI documentation
- **Structured Logging**: JSON-formatted logs with ECS (Elastic Common Schema) format for better observability
- **Request/Response Logging**: Automatic logging of all incoming requests and responses with performance metrics
- **Request ID Tracking**: Unique request IDs for tracing requests through the system
- **Custom Exception Handling**: Structured error responses with proper HTTP status codes
- **Environment-based Configuration**: Flexible configuration management using environment variables
- **Async/Await Support**: Full async support with strict asyncio mode for optimal performance

### Security Features

- **Trivy Vulnerability Scanning**: Comprehensive security scanning for dependencies, filesystem, secrets, and misconfigurations
- **SBOM Generation**: Software Bill of Materials in CycloneDX and SPDX formats for compliance
- **Build-time Security Checks**: Automatic vulnerability checks during build process (blocks on CRITICAL/HIGH/MEDIUM)
- **Docker Image Scanning**: Scan container images for vulnerabilities before deployment
- **Secret Detection**: Automated scanning for exposed secrets and credentials
- **CORS Configuration**: Configurable Cross-Origin Resource Sharing settings
- **Request Size Limits**: Protection against oversized request payloads
- **Input Validation**: Request validation with detailed error messages
- **Security Headers**: Automatic security headers in responses

### Middleware & Request Handling

- **CORS Middleware**: Configurable cross-origin resource sharing
- **Request Size Limiting**: Protection against oversized requests
- **Rate Limiting**: Configurable rate limiting (ready for implementation)
- **JWT Authorization**: JWT token validation middleware (ready for implementation)
- **Permission Authorization**: Role-based access control middleware (ready for implementation)
- **Request Logging Middleware**: Detailed request/response logging with performance metrics

### Development Tools

- **Poetry**: Modern dependency management with lock file support
- **Type Checking**: MyPy integration with comprehensive type stubs
- **Code Formatting**: Black for consistent code style
- **Linting**: Ruff for fast linting and style checking
- **Testing**: Pytest with coverage reporting and multiple output formats (HTML, JUnit, TAP)
- **Pre-commit Hooks**: Automated code quality checks before commits
- **Makefile Automation**: Comprehensive task automation for common development tasks

### CI/CD Integration

- **GitLab CI/CD**: Complete pipeline with test, security scanning, and build stages
- **Automated Security Scanning**: Trivy scans in CI pipeline
- **Docker Image Building**: Automated container image builds
- **Artifact Management**: Build artifacts and reports saved as CI artifacts
- **Multi-stage Pipeline**: Separate stages for test, security, and build

### Project Structure

- **src/ Layout**: Modern Python project structure with source directory
- **Modular Architecture**: Organized core modules (config, logging, exceptions, constants)
- **Separation of Concerns**: Clear separation between application logic and infrastructure
- **Scalable Structure**: Easy to extend with new features and modules

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Configuration](#configuration)
- [Security Scanning](#security-scanning)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Building & Deployment](#building--deployment)
- [Available Make Targets](#available-make-targets)
- [Troubleshooting](#troubleshooting)

## 🏃 Quick Start

### Prerequisites

- [Homebrew](https://brew.sh) installed (macOS) or appropriate package manager (Linux)
- Python 3.9-3.13
- Make

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd python-api-template

# Install all dependencies
make deps

# Run checks, tests, and build
make check test build
```

### Running the API Server

```bash
# Using uvicorn directly
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using the script entry point
poetry run python-api-template

# Or using make
make start
```

The API will be available at:
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **OpenAPI Docs**: http://localhost:8000/docs (if enabled)
- **ReDoc**: http://localhost:8000/redoc (if enabled)

## 📁 Project Structure

```
python-api-template/
├── src/                           # Source code
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   └── core/                     # Core utilities and configuration
│       ├── __init__.py
│       ├── config.py             # Environment configuration management
│       ├── constants.py          # Application constants (HTTP messages, API paths, etc.)
│       ├── enhanced_logging.py   # Structured JSON logging with ECS format
│       └── exceptions.py        # Custom exception classes
├── tests/                        # Test files
├── build/                        # Build artifacts
├── dist/                         # Distribution packages
├── reports/                      # Security and analysis reports
│   ├── trivy-vulnerabilities.json
│   ├── trivy-vulnerabilities-table.txt
│   ├── sbom-cyclonedx.json
│   └── sbom-spdx.json
├── .gitlab-ci.yml               # GitLab CI/CD pipeline configuration
├── .pre-commit-config.yaml      # Pre-commit hooks configuration
├── .trivyignore                 # Trivy ignore patterns
├── pyproject.toml               # Poetry configuration and dependencies
├── poetry.lock                  # Locked dependency versions
├── Dockerfile                   # Docker container definition
├── Makefile                     # Build automation and task runner
└── README.md                    # This file
```

## 🔧 Development Workflow

### Standard Development Cycle

```bash
# 1. Install/update dependencies
make deps

# 2. Run code quality checks
make check

# 3. Run tests
make test

# 4. Run security scans
make check-security

# 5. Build the project
make build
```

### Code Quality

The project uses multiple tools to ensure code quality:

- **Ruff**: Fast Python linter and formatter
- **Black**: Opinionated code formatter (119 character line length)
- **MyPy**: Static type checker with strict settings
- **Pytest**: Testing framework with coverage reporting

```bash
# Run all checks
make check

# Run specific checks
make check-py-ruff-format    # Linting and formatting
make check-py-mypy           # Type checking
make check-py-black-format   # Format code with Black
```

### Pre-commit Hooks

Pre-commit hooks automatically run checks before commits:

```bash
# Install pre-commit hooks
make install-precommit

# Run pre-commit hooks manually
make check-precommit
```

## ⚙️ Configuration

### Environment Variables

The application uses environment variables for configuration. Create a `.env` file or set environment variables:

```bash
# Environment
ENVIRONMENT=development  # development, staging, production

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Security
DISABLE_JWT_VALIDATION=false
REQUEST_SIZE_LIMIT_BYTES=10485760  # 10MB

# Rate Limiting
RATE_LIMIT_ENABLED=true

# Database (if needed)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Logging
LOG_LEVEL=INFO
```

See `src/core/config.py` for all available configuration options.

### Logging Configuration

The application uses structured JSON logging with ECS format:

- **Console Output**: JSON-formatted logs for easy parsing
- **File Logging**: Rotating file handlers for log persistence
- **Log Levels**: Configurable via `LOG_LEVEL` environment variable
- **Request Logging**: Automatic logging of all requests with:
  - Request ID
  - Client IP
  - HTTP method and path
  - Response status code
  - Request duration
  - User agent

## 🔒 Security Scanning

### Trivy Integration

The project includes comprehensive Trivy security scanning:

```bash
# Run comprehensive security scan (vulnerabilities + secrets + misconfig)
make check-security

# Run vulnerability scan only
make check-security-trivy

# Generate Software Bill of Materials (SBOM)
make generate-sbom

# Scan Docker image
make scan-image IMAGE_NAME=python-api-template IMAGE_TAG=latest

# Update Trivy vulnerability database
make update-trivy-db
```

### Security Reports

Security reports are saved to the `reports/` directory:

- `reports/trivy-vulnerabilities.json` - JSON vulnerability report
- `reports/trivy-vulnerabilities-table.txt` - Human-readable vulnerability table
- `reports/sbom-cyclonedx.json` - SBOM in CycloneDX format
- `reports/sbom-spdx.json` - SBOM in SPDX format

### Build-time Security Checks

The `make build` command automatically runs vulnerability checks and will **fail** if CRITICAL/HIGH/MEDIUM vulnerabilities are found. This ensures vulnerable dependencies cannot be deployed.

### Ignoring False Positives

Add patterns to `.trivyignore` to ignore false positives:

```
# .trivyignore
CVE-2023-1234  # Known false positive
CVE-2023-5678  # Already patched in our version
```

## 📚 API Documentation

### OpenAPI/Swagger Documentation

When enabled, the API provides automatic OpenAPI documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Endpoints

The template includes example endpoints. Add your own endpoints in `src/main.py`.

### Request/Response Format

All API responses follow a consistent format:

```json
{
  "detail": "Error message or validation errors",
  "message": "Human-readable message",
  "status_code": 422
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run unit tests only
make test-unittests

# Run with coverage
make test-coverage

# Run specific test file
poetry run pytest tests/test_specific.py
```

### Test Output Formats

Tests generate reports in multiple formats:

- **HTML**: `build/report.html` - Interactive HTML report
- **JUnit XML**: `build/report.junit.xml` - For CI/CD integration
- **TAP**: `build/*.tap` - Test Anything Protocol format
- **Coverage**: `build/coverage/` - Coverage reports

### Test Configuration

Test configuration is in `pyproject.toml`:

- **Async Mode**: Strict asyncio mode for async tests
- **Coverage**: Branch coverage enabled
- **Markers**: Integration and unit test markers available

## 🏗️ Building & Deployment

### Building the Project

```bash
# Build distributable package
make build

# Build with specific version
make build ARTIFACT_VERSION=1.0.0
```

Build artifacts are created in the `dist/` directory.

### Docker

#### Building Docker Image

```bash
# Build the Docker image
docker build -t python-api-template:latest .

# Or using make
make docker-build
```

#### Running Docker Container

```bash
# Run the container
docker run -p 8000:8000 python-api-template:latest

# Run with environment variables
docker run -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e ALLOWED_ORIGINS=https://example.com \
  python-api-template:latest
```

#### Scanning Docker Images

```bash
# Scan image for vulnerabilities
make scan-image IMAGE_NAME=python-api-template IMAGE_TAG=latest
```

### CI/CD Pipeline

The project includes a complete GitLab CI/CD pipeline (`.gitlab-ci.yml`) with:

1. **Test Stage**: Run tests and code quality checks
2. **Security Scan Stage**: Trivy vulnerability scanning and SBOM generation
3. **Build Stage**: Build Docker image and scan for vulnerabilities

The pipeline automatically:
- Runs on every push
- Blocks deployment on security vulnerabilities
- Generates and stores security reports
- Builds and pushes Docker images (when configured)

## 📝 Available Make Targets

Run `make help` to see all available targets. Key targets include:

### Development
- `make deps` - Install all dependencies
- `make check` - Run all code quality checks
- `make test` - Run tests
- `make build` - Build the project
- `make start` - Start the API server

### Security
- `make check-security` - Comprehensive security scan
- `make check-security-trivy` - Vulnerability scan only
- `make generate-sbom` - Generate SBOM files
- `make scan-image` - Scan Docker image
- `make update-trivy-db` - Update Trivy database

### Code Quality
- `make check-py-ruff-format` - Run Ruff linter
- `make check-py-black-format` - Run Black formatter
- `make check-py-mypy` - Run MyPy type checker
- `make check-precommit` - Run pre-commit hooks

### Dependencies
- `make deps-py` - Install Python dependencies
- `make deps-brew` - Install Homebrew dependencies
- `make poetry-update` - Update Poetry dependencies
- `make poetry-relock` - Relock Poetry dependencies

### Docker
- `make docker-build` - Build Docker image
- `make docker-run` - Run Docker container

## 🐛 Troubleshooting

### Common Issues

#### Poetry Command Not Found
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

#### Pyenv Version Not Found
```bash
# Install Python version
pyenv install 3.13
pyenv local 3.13
```

#### Security Vulnerabilities Blocking Build
```bash
# Update vulnerable dependencies
make poetry-update PKGS="package-name"

# Or update all dependencies
make poetry-update
```

#### Trivy Database Update Issues
```bash
# Update Trivy database manually
make update-trivy-db
```

## 📦 Dependencies

### Production Dependencies

- **FastAPI** (^0.116.0): Modern web framework
- **Pydantic** (^2.10.4): Data validation
- **Uvicorn** (^0.34.0): ASGI server
- **Starlette** (^0.49.1+): Web framework (via FastAPI)
- **Jinja2** (^3.1.6+): Template engine
- **h11** (^0.16.0+): HTTP/1.1 protocol implementation

### Development Dependencies

- **Pytest**: Testing framework
- **Black**: Code formatter
- **Ruff**: Linter and formatter
- **MyPy**: Type checker
- **Pytest-cov**: Coverage reporting
- **Pre-commit**: Git hooks

See `pyproject.toml` for the complete list of dependencies.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make check test build` to ensure everything passes
5. Submit a pull request

## 📄 License

See the [LICENSE](LICENSE.md) file for licensing information.

## 🙏 Acknowledgments

- Built following the [Make Python DevEx](https://tech.target.com/blog/make-python-devex) best practices
- Uses [Poetry](https://python-poetry.org/) for dependency management
- Security scanning powered by [Trivy](https://github.com/aquasecurity/trivy)
- "Python" and the Python logos are trademarks or registered trademarks of the Python Software Foundation

---

**Note**: This template is designed for production use with comprehensive security, logging, and development tooling. Customize it to fit your specific needs while maintaining the security and quality standards.
