import asyncio

from TikTokApi import TikTokApi
from TikTokApi.exceptions import EmptyResponseException
from playwright.async_api import async_playwright

ms_token = [
   'iZgHSA8XBb7koapEs0L3dO8zuVmfjcDqbs2YjKRFzWA4o8XfQgoP5HiiMl13HP0k-ajO8opWRRXVq5OqgqIIJfGLF5hG8L8elswUw1VBTNMXEoeDL4elkGF_NuLDrrynrufVUg==',
   'fGCkUZLz0j-VLnkdWh2Gj2uwgY0jaqbj0jlbLm2TRuRnZDCvJ3b0eF6q8qt6Qt8nV6aw4-JzwKSkbrYGURQiQIb2Xn-0H0OTkPuXNkNLgJ8RdxngEwO2KWPAYAZ4dLHiP-3Hkw==',
   'wRtBOQIsArZOwPesEA84dAXQ0XZBMOkL-VyzO4nAmVxh0ndboASwhJ5oES5d0vEix_gDVExND5fBlQdqHd8OHxwFKO14l0tgAlAZPbsdmsfximN-ekR7kMcuJoSO4oj_EeDrNA=='
] 


async def get_day(nick, tokens):
    proxy = [{
        'server': '172.245.198.30:8000',
        'username': '',
        'password': ''  
    }]


    all_likes = 0
    all_comm = 0
    all_izbr = 0
    all_views = 0
    all_share = 0


    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=ms_token, num_sessions=1, sleep_after=30, proxies=proxy, headless=False)
        user = api.user(username=nick)
        inf = await user.info()
        subs = inf['userInfo']['stats']['followerCount']
 
        async for video in user.videos(count=7):
            x = video.as_dict
            try:
                if x['isPinnedItem'] is True:
                    continue
            except KeyError:
                like = x['stats']['diggCount']
                comm = x['stats']['commentCount']
                izbr = x['stats']['collectCount']
                views = x['stats']['playCount']
                share = x['stats']['shareCount']

                all_likes += like
                all_comm += comm
                all_izbr += izbr
                all_views += views
                all_share += share

        return all_likes, all_comm, subs, all_izbr, all_views, all_share, like, comm, izbr, views, share


async def get_tokens():
    proxy = {
        'server': '172.245.198.30:8000',
        'username': '',
        'password': ''  
    }

    tokens = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, proxy=proxy, devtools=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.tiktok.com")
        await asyncio.sleep(10)
        cooks = await context.cookies()
        for i in cooks:
            if i['name'] == 'msToken':
                print(i['value'])
                token = i['value']
                tokens.append(token)
        print(tokens)
        await asyncio.sleep(180)
        await context.close()
        await browser.close()
    return tokens


if __name__ == "__main__":
    # tok = asyncio.run(get_tokens())
    tok = [1]
    for i in range(0, len(tok)):
        try:
            x = asyncio.run(get_day('anus_offishel', tok[i]))
            print(x) 
        except EmptyResponseException:
            continue
    # i = asyncio.run(get_week('zaraznow',dates=[],start=0))
    # a = asyncio.run(get_mounth('zaraznow'))
    # x = asyncio.run(get_tokens())
    # print(x)
    # print(x)
    # print(a)
