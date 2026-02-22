import os
from customtkinter import filedialog
import customtkinter as ctk
import pyperclip
from CTkMenuBarPlus import _register_accelerator
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


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

__all__ = ["select_folder", "select_cookies_file", "resource_path",
           "entry_copy", "entry_cut", "entry_keybinds_normalize"]
