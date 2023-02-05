import json
import requests
import sys
import os

if len(sys.argv) != 2:
    print("Error: URL argument missing")
    sys.exit(1)

url = sys.argv[1]

# Example GraphQL query to retrieve repository information
query = """
query {
  repository(owner:"Rexwang8", name:"ECE461SoftwareEngineeringProject") {
    name
    description
    createdAt
    updatedAt
    diskUsage
    homepageUrl
    pushedAt
    forkCount
    stargazers {
      totalCount
    }
    }
}
"""

headers = {
    "Authorization": "Bearer " + os.environ.get("GITHUB_API_TOKEN"),
    "Content-Type": "application/json"
}

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





