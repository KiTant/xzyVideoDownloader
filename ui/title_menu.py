from CTkMenuBarPlus import *
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager
from utils.settings_manager import *
from utils.ui_manager import show_about, show_preferences
from utils.updater import check_last_version
from utils.variables import FILES
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


class TitleMenu(CTkTitleMenu):
    def __init__(self, MainWindow: "MainWindowClass"):
        super().__init__(master=MainWindow, x_offset=200)

        self.Settings_Button = self.add_cascade("Settings")
        self.About_Button = self.add_cascade("About", command=lambda: show_about(MainWindow))

        self.Settings_Dropdown = CustomDropdownMenu(widget=self.Settings_Button,
                                                    hover_color=ThemeManager.theme["CTkButton"]["fg_color"])

        self.Settings_Dropdown.add_option(option="Preferences", command=lambda: show_preferences(MainWindow),
                                          accelerator="CmdOrCtrl+P")

        self.Settings_Submenu = self.Settings_Dropdown.add_submenu(submenu_name=f"Settings {' '*27}>")

        self.Settings_Submenu.add_option(option="Save settings",
                                         command=lambda: settings_save(MainWindow, FILES.get("settings_file")))

        self.Settings_Submenu.add_option(option="Load settings",
                                         command=lambda: settings_load(MainWindow, FILES.get("settings_file"), set_vars=True))

        self.Queue_Submenu = self.Settings_Dropdown.add_submenu(submenu_name=f"Queue {' '*30}>")

        self.Queue_Submenu.add_option(option="Save queue",
                                      command=lambda: settings_save(MainWindow, FILES.get("queue_file"), queue_obj=MainWindow.download_queue))
        self.Queue_Submenu.add_option(option="Load queue",
                                      command=lambda: settings_load(MainWindow, FILES.get("queue_file"), default_values={}, attr_name="download_queue"))

        self.Settings_Dropdown.add_option(option="Check updates", command=lambda: check_last_version(MainWindow), accelerator="CmdOrCtrl+U")

        self.after(100, self.change_dimension)
