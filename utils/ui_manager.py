from CTkMessagebox import CTkMessagebox
from typing import TYPE_CHECKING, Union
from utils.variables import APP_NAME
import customtkinter as ctk
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def w_show(MainWindow: "MainWindowClass", names: list, func):
    for window in MainWindow.all_children:
        if window.title() in names:
            window.focus_set()
            return
    func()


def w_close(MainWindow: "MainWindowClass", Window: Union["MainWindowClass", ctk.CTkToplevel]):
    MainWindow.all_children.remove(Window)
    Window.destroy()


def w_show_soon():
    CTkMessagebox(title=APP_NAME, message="This option will be soon.", icon="info")


def w_show_preferences(MainWindow: "MainWindowClass"):
    from ui.preferences_window import PreferencesWindow
    w_show(MainWindow, ["Preferences"], lambda: PreferencesWindow(MainWindow))


def w_show_about(MainWindow: "MainWindowClass"):
    from ui.about_window import AboutWindow
    w_show(MainWindow, ["About"], lambda: AboutWindow(MainWindow))

__all__ = ["w_close", "w_show_soon", "w_show_preferences", "w_show_about"]
