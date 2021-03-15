import argparse
import asyncio
import os
import random
import shutil
import string
import time
from pathlib import Path

import hachoir
import requests
import wget
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from selenium import webdriver
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from DaisyX import telethn as borg

headers = {"UserAgent": UserAgent().random}
import asyncio
import json
import math
import os
import re
import shlex
import subprocess
import time
import webbrowser
from os.path import basename
from typing import List, Optional, Tuple, Union

import eyed3
import requests
import telethon
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from pymediainfo import MediaInfo
from telethon import Button, custom, events, functions
from telethon.tl.types import InputMessagesFilterDocument, MessageMediaPhoto

from DaisyX.function.FastTelethon import download_file

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]
BASE_URL = "https://isubtitles.org"
import os
import zipfile

import aiohttp

from DaisyX import TMP_DOWNLOAD_DIRECTORY
from DaisyX.function.FastTelethon import upload_file

session = aiohttp.ClientSession()

sedpath = TMP_DOWNLOAD_DIRECTORY


async def fetch_json(link):
    async with session.get(link) as resp:
        return await resp.json()
def get_readable_file_size(size_in_bytes: Union[int, float]) -> str:
    if size_in_bytes is None:
        return "0B"
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{SIZE_UNITS[index]}"
    except IndexError:
        return "File too large"


def get_readable_time(secs: float) -> str:
    result = ""
    (days, remainder) = divmod(secs, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d"
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h"
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m"
    seconds = int(seconds)
    result += f"{seconds}s"
    return result

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
#For future use
"""
# Thanks To Userge-X
async def crop_vid(input_vid: str, final_path: str):
    media_info = MediaInfo.parse(input_vid)
    for track in media_info.tracks:
        if track.track_type == "Video":
            aspect_ratio = track.display_aspect_ratio
            height = track.height
            width = track.width
    if aspect_ratio != 1:
        crop_by = width if (height > width) else height
        os.system(f'ffmpeg -i {input_vid} -vf "crop={crop_by}:{crop_by}" {final_path}')
        os.remove(input_vid)
    else:
        os.rename(input_vid, final_path)


# Thanks To Userge-X
async def take_screen_shot(
        video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    
    logger.info(
        "[[[Extracting a frame from %s ||| Video duration => %s]]]",
        video_file,
        duration,
    )
    ttl = duration // 2
    thumb_image_path = path or os.path.join(sedpath, f"{basename(video_file)}.jpg")
    command = f'''ffmpeg -ss {ttl} -i "{video_file}" -vframes 1 "{thumb_image_path}"'''
    err = (await runcmd(command))[1]
    if err:
        logger.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None

"""    

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
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
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
        os.rename(pathofsticker2, image_new_path)
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
    await event.edit("`Almost Completed.`")
    return lmao_final

async def get_subtitles(imdb_id, borg, event):
    await event.edit("`Processing..`")
    link = f"https://yts-subs.com/movie-imdb/" + imdb_id
    movie_response = requests.get(url=link)
    subtitles = []
    soup1 = BeautifulSoup(movie_response.content, "html.parser")
    rows = soup1.find_all("tr", class_="high-rating")
    for row in rows:
        td = row.find("td", class_="flag-cell")
        lang = td.find("span", class_="sub-lang").text
        if lang == "English":
            sub_link_tag = row.find("td", class_="download-cell")
            sub_link = sub_link_tag.find("a", class_="subtitle-download").get("href")
            sub_link = f"https://yts-subs.com/{sub_link}"
            sub_name_tag = row.find("td", class_=None)
            sub_name = (
                str(sub_name_tag.find("a").text)
                    .replace("subtitle", "")
                    .replace("\n", "")
            )
            sub = (sub_name, sub_link)
            subtitles.append(sub)
    await event.edit("`Almost Done.`")
    sub_response = requests.get(url=subtitles[0]["sub_link"])
    selected_sub_name = subtitles[0]["sub_name"]
    soup2 = BeautifulSoup(sub_response.content, "html.parser")
    link = soup2.find("a", class_="btn-icon download-subtitle").get("href")
    final_response = requests.get(link, stream=True)
    await event.edit("`Downloading Now`")
    if final_response.status_code == 200:
        with open(sedpath + f"{selected_sub_name}.zip", "wb") as sfile:
            for byte in final_response.iter_content(chunk_size=128):
                sfile.write(byte)
    final_paths = sedpath + f"{selected_sub_name}.zip"
    namez = selected_sub_name
    return final_paths, namez, subtitles[0]["sub_link"]




async def apk_dl(app_name, path, event):
    await event.edit(
        "`Searching, For Apk File. This May Take Time Depending On Your App Size`"
    )
    res = requests.get(f"https://m.apkpure.com/search?q={app_name}")
    soup = BeautifulSoup(res.text, "html.parser")
    result = soup.select(".dd")
    for link in result[:1]:
        s_for_name = requests.get("https://m.apkpure.com" + link.get("href"))
        sfn = BeautifulSoup(s_for_name.text, "html.parser")
        ttl = sfn.select_one("title").text
        noneed = [" - APK Download"]
        for i in noneed:
            name = ttl.replace(i, "")
            res2 = requests.get(
                "https://m.apkpure.com" + link.get("href") + "/download?from=details"
            )
            soup2 = BeautifulSoup(res2.text, "html.parser")
            result = soup2.select(".ga")
        for link in result:
            dl_link = link.get("href")
            r = requests.get(dl_link)
            with open(f"{path}/{name}@DaisyXBot.apk", "wb") as f:
                f.write(r.content)
    await event.edit("`Apk, Downloaded. Let me Upload It here.`")
    final_path = f"{path}/{name}@DaisyXBot.apk"
    return final_path, name


async def _ytdl(url, is_it, event, tgbot):
    await event.edit("`Ok Downloading This Video / Audio - Please Wait.` \n**Powered By @FridayOT**")
    if is_it:
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "480",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    else:
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except Exception as e:
        await event.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    if song:
        file_stark = f"{ytdl_data['id']}.mp3"
        lol_m = await upload_file(
            file_name=f"{ytdl_data['title']}.mp3",
            client=tgbot,
            file=open(file_stark, 'rb'),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, event, c_time, "Uploading Youtube Audio..", file_stark
                )
            ),
        )
        await event.edit(
            file=lol_m,
            text=f"{ytdl_data['title']} \n**Powered by @DaisySupport_Official**"
        )
        os.remove(file_stark)
    elif video:
        file_stark = f"{ytdl_data['id']}.mp4"
        lol_m = await upload_file(
            file_name=f"{ytdl_data['title']}.mp4",
            client=tgbot,
            file=open(file_stark, 'rb'),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, event, c_time, "Uploading Youtube Video..", file_stark
                )
            ),
        )
        await event.edit(
            file=lol_m,
            text=f"{ytdl_data['title']} \n**Report Bugs @DaisySupport_Official**"
        )
        os.remove(file_stark)


async def _deezer_dl(word, event, tgbot):
    await event.edit("`Ok Downloading This Audio - Please Wait.` \n**Powered By @DaisySupport_Official** with the help of @FridayOT")
    urlp = f"https://starkapi.herokuapp.com/deezer/{word}"
    datto = requests.get(url=urlp).json()
    mus = datto.get("url")
    mello = datto.get("artist")
    #thums = urlhp["album"]["cover_medium"]
    sname = f'''{datto.get("title")}.mp3'''
    doc = requests.get(mus)
    with open(sname, 'wb') as f:
      f.write(doc.content)
    car = f"""
**Song Name :** {datto.get("title")}
**Duration :** {datto.get('duration')} Seconds
**Artist :** {mello}
Music Downloaded And Uploaded By @DaisyXBot
Say hi to DaisyTeam @DaisySupport_Official"""
    await event.edit("Song Downloaded.  Waiting To Upload. 🥳🤗")
    c_time = time.time()
    uploaded_file = await upload_file(
        	file_name=sname,
            client=tgbot,
            file=open(sname, 'rb'),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, event, c_time, "Uploading..", sname
                )
            ),
        )
    
    await event.edit(
            file=uploaded_file,
            text=car
    )
    os.remove(sname)

async def fetch_audio(event, ws):
    if not event.reply_to_msg_id:
        await event.edit("`Reply To A Video / Audio.`")
        return
    warner_stark = await event.get_reply_message()    
    if warner_stark.audio is None  and warner_stark.video is None:
        await event.edit("`Format Not Supported`")
        return
    if warner_stark.video:
        await event.edit("`Video Detected, Converting To Audio !`")
        warner_bros = await event.client.download_media(warner_stark.media)
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a friday.mp3"
        await runcmd(stark_cmd)
        final_warner = "friday.mp3"
    elif warner_stark.audio:
        await event.edit("`Download Started !`")
        final_warner = await event.client.download_media(warner_stark.media)
    await event.edit("`Almost Done!`")    
    return final_warner

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
