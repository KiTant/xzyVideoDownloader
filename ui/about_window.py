import customtkinter as ctk
from utils.helpers import resource_path
from utils.ui_manager import window_close
from utils.variables import VERSION, APP_NAME, ICON_PATH
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


class AboutWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: "MainWindowClass"):
        super().__init__()
        self.MainWindow = MainWindow

        self.title("About")
        self.geometry("500x200")
        self.after(300, lambda: self.iconbitmap(resource_path(ICON_PATH)))
        self.resizable(False, False)

        about_text = f"{APP_NAME}\nVersion {VERSION}" \
                     f"\nApplication that allows you to easily download videos from the internet. \n" \
                     f"Simply paste a video link, and the program will save it to your device."
        ctk.CTkLabel(self, text=about_text, justify="center").pack(expand=True)
        MainWindow.all_children.append(self)
        self.protocol("WM_DELETE_WINDOW", lambda: window_close(self.MainWindow, self))

        self.after(100, self.focus_set)
