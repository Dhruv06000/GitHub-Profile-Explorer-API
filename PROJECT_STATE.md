# PROJECT_STATE.md

## Current Status

### Project

GitHub Profile API

---

## Architecture

```text
Client
    ↓
FastAPI Routes
    ↓
Request Validation
    ↓
Service Layer
    ↓
GitHub API
    ↓
GitHubServiceError
    ↓
Centralized FastAPI Exception Handler
    ↓
HTTP Response
```

Configuration and authentication:

```text
.env
    ↓
Pydantic Settings
    ↓
settings.py
    ↓
GitHub Service
    ↓
Authorization Header
    ↓
GitHub API
```

---

## Features Completed

- [x] Fetch repositories
- [x] Fetch GitHub user profile
- [x] Language filter
- [x] Visibility filter
- [x] Sorting
- [x] Ordering
- [x] Client-controlled pagination
- [x] GitHub API pagination
- [x] Query parameter validation
- [x] Pydantic response models
- [x] Repository statistics
- [x] Centralized GitHub error handling
- [x] GitHub `404` → API `404`
- [x] GitHub `5xx` → API `503`
- [x] Network/request failures → API `503`
- [x] GitHub Personal Access Token (PAT) authentication
- [x] Pydantic Settings configuration
- [x] `.env` configuration
- [x] Configurable GitHub API URL
- [x] Authorization header for GitHub requests
- [x] Invalid PAT → API `401`

---

## Important Design Decisions

### Pagination

Current pipeline:

```text
Fetch
  ↓
Filter
  ↓
Sort
  ↓
Paginate
  ↓
Transform
```

Reason:

Users expect page numbers to apply to the filtered and sorted results.

GitHub API pagination is handled separately while fetching repositories. The service fetches repositories in batches of up to 100 until all repositories have been retrieved.

---

### Request Validation

Validation belongs in FastAPI.

Business logic belongs in `github_service.py`.

Current validation includes:

- `page >= 1`
- `1 <= per_page <= 100`
- Enum-based validation for sorting
- Enum-based validation for ordering

---

### Error Handling

GitHub-specific failures are translated into application-level `GitHubServiceError` exceptions inside the service layer.

FastAPI uses a centralized exception handler to convert these exceptions into consistent HTTP responses.

Current behavior:

```text
GitHub 404
    ↓
GitHubServiceError
    ↓
Centralized Exception Handler
    ↓
HTTP 404
```

```text
GitHub 5xx / Network Failure
    ↓
GitHubServiceError
    ↓
Centralized Exception Handler
    ↓
HTTP 503
```

```text
Invalid GitHub PAT
    ↓
GitHub 401
    ↓
GitHubServiceError
    ↓
Centralized Exception Handler
    ↓
HTTP 401
```

This keeps GitHub-specific error handling inside the service layer while keeping HTTP response handling centralized in FastAPI.

---

### Configuration

Application configuration is centralized using Pydantic Settings.

Current configuration:

```text
GITHUB_TOKEN
GITHUB_API_URL
```

Default GitHub API URL:

```text
https://api.github.com
```

Configuration flow:

```text
.env
  ↓
Settings
  ↓
github_service.py
  ↓
GitHub API
```

The GitHub PAT is not hardcoded inside the source code.

---

### Authentication

The GitHub PAT is stored in `.env` during local development.

The client of the FastAPI application does not provide the GitHub PAT in every request.

The backend uses the PAT when communicating with GitHub:

```text
Client
  ↓
FastAPI API
  ↓
GitHub Service
  ↓
Authorization: Bearer <PAT>
  ↓
GitHub API
```

The PAT must never be committed to Git or exposed through API responses.

If a PAT is accidentally exposed, it should be revoked immediately and replaced with a new token.

---

### Service Layer

The current service layer uses standalone functions rather than a `GitHubService` class.

A `GitHubService` class has intentionally not been introduced yet because the current project does not have enough abstraction requirements to justify it.

---

## Current Limitations

- GitHub API rate limits still apply
- Common GitHub request configuration is currently duplicated between service functions
- FastAPI Dependency Injection has not been introduced yet
- Automated tests with Pytest have not been added yet
- Logging has not been implemented yet
- Caching has not been implemented yet
- Production secret management has not been implemented yet
- Project structure has not yet been refactored into separate packages/modules

---

## Next Milestone

Implement **FastAPI Dependency Injection**.

Goals:

- Understand what dependency injection is
- Understand why FastAPI provides it
- Identify suitable dependencies in the current project
- Understand `Depends`
- Gradually introduce Dependency Injection
- Avoid unnecessary refactoring
- Understand how Dependency Injection improves testability and maintainability

The implementation should build on the current architecture rather than restarting or restructuring the project unnecessarily.

---

## Future Roadmap

- Dependency Injection
- Response metadata
- Logging
- Caching
- Testing with Pytest
- Clean project structure
- Docker
- CI/CD
- Production-quality API documentation
- Deployment to Render

---

## Session Notes

### Session 1

Implemented:

- Pagination
- Query validation
- `page` / `per_page`

Learned:

- `Query()`
- Validation
- Separation of concerns
- Pagination order

---

### Session 2

Implemented:

- Centralized FastAPI exception handling
- `GitHubServiceError`
- GitHub `404` error translation
- GitHub `5xx` error translation
- Network/request failure handling

Learned:

- Custom application exceptions
- Exception translation
- Centralized exception handlers
- Separation between service-layer errors and HTTP responses

---

### Session 3

Implemented:

- GitHub Personal Access Token (PAT)
- `.env` configuration
- `settings.py`
- Pydantic Settings
- `GITHUB_TOKEN`
- `GITHUB_API_URL`
- GitHub API authentication
- `Authorization: Bearer <PAT>` header
- Authentication for profile requests
- Authentication for repository requests
- Invalid PAT handling

Testing performed:

- Valid PAT → HTTP `200`
- Invalid PAT → HTTP `401`
- `octocat` profile successfully retrieved
- Repository and statistics data successfully retrieved

Learned:

- Environment variables
- `.env` files
- Pydantic Settings
- Centralized configuration
- Personal Access Tokens
- Authorization headers
- Backend-to-external-API authentication
- Secret management
- Why exposed credentials must be revoked and replaced
- Why `.env` must not be committed
- Why premature abstraction should be avoided

---

## Current Development State

The repository endpoint currently supports:

```text
Fetch
    ↓
Filter
    ↓
Sort
    ↓
Ordering
    ↓
Pagination
    ↓
Response transformation
```

The profile endpoint currently supports:

```text
Client
    ↓
FastAPI Route
    ↓
GitHub Service
    ↓
Authenticated GitHub API Request
    ↓
Profile Response
```

Invalid query parameters are rejected by FastAPI validation, while GitHub/service failures are handled through the centralized exception-handling system.

GitHub API requests are now authenticated using a PAT loaded securely through Pydantic Settings.

### Next focus: **FastAPI Dependency Injection**
