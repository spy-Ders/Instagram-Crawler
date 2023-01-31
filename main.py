from configs import logger_init

from asyncio import new_event_loop, set_event_loop_policy, WindowsSelectorEventLoopPolicy
from platform import system

async def main():
    
    from instagram import Instagram
    from datetime import datetime
    from aiofiles import open as aopen
    from orjson import dumps, OPT_INDENT_2

    all_user = await Instagram.get_user_data()
    ids = list(all_user.keys())[:10]
    data = await Instagram.get_info(ids)
    dt = datetime.now().strftime("%Y%m%d %H-%M-%S")
    async with aopen(f"results\\{dt} InstaStory__output__.json", mode="wb") as _file:
        await _file.write(dumps(data, option=OPT_INDENT_2))

if __name__ == "__main__":
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
     
    logger_init()
    loop = new_event_loop()
    loop.run_until_complete(main())
    loop.close()