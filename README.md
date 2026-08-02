# GitHub Profile Explorer API

A REST API built with **FastAPI** that fetches and analyzes GitHub user data using the **GitHub REST API**.

This project is a refactored version of my original **GitHub Profile Explorer** CLI application. The application has been redesigned using a layered architecture where API routes, business logic, and response models are separated into dedicated modules for better maintainability.

The API retrieves a GitHub user's public profile information, fetches all of their public repositories using automatic pagination, supports repository filtering using query parameters, calculates repository statistics, and exposes clean, structured JSON responses through RESTful endpoints.

---

# Features

- REST API built with FastAPI
- Fetch GitHub user profile information
- Fetch all public repositories
- Automatic GitHub API pagination
- Repository statistics calculation
  - Total stars across all repositories
  - Languages used
  - Most used programming language
- Dedicated repository listing endpoint
- Filter repositories by programming language
- Filter repositories by visibility
- Support multiple query parameter filters
- Case-insensitive repository filtering
- Clean API responses using Pydantic Response Models
- Automatic response validation using `response_model`
- Layered project architecture
- Error handling for:
  - GitHub HTTP errors
  - Network/request errors
  - FastAPI HTTP exceptions

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
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Architecture

```text
Client
   │
   ▼
FastAPI Routes (main.py)
   │
   ▼
Service Layer (github_service.py)
   │
   ▼
GitHub REST API
```

### main.py

Responsibilities:

- Defines all FastAPI routes
- Handles incoming HTTP requests
- Validates input using FastAPI
- Calls the service layer
- Converts Python exceptions into FastAPI `HTTPException` responses

---

### github_service.py

Contains the application's business logic.

Responsibilities include:

- Fetching GitHub profile information
- Fetching public repositories
- Handling GitHub API pagination
- Calculating repository statistics
- Repository filtering by language
- Repository filtering by visibility
- Transforming GitHub responses into API response models

Business logic remains inside the service layer, keeping the API routes clean and focused on request handling.

---

### models.py

Contains the Pydantic response models used by the API.

Current models:

- `ProfileResponse`
- `StatisticsResponse`
- `RepositoryResponse`
- `GitHubUserDashboardResponse`

The API uses Pydantic Response Models to validate responses, expose only selected fields, and automatically generate OpenAPI documentation.

# Installation

Clone the repository:

```bash
git clone https://github.com/Dhruv06000/github-profile-api.git
```

Navigate to the project directory:

```bash
cd github-profile-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

# How to Run

Start the FastAPI development server:

```bash
fastapi dev main.py
```

Or using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

- View all available endpoints
- Explore request and response models
- Test API endpoints directly from your browser

## ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

ReDoc provides a clean, read-only documentation interface.

---

# API Endpoints

## GET /

Returns a welcome message.

### Response

```json
{
  "Message": "GitHub Profile Explorer API"
}
```

---

## GET /profile/{username}

Fetches a GitHub user's profile information along with repository statistics.

This endpoint:

- Fetches the GitHub user profile
- Retrieves all public repositories
- Automatically handles GitHub API pagination
- Calculates repository statistics
- Returns a structured JSON response using `GitHubUserDashboardResponse`

---

## GET /profile/{username}/repositories

Returns public repositories for the specified GitHub user.

Supports optional filtering using query parameters.

### Example Requests

```http
GET /profile/octocat/repositories
```

```http
GET /profile/octocat/repositories?language=Python
```

```http
GET /profile/octocat/repositories?visibility=public
```

```http
GET /profile/octocat/repositories?language=Python&visibility=public
```

### Endpoint Behavior

- Retrieves every public repository from GitHub
- Automatically handles GitHub API pagination
- Supports filtering by programming language
- Supports filtering by repository visibility
- Applies filtering before converting data into response models
- Returns only selected repository fields using `RepositoryResponse`

---

# Query Parameters

The repository endpoint supports optional query parameters for filtering results.

| Parameter    | Type   | Description                                                    |
| ------------ | ------ | -------------------------------------------------------------- |
| `language`   | string | Filter repositories by programming language (case-insensitive) |
| `visibility` | string | Filter repositories by repository visibility                   |

Both query parameters are optional and may be combined in a single request.

Example:

```http
GET /profile/octocat/repositories?language=Python&visibility=public
```

If no filters are provided, the endpoint returns all public repositories.

# Pagination

The GitHub REST API returns a maximum of **100 repositories per request**.

This application automatically requests additional pages until all public repositories have been retrieved, ensuring that repository statistics and filtering are performed on the complete dataset.

---

# Example Requests

## Home Endpoint

```http
GET /
```

## Profile Endpoint

```http
GET /profile/octocat
```

## Repository Endpoint

```http
GET /profile/octocat/repositories
```

### Filter by Programming Language

```http
GET /profile/octocat/repositories?language=Python
```

### Filter by Visibility

```http
GET /profile/octocat/repositories?visibility=public
```

### Filter by Language and Visibility

```http
GET /profile/octocat/repositories?language=Python&visibility=public
```

---

# Example Responses

## Home

```json
{
  "Message": "GitHub Profile Explorer API"
}
```

---

## Profile Endpoint

```json
{
  "profile": {
    "login": "octocat",
    "name": "The Octocat",
    "avatar_url": "https://...",
    "bio": "...",
    "company": "...",
    "location": "...",
    "blog": "...",
    "followers": 0,
    "following": 0,
    "public_repos": 0,
    "html_url": "https://github.com/octocat",
    "created_at": "2011-01-25T18:44:36Z"
  },
  "statistics": {
    "total_stars": 0,
    "languages_used": {
      "Python": 5,
      "JavaScript": 2
    },
    "most_used_language": "Python"
  }
}
```

---

## Repository Endpoint

```json
[
  {
    "name": "Hello-World",
    "description": "My first repository",
    "html_url": "https://github.com/octocat/Hello-World",
    "language": "Python",
    "visibility": "public",
    "stargazers_count": 80,
    "forks_count": 9,
    "open_issues_count": 2,
    "updated_at": "2025-07-29T10:15:20Z",
    "pushed_at": "2025-07-30T18:42:11Z",
    "license": "MIT License"
  }
]
```

---

# Response Models

The API uses **Pydantic Response Models** to expose only the required data.

Current response models:

- `ProfileResponse`
- `StatisticsResponse`
- `RepositoryResponse`
- `GitHubUserDashboardResponse`

The profile endpoint returns:

```python
GitHubUserDashboardResponse
```

The repository endpoint returns:

```python
list[RepositoryResponse]
```

Each repository exposes only the fields required by API consumers instead of the complete GitHub repository payload. This creates a stable API contract while preventing unnecessary GitHub fields from being exposed.

---

# Service Layer Improvements

The `get_user_repositories()` service function has been enhanced to support repository filtering using optional query parameters.

The filtering workflow is:

1. Fetch all repositories from the GitHub REST API.
2. Normalize query parameter values using `strip().lower()`.
3. Filter repositories by visibility (if provided).
4. Filter repositories by programming language (if provided).
5. Convert only the filtered repositories into `RepositoryResponse` models.
6. Return the filtered list.

This approach avoids unnecessary transformations and keeps all business logic inside the service layer.

---

# API Design Decisions

This project follows common REST API design principles.

### Path Parameters

Path parameters identify resources.

Examples:

```text
/profile/octocat

/profile/octocat/repositories
```

### Query Parameters

Query parameters filter resources rather than identify them.

Examples:

```text
?language=Python

?visibility=public

?language=Python&visibility=public
```

### Separation of Concerns

- FastAPI routes in `main.py` handle HTTP requests and input validation.
- Business logic resides in `github_service.py`.
- Response formatting is handled using Pydantic models.

### Efficient Filtering

Repository filtering is performed **before** converting GitHub responses into `RepositoryResponse` models. This avoids unnecessary object creation and improves performance.

### Stable API Contract

The API exposes only the fields explicitly defined in `RepositoryResponse`, ensuring a clean, consistent response format while preventing unnecessary GitHub API fields from being returned.

---

# Testing

The following scenarios were successfully tested.

### Repository Endpoint

- GET `/profile/{username}/repositories`
- GET `/profile/{username}/repositories?language=Python`
- GET `/profile/{username}/repositories?visibility=public`
- GET `/profile/{username}/repositories?language=Python&visibility=public`

### Validation Results

- Language filtering is case-insensitive (`Python`, `python`, and `PYTHON` return identical results).
- Unknown languages return an empty list instead of an error.
- Multiple query parameter filters work together correctly.
- Existing functionality remains unaffected after adding filtering support.

---

# Error Handling

The API handles several types of errors, including:

- GitHub API HTTP errors
- Network and request exceptions
- Invalid GitHub usernames
- FastAPI `HTTPException` responses with appropriate status codes

This provides clear and consistent error responses to API clients.

---

# Future Improvements

Planned enhancements include:

- Repository sorting
- API pagination
- Additional filtering options
- GitHub authentication using Personal Access Tokens
- Caching GitHub API responses
- Logging
- Configuration management
- Automated testing with Pytest
- Docker support
- CI/CD with GitHub Actions
- Deployment to Render or Railway

---

# License

This project is licensed under the MIT License.

Feel free to use, modify, and learn from this project.
