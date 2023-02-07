from utils import Json

CONFIG: dict[str, dict] = {
    "headers": {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition GX-CN)",
        "sec-fetch-site": "same-origin",
        "x-ig-app-id": "",
        "x-csrftoken": "",
        "sec-ch-ua": "\"Opera GX\";v=\"93\", \"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"107\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate"
    },
    "cookies": {},
    "logging": {
        "main": {
            "stream-level": "INFO",
            "file-level": "INFO",
            "backup-count": 5,
            "file-name": "main",
            "dir-path": "logs"
        }
    },
    "update-frequency": 10,
    "timezone": 8,
    "timeout": 5
}

raw_cookies = input("Your Cookies: ")
cookies = {}
for cookie in raw_cookies.split(";"):
    key, value = cookie.split("=", 1)
    cookies[key.strip()] = value.strip()
CONFIG["cookies"] = cookies
CONFIG["headers"]["x-csrftoken"] = cookies.get("csrftoken")
CONFIG["headers"]["x-ig-app-id"] = input("Your X-IG-APP-ID: ")

Json.dump_nowait("config.json", CONFIG)
