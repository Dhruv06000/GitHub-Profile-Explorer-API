# GitHub Profile Explorer API

A REST API built with **FastAPI** that fetches and analyzes GitHub user data using the **GitHub REST API**.

This project follows a layered architecture where API routes, business logic, and response models are separated for better readability, maintainability, and scalability.

---

# Features

- Fetch GitHub user profile information
- Fetch all public repositories
- Repository pagination using page and per_page query parameters
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
- FastAPI Query parameter validation
  - Enum validation
  - Numeric range validation (page, per_page)
- Clean API responses using Pydantic Response Models
- Automatic OpenAPI documentation
- Layered architecture
- HTTP and network error handling

---

# Tech Stack

- Python
- FastAPI
- Requests
- Pydantic
- GitHub REST API

---

# Project Structure

```text
github-profile-api/
├── main.py
├── github_service.py
├── models.py
├── enums.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Architecture

```text
Client
   │
   ▼
FastAPI Routes
   │
   ▼
Service Layer
   │
   ▼
GitHub REST API
```

### Responsibilities

**main.py**

- Defines API routes
- Validates client input
- Handles HTTP requests
- Calls the service layer

**github_service.py**

- GitHub API communication
- Repository filtering
- Repository sorting
- Repository pagination
- Statistics calculation
- Data transformation

**models.py**

- Pydantic response models

**enums.py**

- Shared enums for validated query parameters

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

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
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

Supports filtering and sorting.

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

- Business logic stays inside the service layer.
- FastAPI routes handle validation and HTTP concerns.
- Filtering is applied before sorting.
- Sorting uses Python's stable `sorted()` function.
- Pagination is applied after filtering and sorting to ensure consistent results.
- Response models expose only required fields.
- Enum validation automatically rejects invalid sort and order values with HTTP 422.

---

# Testing

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
- Pagination (page)
- Pagination (per_page)
- Combined filtering, sorting, and pagination

---

# Future Improvements

- Additional filters
- GitHub Personal Access Token support
- Logging
- Caching
- Pytest
- Docker
- CI/CD
- Deployment to Render

---

# License

MIT License
