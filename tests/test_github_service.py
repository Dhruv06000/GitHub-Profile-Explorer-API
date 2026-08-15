from github_service import (
  fetch_user_repositories, 
  fetch_github_user_profile_info,  
  GitHubServiceError 
)
from github_client import GitHubClientError

import pytest

# Testing the profile function fetch_github_user_profile_info()

class FakeGithubClient:
    
    def request(self, method, endpoint, params=None):
        self.method = method 
        self.endpoint = endpoint
        self.params = params
        # return fake profile data here
        return{
            "login": "Dhruv06000",
            "name": "Dhruv Kumar"
        }

def test_fetch_user_profile():
    client = FakeGithubClient()

    profile = fetch_github_user_profile_info("test-user", client)
    assert profile["login"] == "Dhruv06000"
    assert profile["name"] == "Dhruv Kumar"
    assert client.method == "GET"
    assert client.endpoint == "/users/test-user"

class FakeGithubClient404:
    def request(self,method,endpoint,params = None ):
        self.method = method 
        self.endpoint = endpoint
        self.params = params 
        raise GitHubClientError(
            status_code= 404,
            message = "GitHub API request failed"
        )

def test_fetch_error_404():
    client = FakeGithubClient404()

    with pytest.raises(GitHubServiceError) as exc_info:
        fetch_github_user_profile_info("test-user", client)
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "GitHub user not found"

class FakeGithubClient500:
    def request(self,method,endpoint,params=None):
        self.method = method 
        self.endpoint= endpoint
        self.params = params
        raise GitHubClientError(
            status_code=500,
            message = "GitHub service is temporarily unavailable"
        )

def test_fetch_error_500():
    client= FakeGithubClient500()
    with pytest.raises(GitHubServiceError) as exc_info:
        fetch_github_user_profile_info("test-user", client)
    assert exc_info.value.status_code == 503
    assert exc_info.value.message=="GitHub service is temporarily unavailable"

class FakeGithubClientNetworkError:
    def request(self,method,endpoint,params=None):
        self.method= method 
        self.endpoint= endpoint
        self.params= params
        raise GitHubClientError(
            status_code = 503,
            message="GitHub service is temporarily unavailable"
        )

def test_fetch_network_error():
    client = FakeGithubClientNetworkError()
    with pytest.raises(GitHubServiceError) as exc_info:
        fetch_github_user_profile_info("test-user", client)
    assert exc_info.value.status_code == 503
    assert exc_info.value.message == "GitHub service is temporarily unavailable"

# Testing the repositories function fetch_user_repositories()

class FakeGithubRepositoryClient:
    def request(self,method, endpoint,params= None):
        self.method = method 
        self.endpoint = endpoint
        self.params = params 
        return [
    {"name": "repo-one"},
    {"name": "repo-two"}
]

def test_fetch_user_repositories():
    client = FakeGithubRepositoryClient()

    repository = fetch_user_repositories("test-user", client)

    assert repository[0] == {"name": "repo-one"}
    assert repository[1] == {"name": "repo-two"}
    assert client.method == "GET"
    assert client.endpoint =="/users/test-user/repos"
    assert client.params == {
        "per_page" : 100,
        "page" : 1
    }

class FakeGithubPaginationClient:
    def __init__(self):
        self.requests = []
    def request(self,method,endpoint,params = None):
        self.method = method 
        self.endpoint = endpoint
        self.params = params 
        if params["page"] == 1:
            repos = [{"name" : f"repo-{i}"} for i in range(1,101)]
            self.requests.append(params)
            return repos


        elif params["page"] == 2:
            self.requests.append(params)
            return [
    {"name": "repo-101"},
    {"name": "repo-102"},
]

def test_fetch_user_repositories_pagination():
    client = FakeGithubPaginationClient()

    repositories = fetch_user_repositories("test-user", client)
    # 1. Did we collect both pages?
    assert len(repositories) == 102
    # 2. Did the service request page 1 correctly?
    assert client.requests[0] == {
        "per_page" : 100,
        "page" : 1
    }
    # 3. Did the service request page 2 correctly?
    assert client.requests[1] == {
        "per_page" : 100,
        "page" : 2
    }

class FakeGithubRepositoryClient404:
    def request(self,method,endpoint,params = None ):
            self.method = method 
            self.endpoint = endpoint
            self.params = params 
            raise GitHubClientError(
                status_code= 404,
                message = "GitHub API request failed"
            )

def test_fetch_repo_error_404():
    client = FakeGithubRepositoryClient404()
    with pytest.raises(GitHubServiceError) as exc_info:
        fetch_user_repositories("test-user", client)
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "GitHub user not found"

class FakeGithubRepositoryClient500:
    def request(self,method,endpoint,params=None):
        self.method = method 
        self.endpoint = endpoint
        self.params = params 
        raise GitHubClientError(
                        status_code= 500,
                        message = "GitHub API request failed"
                    )
def test_fetch_repo_error_500():
    client = FakeGithubRepositoryClient500()
    with pytest.raises(GitHubServiceError) as exc_info:
        fetch_user_repositories("test-user", client)
    assert exc_info.value.status_code == 503
    assert exc_info.value.message == "GitHub service is temporarily unavailable"


class FakeGithubRepositoryClientError:
    def request(self,method,endpoint,params=None):
            self.method = method 
            self.endpoint = endpoint
            self.params = params 
            raise GitHubClientError(
                            status_code= 401,
                            message = "Bad credentials"
                        )
def test_fetch_repo_error_other_status():
    client = FakeGithubRepositoryClientError()
    with pytest.raises(GitHubServiceError) as exc_info:
        fetch_user_repositories("test-user", client)
    assert exc_info.value.status_code == 401
    assert exc_info.value.message == "Bad credentials"