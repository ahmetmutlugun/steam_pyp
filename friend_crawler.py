import time
import tracemalloc

from steam_pyp.steam import Steam

if __name__ == "__main__":
    tracemalloc.start()

    start_time = time.time()

    # Get the steam key
    steam_key_file = open("steam.key", "r")
    steam_key = steam_key_file.read().replace("\n", "")
    steam_key_file.close()

    # Initialize SteamAPI
    steam = Steam(key=steam_key, return_format="json")
    steam_id = '76561199223184522'

    friends = steam.player_friends(steam_id=[steam_id], relationship="all")['friendslist']['friends']
    friends_dict = {}

    for i in friends:
        if i['steamid'] not in friends_dict:
            try:
                friends_dict.update({i['steamid']: steam.player_friends(steam_id=[i['steamid']], relationship="all")[
                    'friendslist']['friends']})
                print("Added ", i['steamid'], len(friends_dict))
            except KeyError:
                friends_dict.update({i['steamid']: None})

    for _ in range(0, 1):
        new_dict = {}
        for i in friends_dict.keys():
            if friends_dict[i] is not None:
                for j in friends_dict[i]:
                    if j['steamid'] not in friends_dict and j['steamid'] not in new_dict:
                        try:
                            new_dict.update({j['steamid']:
                                                 steam.player_friends(steam_id=[j['steamid']], relationship="all")[
                                                     'friendslist']['friends']})
                            print("Added ", j['steamid'], len(friends_dict) + len(new_dict))
                        except KeyError:
                            new_dict.update({j['steamid']: None})

        friends_dict.update(new_dict)
        print(len(friends_dict))
    print("Done!")
    # Initialize a user

    print("Steam API calls: ", steam.api_calls)

    tracemalloc.stop()

    print(f"Project takes up approximately {tracemalloc.get_traced_memory()[1] / 1000000} MB of memory.")

    # Print time spent
    print(f"Time spent: {time.time() - start_time}")
