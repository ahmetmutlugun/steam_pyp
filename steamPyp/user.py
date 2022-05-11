from steamPyp import SteamPyp


class User:
    def __init__(self, steam_id, steam: SteamPyp):
        self.steam = steam
        self.steam_id = steam_id
        self.set_user_data(steam_id, "730")

    def set_user_data(self, steam_id, appid, language=None, include_app_info=True,
                       include_played_free_games=True, return_format="json", appids_filter=None, count=None,
                       raw_data=False):
        if return_format not in ["json", "xml", "vdf"]:
            raise ValueError("return_format must be: json, xml, or vdf")
        self.games = self.steam.player_games(steam_id, include_app_info, include_played_free_games, return_format,
                                           appids_filter)
        # self.recent_games = self.steam.player_recent_games(steam_id, count, return_format)
        # self.friends = self.steam.player_friends(steam_id)
        # self.achievements = self.steam.player_achievements(steam_id, appid, language)
        if not raw_data:
            return self.games  # bans + stats + games + recent_games + friends + achievements + summary

    def _set_user_summary(self):
        summary = self.steam.player_summary(steam_ids=self.steam_id)

        self.name = summary['response']['players'][0]['personaname']
        self.url = summary['response']['players'][0]['profileurl']
        self.avatar = summary['response']['players'][0]['avatarfull']
        self.real_name = summary['response']['players'][0]['realname']
        self.created = summary['response']['players'][0]['timecreated']

    def _set_bans(self):
        bans = self.steam.player_summary(steam_ids=self.steam_id)

        self.vac_banned = bans['VACBanned']
        self.community_banned = bans['CommunityBanned']
        self.vac_count = bans['NumberOfVACBans']
        self.days_since_ban = bans['DaysSinceLastBan']
        self.game_bans = bans['NumberOfGameBans']
        self.economy_banned = bans['EconomyBan']

    def _set_csgo_stats(self):
        self.csgo = self.steam.player_stats(self.steam_id, 730)['playerstats']['stats']