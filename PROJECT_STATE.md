# PROJECT_STATE.md

## Current Status

### Project

**GitHub Profile API**

The project is a FastAPI backend that retrieves GitHub profile and repository information through the GitHub REST API.

The goal is to develop it incrementally into a production-quality backend project while learning the engineering decisions behind the implementation.

---

# Architecture

## Current Application Flow

```text
Client
   ↓
FastAPI Route
   ↓
Request Validation
   ↓
Dependency Injection
   ↓
Service Layer
   ↓
GitHubClient
   ↓
GitHub API
```

## Error Flow

```text
GitHub API
   ↓
GitHubClient
   ↓
GitHubClientError
   ↓
GitHubServiceError
   ↓
Centralized FastAPI Exception Handler
   ↓
HTTP Response
```

## Configuration Flow

```text
.env
   ↓
Pydantic Settings
   ↓
settings.py
   ↓
GitHubClient
   ↓
Authorization Header
   ↓
GitHub API
```

---

# Features Completed

- [x] Fetch GitHub user profile
- [x] Fetch repositories
- [x] Language filtering
- [x] Visibility filtering
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
- [x] GitHub Personal Access Token authentication
- [x] Pydantic Settings
- [x] `.env` configuration
- [x] Configurable GitHub API URL
- [x] Authorization headers
- [x] Invalid PAT → API `401`
- [x] `GitHubClient` abstraction
- [x] `GitHubClientError`
- [x] Request timeout handling
- [x] FastAPI Dependency Injection
- [x] `get_github_client`
- [x] `Depends(get_github_client)`
- [x] Service-layer unit testing with Pytest
- [x] Fake GitHub clients for service testing
- [x] 9 service-layer tests passing

---

# Important Design Decisions

## 1. Layer Responsibilities

### FastAPI / Routes

Responsible for:

- HTTP endpoints
- Request validation
- Query parameters
- Dependency Injection
- HTTP responses

### Service Layer

Responsible for:

- Business/application logic
- Fetching profile data
- Fetching repositories
- Filtering
- Sorting
- Ordering
- Application-level pagination
- Repository statistics
- Response-model transformation
- Translating `GitHubClientError` → `GitHubServiceError`

The service layer does **not** make HTTP requests directly.

### GitHubClient

Responsible for communication with the external GitHub API.

It handles:

- GitHub API URL
- HTTP requests
- Authentication headers
- Request timeout
- HTTP errors
- Network/request errors
- Raising `GitHubClientError`

It should not contain application/business logic such as filtering, sorting, pagination, statistics, or response transformation.

---

# Pagination Design

There are two separate pagination concerns.

## GitHub API Pagination

```text
GitHub API Page 1
      ↓
GitHub API Page 2
      ↓
GitHub API Page 3
      ↓
...
      ↓
All repositories
```

The service retrieves all repositories in batches of up to 100.

## Application Pagination

After repositories are retrieved:

```text
Fetch
   ↓
Filter
   ↓
Sort
   ↓
Order
   ↓
Paginate
   ↓
Transform
```

Reason:

Users expect `page` and `per_page` to apply to the final filtered/sorted result set.

---

# Request Validation

Validation belongs at the FastAPI boundary.

Business logic belongs in the service layer.

Current validation includes:

- `page >= 1`
- `1 <= per_page <= 100`
- Enum-based sorting validation
- Enum-based ordering validation

The service layer should assume API-level input has already been validated.

---

# Error Handling

GitHub-specific errors are handled in layers.

```text
GitHub HTTP Error
      ↓
GitHubClientError
      ↓
GitHubServiceError
      ↓
FastAPI Exception Handler
      ↓
HTTP Response
```

Current behavior:

| GitHub failure          | API response |
| ----------------------- | ------------ |
| `404`                   | `404`        |
| `5xx`                   | `503`        |
| Network/request failure | `503`        |
| Invalid PAT             | `401`        |

The goal is to keep:

- External API concerns inside `GitHubClient`
- Application error translation inside the service layer
- HTTP response handling inside FastAPI

---

# Configuration & Authentication

Configuration is centralized through Pydantic Settings.

Current settings:

```text
GITHUB_TOKEN
GITHUB_API_URL
```

Default API URL:

```text
https://api.github.com
```

Authentication flow:

```text
Client
   ↓
FastAPI
   ↓
Service
   ↓
GitHubClient
   ↓
Authorization: Bearer <PAT>
   ↓
GitHub API
```

The PAT:

- Must not be hardcoded
- Must not be committed to Git
- Must not be returned through the API
- Should be revoked and replaced if accidentally exposed

---

# Dependency Injection

FastAPI provides `GitHubClient` through:

```text
FastAPI Route
      ↓
Depends(get_github_client)
      ↓
GitHubClient
```

The purpose is to keep dependency construction outside endpoint business logic and make the dependency replaceable during testing.

Current implementation intentionally remains simple.

No unnecessary dependency container or additional abstraction has been introduced.

---

# Service Layer Design

The project currently uses standalone service functions rather than a `GitHubService` class.

A service class has intentionally not been introduced because the current project does not have enough abstraction requirements to justify it.

Avoid adding abstractions simply to make the architecture look more "professional."

Every abstraction should solve an actual problem.

---

# Testing Status

## Current Testing

The service layer has unit tests using fake GitHub clients.

Current architecture:

```text
Pytest
   ↓
Service Function
   ↓
Fake GitHubClient
```

Tests currently cover:

- Profile success
- Profile `404`
- Profile `500`
- Profile network error
- Repository success
- GitHub API pagination
- Repository `404`
- Repository `500`
- Other repository errors

Current result:

```text
9 service-layer tests passing
```

## Important Testing Distinction

The current tests are **service-layer unit tests**.

They are **NOT GitHubClient unit tests**.

Current testing:

```text
Test
   ↓
Service
   ↓
Fake GitHubClient
```

Next GitHubClient testing should be:

```text
Test
   ↓
GitHubClient
   ↓
Mocked HTTP request
```

Unit tests must not call the real GitHub API.

---

# Current Limitations

- GitHub API rate limits still apply
- GitHubClient unit tests are not implemented
- FastAPI integration/API tests are not implemented
- FastAPI Dependency Injection has not yet been tested through endpoint integration tests
- Logging is not implemented
- Caching is not implemented
- Production secret management is not implemented
- Docker is not implemented
- CI/CD is not implemented
- Production deployment is not implemented

---

# Next Milestone

## GitHubClient Unit Testing

This is the immediate next milestone.

Goals:

- Understand `GitHubClient` responsibilities
- Learn mocking
- Mock HTTP requests
- Avoid real GitHub API calls
- Test successful responses
- Test `4xx` responses
- Test `5xx` responses
- Test invalid authentication
- Test network/request failures
- Test timeout behavior
- Verify `GitHubClientError`
- Verify request URL
- Verify HTTP method
- Verify headers
- Verify query parameters
- Verify timeout configuration
- Keep tests deterministic

Expected architecture:

```text
Pytest
   ↓
GitHubClient
   ↓
Mocked HTTP Request
```

Do not use:

```text
Pytest
   ↓
GitHubClient
   ↓
Real GitHub API
```

---

# After GitHubClient Testing

The next milestone will be:

## FastAPI Integration/API Testing

Expected flow:

```text
HTTP Request
   ↓
FastAPI Route
   ↓
Validation
   ↓
Dependency Injection
   ↓
Service
   ↓
GitHubClient
   ↓
Mocked External API
   ↓
HTTP Response
```

Topics:

- FastAPI `TestClient`
- Dependency overrides
- Endpoint testing
- Query validation testing
- Error response testing
- Response model testing
- Dependency Injection testing
- Mocking external services

Real GitHub API requests should not be used in automated tests.

---

# Future Roadmap

Follow this incrementally:

1. GitHubClient unit testing
2. FastAPI integration/API testing
3. Clean project structure
4. Response metadata
5. Logging
6. Caching
7. Docker
8. CI/CD
9. Production-quality API documentation
10. Deployment to Render

Do not implement future infrastructure prematurely.

---

# Session History

## Session 1 — Pagination & Query Validation

### Implemented

- Pagination
- `page`
- `per_page`
- Query validation
- Filtering/sorting/pagination ordering

### Learned

- FastAPI `Query()`
- Validation
- Separation of concerns
- Pagination design
- Why validation belongs at the API boundary

---

## Session 2 — Centralized Error Handling

### Implemented

- Centralized FastAPI exception handling
- `GitHubServiceError`
- GitHub `404` translation
- GitHub `5xx` translation
- Network/request failure handling

### Learned

- Custom exceptions
- Exception translation
- Centralized exception handlers
- Service errors vs HTTP responses

---

## Session 3 — Authentication & Configuration

### Implemented

- GitHub PAT
- `.env`
- `settings.py`
- Pydantic Settings
- `GITHUB_TOKEN`
- `GITHUB_API_URL`
- Authorization header
- Profile authentication
- Repository authentication
- Invalid PAT handling

### Testing

- Valid PAT → `200`
- Invalid PAT → `401`
- `octocat` profile retrieved successfully
- Repository/statistics data retrieved successfully

### Learned

- Environment variables
- `.env`
- Pydantic Settings
- Centralized configuration
- PAT authentication
- Authorization headers
- Secret management
- Why exposed credentials must be revoked
- Why `.env` must not be committed
- Why premature abstraction should be avoided

---

## Session 4 — GitHubClient Abstraction

### Implemented

- `GitHubClient`
- `GitHubClientError`
- Centralized GitHub HTTP communication
- Authentication headers
- GitHub API URL configuration
- Timeout handling
- HTTP error handling
- Network/request error handling

Architecture changed from:

```text
FastAPI
   ↓
Service Layer
   ↓
GitHub API
```

to:

```text
FastAPI
   ↓
Service Layer
   ↓
GitHubClient
   ↓
GitHub API
```

### Learned

- External API client abstraction
- Transport vs business logic separation
- Custom client exceptions
- Why HTTP communication should be isolated
- Why abstractions should solve concrete problems

---

## Session 5 — FastAPI Dependency Injection

### Implemented

- FastAPI Dependency Injection
- `get_github_client`
- `Depends(get_github_client)`
- GitHubClient injection into API routes

### Learned

- Dependency Injection
- FastAPI `Depends`
- Dependency resolution
- Dependency replacement during testing
- How DI improves testability
- Why DI should solve a real dependency problem
- Why unnecessary abstractions should be avoided

---

## Session 6 — Service-Layer Unit Testing

### Implemented

- Pytest service tests
- Fake GitHub clients
- Profile success/error tests
- Repository success/error tests
- GitHub pagination testing
- Network-error testing

### Result

```text
9 service-layer tests passing
```

### Learned

- Unit testing
- Pytest
- Fake dependencies
- Success/error path testing
- Pagination testing
- Independent service testing
- Why tests should not depend on real external APIs
- How DI and client abstraction improve testability

### Important Correction

Session 6 was **service-layer unit testing using fake GitHub clients**.

It was **not GitHubClient unit testing**.

GitHubClient unit testing is the next milestone.

---

# Current Development State

## Repository Endpoint

```text
Fetch All Repositories
        ↓
Filter
        ↓
Sort
        ↓
Order
        ↓
Application Pagination
        ↓
Response Transformation
```

## Profile Endpoint

```text
Client
   ↓
FastAPI Route
   ↓
Request Validation
   ↓
Dependency Injection
   ↓
GitHub Service
   ↓
GitHubClient
   ↓
Authenticated GitHub API Request
   ↓
Profile Response
```

Current state:

- Invalid query parameters are rejected by FastAPI.
- GitHub/service failures use centralized exception handling.
- GitHub API requests use the PAT loaded through Pydantic Settings.
- Service logic is separated from external HTTP communication.
- Service-layer tests are passing.
- GitHubClient unit testing is the next task.

---

# Development Rules

For every new improvement:

1. Briefly introduce the new concept.
2. Explain why it exists.
3. Explain where it belongs in the architecture.
4. Explain alternatives/trade-offs when relevant.
5. Reason through the design with me.
6. Ask me questions before implementation.
7. Let me implement the code myself.
8. Do not provide the complete solution unless I explicitly ask.
9. Review my code like a senior backend engineer.
10. Explain:
    - What I did well
    - What I did wrong
    - Why it is wrong
    - Readability
    - Maintainability
    - Scalability
    - Production practices
    - Interview expectations

11. Run relevant tests after changes.
12. Update documentation when behavior or architecture changes.
13. Update `PROJECT_STATE.md` after meaningful milestones.
14. Update `README.md` when public API behavior changes.
15. Commit every meaningful improvement.
16. Push completed improvements to GitHub.

The goal is to understand software engineering principles, not memorize syntax.

Avoid unnecessary architecture or technologies simply because they are common in production projects.

Always prefer incremental improvements that solve real problems.
