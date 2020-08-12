from requests import get, post
from re import sub
from base64 import b64decode


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


def makeGraph(percent: float) -> str:
    '''Make progress graph from API graph'''
    done_block = '█'
    empty_block = '░'
    pc_rnd = round(percent)
    return f"{done_block * int(pc_rnd / 4)}{empty_block * int(25 - int(pc_rnd / 4))}"


def makeLanguageList(data: list) -> str:
    '''Make List'''
    data_list = []
    for l in data:
        ln = len(l['name'])
        ln_text = len(l['text'])
        op = f"{l['name'][:25]}{' ' * (25 - ln)}{l['text']}{' ' * (20 - ln_text)}{makeGraph(l['percent'])}   {l['percent']}%"
        data_list.append(op)
    return ' \n'.join(data_list)


def makeCommitList(data: list) -> str:
    '''Make List'''
    data_list = []
    for l in data[:7]:
        ln = len(l['name'])
        ln_text = len(l['text'])
        op = f"{l['name']}{' ' * (13 - ln)}{l['text']}{' ' * (15 - ln_text)}{makeGraph(l['percent'])}   {l['percent']}%"
        data_list.append(op)
    return ' \n'.join(data_list)


def generateREADME(stats: str, readme: bytes):
    '''Generate a new Readme.md'''
    print("Generating NEW README.md file... ", end="")
    readme = decodeREADME(readme)
    START_COMMENT = '<!--START_SECTION:readme-info-->'
    END_COMMENT = '<!--END_SECTION:readme-info-->'
    listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

    stats_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
    print("Done")
    return sub(listReg, stats_in_readme, readme)


def decodeREADME(data: str):
    '''Decode the contents of old README'''
    decoded_bytes = b64decode(data)
    return str(decoded_bytes, 'utf-8')
