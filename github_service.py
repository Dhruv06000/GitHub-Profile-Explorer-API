# github_service.py code :
from github_client import GitHubClient, GitHubClientError
from models import RepositoryResponse
from enums import (
    SortOption,
    OrderOption
)
from settings import settings

class GitHubServiceError(Exception):
    """Custom exception for GitHub service errors."""
    def __init__(self, status_code : int , message: str):
      self.status_code = status_code
      self.message = message
      # Pass the customized message back to the base Exception class
      super().__init__(f"GitHub API Error {status_code}: {message}")

def fetch_github_user_profile_info(user_name, client: GitHubClient):
  """Featch GitHub user profile information using the provided GitHubClient."""
  try:
    endpoint = f"/users/{user_name}"
    return client.request("GET", endpoint)
  except GitHubClientError as e:
    if e.status_code == 404:
      raise GitHubServiceError(
          404,
          "GitHub user not found"
      )
    elif 500 <= e.status_code <= 599:
      raise GitHubServiceError(
          503,
          "GitHub service is temporarily unavailable"
      )
    else:
      raise GitHubServiceError(
          e.status_code,
          e.message
      )

  
def fetch_user_repositories(user_name, client: GitHubClient):

  page = 1
  all_repo = []
  while True:
    
    endpoint = f"/users/{user_name}/repos"
    params = {
          "per_page": 100,
          "page": page
      }
    try:
      data = client.request("GET", endpoint, params=params)
      all_repo.extend(data)
      if len(data) < 100:
        break
      page += 1

    except GitHubClientError as e:
      if e.status_code == 404:
        raise GitHubServiceError(
            404,
            "GitHub user not found"
        )
      elif 500 <= e.status_code <= 599:
        raise GitHubServiceError(
            503,
            "GitHub service is temporarily unavailable"
        )
      else:
        raise GitHubServiceError(
            e.status_code,
            e.message
        )
  return all_repo


def get_user_repositories(
    user_name: str,
    page : int,
    per_page : int,
    client: GitHubClient,
    language : str | None = None,
    visibility : str | None = None,
    sort : SortOption | None = None ,
    order : OrderOption | None = None
    ) -> list[RepositoryResponse]:
  # Fetch
  repositories = fetch_user_repositories(user_name,client)

  # Filter
  visibility = visibility.strip().lower() if visibility else None
  language =  language.strip().lower() if language else None
  if visibility:
    repositories = [repo for repo in repositories if repo["visibility"].lower() == visibility]
  if language:
    repositories = [repo  for repo in repositories if repo["language"] and repo["language"].lower() == language]

  # Sort
  sort_mapping = {
    SortOption.NAME: "name",
    SortOption.STARS: "stargazers_count",
    SortOption.FORKS: "forks_count",
    SortOption.UPDATED: "updated_at"
  }
  if sort in sort_mapping:
    sort_key = sort_mapping[sort.value]
    repositories = sorted(repositories, key = lambda repo : repo[sort_key] , reverse = order == OrderOption.DESC)

  # Pagination
  start = (page - 1) * per_page
  end = start + per_page
  paginated_repositories = repositories[start:end]
  
  # Transform
  result = []
  for repo in paginated_repositories:
    license_name = repo["license"]["name"] if repo["license"] else None

    result.append(RepositoryResponse(
      name = repo["name"],
      description = repo["description"],
      html_url = repo["html_url"],
      language = repo["language"],
      visibility = repo["visibility"],
      stargazers_count = repo["stargazers_count"],
      forks_count = repo["forks_count"],
      open_issues_count = repo["open_issues_count"],
      updated_at = repo["updated_at"],
      pushed_at = repo["pushed_at"],
      license = license_name
    ))
  return result

  
  
  
def calculate_statistics(repositories):
  
  total_stars = sum(repo["stargazers_count"] for repo in repositories)
  language_used = {}

  for repo in repositories:
    if repo["language"]:
      language_used[repo["language"]] = language_used.get(repo["language"], 0) + 1
  most_used_language = (
    max(language_used, key = language_used.get)
    if language_used else "No Language data"
    )
  return  total_stars, language_used, most_used_language
  
