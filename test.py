import sys
import time
import tracemalloc

from steam_pyp.steam import Steam
from steam_pyp.user import User

if __name__ == "__main__":

    start_time = time.time()

    # Get the steam key
    steam_key_file = open("steam.key", "r")
    steam_key = steam_key_file.read().replace("\n", "")
    steam_key_file.close()

    # Initialize SteamAPI
    steam = Steam(key=steam_key, return_format="json")
    steam_id = '76561198342056792'

    # Print CS:GO server status
    print(steam.game_servers_status())

    # Print the most recent CS:GO news
    news = steam.news_from_app(appid=730, count=1, raw=True).json()
    print(news)

    # Print player summary of a user
    summary = steam.player_summary(steam_ids=[steam_id])
    print(summary)

    # Print friends of a user
    friends = steam.player_friends(steam_id=[steam_id], relationship="all")
    print(friends)

    # Get achievements for a game
    achievements = steam.player_achievements(steam_id=steam_id, appid="730")
    print(achievements)

    # Get status from a user
    stats = steam.player_stats(steam_id=steam_id, appid="730")
    print(stats)

    # Get games from a user
    games = steam.player_games(steam_id=steam_id)
    print(games)

    # Get recent games of a user
    recents = steam.player_recent_games(steam_id=steam_id)
    print(recents)

    # Initialize a user

    tracemalloc.start()

    user = User(steam_id, steam, detailed=False)
    print("Steam API calls: ", steam.api_calls)
    print(f"User takes up approximately {tracemalloc.get_traced_memory()[1]/1000000} MB of memory.")
    tracemalloc.stop()
    print(user)

    # Print time spent
    print(f"Time spent: {time.time() - start_time}")
