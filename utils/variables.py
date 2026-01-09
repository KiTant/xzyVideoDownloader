import os

APP_NAME = "xzyVideoDownloader"
REPO_NAME = APP_NAME
ICON_PATH = 'assets/xzy-video-downloader-icon.ico'
VERSION = "1.3.0"
RPC_ID = "1399413906010673282"

APPDATA = os.getenv('APPDATA')
FILES = {"settings_file": os.path.join(APPDATA, APP_NAME, 'settings.json'),
         "previous_settings_file": os.path.join(APPDATA, APP_NAME, 'previous_settings.json'),
         "special_settings_file": os.path.join(APPDATA, APP_NAME, 'special_settings.json'),
         "queue_file": os.path.join(APPDATA, APP_NAME, 'saved_queue.json')}

MAIN_THEMES = {
    0: "Carrot",
    1: "Rose",
    2: "Blue",
    3: "Dark-Blue",
    4: "Green",
    5: "Pink",
    6: "Violet",
    7: "Yellow",
    8: "Coffee",
    9: "Sky",
    10: "Red",
    11: "Marsh",
    12: "Metal"
}

DEFAULT_SETTINGS = {
    "theme": "Dark",
    "main_theme": "Carrot",
    "notifications": "TextAndWindowsNotification",  # OnlyText; TextAndMessageBox; TextAndWindowsNotification
    "auto_load": "Enabled",
    "auto_save": "Enabled",
    "queue_auto_load": "Enabled",
    "queue_auto_save": "Enabled",
    "link_auto_remove": "Enabled",
    "discord_rpc": "Disabled",
    "custom_format": ""
}

DEFAULT_SPECIAL_SETTINGS = {  # Special settings will be saved anyway after any change(s) (and auto loaded always)
    "default_path": "",
    "saved_link_input": "",
    "download_type": "",
    "quality": "",
    "use_queue": "",
    "use_cookies": "",
    "cookies_path": "",
}
