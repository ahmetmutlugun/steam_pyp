import requests
import time
import json


class SteamPyp:
    """ the API Class"""

    def __init__(self, key=None, return_format="json"):
        """
        Initialize the SteamAPI class. API Keys can be obtained through behttps://steamcommunity.com/dev/apikey
        :param key: Steam API key
        """
        self.return_format = return_format
        self.key = key
        self.url = "https://api.steampowered.com"

    def set_key(self, key: str):
        """ Authenticate with the API"""
        self.key = key

    def set_format(self, return_format: str = "json"):
        self.return_format = return_format

    def get_game_servers_status(self, interval: str = "day", game_mode: str = "competitive"):
        """
        Get CS:GO Server Status
        :param interval: day, week or month interval
        :param game_mode: competitive or casual game mode
        :return: API Response
        """
        r = requests.get(url=f"https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/",
                         headers={'Accept': 'application/json'}, params={"key": self.key, "interval": interval,
                                                                         "gamemode": game_mode})
        return r

    def get_news_from_app(
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
            f'https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/',
            headers={'Accept': 'application/json'},
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
                raise Exception(f"")
