import customtkinter as ctk
import os
import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def s_apply(MainWindow: "MainWindowClass"):
    ctk.set_appearance_mode(MainWindow.settings['theme'])
    ctk.set_default_color_theme(MainWindow.resource_path(f'assets/themes/'
                                                         f'{MainWindow.settings["main_theme"].lower()}.json'))


def s_change_new_keys(settings, default_values: dict):
    for key in list(default_values.keys()):
        if key not in list(settings.keys()):
            settings[key] = default_values[key]
    for key in list(settings.keys()):
        if key not in list(default_values.keys()):
            settings[key] = None
    return settings


def s_save(MainWindow: "MainWindowClass", file, values: dict):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as f:
        json.dump(values if values else MainWindow.settings, f, indent=4)
        f.close()


def s_load(MainWindow: "MainWindowClass", file, auto_load: bool, set_vars: bool,
           default_values: dict, settings_name: str):
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = s_change_new_keys(json.load(f), default_values)
            if (auto_load is True and data['auto_load'] == "Enabled") or (auto_load is False):
                setattr(MainWindow, settings_name, data)
                if set_vars is True:
                    for window in MainWindow.all_children:
                        if window.title() in ["Preferences"]:
                            window.set_vars()
                s_apply(MainWindow)
            f.close()
    else:
        s_apply(MainWindow)

__all__ = ["s_save", "s_load"]
