# main.py code :
from fastapi import FastAPI, status , Query, Depends


from fastapi.responses import JSONResponse

from github_service import (
    calculate_statistics,
    fetch_github_user_profile_info,
    fetch_user_repositories,
    get_user_repositories,
    GitHubServiceError
)

from models import (
  GitHubUserDashboardResponse,
  RepositoryResponse
)

from enums import (
    SortOption,
    OrderOption
)

from github_client import GitHubClient

from settings import settings

github_client = GitHubClient(
   settings.github_token,
   settings.github_api_url
)
def get_github_client():
    return github_client

app = FastAPI()

@app.exception_handler(GitHubServiceError)
async def github_service_error_handler(request, exc: GitHubServiceError):
   return JSONResponse(
      status_code=exc.status_code,
      content={"detail": exc.message},
   )

@app.get("/",status_code= status.HTTP_200_OK)
def root():
  return { "Message" : "GitHub Profile Explorer API"}

@app.get("/profile/{user_name}",status_code=status.HTTP_200_OK,response_model=GitHubUserDashboardResponse)
def get_profile(user_name: str, client : GitHubClient = Depends(get_github_client)) -> GitHubUserDashboardResponse:
    profile_data = fetch_github_user_profile_info(user_name,client)
    repositories = fetch_user_repositories(user_name,client)
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
  

@app.get("/profile/{user_name}/repositories",status_code = status.HTTP_200_OK,response_model = list[RepositoryResponse])
def get_repositories(
   user_name: str,
   page : int = Query(default= 1 , ge=1, description = "Page number to retrieve."),
   per_page : int = Query(default=30, ge=1, le=100, description="Number of repositories to retrieve per page"),
   client: GitHubClient = Depends(get_github_client),
   language : str | None = None,
   visibility: str | None = None, 
   sort : SortOption | None = None , 
   order : OrderOption |None = None 
   ) -> list[RepositoryResponse]:
   repositories = get_user_repositories(user_name,
                                        page ,
                                        per_page,
                                        client, 
                                        language , 
                                        visibility,
                                        sort,
                                        order)
   return repositories
   