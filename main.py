import customtkinter as ctk
import os
from ui.main_window import MainWindow
from utils.variables import APP_NAME


def resource_path(file):
    data_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(data_dir, file)

appdata_dir = os.getenv('APPDATA')
files = {"settings_file": os.path.join(appdata_dir, APP_NAME, 'settings.json'),
         "previous_settings_file": os.path.join(appdata_dir, APP_NAME, 'previous_settings.json'),
         "special_settings_file": os.path.join(appdata_dir, APP_NAME, 'special_settings.json')}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(resource_path('assets/themes/carrot.json'))

if __name__ == '__main__':
    app = MainWindow(resource_path=resource_path, files=files)
    app.mainloop()
