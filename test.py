from steamPyp import SteamPyp

if __name__ == "__main__":
    # Get the steam key
    steam_key_file = open("steam.key", "r")
    steam_key = steam_key_file.read().replace("\n", "")
    steam_key_file.close()

    # Initialize SteamAPI
    steam = SteamPyp(key=steam_key, return_format="json")

    # Print CS:GO server status
    print(steam.get_game_servers_status().json())

    # Print the most recent CS:GO news
    r = steam.get_news_from_app(appid=730, count=1)
    print(r)



