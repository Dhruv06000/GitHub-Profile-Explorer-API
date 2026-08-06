# github_service.py code :
import requests
from models import RepositoryResponse
from enums import (
    SortOption,
    OrderOption
)


def fetch_github_user_profile_info(user_name):
  # username = input("Enter Github username:")
  url = f"https://api.github.com/users/{user_name}"
  response = requests.get(url, timeout = 5)
  
  response.raise_for_status()
  data = response.json()
    
  return data

  
def fetch_user_repositories(user_name):

  page = 1
  all_repo = []
  while True:
    url = f"https://api.github.com/users/{user_name}/repos"
    response = requests.get(url, 
                            params={
                              "page": page,
                              "per_page" : 100
                            },
                            timeout = 5)
    response.raise_for_status()
    data = response.json()
    all_repo.extend(data)
    if len(data) < 100:
      break
    page += 1

  return all_repo

def get_user_repositories(
    user_name: str,
    page : int,
    per_page : int,
    language : str | None = None,
    visibility : str | None = None,
    sort : SortOption | None = None ,
    order : OrderOption | None = None
    ) -> list[RepositoryResponse]:
  # Fetch
  repositories = fetch_user_repositories(user_name)

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
  
