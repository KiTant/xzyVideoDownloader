import os
import queue
from customtkinter import filedialog
import customtkinter as ctk
import pyperclip
from CTkMenuBarPlus import _register_accelerator
from utils.ui_manager import *
from utils.settings_manager import *
from utils.download_manager import *
from utils.notify_manager import *
from utils.queue_manager import *
from utils.updater import check_last_version
from utils.variables import DEFAULT_SETTINGS
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def make_notification(MainWindow: "MainWindowClass", notifyParams: dict):
    notification(MainWindow, notifyParams)


def progress_hook(MainWindow: "MainWindowClass", d):
    d_progress_hook(MainWindow, d)


def select_folder(MainWindow: "MainWindowClass"):
    MainWindow.menu.hide()
    folder_path = filedialog.askdirectory()
    if folder_path and os.path.exists(folder_path):
        MainWindow.save_path_var.set(folder_path)
    MainWindow.menu.show()


def select_cookies_file(MainWindow: "MainWindowClass"):
    MainWindow.menu.hide()
    file_path = filedialog.askopenfilename()
    if file_path and os.path.exists(file_path):
        MainWindow.cookies_file_path_var.set(file_path)
    MainWindow.menu.show()


def start_download_thread(MainWindow: "MainWindowClass"):
    d_start_download_thread(MainWindow)


def download_video(MainWindow: "MainWindowClass", url: str = None, queue_enabled: bool = False):
    d_download_video(MainWindow, url, queue_enabled)


def stop_download(MainWindow: "MainWindowClass"):
    d_stop_download(MainWindow)


def save_settings(MainWindow: "MainWindowClass", file, values: dict = None, queue_obj: queue.Queue = None):
    s_save(MainWindow, file, values, queue_obj)


def load_settings(MainWindow: "MainWindowClass", file, auto_load: bool = False, set_vars: bool = False,
                  default_values: dict = DEFAULT_SETTINGS, attr_name: str = "settings"):
    s_load(MainWindow, file, auto_load, set_vars, default_values, attr_name)


def show_soon():
    w_show_soon()


def show_about(MainWindow: "MainWindowClass"):
    w_show_about(MainWindow)


def show_preferences(MainWindow: "MainWindowClass"):
    w_show_preferences(MainWindow)


def close_window(MainWindow: "MainWindowClass", Window: Union["MainWindowClass", ctk.CTkToplevel]):
    w_close(MainWindow, Window)


def check_updates(MainWindow: "MainWindowClass"):
    check_last_version(MainWindow)


def add_to_queue(MainWindow: "MainWindowClass", url: str = None):
    q_add_to_queue(MainWindow, url)


def clear_queue(MainWindow: "MainWindowClass"):
    q_clear_queue(MainWindow)


def start_queue_processing(MainWindow: "MainWindowClass"):
    q_start_queue_processing(MainWindow)


def resource_path(file):
    data_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(data_dir, file)


def entry_paste(entry: ctk.CTkEntry):
    try:
        try:
            entry.delete(ctk.SEL_FIRST, ctk.SEL_LAST)
        finally:
            entry.insert(ctk.INSERT, pyperclip.paste())
    except:
        return


def entry_copy(entry: ctk.CTkEntry):
    try:
        pyperclip.copy(entry.get()[entry.index(ctk.SEL_FIRST):entry.index(ctk.SEL_LAST)])
    except:
        return


def entry_cut(entry: ctk.CTkEntry):
    try:
        entry_copy(entry)
        entry.delete(ctk.SEL_FIRST, ctk.SEL_LAST)
    except:
        return


def entry_keybinds_normalize(entry: ctk.CTkEntry):
    _register_accelerator(entry, "Ctrl+C", lambda: entry_copy(entry), bind_scope='widget')
    _register_accelerator(entry, "Ctrl+V", lambda: entry_paste(entry), bind_scope='widget')
    _register_accelerator(entry, "Ctrl+X", lambda: entry_cut(entry), bind_scope='widget')
    _register_accelerator(entry, "Esc", entry.master.focus)
    _register_accelerator(entry, "Return", entry.master.focus)

__all__ = ["make_notification", "progress_hook", "select_folder", "start_download_thread", "download_video",
           "stop_download", "save_settings", "load_settings", "show_soon", "show_about", "select_cookies_file",
           "show_preferences", "check_updates", "close_window", "add_to_queue", "clear_queue", "start_queue_processing",
           "resource_path", "entry_copy", "entry_cut", "entry_keybinds_normalize"]
