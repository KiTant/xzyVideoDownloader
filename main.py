import customtkinter as ctk
from ui.main_window import MainWindow
from utils.helpers import resource_path


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(resource_path('assets/themes/carrot.json'))

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
