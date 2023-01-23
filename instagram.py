from asyncio import create_task, gather
from typing import Optional, Union

from aiohttp import ClientSession
from aiorequests import new_session, requests
from pydantic import BaseModel

class InstagramFriendship(BaseModel):
    muting: Optional[bool]=None
    is_muting_reel: Optional[bool]=None
    following: bool
    is_bestie: bool
    is_private: Optional[bool]=None
    incoming_request: Optional[bool]=None
    outgoing_request: bool
    is_restricted: Optional[bool]=None
    is_feed_favorite: Optional[bool]=None

class InstagramUser(BaseModel):
    pk: int
    pk_id: int
    username: str
    full_name: str
    is_private: bool
    is_verified: bool
    profile_pic_id: str=""
    profile_pic_url: str=""
    friendship_status: InstagramFriendship

class Instagram:
    @staticmethod
    async def get_info(
        ids: Optional[Union[list[str], str]]=None,
        client: Optional[ClientSession]=None
    ) -> dict[str, dict]:
        # For Debug
        # from aiofiles import open as aopen
        # from orjson import loads
        # async with aopen("debug.json", mode="rb") as _file:
        #     data: dict[str, dict] = loads(await _file.read())
        # if type(ids) != list:
        #     ids = [ids]
        # results = {}
        # for id_ in ids:
        #     val = data.get(id_)
        #     if val:
        #         results[id_] = val
        # return results

        need_close = False
        if client == None:
            client = new_session()
            need_close = True
        
        user_data = await Instagram.get_user_data(client=client)
        l_ids = tuple(user_data.keys())
        if ids == None:
            ids = l_ids
        else:
            if type(ids) != list:
                ids = [ids]
            ids = [id_ for id_ in ids if id_ in l_ids]
        
        result = {}
        if len(ids) != 0:
            __api_url = "https://www.instagram.com/api/v1/feed/reels_media/?reel_ids="
            tasks = []
            for i in range(0, len(ids), 10):
                tasks.append(create_task(
                    requests(__api_url + "&reel_ids=".join(ids[i:i+10]), client=client, json=True)
                ))
            results: list[dict[str, dict]] = await gather(*tasks)

            for data in results:
                result.update(data["reels"])

        if need_close:
            await client.close()
        
        return result
    
    @staticmethod
    async def get_user_data(
        client: Optional[ClientSession]=None,
    ) -> Union[dict[str, InstagramUser], dict[str, dict]]:
        need_close = False
        if client == None:
            client = new_session()
            need_close = True
        
        data = await requests("https://www.instagram.com/api/v1/feed/reels_tray/", client=client, json=True)
        
        result = {
            d["id"]: InstagramUser(**d["user"])
            for d in data["tray"] if d["reel_type"] == "user_reel"
        }

        if need_close: await client.close()

        return result
        