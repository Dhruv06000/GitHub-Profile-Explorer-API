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