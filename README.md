# GitHub Profile Explorer API

A REST API built with **FastAPI** that fetches and analyzes GitHub user data using the **GitHub REST API**.

This project follows a layered architecture where API routes, business logic, and response models are separated for better readability, maintainability, and scalability.

---

# Features

- Fetch GitHub user profile information
- Fetch all public repositories
- Repository pagination using `page` and `per_page`
- GitHub API pagination
- Repository statistics
  - Total stars
  - Languages used
  - Most used language

- Repository filtering
  - Language (case-insensitive)
  - Visibility

- Repository sorting
  - Name
  - Stars
  - Forks
  - Last Updated

- Repository ordering
  - Ascending
  - Descending

- FastAPI query parameter validation
  - Enum validation
  - Numeric range validation (`page`, `per_page`)

- Clean API responses using Pydantic Response Models
- Automatic OpenAPI documentation
- Layered architecture
- `GitHubClient` abstraction
- Centralized GitHub HTTP communication
- FastAPI Dependency Injection
- Centralized API error handling
  - GitHub `404` → API `404`
  - GitHub `5xx` → API `503`
  - Network/request failures → API `503`
  - Invalid GitHub PAT → API `401`

- GitHub API authentication using a Personal Access Token (PAT)
- Environment-based configuration using Pydantic Settings
- Service-layer unit testing with Pytest
- Fake GitHub client dependencies for isolated service testing
- 9 service-layer tests passing

---

# Tech Stack

- Python
- FastAPI
- Requests
- Pydantic
- Pydantic Settings
- Pytest
- GitHub REST API

---

# Project Structure

```text
github-profile-api/
├── main.py
├── github_service.py
├── github_client.py
├── settings.py
├── models.py
├── enums.py
├── tests/
│   └── test_github_service.py
├── README.md
├── PROJECT_STATE.md
├── requirements.txt
└── .gitignore
```

---

# Architecture

```text
Client
    ↓
FastAPI Routes
    ↓
Request Validation
    ↓
Dependency Injection
    ↓
Service Layer
    ↓
GitHubClient
    ↓
GitHub REST API
    ↓
GitHubClientError
    ↓
GitHubServiceError
    ↓
Centralized FastAPI Exception Handler
    ↓
HTTP Response
```

### Responsibilities

**main.py**

- Defines API routes
- Validates client input
- Handles HTTP requests
- Uses FastAPI Dependency Injection
- Registers centralized exception handlers
- Calls the service layer

**github_service.py**

- Application/business logic
- Fetches GitHub profile data
- Fetches repositories
- Repository filtering
- Repository sorting
- Repository ordering
- Repository pagination
- GitHub API pagination logic
- Statistics calculation
- Data transformation
- Translates `GitHubClientError` into `GitHubServiceError`

**github_client.py**

- Handles communication with the GitHub REST API
- Builds GitHub API requests
- Handles authentication headers
- Handles request timeouts
- Handles GitHub HTTP errors
- Handles network/request failures
- Raises `GitHubClientError`

**models.py**

- Pydantic response models

**enums.py**

- Shared enums for validated query parameters

**settings.py**

- Loads application configuration from environment variables
- Loads local development variables from `.env`
- Provides centralized access to GitHub API configuration
- Stores the GitHub API URL and Personal Access Token configuration

---

# Installation

```bash
git clone https://github.com/Dhruv06000/github-profile-api.git

cd github-profile-api

python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
fastapi dev main.py
```

or

```bash
uvicorn main:app --reload
```

---

# Configuration

The application uses Pydantic Settings for configuration management.

For local development, create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_API_URL=https://api.github.com
```

---

# Testing

The project uses **Pytest** for automated testing.

The service layer is tested independently from the real GitHub API by using fake GitHub client implementations.

Current coverage includes:

- Profile success response
- Profile `404` handling
- Profile `500` handling
- Profile network-error handling
- Repository success response
- GitHub API pagination
- Repository `404` handling
- Repository `500` handling
- Repository other-status handling

Current test status:

````text
9 service-layer tests passing

# API Documentation

Swagger UI

```text
http://127.0.0.1:8000/docs
````

ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Endpoints

## GET /

Returns a welcome message.

---

## GET /profile/{username}

Returns:

- GitHub profile
- Repository statistics

---

## GET /profile/{username}/repositories

Supports filtering, sorting, ordering, and pagination.

### Query Parameters

| Parameter  | Description                           |
| ---------- | ------------------------------------- |
| language   | Filter by language                    |
| page       | Page number (>=1, default: 1)         |
| per_page   | Results per page (1-100, default: 30) |
| visibility | Filter by visibility                  |
| sort       | name, stars, forks, updated           |
| order      | asc, desc                             |

### Example Requests

```http
GET /profile/octocat/repositories

GET /profile/octocat/repositories?language=Python

GET /profile/octocat/repositories?sort=stars

GET /profile/octocat/repositories?sort=stars&order=desc

GET /profile/octocat/repositories?language=Python&sort=forks&order=desc

GET /profile/octocat/repositories?page=2

GET /profile/octocat/repositories?per_page=5

GET /profile/octocat/repositories?page=2&per_page=10

GET /profile/octocat/repositories?language=Python&page=1&per_page=5
```

---

# Design Decisions

- Application configuration is centralized using Pydantic Settings.
- GitHub credentials are stored in environment variables rather than hardcoded in source code.
- FastAPI routes handle validation and HTTP concerns
- GitHub-specific failures are translated into application-level `GitHubServiceError` exceptions.
- FastAPI handles `GitHubServiceError` through one centralized exception handler.
- Filtering is applied before sorting.
- Sorting uses Python's stable `sorted()` function.
- Pagination is applied after filtering and sorting to ensure consistent results.
- Pagination happens before creating `RepositoryResponse` objects.
- Response models expose only required fields.
- Enum validation automatically rejects invalid sort and order values with HTTP 422.
- Network failures are returned as HTTP 503 responses.
- External GitHub API communication is isolated inside `GitHubClient`.
- `GitHubClientError` represents GitHub client-level failures.
- `GitHubServiceError` represents application-level service failures.
- FastAPI Dependency Injection provides the `GitHubClient` to API routes.
- Dependencies can be replaced during testing to avoid real GitHub API requests.

---

# Manual API Testing

Successfully tested:

- Profile endpoint
- Repository endpoint
- Language filtering
- Visibility filtering
- Sorting by name
- Sorting by stars
- Sorting by forks
- Sorting by updated date
- Ascending and descending order
- Invalid enum values (HTTP 422)
- Combined filtering and sorting
- Pagination (`page`)
- Pagination (`per_page`)
- Combined filtering, sorting, and pagination
- Nonexistent GitHub user (HTTP 404)
- Centralized GitHub error handling
- Network/service failure handling
- GitHub API authentication with a valid PAT (HTTP 200)
- Invalid GitHub PAT handling (HTTP 401)
- GitHubClient integration with the service layer
- Dependency Injection through FastAPI

Example error response:

```json
{
  "detail": "GitHub user not found"
}
```

---

# Future Improvements

- Response metadata
- Logging
- Caching
- GitHubClient unit testing
- FastAPI integration/API testing
- Clean project structure
- Docker
- CI/CD
- Production-quality API documentation
- Deployment to Render

---

# License

MIT License
