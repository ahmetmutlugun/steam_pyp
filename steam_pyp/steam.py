import os
import requests
import time
import json

from requests import HTTPError


# TODO
# Add comments for the last 5 commands
# Add a wrapper for all profile commands that returns a combined, formatted json
# Make commands more readable, maybe higher level


class Steam:
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
        self.api_calls = 0

        f = open(os.getcwd() + '/steam_pyp/languages.json', 'r+')
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

        data = self.api_call(f"{self.url}/ICSGOServers_730/GetGameServersStatus/v1/",
                             {"key": self.key, "interval": interval, "gamemode": game_mode})
        return data

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
        self.api_calls += 1
        r = requests.get(
            f'{self.url}/ISteamNews/GetNewsForApp/v0002/',
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
                raise HTTPError(f"Status code {r.status_code}")

    def player_ban(self, steam_id):
        """
            Get ban information from steam id
            :param steam_id: steam id from a steam profile
            :return: ban data in json format
            """
        data = self.api_call(f'{self.url}/ISteamUser/GetPlayerBans/v1', {"key": self.key, "steamids": f"{steam_id}"})
        if len(data['players']) < 1:
            return None
        return data["players"][0]

    def player_summary(self, steam_ids):
        data = self.api_call(f"{self.url}/ISteamUser/GetPlayerSummaries/v0002",
                             {'key': self.key, "steamids": steam_ids})
        return data

    def player_friends(self, steam_id, relationship="friend"):
        data = self.api_call(f"{self.url}/ISteamUser/GetFriendList/v0001",
                             {'key': self.key, "steamid": steam_id, "relationship": relationship})
        return data

    def player_achievements(self, steam_id, appid, language=None):
        data = self.api_call(f"{self.url}/ISteamUserStats/GetPlayerAchievements/v0001",
                             {'key': self.key, "steamid": steam_id, "appid": appid, "l": language})
        return data

    def player_stats(self, steam_id, appid, language=None):
        data = self.api_call(f"{self.url}/ISteamUserStats/GetUserStatsForGame/v0002",
                             {'key': self.key, "steamid": steam_id, "appid": appid, "l": language})
        return data

    def player_games(self, steam_id, include_app_info=True, include_played_free_games=True,
                     return_format="json", appids_filter=None):
        data = self.api_call(f"{self.url}/IPlayerService/GetOwnedGames/v0001", {'key': self.key,
                                                                                "steamid": steam_id,
                                                                                "include_played_free_games": include_played_free_games,
                                                                                "include_appinfo": include_app_info,
                                                                                "format": return_format,
                                                                                "appids_filter": appids_filter})
        return data

    def player_recent_games(self, steam_id, count=None):
        data = self.api_call(f"{self.url}/IPlayerService/GetRecentlyPlayedGames/v0001",
                             {'key': self.key, "steamid": steam_id, "count": count})
        return data

    def api_call(self, url, params):
        self.api_calls += 1
        r = requests.get(url, params=params)
        return r.json()
