from modules import Json
from configs import HEADERS, COOKIES, TIMEOUT

from logging import getLogger
from traceback import format_exception
from typing import Any, Literal, Optional, Union

from aiohttp import ClientResponse, ClientSession
from multidict import CIMultiDictProxy

def new_session(
    headers: Optional[dict]=None,
    cookies: Optional[dict[str, str]]=None
):
    if headers == None:
        headers = HEADERS
    if cookies == None:
        cookies = COOKIES
    return ClientSession(
        headers=headers,
        cookies=cookies,
        conn_timeout=TIMEOUT,
    )

async def requests(
    url: str,
    client: Optional[ClientSession]=None,
    *,
    data: Any=None,
    method: Literal["GET", "POST", "HEAD"]="GET",
    headers: Optional[dict]=None,
    cookies: Optional[dict[str, str]]=None,
    raw: bool=False,
    json: bool=False
) -> Optional[Union[bytes, CIMultiDictProxy, ClientResponse]]:
    """
    非同步請求。

    url: :class:`str`
        連結。
    method: :class:`Literal["GET", "POST", "HEAD"]`
        請求方法。
    
    return: :class:`Optional[Union[bytes, CIMultiDictProxy, ClientResponse]]`
    """
    __logger = getLogger("main")
    try:
        method = method.upper()
        need_close = False

        if type(data) in [dict, list]: data = Json.dumps(data)
        if client == None:
            client = new_session(headers, cookies)
            need_close = True
        
        _headers = client.headers.copy()
        if headers != None:
            _headers.update(headers)
        if method == "HEAD":
            res = await client.head(url, headers=_headers)
        elif method == "POST":
            res = await client.post(url, data=data, headers=_headers)
        else:
            res = await client.get(url, headers=_headers)
        
        if raw:
            result = res
        elif method == "HEAD":
            result = res.headers.copy()
        elif json:
            result = await res.json()
        else:
            result = await res.content.read()

        if need_close:
            await client.close()
        
        return result
    except Exception as __exc:
        __exc_text = "".join(format_exception(__exc))
        __logger.error(f"Requests Error: {__exc_text}")
    return None
