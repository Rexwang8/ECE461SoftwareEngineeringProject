import json
import requests
import sys

if len(sys.argv) != 4: #1st arg name of json file 2nd arg github url 3rd arg is token
    #print("Error: URL argument missing")
    sys.exit(1)

def parse_github_url(url):
    return url.split('/')[-2], url.split('/')[-1]

the_owner, the_repo = parse_github_url(sys.argv[2])

headers = {
    "Authorization": "Bearer " + sys.argv[3],	#the token
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
with open(sys.argv[1] + ".json", "w") as f:
    json.dump(response.json(), f)

