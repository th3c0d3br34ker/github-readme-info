from re import sub
from base64 import b64decode


# TODO: Make for each Section

class ReadmeGenerator():

    def __init__(self, readme):
        self.readme = self.decodeREADME(readme)

    def getREADME(self):
        return self.readme

    def generateDailyStats(self, stats: str):
        print("Generating Daily Section... ", end="")
        START_COMMENT = '<!--START_SECTION_DAILY_COMMIT:readme-info-->'
        END_COMMENT = '<!--END_SECTION_DAILY_COMMIT:readme-info-->'
        daily_commit_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
        listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

        self.readme = sub(listReg, daily_commit_in_readme, self.readme)
        print("Done")

    def generateWeeklyStats(self, stats: str):
        print("Generating Weekly Section... ", end="")
        START_COMMENT = '<!--START_SECTION_WEEKLY_COMMIT:readme-info-->'
        END_COMMENT = '<!--END_SECTION_WEEKLY_COMMIT:readme-info-->'
        weekly_commit_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
        listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

        self.readme = sub(listReg, weekly_commit_in_readme, self.readme)
        print("Done")

    def generateProfileViewsStats(self, stats: str):
        print("Generating Profile Views Section... ", end="")
        START_COMMENT = '<!--START_SECTION_PROFILE_VIEWS:readme-info-->'
        END_COMMENT = '<!--END_SECTION_PROFILE_VIEWS:readme-info-->'
        profile_views_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
        listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

        self.readme = sub(listReg, profile_views_in_readme, self.readme)
        print("Done")

    def generateLinesOfCodeStats(self, stats: str):
        print("Generating Lines Of Code Section... ", end="")
        START_COMMENT = '<!--START_SECTION_LINES_OF_CODE:readme-info-->'
        END_COMMENT = '<!--END_SECTION_LINES_OF_CODE:readme-info-->'
        lines_of_code_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
        listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

        self.readme = sub(listReg, lines_of_code_in_readme, self.readme)
        print("Done")

    def generateMostUsedLanguage(self, stats: str):
        print("Generating Lines Of Code Section... ", end="")
        START_COMMENT = '<!--START_SECTION_LANGUAGE:readme-info-->'
        END_COMMENT = '<!--END_SECTION_LANGUAGE:readme-info-->'
        language_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
        listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

        self.readme = sub(listReg, language_in_readme, self.readme)
        print("Done")

    def generateTotalContributions(self, stats: str):
        print("Generating Total Contributions Section... ", end="")
        START_COMMENT = '<!--START_CONTRIBUTIONS:readme-info-->'
        END_COMMENT = '<!--END_CONTRIBUTIONS:readme-info-->'
        contributions_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
        listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

        self.readme = sub(listReg, contributions_in_readme, self.readme)
        print("Done")

    def generateSayThanks(self):
        START_COMMENT = '<!--START_SECTION_THANK_ME:readme-info-->'
        END_COMMENT = '<!--END_SECTION_THANK_ME:readme-info-->'
        stats = "Made with 🖤 by [Jainam Desai](https://th3c0d3br34ker.github.io)"
        lines_of_code_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
        listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

        self.readme = sub(listReg, lines_of_code_in_readme, self.readme)
        print("Thank You! ❤")

    @staticmethod
    def decodeREADME(data: str):
        '''Decode the contents of old README'''
        decoded_bytes = b64decode(data)
        return str(decoded_bytes, 'utf-8')
