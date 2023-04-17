def read_steam_key(path) -> str:
    steam_key_file = open(path, "r")
    steam_key = steam_key_file.read().replace("\n", "")
    steam_key_file.close()
    return steam_key
