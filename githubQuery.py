from string import Template
from requests import get, post

userInfoQuery = """
{
    viewer {
      login
      id
    }
  }
"""

createContributedRepoQuery = Template("""
query {
    user(login: "$username") {
      repositoriesContributedTo(last: 100, includeUserRepositories: true) {
        nodes {
          isFork
          name
          owner {
            login
          }
        }
      }
    }
  }
""")

createCommittedDateQuery = Template("""
query {
    repository(owner: "$owner", name: "$name") {
      ref(qualifiedName: "master") {
        target {
          ... on Commit {
            history(first: 100, author: { id: "$id" }) {
              edges {
                node {
                  committedDate
                }
              }
            }
          }
        }
      }
    }
  }
""")


repositoryListQuery = Template("""
{
  user(login: "$username") {
    repositories(orderBy: {field: CREATED_AT, direction: ASC}, last: 100, affiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER], isFork: false) {
      totalCount
      edges {
        node {
          object(expression:"master") {
                ... on Commit {
                history (author: { id: "$id" }){
                totalCount
                    }
                }
                }
          primaryLanguage {
            color
            name
            id
          }
          stargazers {
            totalCount
          }
          collaborators {
            totalCount
          }
          createdAt
          name
          owner {
            id
            login
          }
          nameWithOwner
        }
      }
    }
    location
    createdAt
    name
  }
}
""")


getLinesOfCodeQuery = Template("""/repos/$owner/$repo/stats/code_frequency""")

getProfileViewQuery = Template(
    """/repos/$owner/$repo/traffic/views""")

getProfileTrafficQuery = Template(
    """/repos/$owner/$repo/traffic/popular/referrers""")


class RunQuery():

    def __init__(self, headers):
        self.headers = headers

    def runGithubAPIQuery(self, query):
        request = get("https://api.github.com" + query, headers=self.headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(
                "Query failed to run by returning code of {}. {},... {}".format(
                    request.status_code, query, str(request.json())))

    def runGithubGraphqlQuery(self, query) -> dict:
        request = post("https://api.github.com/graphql",
                       json={"query": query}, headers=self.headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(
                request.status_code, query))

    def runGithubContributionsQuery(self, username):
        request = get(
            "https://github-contributions.now.sh/api/v1/" + username)
        if request.status_code == 200:
            return request.json()
