from modules import Json

from datetime import timedelta, timezone
from logging import getLevelName
from pydantic import BaseModel, Field, ValidationError, validator
from typing import Union

# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
# NOTSET
class LoggingConfig(BaseModel):
    stream_level: Union[int, str]=Field(20, alias="stream-level")
    file_level: Union[int, str]=Field(20, alias="file-level")
    backup_count: int=Field(3, alias="backup-count")
    file_name: str=Field(alias="file-name")
    dir_path: str=Field("logs", alias="dir-path")

    @validator("stream_level", "file_level")
    def level_name_validator(cls, value):
        if type(value) == int:
            if value in range(0, 51, 10):
                return value
        else:
            new_value = getLevelName(value)
            if type(new_value) == int:
                return new_value
        raise ValueError(f"Illegal level name: \"{value}\"")
    
    class Config:
        extra = "ignore"

# 預設設置
CONFIG: dict[str, dict] = {
    "cookies": {
    },
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

# 補全設置
try:
    RAW_CONFIG: dict[str, Union[dict, str, int]] = Json.load("config.json")
    for key, value in RAW_CONFIG.items():
        if type(value) == dict:
            for s_key, s_value in value.items():
                CONFIG[key][s_key] = s_value
        else:
            CONFIG[key] = value
except: pass
finally:
    Json.dump("config.json", CONFIG)

COOKIES: dict[str, str] = CONFIG["cookies"]
HEADERS: dict[str, str] = CONFIG["headers"]
LOGGING_CONFIG: dict[str, LoggingConfig] = {
    key: LoggingConfig(**value)
    for key, value in CONFIG["logging"].items()
}
TIMEZONE: timezone = timezone(timedelta(hours=CONFIG["timezone"]))
TIMEOUT: int = CONFIG["timeout"]
