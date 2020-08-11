# Python: 3.8.x

# System Imports

from os import getenv
from datetime import datetime
from traceback import print_exc


# Third Party Imports
from github import Github, GithubException
from dotenv import load_dotenv
import humanize
from pytz import utc, timezone

# Custom Imports
from githubQuery import *
from utility import RunQuery, makeCommitList

# Load Environment Variables
load_dotenv()

START_COMMENT = '<!--START_SECTION:readme-info-->'
END_COMMENT = '<!--END_SECTION:readme-info-->'
listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

# Get TOKEN
ghtoken = getenv('INPUT_GH_TOKEN')

# Get System Variables
showCommit = getenv('INPUT_SHOW_COMMIT')
show_days_of_week = getenv('INPUT_SHOW_DAYS_OF_WEEK')


def getDailyCommitData(repositoryList: list) -> str:
    tz = getenv('INPUT_TIMEZONE')

    morning = 0  # 4 - 10
    daytime = 0  # 10 - 16
    evening = 0  # 16 - 22
    nighttime = 0  # 0 - 4

    for repository in repositoryList:
        result = Query.runGithubGraphqlQuery(
            createCommittedDateQuery.substitute(owner=repository["owner"]["login"], name=repository["name"], id=id))
        try:
            commitedDates = result["data"]["repository"]["ref"]["target"]["history"]["edges"]

            for committedDate in commitedDates:
                date = datetime.strptime(committedDate["node"]["committedDate"],
                                         "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc).astimezone(
                    timezone(tz))

                hour = date.hour

                if 6 <= hour < 12:
                    morning += 1
                if 12 <= hour < 18:
                    daytime += 1
                if 18 <= hour < 24:
                    evening += 1
                if 0 <= hour < 6:
                    nighttime += 1
        except Exception as exception:
            print("ERROR", repository["name"], "is private!")

    totalCommits = morning + daytime + evening + nighttime

    if morning + daytime >= evening + nighttime:
        title = "I'm an early 🐤"
    else:
        title = "I'm a night 🦉"

    eachDay = [
        {"name": "🌞 Morning", "text": str(
            morning) + " commits", "percent": round((morning / totalCommits) * 100, 2)},
        {"name": "🌆 Daytime", "text": str(
            daytime) + " commits", "percent": round((daytime / totalCommits) * 100, 2)},
        {"name": "🌃 Evening", "text": str(
            evening) + " commits", "percent": round((evening / totalCommits) * 100, 2)},
        {"name": "🌙 Night", "text": str(
            nighttime) + " commits", "percent": round((nighttime / totalCommits) * 100, 2)},
    ]

    data = '**' + title + '** \n\n' + \
        '```text\n' + makeCommitList(eachDay) + '\n\n```\n'

    return data


def getWeeklyCommitData(repositoryList: list) -> str:
    tz = getenv('INPUT_TIMEZONE')

    weekdays = [0, 0, 0, 0, 0, 0, 0]

    for repository in repositoryList:
        result = Query.runGithubGraphqlQuery(
            createCommittedDateQuery.substitute(owner=username, name=repository["name"], id=id))
        try:
            commitedDates = result["data"]["repository"]["ref"]["target"]["history"]["edges"]

            for committedDate in commitedDates:
                date = datetime.strptime(committedDate["node"]["committedDate"],
                                         "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc).astimezone(
                    timezone(tz))

                weekday = date.strftime('%A')

                if weekday == "Monday":
                    weekdays[0] += 1
                if weekday == "Tuesday":
                    weekdays[1] += 1
                if weekday == "Wednesday":
                    weekdays[2] += 1
                if weekday == "Thursday":
                    weekdays[3] += 1
                if weekday == "Friday":
                    weekdays[4] += 1
                if weekday == "Saturday":
                    weekdays[5] += 1
                if weekday == "Sunday":
                    weekdays[6] += 1

        except Exception as exception:
            print("ERROR", repository["name"], "is private!")

    totalCommits = sum(weekdays)

    dayOfWeek = [
        {"name": "Monday", "text": str(
            weekdays[0]) + " commits", "percent": round((weekdays[0] / totalCommits) * 100, 2)},
        {"name": "Tuesday", "text": str(
            weekdays[1]) + " commits", "percent": round((weekdays[1] / totalCommits) * 100, 2)},
        {"name": "Wednesday", "text": str(
            weekdays[2]) + " commits", "percent": round((weekdays[2] / totalCommits) * 100, 2)},
        {"name": "Thursday", "text": str(
            weekdays[3]) + " commits", "percent": round((weekdays[3] / totalCommits) * 100, 2)},
        {"name": "Friday", "text": str(
            weekdays[4]) + " commits", "percent": round((weekdays[4] / totalCommits) * 100, 2)},
        {"name": "Saturday", "text": str(
            weekdays[5]) + " commits", "percent": round((weekdays[5] / totalCommits) * 100, 2)},
        {"name": "Sunday", "text": str(
            weekdays[6]) + " commits", "percent": round((weekdays[6] / totalCommits) * 100, 2)},
    ]

    max_element = {
        'percent': 0
    }

    for day in dayOfWeek:
        if day['percent'] > max_element['percent']:
            max_element = day

    title = 'I\'m Most Productive on ' + max_element['name'] + 's'

    data = '📅 **' + title + '** \n\n' + \
        '```text\n' + makeCommitList(dayOfWeek) + '\n\n```\n'

    return data


def getProfileViews() -> str:

    data = Query.runGithubAPIQuery(getProfileViewQuery.substitute(
        owner=username, repo=username))
    return str(data["count"])


def getLinesOfCode(repositoryList):

    totalLOC = 0
    for repository in repositoryList:
        try:
            # time.sleep(0.7)
            datas = Query.runGithubAPIQuery(getLinesOfCodeQuery.substitute(
                owner=repository["owner"]["login"], repo=repository["name"]))
            for data in datas:
                totalLOC += (data[1] - data[2])
        except Exception as execption:
            print(execption)

    return humanize.intword(int(totalLOC))


def generateCommitData() -> str:

    string = ''
    print("Generating Commit Data for... {}".format(username))

    result = Query.runGithubGraphqlQuery(
        createContributedRepoQuery.substitute(username=username))
    nodes = result["data"]["user"]["repositoriesContributedTo"]["nodes"]

    repos = [d for d in nodes if d['isFork'] is False]

    print("Lines Of Code: ", getLinesOfCode(repos))
    print("Profile Views: ", getProfileViews())
    print(getWeeklyCommitData(repos))
    print(getDailyCommitData(repos))

    return string


if __name__ == "__main__":
    try:
        if ghtoken is None:
            raise Exception('Token not available')

        # Strart the Calculation
        githubObject = Github(ghtoken)
        headers = {"Authorization": "Bearer " + ghtoken}

        Query = RunQuery(headers)

        # Execute the query
        user_data = Query.runGithubGraphqlQuery(userInfoQuery)
        username = user_data["data"]["viewer"]["login"]
        id = user_data["data"]["viewer"]["id"]

        print("Running task for... ", username)

        # Get user repository
        repo = githubObject.get_repo(f"{username}/{username}")

        # Running task now ...
        print(generateCommitData())
    except Exception as e:
        print_exc()
        print("ERROR:: ", str(e))
