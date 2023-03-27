from configs import logger_init, TIMEZONE
from instagram import Instagram
from utils import Json

from asyncio import new_event_loop, set_event_loop_policy, WindowsSelectorEventLoopPolicy
from datetime import datetime
from os import makedirs
from os.path import isdir, isfile
from platform import system

from gen_config import gen_CONFIG

privacy_file = ["config.json"]

for f in privacy_file:
    
    if not isfile(f):
        
        _ = open(f, "w+")
        
        if f == "config.json":
        
            gen_CONFIG()

async def main():
    # 抓取資料
    users = await Instagram.get_user_data(10)
    data = await Instagram.get_info(users.keys())

    # 檢查資料夾是否存在
    if not isdir("results"):
        makedirs("results")
    
    # 輸出至檔案
    await Json.dump(
        f"results/{datetime.now(TIMEZONE).isoformat().replace(':', '-')} InstaStory__output__.json",
        data
    )

if __name__ == "__main__":
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
     
    logger_init()
    loop = new_event_loop()
    loop.run_until_complete(main())
    loop.close()