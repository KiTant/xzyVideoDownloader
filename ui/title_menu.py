from CTkMenuBar import *
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager
from utils.helpers import *
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
        self.Settings_Dropdown.add_option(option="Preferences", command=lambda: show_preferences(MainWindow))

        self.Settings_Dropdown.add_option(option="Save settings",
                                          command=lambda: save_settings(MainWindow,
                                                                        MainWindow.files.get("settings_file")))
        self.Settings_Dropdown.add_option(option="Load settings",
                                          command=lambda:
                                          load_settings(MainWindow, MainWindow.files.get("settings_file"),
                                                        set_vars=True))

        self.Settings_Dropdown.add_option(option="Save queue",
                                          command=lambda: save_settings(MainWindow,
                                                                        MainWindow.files.get("queue_file"),
                                                                        queue_obj=MainWindow.download_queue))
        self.Settings_Dropdown.add_option(option="Load queue",
                                          command=lambda:
                                          load_settings(MainWindow, MainWindow.files.get("queue_file"),
                                                        default_values={}, attr_name="download_queue"))

        self.Settings_Dropdown.add_option(option="Check updates", command=lambda: check_updates(MainWindow))

        self.after(100, self.change_dimension)
