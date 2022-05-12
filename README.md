[![Codacy Badge](https://app.codacy.com/project/badge/Grade/d4a80415b78a48e6aa823db230996420)](https://www.codacy.com/gh/ahmetmutlugun/steam_pyp/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ahmetmutlugun/steam_pyp&amp;utm_campaign=Badge_Grade)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/ahmetmutlugun/steam_pyp)
![Lines of code](https://img.shields.io/tokei/lines/github/ahmetmutlugun/steam_pyp)
![GitHub issues](https://img.shields.io/github/issues/ahmetmutlugun/steam_pyp)
![GitHub](https://img.shields.io/github/license/ahmetmutlugun/steam_pyp)
![GitHub Repo stars](https://img.shields.io/github/stars/ahmetmutlugun/steam_pyp?style=social)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ahmetmutlugun/steam_pyp)

# steam_pyp

Steam Pyp (Pipe) is a Steam API wrapper for Python.

---

## Installation

When the package is published, it will be installed with something like:

`pip install steam_pyp`

---

## Steam

Steam is the class that holds functions regarding API calls. It can be initialized with the steam key and a return
format. Currently, json is the only supported return format.

The Steam class can be used standalone as a low-level api wrapper.

### Initialization

```python
from steam_pyp.steam import Steam

steam = Steam(key="STEAM API KEY", return_format="json")
```

### Functions

-  set_key
-  set_format
-  game_servers_status
-  news_from_app
-  player_ban
-  player_summary
-  player_friends
-  player_achievements
-  player_stats
-  player_games
-  player_recent_games

---

## User

User is a class to initialize, store and update user data. It is used to gather and store user data without bothering
with the Steam API.

### Usage

```python
from steam_pyp.user import User
from steam_pyp.steam import Steam

steam = Steam(key="STEAM API KEY", return_format="json")

user = User(steam_id="76561198342056792", steam=steam)
```

### Methods

-  set_user_data
-  _set_user_summary
-  _set_bans
-  _set_csgo_stats
