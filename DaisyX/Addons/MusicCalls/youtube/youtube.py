from youtube_dl import YoutubeDL

from DaisyX import DURATION_LIMIT
from DaisyX.Addons.MusicCalls.helpers.errors import DurationLimitError

DURATION_LIMIT = get_str_key("DURATION_LIMIT", required=True)
ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)"
        )

    ydl.download([url])
    return f"downloads/{info['id']}.{info['ext']}"
