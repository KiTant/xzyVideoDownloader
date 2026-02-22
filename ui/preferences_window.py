import customtkinter as ctk
import webbrowser
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager
from CTkMessagebox import CTkMessagebox
from utils.helpers import resource_path, entry_keybinds_normalize
from utils.ui_manager import window_close
from utils.settings_manager import *
from utils.variables import DEFAULT_SETTINGS, MAIN_THEMES, APP_NAME, ICON_PATH, FILES
from CTkListbox import CTkListbox
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


class PreferencesWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: "MainWindowClass"):
        super().__init__()
        self.MainWindow = MainWindow
        self.title("Preferences")
        self.geometry("1000x400")
        self.resizable(False, False)
        self.after(300, lambda: self.iconbitmap(resource_path(ICON_PATH)))

        self._initialize_components()

    def _initialize_components(self):
        ctk.CTkLabel(self, text="Theme:").place(relx=0.025, rely=0.01)
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        ctk.CTkRadioButton(self, text="Dark", variable=self.theme_var, value="Dark").place(relx=0.025, rely=0.1)
        ctk.CTkRadioButton(self, text="Light", variable=self.theme_var, value="Light").place(relx=0.025, rely=0.2)

        ctk.CTkLabel(self, text="Auto Load (settings):").place(relx=0.025, rely=0.3)
        self.auto_load = ctk.StringVar(value=self.MainWindow.settings["auto_load"])
        ctk.CTkRadioButton(self, text="Enabled", variable=self.auto_load, value="Enabled").place(relx=0.025, rely=0.4)
        ctk.CTkRadioButton(self, text="Disabled", variable=self.auto_load, value="Disabled").place(relx=0.025, rely=0.5)

        ctk.CTkLabel(self, text="Auto Save (settings):").place(relx=0.17, rely=0.3)
        self.auto_save = ctk.StringVar(value=self.MainWindow.settings["auto_save"])
        ctk.CTkRadioButton(self, text="Enabled", variable=self.auto_save, value="Enabled").place(relx=0.17, rely=0.4)
        ctk.CTkRadioButton(self, text="Disabled", variable=self.auto_save, value="Disabled").place(relx=0.17, rely=0.5)

        ctk.CTkLabel(self, text="Notifications:").place(relx=0.15, rely=0.01)
        self.notifications = ctk.StringVar(value=self.MainWindow.settings["notifications"])
        ctk.CTkRadioButton(self, text="Only Text", variable=self.notifications, value="OnlyText").place(relx=0.15, rely=0.1)
        ctk.CTkRadioButton(self, text="Text + Message Box", variable=self.notifications, value="TextAndMessageBox").place(relx=0.15, rely=0.2)
        ctk.CTkRadioButton(self, text="Text + Windows Notification", variable=self.notifications,
                           value="TextAndWindowsNotification").place(relx=0.25, rely=0.1)

        ctk.CTkLabel(self, text="Auto Load (queue):").place(relx=0.025, rely=0.6)
        self.queue_auto_load = ctk.StringVar(value=self.MainWindow.settings["queue_auto_load"])
        ctk.CTkRadioButton(self, text="Enabled", variable=self.queue_auto_load, value="Enabled").place(relx=0.025, rely=0.7)
        ctk.CTkRadioButton(self, text="Disabled", variable=self.queue_auto_load, value="Disabled").place(relx=0.025, rely=0.8)

        ctk.CTkLabel(self, text="Auto Save (queue):").place(relx=0.17, rely=0.6)
        self.queue_auto_save = ctk.StringVar(value=self.MainWindow.settings["queue_auto_save"])
        ctk.CTkRadioButton(self, text="Enabled", variable=self.queue_auto_save, value="Enabled").place(relx=0.17, rely=0.7)
        ctk.CTkRadioButton(self, text="Disabled", variable=self.queue_auto_save, value="Disabled").place(relx=0.17, rely=0.8)

        ctk.CTkLabel(self, text="Discord RPC:").place(relx=0.3, rely=0.3)
        self.discord_rpc = ctk.StringVar(value=self.MainWindow.settings["discord_rpc"])
        ctk.CTkRadioButton(self, text="Enabled", variable=self.discord_rpc, value="Enabled").place(relx=0.3, rely=0.4)
        ctk.CTkRadioButton(self, text="Disabled", variable=self.discord_rpc, value="Disabled").place(relx=0.3, rely=0.5)

        ctk.CTkLabel(self, text="Link auto remove\n(after adding to the queue):").place(relx=0.3, rely=0.59)
        self.link_auto_remove = ctk.StringVar(value=self.MainWindow.settings["link_auto_remove"])
        ctk.CTkRadioButton(self, text="Enabled", variable=self.link_auto_remove, value="Enabled").place(relx=0.3, rely=0.7)
        ctk.CTkRadioButton(self, text="Disabled", variable=self.link_auto_remove, value="Disabled").place(relx=0.3, rely=0.8)

        ctk.CTkLabel(self, text="Main Theme:").place(relx=0.5, rely=0.01)
        self.main_themes = CTkListbox(self, width=125, font=ctk.CTkFont(family="Arial", size=12),
                                      hover_color=ThemeManager.theme["CTkOptionMenu"]["button_hover_color"],
                                      highlight_color=ThemeManager.theme["CTkButton"]["hover_color"])
        self.main_themes.place(relx=0.5, rely=0.1, relheight=0.5)
        for theme in MAIN_THEMES.values():
            self.main_themes.insert("END", theme)
        self.main_themes.select(list(MAIN_THEMES.keys())[list(MAIN_THEMES.values()).index(self.MainWindow.settings["main_theme"].title())])

        ctk.CTkLabel(self, text="Custom Format:").place(relx=0.5, rely=0.635)
        self.custom_format = ctk.StringVar(value=self.MainWindow.settings["custom_format"])
        cust_form_entry = ctk.CTkEntry(self, textvariable=self.custom_format, width=450)
        cust_form_entry.place(relx=0.5, rely=0.7)
        entry_keybinds_normalize(cust_form_entry)

        ctk.CTkButton(self, text="Read more about custom formats", font=ctk.CTkFont(family="Arial", size=15), corner_radius=15,
                      command=lambda: webbrowser.open("https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#format-selection"),
                      width=160, height=20).place(relx=0.7, rely=0.8)

        self.MainWindow.all_children.append(self)

        ctk.CTkButton(self, text="Apply (with auto save)", font=ctk.CTkFont(family="Arial", size=15), corner_radius=15,
                      command=self.apply_preferences, width=160, height=35).place(relx=0.01, rely=0.9)
        ctk.CTkButton(self, text="Apply default settings", font=ctk.CTkFont(family="Arial", size=15), corner_radius=15,
                      command=lambda: self.apply_preferences(True), width=180, height=35).place(relx=0.2, rely=0.9)
        ctk.CTkButton(self, text="Apply previous settings", font=ctk.CTkFont(family="Arial", size=15), corner_radius=15,
                      command=self.apply_previous_preferences, width=160, height=35).place(relx=0.39, rely=0.9)

        self.protocol("WM_DELETE_WINDOW", lambda: window_close(self.MainWindow, self))

        self.after(100, self.focus_set)

    def apply_preferences(self, default=False):
        settings_save(self.MainWindow, FILES.get("previous_settings_file"))
        if not default:
            self.MainWindow.settings["notifications"] = self.notifications.get()
            if self.MainWindow.settings["main_theme"].title() != self.main_themes.get():
                CTkMessagebox(title=f"{APP_NAME} (changing main theme)", icon="warning",
                              message=f"To apply main theme. Restart the {APP_NAME}.")
                self.MainWindow.settings["main_theme"] = self.main_themes.get()
            self.MainWindow.settings["auto_load"] = self.auto_load.get()
            self.MainWindow.settings["auto_save"] = self.auto_save.get()
            self.MainWindow.settings["queue_auto_load"] = self.queue_auto_load.get()
            self.MainWindow.settings["queue_auto_save"] = self.queue_auto_save.get()
            self.MainWindow.settings["link_auto_remove"] = self.link_auto_remove.get()
            self.MainWindow.settings["discord_rpc"] = self.discord_rpc.get()
            self.MainWindow.settings["custom_format"] = self.custom_format.get()
            if self.discord_rpc.get() == "Enabled":
                self.MainWindow.rpc.rpc_connect()
            else:
                self.MainWindow.rpc.rpc_close()
            if self.MainWindow.settings["auto_save"] == "Enabled":
                settings_save(self.MainWindow, FILES.get("settings_file"))
        else:
            self.MainWindow.settings = DEFAULT_SETTINGS.copy()
            self.set_vars()
        ctk.set_appearance_mode(self.theme_var.get())
        ctk.set_default_color_theme(resource_path(f'assets/themes/{self.main_themes.get().lower()}.json'))
        self.after(50, self.focus_set)

    def apply_previous_preferences(self):
        settings_load(self.MainWindow, FILES.get("previous_settings_file"), set_vars=True)
        if self.MainWindow.settings["discord_rpc"] == "Enabled":
            self.MainWindow.rpc.rpc_connect()
        else:
            self.MainWindow.rpc.rpc_close()

    def set_vars(self):
        self.auto_load.set(self.MainWindow.settings['auto_load'])
        self.auto_save.set(self.MainWindow.settings['auto_save'])
        self.queue_auto_load.set(self.MainWindow.settings['queue_auto_load'])
        self.queue_auto_save.set(self.MainWindow.settings['queue_auto_save'])
        self.link_auto_remove.set(self.MainWindow.settings['link_auto_remove'])
        self.discord_rpc.set(self.MainWindow.settings["discord_rpc"])
        self.custom_format.set(self.MainWindow.settings["custom_format"])
        self.notifications.set(self.MainWindow.settings['notifications'])
        self.theme_var.set(self.MainWindow.settings['theme'])
        self.main_themes.select(list(MAIN_THEMES.keys())[list(MAIN_THEMES.values()).index(self.MainWindow.settings["main_theme"].title())])
