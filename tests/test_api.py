# test_api.py code :
from fastapi.testclient import TestClient

import pytest

from main import get_github_client

from github_client import GitHubClientError

from main import app

client = TestClient(app)

# Test For Root : GET /

def test_root():
  response = client.get("/")

  assert response.status_code == 200
  assert response.json() == {
  "Message": "GitHub Profile Explorer API"
}
# Test for Profile Endpoint : GET /profile/Test_User

# Created dumy class 

class FakeGitHubClient:
  def request(self,method,endpoint,params = None):

    if endpoint == "/users/Test_User":
      # return fake profile data
      return {
                "login": "Test_User",
                "name": "Dhruv Kumar",
                "avatar_url": "https://example.com/avatar.jpg",
                "followers": 10,
                "following": 5,
                "public_repos": 1,
                "html_url": "https://github.com/Test_User",
                "created_at": "2020-01-01T00:00:00Z"
            }
    
    if endpoint == "/users/Test_User/repos":
      return [
    {
        "name": "python-repo",
        "description": "Python repository",
        "html_url": "https://github.com/Test_User/python-repo",
        "language": "Python",
        "visibility": "public",
        "stargazers_count": 10,
        "forks_count": 2,
        "open_issues_count": 1,
        "updated_at": "2026-08-20T00:00:00Z",
        "pushed_at": "2026-08-20T00:00:00Z",
        "license": {
            "name": "MIT"
        }
    },
    {
        "name": "javascript-repo",
        "description": "JavaScript repository",
        "html_url": "https://github.com/Test_User/javascript-repo",
        "language": "JavaScript",
        "visibility": "private",
        "stargazers_count": 5,
        "forks_count": 1,
        "open_issues_count": 0,
        "updated_at": "2026-08-19T00:00:00Z",
        "pushed_at": "2026-08-19T00:00:00Z",
        "license": None
    }
]

# Function to return class

def get_fake_github_client():
  return FakeGitHubClient()

# different test dependency overrides don't conflict with each other 

@pytest.fixture
def fake_github_dependency():
  app.dependency_overrides[get_github_client] =  get_fake_github_client

  yield 

  app.dependency_overrides.clear()


# app.dependency_overrides[get_github_client] = get_fake_github_client

def test_profile(fake_github_dependency):
  response = client.get("/profile/Test_User")

  assert response.status_code == 200
  data = response.json()
  assert data["profile"]["login"] == "Test_User"
  assert data["profile"]["name"] == "Dhruv Kumar"
  assert data["statistics"]["total_stars"] == 15
  assert data["statistics"]["most_used_language"] == "Python"

# Test for : 404 Error Handling

class FakeGitHubClient404:
    def request(self, method, endpoint, params=None):
        raise GitHubClientError(
            status_code=404,
            message="GitHub API request failed"
        )

def get_fake_github_client_404():
  return FakeGitHubClient404()

@pytest.fixture
def fake_github_404_dependency():
  app.dependency_overrides[get_github_client] = get_fake_github_client_404
  yield
  app.dependency_overrides.clear()

def test_profile_not_found(fake_github_404_dependency):
  response = client.get("/profile/Unknown_User")

  assert response.status_code == 404


# Test for : 500 Error Handling

class FakeGitHubClient500:
  def request(self,method,endpoint,params= None):
    raise GitHubClientError(
      status_code=503,
      message = "GitHub service is temporarily unavailable"
    )

def get_fake_github_client_500():
  return FakeGitHubClient500()

@pytest.fixture
def fake_github_500_dependency():
  app.dependency_overrides[get_github_client] = get_fake_github_client_500
  yield
  app.dependency_overrides.clear()

def test_profile_github_service_unavailable(fake_github_500_dependency):
  response = client.get("/profile/Test_User")

  assert response.status_code == 503

# Test for : Network Error Handling

class FakeGitHubClientNetworkError:
    def request(self, method, endpoint, params=None):
        raise GitHubClientError(
            status_code=503,
            message="GitHub service is temporarily unavailable"
        )

def get_fake_github_client_network():
  return FakeGitHubClientNetworkError()

@pytest.fixture
def fake_github_network_dependency():
  app.dependency_overrides[get_github_client] = get_fake_github_client_network
  yield
  app.dependency_overrides.clear()

def test_profile_github_network_error(fake_github_network_dependency):
  response = client.get("/profile/Test_User")

  assert response.status_code == 503

# Test for Repository Endpoint : GET /profile/Test_User/repositories

def test_repository(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories")

  assert response.status_code == 200

  data = response.json()

  assert len(data) == 2
  assert data[0]["name"] == "python-repo"
  assert data[0]["language"] == "Python"
  assert data[0]["visibility"] == "public"
  assert data[0]["stargazers_count"] == 10

  assert data[1]["name"] == "javascript-repo"
  assert data[1]["language"] == "JavaScript"
  assert data[1]["visibility"] == "private"
  assert data[1]["stargazers_count"] == 5

# Test for : Language Filtering 

def test_repository_language_filter(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?language=Python")

  assert response.status_code == 200
  data = response.json()
  assert len(data) == 1
  assert data[0]["name"] == "python-repo"
  assert data[0]["language"] == "Python"

# Test for : Visibility Filtering

def test_repository_visibility_filter(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?visibility=private")

  assert response.status_code == 200

  data = response.json()
  assert len(data) == 1
  assert data[0]["name"] == "javascript-repo"
  assert data[0]["visibility"] == "private"

# Test for : Sort by stars and order is descending

def test_repository_sort_desc(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?sort=stars&order=desc")

  assert response.status_code == 200

  data = response.json()
  assert data[0]["name"] == "python-repo"
  assert data[0]["stargazers_count"] == 10

  assert data[1]["name"] == "javascript-repo"
  assert data[1]["stargazers_count"] == 5

# Test for : Sorting Ascending

def test_repository_sort_asc(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?sort=stars&order=asc")
  assert response.status_code == 200
  data = response.json()
  assert data[0]["name"] == "javascript-repo"
  assert data[0]["stargazers_count"] == 5
  
  assert data[1]["name"] == "python-repo"
  assert data[1]["stargazers_count"] == 10

# Test for : Pagination - First Page

def test_repository_pagination_first_page(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?page=1&per_page=1")

  assert response.status_code == 200

  data = response.json()

  assert len(data) == 1
  assert data[0]["name"] == "python-repo"

# Test for : Pagination - Second Page

def test_repository_pagination_second_page(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?page=2&per_page=1")

  assert response.status_code == 200

  data = response.json()

  assert len(data) == 1
  assert data[0]["name"] == "javascript-repo"

# Test for : Filtering + Pagination

def test_repository_filter_pagination(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?language=javascript&page=1&per_page=1")

  assert response.status_code == 200

  data = response.json()

  assert len(data) == 1
  assert data[0]["name"] == "javascript-repo"
  assert data[0]["language"] == "JavaScript"

# Test for : Sorting + Pagination

def test_repository_sort_pagination(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?sort=stars&order=desc&page=1&per_page=1")

  assert response.status_code == 200

  data = response.json()

  assert len(data) == 1
  assert data[0]["name"] == "python-repo"
  assert data[0]["language"] == "Python"
  assert data[0]["stargazers_count"] == 10

# Test for : Invalid page 
def test_repository_invalid_page(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?page=0")
  assert response.status_code == 422

# Test for : Invalid per_page
def test_repository_invalid_per_page(fake_github_dependency):
  response = client.get("/profile/Test_User/repositories?per_page=0")
  assert response.status_code == 422
