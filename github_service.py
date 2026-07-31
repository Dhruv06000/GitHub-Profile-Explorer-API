import requests



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
  
  
# def main():
  
#   try:
#     user_name = input("Enter Github username: ")
#     print("\n========================\nPROFILE\n========================\n")

#     profile = fetch_github_user_profile_info(user_name)
#     print(f'Username : {profile["login"]}\nName : {profile["name"]}\nFollowers: {profile["followers"]}\nRepos    : {profile["public_repos"]}\nEmail : {profile["email"] or "Not Public"}\n')

#     repositories = fetch_user_repositories(user_name)
#     # print("\n========================\nREPOSITORIES\n========================\n")
#     # for index, repo in enumerate(repositories, start= 1):
#     #   print(f'{index}. {repo["name"]}\n    Language : {repo["language"] or "Not Specified"}\n    Stars : {repo["stargazers_count"]}\n')

#     total_stars, language_used, most_used_language = calculate_statistics(repositories)
#     print("\n========================\nSTATISTICS\n========================\n")
#     print(f'Total Repositories : {len(repositories)}\n\nTotal Stars : {total_stars}\n\nMost Used Language: {most_used_language}\n\nLanguage Used\n')
#     for language, count in language_used.items():
#       print(f'{language} : {count}')

#   except requests.exceptions.Timeout:
#       # Request took too long
#       print("❌ The request timed out. Please check your internet connection or try again later.")

#   except requests.exceptions.RequestException as e:
#       # Other request-related problems
#       print(f"❌ Failed to communicate with the GitHub API: {e}")

#   except Exception as e:
#       # Programming errors or anything unexpected
#       print(f"❌ An unexpected error occurred: {e}")

# if __name__ == "__main__":
#   main()