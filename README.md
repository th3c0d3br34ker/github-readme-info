<h1 align="center">✨README Info Generator ✨</h1>

<p align="center">
<img src="https://img.shields.io/badge/Made%20with-Python-blue.svg"/>
<img src="https://img.shields.io/badge/Made%20with-Markdown-black.svg"/>
<img src="https://img.shields.io/github/license/th3c0d3br34ker/github-readme-info"/>
<img src="https://img.shields.io/github/stars/th3c0d3br34ker/github-readme-info"/>
<img src="https://img.shields.io/github/forks/th3c0d3br34ker/github-readme-info"/> 
<img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=this%20Repository&style=style=flat&color=blue" alt="Star Badge"/>
<img src="https://app.codacy.com/project/badge/Grade/282ae5620b4140c99a0c5f4b8e6a362a"/>
</p>

<span align="center">

Flex your Stats with this highly customizable tool!<br/>
Are you an early 🐤 or a night 🦉?<br/>
When are you most productive during the day?<br/>
What are languages you code in?<br/>

</span>

## Setup

1.  You need to update the markdown file(.md) with the `START_SECTION` and `STOP_SECTION` comments. You can refer [this](#entry-points) section for updating it.

2.  You'll need a GitHub API Token with `repo` and `user` scope from [here](https://github.com/settings/tokens) if you're running the action to get commit metrics

> enabling the `repo` scope seems **DANGEROUS**<br/>
> but this GitHub Action only accesses your commit timestamp and lines of code added or deleted in repository you contributed.

3.  You need to save the GitHub API Token in the repository secrets. You can find that in the Settings of your repository. Be sure to save those as GitHub Personal Access Token as `GH_TOKEN=<your github access token>`

4.  You can enable and disable feature flags based on requirements. See [this](#flags-available).

5.  For the final step you need to add an `.yml` file in your workflows folder. You can copy/paste [this](./example/readme-info-schedule.yml) example file and enable/disable flags as you wish!.

### The Required fields are

> GH_TOKEN Your GitHub token explainer in Step 2.  
> TIMEZONE Your timezone, defaults to "Asia/Kolkata" for India.

### Entry Points

Add a comment to your `README.md` like this:

```md
<!--START_SECTION:readme-info-->
<!--END_SECTION:readme-info-->
```

See this example [file](./example/README.md). You can put these Entry Points anywhere and in any order you please! 🤷‍♂️

## Flags Available

`SHOW_LINES_OF_CODE` flag can be set to `True` to show the Lines of code writen till date

```text
From Hello World I have written 1.6 million Lines of Code ✍️
```

`SHOW_PROFILE_VIEWS` flag can be set to `False` to hide the Profile views

```text
✨ 216 people were here!
```

`SHOW_DAILY_COMMIT` flag can be set to `False` to hide the commit stat

```text
I'm a night 🦉

🌞 Morning    57 commits     ████░░░░░░░░░░░░░░░░░░░░░   16.76%
🌆 Daytime    85 commits     ██████░░░░░░░░░░░░░░░░░░░   25.0%
🌃 Evening    128 commits    █████████░░░░░░░░░░░░░░░░   37.65%
🌙 Night      70 commits     █████░░░░░░░░░░░░░░░░░░░░   20.59%

```

`SHOW_WEEKLY_COMMIT` flag can be set to `False` to hide the commit stat

```text
📅 I'm Most Productive on Mondays

Monday       64 commits     █████░░░░░░░░░░░░░░░░░░░░   21.19%
Tuesday      33 commits     ██░░░░░░░░░░░░░░░░░░░░░░░   10.93%
Wednesday    59 commits     █████░░░░░░░░░░░░░░░░░░░░   19.54%
Thursday     41 commits     ███░░░░░░░░░░░░░░░░░░░░░░   13.58%
Friday       40 commits     ███░░░░░░░░░░░░░░░░░░░░░░   13.25%
Saturday     35 commits     ███░░░░░░░░░░░░░░░░░░░░░░   11.59%
Sunday       30 commits     ██░░░░░░░░░░░░░░░░░░░░░░░   9.93%

```

`SHOW_LANGUAGE` flag can be set to `False` to hide the Number of repository in different language and framework

```text
My 💖 languages Python

Python      12 repos █████████████░░░░░░░░░░░░ 54.55%
JavaScript   7 repos ████████░░░░░░░░░░░░░░░░░ 31.82%
CSS          2 repos ██░░░░░░░░░░░░░░░░░░░░░░░ 9.09%
HTML         1 repos █░░░░░░░░░░░░░░░░░░░░░░░░ 4.55%

```

`SHOW_TOTAL_CONTRIBUTIONS` flag can be set to `False` to hide the total Number of Contributions

```text
🏆 531 Contributions in year 2020
```

### Inspired By 🚀

> [matchai/awesome-pinned-gists](https://github.com/matchai/awesome-pinned-gists)  
> [athul/waka-readme](https://github.com/athul/waka-readme)  
> [anmol098/waka-readme-stats](https://github.com/anmol098/waka-readme-stats)

```text
Liked this Project? Why not 🌟 it?
```
