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

---

## Features Completed

- [x] Fetch repositories
- [x] Language filter
- [x] Visibility filter
- [x] Sorting
- [x] Ordering
- [x] Pagination
- [x] Query parameter validation
- [x] Centralized GitHub error handling
- [x] GitHub `404` → API `404`
- [x] GitHub `5xx` → API `503`
- [x] Network/request failures → API `503`

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

---

### Request Validation

Validation belongs in FastAPI.

Business logic belongs in `github_service.py`.

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

This keeps GitHub-specific error handling inside the service layer while keeping HTTP response handling centralized in FastAPI.

---

## Current Limitations

- GitHub API rate limit
- No authentication yet

---

## Next Milestone

Implement GitHub Personal Access Token (PAT) authentication.

---

## Future Roadmap

- Dependency Injection
- Pydantic Settings
- Response metadata
- Logging
- Caching
- Testing with Pytest
- Clean project structure
- Docker
- CI/CD
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

## Current Development State

The repository endpoint currently supports:

```text
Filtering
    ↓
Sorting
    ↓
Ordering
    ↓
Pagination
    ↓
Response transformation
```

Invalid query parameters are rejected by FastAPI validation, while GitHub/service failures are handled through the centralized exception-handling system.

Next focus: **GitHub Personal Access Token (PAT) authentication.**
