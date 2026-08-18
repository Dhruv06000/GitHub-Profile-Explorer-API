# import pytest
from github_client import GitHubClient , GitHubClientError
import requests
import pytest
from unittest.mock import Mock

class FakeHTTPResponse:
  def raise_for_status(self):
    # Because our GitHubClient return nothing when our request is successful
    return None
  def json(self):

    return {
            "login": "Dhruv06000",
            "name": "Dhruv Kumar"
        }



def test_successful_request(monkeypatch):
    # monkeypatch.setattr(...) goes here
    mock_request = Mock()
    mock_request.return_value=FakeHTTPResponse()
    monkeypatch.setattr(requests, "request", mock_request)

    # create GitHubClient
    client = GitHubClient("test-token","https://api.github.test")

    # call client.request()
    response = client.request(
    method="GET",
    endpoint="/test-user",
    params=None
)
    mock_request.assert_called_once_with("GET",
                    "https://api.github.test/test-user",
                    headers={"Authorization": f"Bearer test-token",
                                "Accept": "application/vnd.github.v3+json",},
                    params=None,
                    timeout=5,)

    # assert result
    assert response["login"] == "Dhruv06000"
    assert response["name"] == "Dhruv Kumar"
# Error

class FakeHTTPErrorResponse404:
    status_code = 404
    reason = "Not Found"

    def raise_for_status(self):
        error = requests.exceptions.HTTPError(self.reason)
        error.response = self
        raise error

def test_github_client_404(monkeypatch):
   mock_request = Mock()
   mock_request.return_value = FakeHTTPErrorResponse404()
   monkeypatch.setattr(requests, "request", mock_request)
   client = GitHubClient("test-token","https://api.github.test")
   with pytest.raises(GitHubClientError) as exc_info:
      client.request(
          method="GET",
          endpoint="/test-user",
          params=None
      )
   assert exc_info.value.status_code == 404
   assert exc_info.value.message == "Not Found" 

class FakeHTTPErrorResponse500:
   status_code = 500
   reason = "Internal Server Error"

   def raise_for_status(self):
      error = requests.exceptions.HTTPError(self.reason)
      error.response = self
      raise error 
   
def test_github_client_500(monkeypatch):
   mock_request = Mock()
   mock_request.return_value = FakeHTTPErrorResponse500()
   monkeypatch.setattr(requests, "request", mock_request)
   client = GitHubClient("test-token","https://api.github.test")
   with pytest.raises(GitHubClientError) as exc_info:
      client.request(
          method="GET",
          endpoint="/test-user",
          params=None
      )
   assert exc_info.value.status_code == 500
   assert exc_info.value.message == "Internal Server Error"

# Time out and other errors 
def test_github_client_network_error(monkeypatch):
   mock_request = Mock()
   mock_request.side_effect = requests.exceptions.RequestException("Connection Fail")
   monkeypatch.setattr(requests, "request", mock_request)
   client = GitHubClient("test-token","https://api.github.test")
   with pytest.raises(GitHubClientError) as exc_info:
         client.request(
             method="GET",
             endpoint="/test-user",
             params=None
         )
    
   assert exc_info.value.status_code == 503
   assert exc_info.value.message == "Unable to communicate with GitHub: Connection Fail"

# Timeout test
def test_github_client_timeout(monkeypatch):
   mock_request = Mock()
   mock_request.side_effect = requests.exceptions.Timeout()
   monkeypatch.setattr(requests, "request",mock_request)
   client = GitHubClient("test-token","https://api.github.test")
   with pytest.raises(GitHubClientError) as exc_info:
      client.request(
             method="GET",
             endpoint="/test-user",
             params=None
         )
   assert exc_info.value.status_code == 503
   assert "Unable to communicate with GitHub" in exc_info.value.message
   