import json
import requests
import sys
import os

if len(sys.argv) != 2:
    print("Error: URL argument missing")
    sys.exit(1)

url = sys.argv[1]

OWNER = "Rexwang8"
REPO = "ECE461SoftwareEngineeringProject"

headers = {
    "Authorization": "Bearer " + os.environ.get("GITHUB_API_TOKEN"),
    "Content-Type": "application/json"
}

HEADERS = {
    "Authorization": f"Token {os.environ.get('GITHUB_API_TOKEN')},
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

# Example GraphQL query to retrieve repository information
query = """
query {
  repository(owner:OWNER, name:REPO) {
    name
    description
    createdAt
    updatedAt
    diskUsage
    licenseInfo {
      name
      spdxId
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

response = requests.post(url, json={'query': query}, headers=headers)

# Check for API response status
if response.status_code != 200:
    print("Failed to retrieve repository information.")
    sys.exit(1)

# Write JSON response to output file
with open("output.json", "w") as f:
    json.dump(response.json(), f)
print(response)
print("Repository information successfully written to output.json.")





