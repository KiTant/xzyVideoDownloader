import queue
import customtkinter as ctk
import os
import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def s_apply(MainWindow: "MainWindowClass"):
    from utils.helpers import resource_path
    ctk.set_appearance_mode(MainWindow.settings['theme'])
    ctk.set_default_color_theme(resource_path(f'assets/themes/{MainWindow.settings["main_theme"].lower()}.json'))


def s_change_new_keys(settings, default_values: dict):
    for key in list(default_values.keys()):
        if key not in list(settings.keys()):
            settings[key] = default_values[key]
    for key in list(settings.keys()):
        if key not in list(default_values.keys()):
            settings[key] = None
    return settings


def s_save(MainWindow: "MainWindowClass", file, values: dict, queue_obj: queue.Queue):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w', encoding='utf-8') as f:
        if queue_obj:
            with queue_obj.mutex:
                values = list(queue_obj.queue)
        if (queue_obj and values) or not queue_obj:
            json.dump(values if values else MainWindow.settings, f, indent=4, ensure_ascii=False)
        f.close()


def s_load(MainWindow: "MainWindowClass", file, auto_load: bool, set_vars: bool,
           default_values: dict, attr_name: str):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            if default_values:
                data = s_change_new_keys(json.load(f), default_values)
            else:
                try:
                    from utils.helpers import add_to_queue
                    data = json.load(f)
                    for item in data:
                        add_to_queue(MainWindow, item)
                except json.JSONDecodeError:
                    pass
                data = None
            if ((auto_load and data['auto_load'] == "Enabled") or (not auto_load)) and data:
                setattr(MainWindow, attr_name, data)
                if set_vars:
                    for window in MainWindow.all_children:
                        if window.title() in ["Preferences"]:
                            window.set_vars()
                s_apply(MainWindow)
            f.close()
    else:
        s_apply(MainWindow)

__all__ = ["s_save", "s_load"]
