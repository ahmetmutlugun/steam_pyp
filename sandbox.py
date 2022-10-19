import asyncio
import aiohttp
import requests
import json
import firebase

from aiohttp import ContentTypeError



f = open('config.json')
config = json.load(f)
f.close()

proxies = config['proxies']
username = config['username']
password = config['password']

results = []


async def get_price(session, url, name):
    proxy = proxies.pop(0)
    proxies.append(proxy)

    proxy_auth = aiohttp.BasicAuth(username, password)
    async with session.get(url, proxy=proxy, proxy_auth=proxy_auth) as resp:
        data = {"failed": True}

        try:
            data = await resp.json()
            if data is None:
                data = {"failed": True}
        except ContentTypeError:
            print(await resp.text())

        return name, data


async def start(items):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for j in items:
            url = f"http://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={j}"
            tasks.append(asyncio.ensure_future(get_price(session, url, j)))

        original_item = await asyncio.gather(*tasks)
        firebase.set_item(original_item)
        await asyncio.sleep(10)


if __name__ == "__main__":
    count = 0
    all_items = requests.get("https://api.steamapis.com/image/items/730")
    item_queue = list(all_items.json().keys())[-1::]
    length = len(item_queue)

    while True:
        next10 = item_queue[0:10]
        asyncio.run(start(next10))
        for i in range(0, 10):
            item = item_queue.pop(0)
            item_queue.append(item)
        count += 10
        if count > length:
            items = requests.get("https://api.steamapis.com/image/items/730")
            item_queue = list(items.json().keys())
            length = len(item_queue)
        print(f"{count}/{length}")
