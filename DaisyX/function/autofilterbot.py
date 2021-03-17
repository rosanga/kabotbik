#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from pyrogram import (
    __version__,
    Client
)
import os
import logging
from logging.handlers import RotatingFileHandler


from DaisyX.config import get_str_key, get_int_key
#from DaisyX.services.pyrogram import pbot as Client
TG_BOT_TOKEN = get_str_key("TOKEN", required=True)
APP_ID = get_int_key("AUTOFILTER_APP_ID", required=True)
API_HASH = get_str_key("AUTOFILTER_APP_HASH", required=True)
TG_USER_SESSION = get_str_key("AUTOFILTER_SESSION", required=True)
TG_BOT_WORKERS = 4
LOG_FILE_NAME = "filterbot.txt"
#from user import User

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

class User(Client):
    def __init__(self):
        super().__init__(
            TG_USER_SESSION,
            api_hash=API_HASH,
            api_id=APP_ID,
            workers=TG_BOT_WORKERS
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.set_parse_mode("html")
        return (self, usr_bot_me.id)

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
 
class Bot(Client):
    USER: User = None
    USER_ID: int = None
    async def start(self):
        #AUTH_USERS.add(680815375)
        self.USER, self.USER_ID = await User().start()
Bot().run()
