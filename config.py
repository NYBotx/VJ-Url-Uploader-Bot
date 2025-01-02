# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
from os import environ, getenv

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

class Config(object):
    # Bot Information 
    TECH_VJ_BOT_TOKEN = "8120897740:AAHBzDf484aQZwOlz4Sp5s7rwfHAMyU0JNM"
    TECH_VJ_BOT_USERNAME = "Url_uploader_nybot"  # Bot username without @.

    # The Telegram API things
    TECH_VJ_API_ID = 13963336
    TECH_VJ_API_HASH = "a144d1e22ef0b29738e8c00713d02678"

    # The download location, where the HTTP Server runs
    TECH_VJ_DOWNLOAD_LOCATION = "./DOWNLOADS"

    # Telegram maximum file upload size
    TECH_VJ_MAX_FILE_SIZE = 2097152000
    TECH_VJ_TG_MAX_FILE_SIZE = 2097152000
    TECH_VJ_FREE_USER_MAX_FILE_SIZE = 2097152000

    # Chunk size that should be used with requests
    TECH_VJ_CHUNK_SIZE = 128

    # Default thumbnail to be used in the videos
    TECH_VJ_HTTP_PROXY = ""

    # Maximum message length in Telegram
    TECH_VJ_MAX_MESSAGE_LENGTH = 4096

    # Set timeout for subprocess
    TECH_VJ_PROCESS_MAX_TIMEOUT = 0

    # Your telegram account ID
    TECH_VJ_OWNER_ID = 2103299862
    TECH_VJ_SESSION_NAME = "Url_uploader_nybot"

    # Database URI (mongodb)
    TECH_VJ_DATABASE_URL = "mongodb+srv://Nischay999:Nischay999@cluster0.5kufo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    TECH_VJ_MAX_RESULTS = "50"

    # Channel Information
    TECH_VJ_LOG_CHANNEL = -1002421238378  # Your log channel ID and make bot admin in log channel with full rights

    # If you want force subscribe then give your channel ID below else leave blank
    TECH_VJ_UPDATE_CHANNEL = -1002465691872  # Your update channel ID and make bot admin in update channel with full rights
    TECH_VJ_UPDATES_CHANNEL = -1002465691872

    # Url Shortener Information
    TECH_VJ = False  # Set False if you want shortlink off else True
    TECH_VJ_URL = ""  # Your shortlink URL domain or URL without https://
    TECH_VJ_API = ""  # Your URL shortener API
    TECH_VJ_TUTORIAL = "https://t.me/How_To_Open_Linkl"  # Tutorial link
