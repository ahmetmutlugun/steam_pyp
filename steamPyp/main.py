import os
import requests
import time
import json


# TODO
# Add comments for the last 5 commands
# Add a wrapper for all profile commands that returns a combined, formatted json
# Make commands more readable, maybe higher level


class SteamPyp:
    """The API Class"""

    def __init__(self, key=None, return_format="json"):
        """
        Initialize the SteamAPI class. API Keys can be obtained through be https://steamcommunity.com/dev/apikey
        :param key: Steam API key
        """
        self.return_format = return_format
        self.key = key
        self.url = "https://api.steampowered.com"
        self.header = {'Accept': 'application/json'}

        f = open(os.getcwd() + '/steamPyp/languages.json', 'r+')
        self.languages = json.load(f)
        f.close()

    def set_key(self, key: str):
        """Authenticate with the API"""
        self.key = key

    def set_format(self, return_format: str = "json"):
        self.return_format = return_format

    def game_servers_status(self, interval: str = "day", game_mode: str = "competitive"):
        """
        Get CS:GO Server Status
        :param interval: day, week or month interval
        :param game_mode: competitive or casual game mode
        :return: API Response
        """
        r = requests.get(url="https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/",
                         headers=self.header, params={"key": self.key, "interval": interval,
                                                      "gamemode": game_mode})
        return r

    def news_from_app(
            self, appid: int, max_length: int = 0,
            count: int = 1, response_format: str = "json",
            end_date: int = time.time(), feeds: list = None, tags: list = None, raw: bool = False):
        """
        Get a number of app news. If the raw parameter is false, the results will be returned as a json such as:
        1: {title: str,
            url: str,
            author: str,
            content: str,
            date: int,
            feedname: str},
         2: {...},
         3: {...}
        :param appid: Steam ID app id
        :param max_length: Length of the returned news. Use 0 to get the full content
        :param count: Number of news
        :param response_format: json, xml or vdf format
        :param end_date: get news from before the provided unix time
        :param feeds: list of feed names
        :param tags: list of news tags
        :param raw: If True, return the response without parsing/trimming it
        :return: returns news from the given appid
        """
        r = requests.get(
            'https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/',
            headers=self.header,
            params={"key": self.key, "maxlength": max_length, "count": count,
                    "appid": appid, "format": response_format, "enddate": end_date, "feeds": feeds, "tags": tags})
        if raw:
            return r
        else:
            if r.status_code == 200:
                new_response = {}
                response = r.json()['appnews']['newsitems']
                n = 0
                for news in response:
                    n += 1
                    new_response.update({n: {"title": news["title"],
                                             "url": news["url"], "author": news["author"], "content": news["contents"],
                                             "date": news["date"], "feedname": news["feedname"]}
                                         })
                return json.dumps(new_response, indent=4)
            else:
                raise Exception(f"Status code {r.status_code}")

    def player_ban(self, steam_id):
        """
            Get ban information from steam id
            :param steam_id: steam id from a steam profile
            :return: ban data in json format
            """
        r = requests.get(
            'https://api.steampowered.com/ISteamUser/GetPlayerBans/v1',
            params={"key": self.key, "steamids": f"{steam_id}"},
            headers=self.header)
        data = r.json()
        if len(data['players']) < 1:
            return None
        return data["players"][0]

    def player_summary(self, steam_ids):
        r = requests.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002",
                         params={'key': self.key, "steamids": steam_ids})
        data = r.json()
        return data

    def player_friends(self, steam_id, relationship="friend"):
        r = requests.get("https://api.steampowered.com/ISteamUser/GetFriendList/v0001",
                         params={'key': self.key, "steamid": steam_id, "relationship": relationship})
        data = r.json()
        return data

    def player_achievements(self, steam_id, appid, language=None):
        r = requests.get("https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001",
                         params={'key': self.key, "steamid": steam_id, "appid": appid, "l": language})
        data = r.json()
        return data

    def player_stats(self, steam_id, appid, language=None):
        r = requests.get("https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002",
                         params={'key': self.key, "steamid": steam_id, "appid": appid, "l": language})
        data = r.json()
        return data

    def player_games(self, steam_id, include_app_info=True, include_played_free_games=True,
                     return_format="json", appids_filter=None):
        r = requests.get("https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001",
                         params={'key': self.key,
                                 "steamid": steam_id,
                                 "include_played_free_games": include_played_free_games,
                                 "include_appinfo": include_app_info,
                                 "format": return_format, "appids_filter": appids_filter})
        data = r.json()
        return data

    def player_recent_games(self, steam_id, count=None, return_format="json"):
        r = requests.get("https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001",
                         params={'key': self.key, "steamid": steam_id, "count": count, "format": return_format})
        data = r.json()
        return data
