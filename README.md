# GitHub Profile Explorer API

A REST API built with **FastAPI** that fetches and analyzes GitHub user data using the **GitHub REST API**.

This project is a refactored version of my original **GitHub Profile Explorer** CLI application. The application has been redesigned using a layered architecture where API routes, business logic, and response models are separated into dedicated modules for better maintainability.

The API retrieves a GitHub user's public profile information, fetches all of their public repositories using automatic pagination, calculates repository statistics, and returns a clean, structured JSON response.

---

# Features

- REST API built with FastAPI
- Fetch GitHub user profile information
- Fetch all public repositories
- Automatic GitHub API pagination
- Calculate repository statistics:
  - Total stars across all repositories
  - Languages used
  - Most used programming language

- Clean JSON responses using Pydantic Response Models
- Automatic response filtering with `response_model`
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

### `main.py`

- Defines all FastAPI routes
- Handles incoming HTTP requests
- Converts Python exceptions into FastAPI `HTTPException` responses

### `github_service.py`

Contains the application's business logic.

Responsibilities include:

- Fetching GitHub profile information
- Fetching public repositories
- Handling GitHub API pagination
- Calculating repository statistics

### `models.py`

Contains the Pydantic response models used by the API.

Current models:

- `ProfileResponse`
- `StatisticsResponse`
- `GitHubUserDashboardResponse`

The `/profile/{username}` endpoint uses:

```python
response_model = GitHubUserDashboardResponse
```

This ensures that only selected fields are exposed in the API response.

---

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

### Swagger UI

Open the following URL after starting the server:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

- View all available endpoints
- Explore request and response models
- Test API endpoints directly from your browser

### ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

ReDoc provides a clean, read-only documentation interface for your API.

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

Fetches a GitHub user's profile and repository statistics.

This endpoint:

- Fetches the GitHub user profile
- Retrieves all public repositories
- Automatically handles pagination
- Calculates repository statistics
- Returns a structured JSON response

---

## Pagination

The GitHub REST API returns a maximum of **100 repositories per request**.

This application automatically requests additional pages until all public repositories have been retrieved.

---

# Example Requests

### Home Endpoint

```http
GET /
```

### Profile Endpoint

```http
GET /profile/octocat
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

# Response Models

The API uses Pydantic Response Models to expose only the required data.

Current response models:

- `ProfileResponse`
- `StatisticsResponse`
- `GitHubUserDashboardResponse`

The profile response intentionally exposes only:

- `login`
- `name`
- `avatar_url`
- `bio`
- `company`
- `location`
- `blog`
- `followers`
- `following`
- `public_repos`
- `html_url`
- `created_at`

This prevents unnecessary fields returned by the GitHub API from being included in the final response.

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

- Repository endpoint
- Query parameter filtering
- Sorting
- Logging
- Docker support
- Automated testing
- Deployment

---

# License

This project is licensed under the MIT License.

Feel free to use, modify, and learn from this project.
