import json
import requests
import sys
import os

if len(sys.argv) != 3:
    print("Error: URL argument missing")
    sys.exit(1)

url = sys.argv[2]

the_owner = "Rexwang8"
the_repo = "ECE461SoftwareEngineeringProject"

headers = {
    "Authorization": "Bearer " + os.environ.get("GITHUB_API_TOKEN"),
    "Content-Type": "application/json"
}
'''
HEADERS = {
    "Authorization": f"Token {os.environ.get('GITHUB_API_TOKEN')}",
    "Accept": "application/vnd.github.vUL-preview+json",
}

def get_security_vulnerabilities(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/vulnerabilities"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        vulnerabilities = response.json()
        for vulnerability in vulnerabilities:
            print(vulnerability["id"], vulnerability["package_name"], vulnerability["severity"])
    else:
        print(f"Error retrieving security vulnerabilities: {response.text}")

get_security_vulnerabilities(OWNER, REPO)
'''
# Example GraphQL query to retrieve repository information
query = """
query {
  repository(owner:the_owner, name:the_repo) {
    name
    description
    createdAt
    updatedAt
    diskUsage
    licenseInfo {
      name
      spdxId
    } 
    isEmpty
    isDisabled
    isFork
    isPrivate
    watchers(first:100) {
      nodes {
        login
      }
    }
    collaborators(first: 100) {
      nodes {
        login
        name
        email
        avatarUrl
      }
    }
    discussions(first: 100) {
      edges {
        node {
          id
          body
          createdAt
          updatedAt
        }
      }
    }
    homepageUrl
    pushedAt
    forkCount
    stargazers {
      totalCount
    }
    }
}
"""

response = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)

# Check for API response status
if response.status_code != 200:
    print("Failed to retrieve repository information.")
    sys.exit(1)

# Write JSON response to output file
with open(sys.argv[1] + ".json", "w") as f:
    json.dump(response.json(), f)
    print(response.json())
print(response)
print("Repository information successfully written to " + sys.argv[1] + ".json")





