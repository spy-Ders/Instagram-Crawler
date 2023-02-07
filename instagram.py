from asyncio import create_task, gather
from typing import Iterable, Optional, Union

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

class StoryUser(BaseModel):
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
        ids: Optional[Union[list[str], str, int]]=None,
        client: Optional[ClientSession]=None
    ) -> dict[str, dict]:
        """
        取得限時動態資訊。

        :param ids: :class:`list|str|int|None`使用者IDs。
        :param client: :class:`ClientSession`對話。
        """
        # 檢查是否需要開新連線
        need_close = False if client else True
        client = client if client else new_session()
        
        # 檢查目標IDs是否為空
        if ids == None:
            # 如果為空，則抓取所有IDs
            user_data = await Instagram.get_user_data(client=client)
            ids = list(user_data.keys())
        else:
            # 如果行不為列表，則轉換為列表
            if issubclass(type(ids), Iterable) and type(ids) != str:
                ids = list(ids)
            elif type(ids) != list:
                ids = [ids]
            # 將列表內容轉換為字串
            ids = list(map(str, ids))
        
        result = {}
        if len(ids) != 0:
            # 取得資料
            __api_url = "https://www.instagram.com/api/v1/feed/reels_media/?reel_ids="
            results: list[dict[str, dict]] = await gather(*(
                create_task(
                    requests(__api_url + "&reel_ids=".join(ids[i:i+5]), client=client, json=True)
                )
                for i in range(0, len(ids), 5)
            ))

            # 更新資料
            for data in results:
                result.update(data["reels"])

        # 檢查是否需要關閉連線
        if need_close:
            await client.close()

        # 回傳
        return result
    
    @staticmethod
    async def get_user_data(
        length: Optional[int]=None,
        client: Optional[ClientSession]=None,
    ) -> Union[dict[str, StoryUser], dict[str, dict]]:
        """
        取得目前有發布限動的使用者資料。

        :param length: :class:`int`資料長度。
        :param client: :class:`ClientSession`對話。
        """
        # 檢查是否需要開新連線
        need_close = False if client else True
        client = client if client else new_session()
        
        # 取得資料
        data = await requests("https://www.instagram.com/api/v1/feed/reels_tray/", client=client, json=True)
        tray = filter(lambda d: d["reel_type"] == "user_reel", data["tray"])
        
        # 資料長度
        length = length if length else len(tray)

        # 結果
        result = {
            d["id"]: StoryUser(**d["user"])
            for d, _ in zip(
                tray,
                range(length)
            )
        }

        # 檢查是否需要關閉連線
        if need_close:
            await client.close()

        # 回傳
        return result
        