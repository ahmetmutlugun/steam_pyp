import os

import redis


def read_steam_key(path) -> str:
    steam_key_file = open(path, "r")
    steam_key = steam_key_file.read().replace("\n", "")
    steam_key_file.close()
    return steam_key


def redis_connect() -> redis.Redis:
    redis_host = os.getenv('REDISHOST')
    redis_port = int(os.getenv('REDISPORT'))
    redis_password = os.getenv('REDISPASSWORD')
    redis_user = os.getenv('REDISUSER')

    return redis.Redis(host=redis_host, port=redis_port, password=redis_password, username=redis_user)


def redis_set_item(items, redis_client: redis.Redis):
    for i in items:
        name = str(i[0])
        name = name.replace(".", "(dot)")
        if i[1] is not None and 'success' in i[1]:
            i[1].pop("success")
        try:
            redis_client.hmset(name, i[1])
        except redis.exceptions.DataError:
            print("No price:", name, i[1])