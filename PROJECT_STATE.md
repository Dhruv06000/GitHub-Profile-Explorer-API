# PROJECT_STATE.md

## Current Status

### Project

GitHub Profile API

---

## Architecture

```
Client
    ↓
FastAPI
    ↓
Validation
    ↓
Service Layer
    ↓
GitHub API
    ↓
Response Models
```

---

## Features Completed

- [x] Fetch repositories
- [x] Language filter
- [x] Visibility filter
- [x] Sorting
- [x] Ordering
- [x] Pagination

---

## Important Design Decisions

### Pagination

Current pipeline:

Fetch
↓

Filter
↓

Sort
↓

Paginate
↓

Transform

Reason:

Users expect page numbers after filters.

---

### Request Validation

Validation belongs in FastAPI.

Business logic belongs in services.py.

---

## Current Limitations

- GitHub API rate limit
- No authentication yet

---

## Next Milestone

Implement GitHub Personal Access Token (PAT) authentication.

---

## Future Roadmap

- Better error handling
- Dependency Injection
- Pydantic Settings
- Response metadata
- Caching
- Logging
- Testing
- Docker
- CI/CD

---

## Session Notes

### Session 1

Implemented:

- Pagination
- Query validation
- page/per_page

Learned:

- Query()
- Validation
- Separation of concerns
- Pagination order

Ready to commit.
