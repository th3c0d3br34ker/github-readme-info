# Python: 3.8.x

# System Imports
from os import getenv
from datetime import datetime
from traceback import print_exc


# Third Party Imports
from github import Github
from dotenv import load_dotenv
import humanize
from pytz import utc, timezone

# Custom Imports
from githubQuery import *
from ReadmeMaker import ReadmeGenerator
from utility import makeCommitList, makeLanguageList

# Load Environment Variables
load_dotenv()

# Get TOKEN
ghtoken = getenv('INPUT_GH_TOKEN')


def getDailyCommitData(repositoryList: list) -> str:
    print("Generating Daily Commit Data... ")

    if getenv('INPUT_TIMEZONE') == None:
        tz = "Asia/Kolkata"
    else:
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

    print("Daily Commit Data created!")

    return "**" + title + "** \n" + """
| | | | |
| --- | --- | --- | --- |
""" + makeCommitList(eachDay) + """
| | | | |\n"""


def getWeeklyCommitData(repositoryList: list) -> str:
    print("Generating Weekly Commit Data... ")

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
            print("ERROR", repository["name"])

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

    print("Weekly Commit Data created!")

    title = 'I\'m Most Productive on ' + max_element['name'] + 's'
    return "📅 **" + title + "** \n"+"""
| | | | |
| --- | --- | --- | --- |
""" + makeCommitList(dayOfWeek) + """
| | | | |\n"""


def getLanguagesPerRepo() -> str:
    print("Generating Most used Language... ", end="")

    language_count = {}
    total = 0
    result = Query.runGithubGraphqlQuery(
        repositoryListQuery.substitute(username=username, id=id))

    for repo in result['data']['user']['repositories']['edges']:
        if repo['node']['primaryLanguage'] is None:
            continue
        language = repo['node']['primaryLanguage']['name']
        color_code = repo['node']['primaryLanguage']['color']
        total += 1
        if language not in language_count.keys():
            language_count[language] = {}
            language_count[language]['count'] = 1
        else:
            language_count[language]['count'] = language_count[language]['count'] + 1
        language_count[language]['color'] = color_code
    data = []
    sorted_labels = list(language_count.keys())
    sorted_labels.sort(key=lambda x: language_count[x]['count'], reverse=True)
    most_language_repo = sorted_labels[0]
    for label in sorted_labels:
        percent = round(language_count[label]['count'] / total * 100, 2)
        data.append({
            "name": label,
            "text": str(language_count[label]['count']) + " repos",
            "percent": percent
        })

    print("Done")
    title = "My 💖 languages " + most_language_repo
    return "**" + title + "** \n" + """
| | | | |
| --- | --- | --- | --- |
""" + makeLanguageList(data) + """
| | | | |\n"""


def getProfileViews() -> str:

    data = Query.runGithubAPIQuery(getProfileViewQuery.substitute(
        owner=username, repo=username))

    return ('**✨ ' + str(data["count"]) + ' people were here!**\n\n')


def getLinesOfCode(repositoryList):
    print("Generating Lines Of Code... ", end="")
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
    print("Done")
    return ("**From Hello World I have written " + humanize.intword(int(totalLOC)) + " Lines of Code ✍️**\n\n")


def getTotalContributions():
    data = Query.runGithubContributionsQuery(username)
    total = data['years'][0]['total']
    year = data['years'][0]['year']
    return "**🏆 " + humanize.intcomma(total) + " Contributions in year " + year + "**\n\n"


def generateData() -> str:

    stats = ""
    print("Generating new README Data... ")

    ReadmeMaker = ReadmeGenerator(readme.content)

    result = Query.runGithubGraphqlQuery(
        createContributedRepoQuery.substitute(username=username))
    nodes = result["data"]["user"]["repositoriesContributedTo"]["nodes"]

    repos = [d for d in nodes if d['isFork'] is False]

    if getenv('INPUT_SHOW_TOTAL_CONTRIBUTIONS') == 'True':
        stats = getTotalContributions()
        ReadmeMaker.generateTotalContributions(stats)
    if getenv("INPUT_SHOW_LINES_OF_CODE") == 'True':
        stats = getLinesOfCode(repos)
        ReadmeMaker.generateLinesOfCodeStats(stats)
    if getenv("INPUT_SHOW_PROFILE_VIEWS") == 'True':
        stats = getProfileViews()
        ReadmeMaker.generateProfileViewsStats(stats)
    if getenv("INPUT_SHOW_DAILY_COMMIT") == 'True':
        stats = getDailyCommitData(repos)
        ReadmeMaker.generateDailyStats(stats)
    if getenv("INPUT_SHOW_WEEKLY_COMMIT") == 'True':
        stats = getWeeklyCommitData(repos)
        ReadmeMaker.generateWeeklyStats(stats)
    if getenv("INPUT_SHOW_LANGUAGE") == 'True':
        stats = getLanguagesPerRepo()
        ReadmeMaker.generateMostUsedLanguage(stats)

    print("README data created!")

    newREADME = ReadmeMaker.getREADME()
    return newREADME


if __name__ == "__main__":
    try:
        if ghtoken is None:
            raise Exception("Token not available")

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

        readme = repo.get_readme()

        # Running task now ...
        newREADME = generateData()

        repo.update_file(path=readme.path, message="⤴ Auto Updated README",
                         content=newREADME, sha=readme.sha, branch='master')
    except Exception as e:
        print_exc()
        print("ERROR:: ", str(e))
