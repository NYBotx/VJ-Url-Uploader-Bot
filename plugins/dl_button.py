# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import logging
import asyncio
import aiohttp
import os
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from config import Config
from translation import Translation

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def download_file(url, file_path, bot, chat_id, message_id):
    """
    Download a file from a given URL.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=Config.TECH_VJ_PROCESS_MAX_TIMEOUT) as response:
            total_length = int(response.headers.get("Content-Length", 0))
            content_type = response.headers.get("Content-Type", "")
            if "googlevideo.com" not in url or not content_type.startswith("video/"):
                await bot.edit_message_text(
                    chat_id,
                    message_id,
                    text="Invalid or unsupported video URL."
                )
                return None

            await bot.edit_message_text(
                chat_id,
                message_id,
                text=f"**Downloading File**\nURL: {url}\nFile Size: {humanbytes(total_length)}"
            )
            with open(file_path, "wb") as f:
                downloaded = 0
                start_time = time.time()
                async for chunk in response.content.iter_chunked(Config.TECH_VJ_CHUNK_SIZE):
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    now = time.time()
                    diff = now - start_time
                    if round(diff % 5.00) == 0 or downloaded == total_length:
                        percentage = downloaded * 100 / total_length
                        speed = downloaded / diff
                        eta = (total_length - downloaded) / speed
                        await bot.edit_message_text(
                            chat_id,
                            message_id,
                            text=f"**Download Progress**\n{humanbytes(downloaded)} of {humanbytes(total_length)} "
                                 f"({round(percentage, 2)}%)\nSpeed: {humanbytes(speed)}/s\nETA: {TimeFormatter(eta * 1000)}"
                        )
            return file_path


async def extract_metadata(file_path):
    """
    Extract video metadata.
    """
    metadata = extractMetadata(createParser(file_path))
    if metadata:
        return metadata.get("duration").seconds, metadata.get("width"), metadata.get("height")
    return None, None, None


async def generate_thumbnail(file_path, duration, output_path):
    """
    Generate a thumbnail for the video.
    """
    try:
        from ffmpeg import input as ffmpeg_input
        ffmpeg_input(file_path, ss=duration // 2).output(output_path, vframes=1).run(overwrite_output=True)
    except Exception as e:
        logger.error(f"Failed to generate thumbnail: {e}")
        return None
    return output_path


async def upload_file(file_path, bot, chat_id, message_id, tg_send_type):
    """
    Upload the downloaded file to Telegram.
    """
    start_time = time.time()
    description = f"**Uploaded by @VJ_Botz**"
    duration, width, height = await extract_metadata(file_path)

    if tg_send_type == "video":
        thumb_path = await generate_thumbnail(file_path, duration, f"{file_path}.jpg")
        await bot.send_video(
            chat_id=chat_id,
            video=file_path,
            caption=description,
            duration=duration,
            width=width,
            height=height,
            supports_streaming=True,
            thumb=thumb_path,
            reply_to_message_id=message_id,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.TECH_VJ_UPLOAD_START,
                message_id,
                start_time
            )
        )
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)
    elif tg_send_type == "audio":
        duration, _ = await extract_metadata(file_path)
        await bot.send_audio(
            chat_id=chat_id,
            audio=file_path,
            caption=description,
            duration=duration,
            reply_to_message_id=message_id,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.TECH_VJ_UPLOAD_START,
                message_id,
                start_time
            )
        )
    elif tg_send_type == "file":
        await bot.send_document(
            chat_id=chat_id,
            document=file_path,
            caption=description,
            reply_to_message_id=message_id,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.TECH_VJ_UPLOAD_START,
                message_id,
                start_time
            )
        )

    os.remove(file_path)


async def process_direct_link(bot, update):
    """
    Process a direct link, download, and upload it.
    """
    url = update.message.text.strip()
    custom_file_name = "downloaded_video.mp4"  # Default file name
    user_id = update.message.chat.id

    # Directories
    download_dir = os.path.join(Config.TECH_VJ_DOWNLOAD_LOCATION, str(user_id))
    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, custom_file_name)

    # Step 1: Download
    await bot.edit_message_text(
        chat_id=update.message.chat.id,
        message_id=update.message.id,
        text="**Starting download...**"
    )
    downloaded_file = await download_file(url, file_path, bot, update.message.chat.id, update.message.id)

    if not downloaded_file:
        await bot.edit_message_text(
            chat_id=update.message.chat.id,
            message_id=update.message.id,
            text="**Failed to download the file.**"
        )
        return

    # Step 2: Upload
    await bot.edit_message_text(
        chat_id=update.message.chat.id,
        message_id=update.message.id,
        text="**Starting upload...**"
    )
    tg_send_type = "video"  # Default to video
    await upload_file(downloaded_file, bot, update.message.chat.id, update.message.id, tg_send_type)
