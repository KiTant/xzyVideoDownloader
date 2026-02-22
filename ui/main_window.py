import threading
import customtkinter as ctk
import os
from utils.helpers import *
from utils.variables import DEFAULT_SETTINGS, DEFAULT_SPECIAL_SETTINGS, ICON_PATH, APP_NAME, FILES
from utils.settings_manager import *
from utils.download_manager import start_download_thread, stop_download
from utils.queue_manager import *
from ui.title_menu import TitleMenu
from ui.queue_window import QueueWindow
from utils.rpc_manager import RPCManager
import queue


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("720x640")
        self.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)
        self.after(300, lambda: self.iconbitmap(resource_path(ICON_PATH)))

        self.all_children = []

        self.settings = DEFAULT_SETTINGS.copy()
        self.special_settings = DEFAULT_SPECIAL_SETTINGS.copy()

        self.download_queue = queue.Queue()
        self.queue_for_display = []
        self.display_lock = threading.Lock()

        self.use_cookies_var = ctk.BooleanVar(value=False)
        self.use_queue_var = ctk.BooleanVar(value=False)
        self.url_var = ctk.StringVar()
        self.download_type_var = ctk.StringVar(value="Video and Audio")
        self.quality_var = ctk.StringVar(value="Best (both)")
        self.save_path_var = ctk.StringVar(value=os.path.join(os.path.expanduser('~'), 'Downloads'))
        self.cookies_file_path_var = ctk.StringVar(value="None")

        self.rpc = RPCManager()

        self.download_thread = None
        self.stop_download_flag = False
        self.is_processing_queue = False

        settings_load(self, FILES.get("settings_file"), auto_load=True, set_vars=True)
        settings_load(self, FILES.get("special_settings_file"),
                      default_values=DEFAULT_SPECIAL_SETTINGS, attr_name="special_settings")

        self._initialize_components()

    def _initialize_components(self):
        self.url_label = ctk.CTkLabel(self, text="Video URL (YouTube; TikTok; RuTube; VK; Instagram; etc):")
        self.url_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.url_entry = ctk.CTkEntry(self, textvariable=self.url_var, width=400)
        self.url_entry.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        entry_keybinds_normalize(self.url_entry)

        if self.special_settings["saved_link_input"]:
            self.url_var.set(self.special_settings["saved_link_input"])

        self.download_type_label = ctk.CTkLabel(self, text="Download Type:")
        self.download_type_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.radio_video_audio = ctk.CTkRadioButton(self, text="Video and Audio",
                                                    variable=self.download_type_var, value="Video and Audio")
        self.radio_video_audio.grid(row=3, column=0, padx=20, pady=3, sticky="w")
        self.radio_video_only = ctk.CTkRadioButton(self, text="Video Only", variable=self.download_type_var,
                                                   value="Video Only")
        self.radio_video_only.grid(row=4, column=0, padx=20, pady=3, sticky="w")
        self.radio_audio_only = ctk.CTkRadioButton(self, text="Audio Only (MP3)",
                                                   variable=self.download_type_var, value="Audio Only (MP3)")
        self.radio_audio_only.grid(row=5, column=0, padx=20, pady=3, sticky="w")
        self.radio_custom_format = ctk.CTkRadioButton(self, text="Custom Format",
                                                      variable=self.download_type_var, value="Custom Format")
        self.radio_custom_format.grid(row=4, column=0, padx=125, pady=3, sticky="w")

        if self.special_settings["download_type"]:
            self.download_type_var.set(self.special_settings["download_type"])

        self.quality_label = ctk.CTkLabel(self, text="Quality:")
        self.quality_label.grid(row=2, column=0, padx=20, pady=(10, 2), sticky="n")
        self.quality_menu = ctk.CTkOptionMenu(self, variable=self.quality_var,
                                              values=["Best (both)", "Best (audio); Worst (video)",
                                                      "Worst (audio); Best (video)", "Worst (both)",
                                                      "1080p", "720p", "480p", "360p"])
        self.quality_menu.grid(row=3, column=0, padx=20, pady=2, sticky="n")

        if self.special_settings["quality"] and self.special_settings["quality"] in self.quality_menu.cget("values"):
            self.quality_var.set(self.special_settings["quality"])

        self.add_to_queue_button = ctk.CTkButton(self, text="Add to the queue", command=lambda: add_to_queue(self))
        self.add_to_queue_button.grid(row=2, column=0, padx=20, pady=5, sticky="e")

        self.check_queue_button = ctk.CTkButton(self, text="Show queue",
                                                command=lambda: (self.queue_window.deiconify(), self.queue_window.lift()))
        self.check_queue_button.grid(row=3, column=0, padx=20, pady=5, sticky="e")

        self.clear_queue_button = ctk.CTkButton(self, text="Clear queue", command=lambda: clear_queue(self))
        self.clear_queue_button.grid(row=4, column=0, padx=20, pady=5, sticky="e")

        self.cookies_checkbox = ctk.CTkCheckBox(self, text="Use queue for download", variable=self.use_queue_var)
        self.cookies_checkbox.grid(row=5, column=0, padx=20, sticky="e")

        if self.special_settings["use_queue"]:
            self.use_queue_var.set(self.special_settings["use_queue"])

        self.queue_window = QueueWindow()
        self.queue_window.withdraw()

        self.cookies_file_label = ctk.CTkLabel(self, text="Cookies file:")
        self.cookies_file_label.grid(row=6, column=0, padx=20, pady=(10, 5), sticky="w")
        self.cookies_file_entry = ctk.CTkEntry(self, textvariable=self.cookies_file_path_var, state="readonly")
        self.cookies_file_entry.grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        self.select_cookies_file_button = ctk.CTkButton(self, text="Select cookies file",
                                                        command=lambda: select_cookies_file(self))
        self.select_cookies_file_button.grid(row=8, column=0, padx=20, pady=5, sticky="w")

        if self.special_settings["cookies_path"]:
            self.cookies_file_path_var.set(self.special_settings["cookies_path"])

        self.cookies_checkbox = ctk.CTkCheckBox(self, text="Use cookies (from choosed file)",
                                                variable=self.use_cookies_var)
        self.cookies_checkbox.grid(row=8, column=0, padx=20, sticky="s")

        if self.special_settings["use_cookies"]:
            self.use_cookies_var.set(self.special_settings["use_cookies"])

        self.save_folder_label = ctk.CTkLabel(self, text="Save Folder:")
        self.save_folder_label.grid(row=9, column=0, padx=20, pady=(10, 5), sticky="w")
        self.save_folder_entry = ctk.CTkEntry(self, textvariable=self.save_path_var, state="readonly")
        self.save_folder_entry.grid(row=10, column=0, padx=20, pady=5, sticky="ew")
        self.select_folder_button = ctk.CTkButton(self, text="Select Folder", command=lambda: select_folder(self))
        self.select_folder_button.grid(row=11, column=0, padx=20, pady=5, sticky="w")

        if self.special_settings["default_path"]:
            self.save_path_var.set(self.special_settings["default_path"])

        self.download_button = ctk.CTkButton(self, text="Download", command=self.start_download)
        self.download_button.grid(row=12, column=0, padx=20, pady=(10, 5), sticky="ew")
        self.stop_button = ctk.CTkButton(self, text="Stop Download", command=lambda: stop_download(self),
                                         state="disabled")
        self.stop_button.grid(row=13, column=0, padx=20, pady=5, sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="",
                                         font=ctk.CTkFont(family="Arial", size=16))
        self.status_label.grid(row=14, column=0, padx=20, pady=5, sticky="w")
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=16, column=0, padx=20, pady=(5, 20), sticky="ew")

        self.menu = TitleMenu(self)

        if self.settings["discord_rpc"] == "Enabled":
            self.rpc.rpc_connect()

        self.protocol("WM_DELETE_WINDOW", self.window_close)

        if self.settings["queue_auto_load"] == "Enabled":
            settings_load(self, FILES.get("queue_file"), default_values={}, attr_name="download_queue")

    def update_status(self, message, **kwargs):
        self.status_label.configure(text=message, **kwargs)

    def window_close(self):
        try:
            self.rpc.rpc_close()
            self.save_spec_attrs()
        finally:
            self.destroy()

    def save_spec_attrs(self):
        self.special_settings["saved_link_input"] = self.url_entry.get()
        self.special_settings["default_path"] = self.save_path_var.get()
        self.special_settings["download_type"] = self.download_type_var.get()
        self.special_settings["quality"] = self.quality_var.get()
        self.special_settings["use_queue"] = self.use_queue_var.get()
        self.special_settings["use_cookies"] = self.use_cookies_var.get()
        self.special_settings["cookies_path"] = self.cookies_file_path_var.get()
        settings_save(self, FILES.get("special_settings_file"), self.special_settings)
        if self.settings["queue_auto_save"] == "Enabled":
            settings_save(self, FILES.get("queue_file"), queue_obj=self.download_queue)

    def start_download(self):
        self.save_spec_attrs()
        if self.use_queue_var.get():
            start_queue_processing(self)
        else:
            start_download_thread(self)
