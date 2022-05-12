from steam_pyp.steam import Steam


class User:
    def __init__(self, steam_id, steam: Steam, detailed = False):

        self.achievements = []
        self.game_stats = []
        self._steam = steam
        self.steam_id = steam_id
        self._set_user_data(steam_id, "730")
        if detailed:
            self._set_achievements()
            self._set_all_game_stats()

    def _set_user_data(self, steam_id, appid, language=None, include_app_info=True,
                       include_played_free_games=True, return_format="json", appids_filter=None, count=None,
                       raw_data=False):
        if return_format not in ["json", "xml", "vdf"]:
            raise ValueError("return_format must be: json, xml, or vdf")
        if not raw_data:
            self._set_user_summary()
            self._set_bans()
            self._set_csgo_stats()
            self._set_games()
            self._set_recent_games()
            self._set_friends()
            # Removed due to slowness
            return None  # bans + stats + games + recent_games + friends + achievements + summary

    def _set_user_summary(self):
        summary = self._steam.player_summary(steam_ids=self.steam_id)

        self.name = summary['response']['players'][0]['personaname']
        self.url = summary['response']['players'][0]['profileurl']
        self.avatar = summary['response']['players'][0]['avatarfull']
        self.real_name = summary['response']['players'][0]['realname']
        self.created = summary['response']['players'][0]['timecreated']

    def _set_bans(self):
        bans = self._steam.player_ban(self.steam_id)

        self.vac_banned = bans['VACBanned']
        self.community_banned = bans['CommunityBanned']
        self.vac_count = bans['NumberOfVACBans']
        self.days_since_ban = bans['DaysSinceLastBan']
        self.game_bans = bans['NumberOfGameBans']
        self.economy_banned = bans['EconomyBan']

    def _set_csgo_stats(self):
        self.csgo = self._steam.player_stats(self.steam_id, 730)['playerstats']['stats']

    def _set_games(self, include_app_info=True, include_played_free_games=True, return_format="json",
                   appids_filter=None):
        self.games = self._steam.player_games(self.steam_id, include_app_info, include_played_free_games, return_format,
                                              appids_filter)
        games = []
        for i in self.games['response']['games']:
            games.append(i['appid'])
        self.games_list = games

    def _set_recent_games(self, count=None, return_format="json"):
        self.recent_games = self._steam.player_recent_games(self.steam_id, count, return_format)

    def _set_friends(self):
        self.friends = self._steam.player_friends(self.steam_id)

    def _set_achievements(self, appid="730", language=None):
        for i in self.games_list:
            self.achievements.append(self._steam.player_achievements(self.steam_id, i, language))

    def _set_all_game_stats(self):
        for i in self.games_list:
            self.game_stats.append(self._steam.player_stats(self.steam_id, i))
