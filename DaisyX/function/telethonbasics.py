from telethon import events

async def get_all_admin_chats(event):
    lul_stark = []
    all_chats = [
        d.entity
            for d in await event.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
    try:
        for i in all_chats:
            if i.creator or i.admin_rights:
                lul_stark.append(i.id)
    except:
        pass
    return lul_stark

                  
async def is_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod

# ================================================


import random
import requests

from bs4 import BeautifulSoup
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import hachoir
import asyncio
import os
from selenium import webdriver
import time
import requests
import wget
from DaisyX.services.telethon import tbot as borg
from telethon.tl.types import DocumentAttributeAudio
from PIL import Image
import requests
from bs4 import BeautifulSoup
import asyncio
import json
import math
import re
import subprocess
import time
from os.path import basename
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup as bs
import re
from telethon.tl.types import InputMessagesFilterDocument
import telethon
from telethon import Button, custom, events, functions
from pymediainfo import MediaInfo
from telethon.tl.types import MessageMediaPhoto
SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]
import aiohttp
import numpy as np
import cv2
sedpath = "./"


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["🟠" for i in range(math.floor(percentage / 10))]),
            "".join(["🔘" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await event.edit(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                    
                )
            except:
                pass
        else:
            try:
                await event.edit("{}\n{}".format(type_of_ps, tmp))
            except:
                pass


def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
            ((str(days) + " day(s), ") if days else "")
            + ((str(hours) + " hour(s), ") if hours else "")
            + ((str(minutes) + " minute(s), ") if minutes else "")
            + ((str(seconds) + " second(s), ") if seconds else "")
            + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


# Thanks To Userge-X
# Ported By @STARKXD
async def convert_to_image(event, borg):
    lmao = await event.get_reply_message()
    if not (
            lmao.gif
            or lmao.audio
            or lmao.voice
            or lmao.video
            or lmao.video_note
            or lmao.photo
            or lmao.sticker
            or lmao.media
    ):
        await event.edit("`Format Not Supported.`")
        return
    else:
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                lmao.media,
                sedpath,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "`Downloading...`")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit(
                "Downloaded to `{}` successfully.".format(downloaded_file_name)
            )
    if not os.path.exists(downloaded_file_name):
        await event.edit("Download Unsucessfull :(")
        return
    if lmao and lmao.photo:
        lmao_final = downloaded_file_name
    elif lmao.sticker and lmao.sticker.mime_type == "application/x-tgsticker":
        rpath = downloaded_file_name
        image_name20 = os.path.join(sedpath, "SED.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {downloaded_file_name} {image_name20}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(rpath)
        lmao_final = image_name20
    elif lmao.sticker and lmao.sticker.mime_type == "image/webp":
        pathofsticker2 = downloaded_file_name
        image_new_path = sedpath + "image.png"
        im = Image.open(pathofsticker2)
        im.save(image_new_path, "PNG")
        if not os.path.exists(image_new_path):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = image_new_path
    elif lmao.audio:
        sed_p = downloaded_file_name
        hmmyes = sedpath + "stark.mp3"
        imgpath = sedpath + "starky.jpg"
        os.rename(sed_p, hmmyes)
        await runcmd(f"ffmpeg -i {hmmyes} -filter:v scale=500:500 -an {imgpath}")
        os.remove(sed_p)
        if not os.path.exists(imgpath):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = imgpath
    elif lmao.gif or lmao.video or lmao.video_note:
        sed_p2 = downloaded_file_name
        jpg_file = os.path.join(sedpath, "image.jpg")
        await take_screen_shot(sed_p2, 0, jpg_file)
        os.remove(sed_p2)
        if not os.path.exists(jpg_file):
            await event.edit("`Couldn't Fetch. SS`")
            return
        lmao_final = jpg_file
    return lmao_final



async def is_nsfw(event):
    lmao = event
    if not (
            lmao.gif
            or lmao.video
            or lmao.video_note
            or lmao.photo
            or lmao.sticker
            or lmao.media
    ):
        return False
    if lmao.video or lmao.video_note or lmao.sticker or lmao.gif:
        try:
            starkstark = await event.client.download_media(lmao.media, thumb=-1)
        except:
            return False
    elif lmao.photo or lmao.sticker:
        try:
            starkstark = await event.client.download_media(lmao.media)
        except:
            return False
    img = starkstark
    f = {"file": (img, open(img, "rb"))}
    
    r = requests.post("https://starkapi.herokuapp.com/nsfw/", files = f).json()
    if r.get("success") is False:
      is_nsfw = False
    elif r.get("is_nsfw") is True:
      is_nsfw = True
    elif r.get("is_nsfw") is False:
      is_nsfw = False
    return is_nsfw
    

