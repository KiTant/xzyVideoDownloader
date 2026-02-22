from CTkMessagebox import CTkMessagebox
from typing import TYPE_CHECKING, Union
from utils.variables import APP_NAME
import customtkinter as ctk
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def window_show(MainWindow: "MainWindowClass", names: list, func):
    for window in MainWindow.all_children:
        if window.title() in names:
            window.focus_set()
            return
    func()


def window_close(MainWindow: "MainWindowClass", Window: Union["MainWindowClass", ctk.CTkToplevel]):
    MainWindow.all_children.remove(Window)
    Window.destroy()


def show_soon():
    CTkMessagebox(title=APP_NAME, message="This option will be soon.", icon="info")


def show_preferences(MainWindow: "MainWindowClass"):
    from ui.preferences_window import PreferencesWindow
    window_show(MainWindow, ["Preferences"], lambda: PreferencesWindow(MainWindow))


def show_about(MainWindow: "MainWindowClass"):
    from ui.about_window import AboutWindow
    window_show(MainWindow, ["About"], lambda: AboutWindow(MainWindow))

__all__ = ["window_close", "show_soon", "show_preferences", "show_about"]
