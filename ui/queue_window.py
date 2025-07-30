import customtkinter as ctk
from utils.variables import ICON_PATH
from utils.helpers import resource_path


class QueueWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.title("Queue")
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self.after(300, lambda: self.iconbitmap(resource_path(ICON_PATH)))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self, state="disabled")
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
