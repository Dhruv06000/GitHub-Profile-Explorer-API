from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProfileResponse(BaseModel):
  login : str
  name : Optional[str] = None
  avatar_url : str
  bio : Optional[str] = None
  company : Optional[str] = None
  location : Optional[str] = None
  blog : Optional[str] = None
  followers : int
  following : int
  public_repos : int 
  html_url : str
  created_at : datetime

class StatisticsResponse(BaseModel):
    total_stars: int
    languages_used: dict[str, int]
    most_used_language: str

# This is Composition :
class GitHubUserDashboardResponse(BaseModel):
   profile : ProfileResponse
   statistics : StatisticsResponse

# class LicenseName(BaseModel):
#    name : str

class RepositoryResponse(BaseModel):
   name : str
   description : str | None = None
   html_url : str
   language : str | None = None
   visibility : str
   stargazers_count : int
   forks_count : int
   open_issues_count : int
   updated_at : datetime
   pushed_at : datetime
   license : str | None = None