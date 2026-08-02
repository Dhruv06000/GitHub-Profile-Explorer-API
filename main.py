from fastapi import FastAPI, HTTPException, status

import requests


from github_service import (
    calculate_statistics,
    fetch_github_user_profile_info,
    fetch_user_repositories,
    get_user_repositories
)
from models import GitHubUserDashboardResponse,RepositoryResponse



app = FastAPI()

@app.get("/",status_code= status.HTTP_200_OK)
def root():
  return { "Message" : "GitHub Profile Explorer API"}

@app.get("/profile/{user_name}",status_code=status.HTTP_200_OK,response_model=GitHubUserDashboardResponse)
def get_profile(user_name: str) -> GitHubUserDashboardResponse:
  try:
    profile_data = fetch_github_user_profile_info(user_name)
    repositories = fetch_user_repositories(user_name)
    total_stars, language_used, most_used_language = calculate_statistics(repositories)
    return {
       "profile" : profile_data,
      #  "Repositories" : repositories,
       "statistics" : {
          "total_stars" : total_stars,
          "languages_used" : language_used,
          "most_used_language" : most_used_language
       }
    }
  except requests.exceptions.HTTPError as err:
    status_code = err.response.status_code
    raise HTTPException(
      status_code= status_code,
      detail=f"GitHub API error :{err.response.reason}"
    )
  except requests.exceptions.RequestException:
        # Catch network timeouts or connection drops
        raise HTTPException(
            status_code=503, 
            detail="GitHub service is temporarily unavailable"
        )

@app.get("/profile/{user_name}/repositories",status_code = status.HTTP_200_OK,response_model = list[RepositoryResponse])
def get_repositories(user_name: str,language : str | None = None, visibility: str | None = None) -> list[RepositoryResponse]:
   try:
      repositories = get_user_repositories(user_name, language , visibility)
      return repositories
   except requests.exceptions.HTTPError as err:
      status_code = err.response.status_code
      raise HTTPException(
         status_code= status_code,
         detail=f"GitHub API error :{err.response.reason}"
      )
   except requests.exceptions.RequestException:
           # Catch network timeouts or connection drops
           raise HTTPException(
               status_code=503, 
               detail="GitHub service is temporarily unavailable"
           )
   
  