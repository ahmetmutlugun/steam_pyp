import time

from steamPyp import SteamPyp
from steamPyp.user import User

if __name__ == "__main__":
    start_time = time.time()

    # Get the steam key
    steam_key_file = open("steam.key", "r")
    steam_key = steam_key_file.read().replace("\n", "")
    steam_key_file.close()

    # Initialize SteamAPI
    steam = SteamPyp(key=steam_key, return_format="json")

    # Print CS:GO server status
    print(steam.game_servers_status().json())

    # Print the most recent CS:GO news
    news = steam.news_from_app(appid=730, count=1, raw=True).json()
    print(news)

    # Print player summary of 76561198342056792
    summary = steam.player_summary(steam_ids=['76561198342056792'])
    print(summary)

    # Print friends of 76561198342056792
    friends = steam.player_friends(steam_id=['76561198342056792'], relationship="all")
    print(friends)

    achievements = steam.player_achievements(steam_id="76561198342056792", appid="730")
    print(achievements)

    stats = steam.player_stats(steam_id="76561198342056792", appid="730")
    print(stats)

    games = steam.player_games(steam_id="76561198342056792")
    print(games)

    recents = steam.player_recent_games(steam_id="76561198342056792")
    print(recents)

    user = User("76561198342056792", steam)
    print(user.set_user_data("76561198342056792", 730))
    # Print time spent
    print(f"Time spent: {time.time() - start_time}")
