import requests


class GitHubClientError(Exception):
    """Exception raised when communication with GitHub fails."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


class GitHubClient:
    def __init__(self, github_token, github_api_url):
        self.base_url = github_api_url
        self.github_token = github_token

        self.headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def request(self, method, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                params=params,
                timeout=5,
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code

            raise GitHubClientError(
                status_code,
                err.response.reason or "GitHub API request failed",
            )

        except requests.exceptions.RequestException as err:
            raise GitHubClientError(
                503,
                f"Unable to communicate with GitHub: {err}",
            )
        
  
