# PROJECT_STATE.md

## Current Status

The GitHubClient, GitHubService, and FastAPI endpoint layers are implemented and tested.

Current test status:

- GitHubClient: 5 tests passing
- GitHubService: 9 tests passing
- FastAPI endpoints (TestClient): 16 tests passing
- Full test suite: 30/30 tests passing

Current milestone:
Clean project structure.

The next major goal after that is Response Metadata, followed by production configuration review and deployment.

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
- [x] GitHubClient unit testing with Pytest
- [x] Successful GitHubClient request test
- [x] GitHubClient 404 error test
- [x] GitHubClient 500 error test
- [x] GitHubClient network error test
- [x] GitHubClient timeout test
- [x] Mocked HTTP requests for GitHubClient testing
- [x] FastAPI endpoint/integration testing with `TestClient`
- [x] Dependency override testing (`app.dependency_overrides`)
- [x] Endpoint-level 404 verification (profile not found)
- [x] Endpoint-level 503 verification (GitHub 5xx and network error paths)
- [x] Repository filtering tested through the API layer
- [x] Repository visibility filtering tested through the API layer
- [x] Repository sorting (asc/desc) tested through the API layer
- [x] Repository pagination (first page, second page) tested through the API layer
- [x] Combined filter+pagination and sort+pagination tested through the API layer
- [x] Query validation tested through the API layer (422 for invalid `page`/`per_page`)
- [x] 16 FastAPI endpoint tests passing

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

**Note on 5xx vs. network errors:** `GitHubServiceError` currently carries only a `status_code` and `message` — there is no field distinguishing "GitHub responded with a 5xx" from "the request itself failed before GitHub responded." Both collapse to API `503` by design. `test_profile_github_service_unavailable` and `test_profile_github_network_error` are therefore two regression guards over the same collapsed code path (different failure origins, same observable behavior), not two distinct branches. This is an intentional simplification for now, not an oversight — revisit if a future need arises to alert/log differently on the two origins.

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

## Service Layer Testing

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

## GitHubClient Unit Testing

GitHubClient is tested independently from the real GitHub API using mocked HTTP requests.

Current architecture:

```text
Pytest
   ↓
GitHubClient
   ↓
Mocked HTTP Request
```

Current result:

```text
5 GitHubClient tests passing
```

## FastAPI Endpoint/Integration Testing

The FastAPI layer is now tested end-to-end using `TestClient`, with the real `GitHubClient` replaced by fakes through `app.dependency_overrides`.

Current architecture:

```text
Pytest
   ↓
FastAPI TestClient
   ↓
FastAPI Route
   ↓
Dependency Override
   ↓
Service
   ↓
Fake GitHubClient
```

Tests currently cover:

- Root endpoint (`GET /`)
- Profile success
- Profile `404`
- Profile `503` (GitHub 5xx)
- Profile `503` (network error)
- Repository success
- Repository language filtering
- Repository visibility filtering
- Repository sorting (asc, desc)
- Repository pagination (first page, second page)
- Repository filter + pagination combined
- Repository sort + pagination combined
- Invalid `page` → `422`
- Invalid `per_page` → `422`

Each test uses a pytest fixture that applies `app.dependency_overrides[get_github_client]` and clears it on teardown, so overrides from one test never leak into another.

Current result:

```text
16 FastAPI endpoint tests passing
```

## Full Suite

```text
GitHubClient:   5 passed
GitHubService:  9 passed
FastAPI (API): 16 passed
Total:         30/30 passed
```

---

# Current Limitations

- Logging is not implemented
- Caching is not implemented
- Production secret management is not implemented
- Docker is not implemented
- CI/CD is not implemented
- Production deployment is not implemented
- `GitHubServiceError` does not distinguish GitHub 5xx from network/request failures (both map to `503` by design — see note under Error Handling)

---

# Next Milestone

## Clean Project Structure

This is the immediate next milestone.

Goals:

- Review current file/folder organization against typical FastAPI project layouts
- Decide whether routes, services, and clients should be grouped into packages (e.g. `app/`, `routers/`) or remain flat, and justify the choice rather than restructuring for its own sake
- Ensure test files mirror source structure clearly
- Keep `requirements.txt` accurate and minimal
- Confirm `.env` / secrets are properly excluded from version control
- Do not introduce structure that isn't earning its complexity yet (e.g. no premature package-per-layer split if the project doesn't need it)

Expected outcome:

A project layout that is easy for a new reader (or interviewer) to navigate, with no leftover clutter from earlier sessions.

---

# After Clean Project Structure

Once project structure is reviewed, the project moves to Response Metadata, then production configuration review, then deployment.

```text
Clean Project Structure
        ↓
Response Metadata
        ↓
Production Configuration Review
        ↓
Deployment
        ↓
Test Live API
```

---

# Future Roadmap

Follow this incrementally:

1. ~~FastAPI integration/API testing~~ ✅ Completed (Session 8)
2. Clean project structure ← current milestone
3. Response metadata
4. Production configuration review
5. Deployment to Render
6. Verify and test the live API
7. Logging
8. Caching
9. Docker
10. CI/CD

Do not implement future infrastructure prematurely.

The first deployment is prioritized before optional infrastructure such as Docker and CI/CD.

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

---

## Session 7 — GitHubClient Unit Testing

### Implemented

- Mocked `requests.request()`
- Tested successful GitHubClient requests
- Tested GitHub `404` HTTP errors
- Tested GitHub `500` HTTP errors
- Tested network/request errors
- Tested timeout errors
- Verified request URL
- Verified HTTP method
- Verified headers
- Verified query parameters
- Verified timeout configuration

### Result

```text
GitHubClient: 5/5 tests passing
GitHubService: 9/9 tests passing
Full test suite: 14/14 tests passing
```

### Learned

- unittest.mock.Mock
- return_value
- side_effect
- monkeypatch.setattr()
- pytest.raises()
- exc_info.value
- Mocking external HTTP requests
- Fake HTTP response objects
- HTTPError.response
- HTTP error handling
- Network error handling
- Timeout testing
- Verifying mocked function calls
- Mock.assert_called_once_with()

---

## Session 8 — FastAPI Endpoint/Integration Testing

### Implemented

- FastAPI `TestClient` setup (`tests/test_api.py`)
- Dependency override fixtures (`app.dependency_overrides[get_github_client]`, cleared via `yield` teardown)
- Fake GitHub clients dedicated to endpoint-level testing (success, 404, 500, network error)
- Root endpoint test
- Profile endpoint success test
- Profile endpoint `404` / `503` (5xx) / `503` (network error) tests
- Repository endpoint success test
- Repository language filter test
- Repository visibility filter test
- Repository sort tests (asc, desc)
- Repository pagination tests (first page, second page)
- Combined filter+pagination test
- Combined sort+pagination test
- Invalid `page`/`per_page` validation tests (`422`)

### Result

```text
GitHubClient:   5/5 tests passing
GitHubService:  9/9 tests passing
FastAPI (API): 16/16 tests passing
Full test suite: 30/30 tests passing
```

### Learned

- FastAPI `TestClient`
- Testing endpoints without calling the real GitHub API
- `app.dependency_overrides` and why it must be cleared per-test to avoid cross-test leakage
- Writing fixtures with `yield` for setup/teardown
- Testing query validation at the FastAPI boundary (`422` responses)
- Testing combinatorial query parameter behavior (filter+pagination, sort+pagination), not just isolated cases
- That `GitHubServiceError`'s flat `status_code`/`message` shape means distinct failure origins (5xx vs. network error) can legitimately collapse into the same HTTP response and the same test outcome — and how to recognize when that's a deliberate simplification vs. redundant test coverage

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
- GitHubClient unit tests are passing.
- FastAPI endpoint tests are passing, including dependency overrides, filtering, sorting, pagination, and validation boundaries.
- Full test suite has 30/30 tests passing.
- Clean project structure is the next task.
- Deployment has not started yet.

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
