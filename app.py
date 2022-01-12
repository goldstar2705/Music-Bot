# Telegram Channel @JaguarBots

import os
import asyncio
import wget
from pyrogram import Client, filters
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos

bot = Client(
    "Music Bot",
    bot_token = os.environ["829809566:AAH97GqDC9_sGApp1nWwSBDItxQKaGjbaPU"],
    api_id = int(os.environ["1286763"]),
    api_hash = os.environ["676238949450c128a465ec4c0cc9c170"]
)

START_TEXT = """
 **{}** 
Behzod Shokirov Tark etding
  **@GOLD_STARUZ**
"""

@bot.on_message(filters.command("start") & filters.private)
async def start(_, message):
    msg = START_TEXT.format(message.from_user.mention)
    await message.reply_text(text = msg, disable_web_page_preview=True)
    
    
@bot.on_message(filters.text & filters.private & ~filters.command("start"))
async def get_songs(_, message):
    query = message.text
    m = await message.reply_text("Searching", quote=True)
    search = SearchVideos(f"{query}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    lenk = mio[0]["link"]
    title = mio[0]["title"]
    ytid = mio[0]["id"]
    channel = mio[0]["channel"]
    #views = mio[0]["views"]
    dur = mio[0]["duration"]
    tblink = f"https://img.youtube.com/vi/{ytid}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    tb = wget.download(tblink)
    
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
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    
    await m.edit("Behzod Shokirov Tark etding")
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(lenk, download=True)
    except Exception as e:
        return await m.edit(f"**Download Failed** \n\n```{e}```")
      
    cap = f"**🎧 Title:** {title} \n**🎥 Channel:** {channel} \n**⏳ Duration:** {dur} \n\n**📮 By @GOLD_STARUZ**"
    aud = f"{ytdl_data['id']}.mp3"
    await m.edit("Uploading")
    await message.reply_audio(audio=open(aud, "rb"), 
                              duration=int(ytdl_data["duration"]), 
                              title=str(ytdl_data["title"]), 
                              performer=str(ytdl_data["uploader"]),
                              thumb=tb,
                              caption=cap,
                              quote=True)
    await m.delete()
    for files in (tb, aud):
        if files and os.path.exists(files):
            os.remove(files)
    
    
bot.run()
