import json
import requests
import sys

def parse_github_url(url):
    return url.split('/')[-2], url.split('/')[-1]

def run_git_module(name, url, token):
    the_owner, the_repo = parse_github_url(url)
    headers = {
        "Authorization": "Bearer " + token,	#the token
        "Content-Type": "application/json"
    }

    # Example GraphQL query to retrieve repository information
    query = """
    query {{
      repository(owner: "{}", name: "{}") {{
        name
        description
        createdAt
        updatedAt
        diskUsage
        licenseInfo {{
          name
          spdxId
        }}
        isEmpty
        isDisabled
        isFork
        isPrivate
        watchers(first:100) {{
          totalCount
        }}
        issues(first:100) {{
          totalCount
        }}
        
        homepageUrl
        pushedAt
        forkCount
        stargazers {{
          totalCount
        }}
      }}
    }}
    """.format(the_owner, the_repo)

    response = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)

    # Check for API response status
    if response.status_code != 200:
        
        sys.exit(1)

    # Write JSON response to output file
    with open(name + ".json", "w") as f:
        json.dump(response.json(), f)

if __name__ == "__main__":
    if len(sys.argv) != 4: #1st arg name of json file 2nd arg github url 3rd arg is token
    	print("Incorrect number of arguments")
    	sys.exit(1)
    else:
        the_url = sys.argv[2]
        the_token = sys.argv[3]
        the_name = sys.argv[1]
        run_git_module(the_name, the_url, the_token)



