from CTkMessagebox import CTkMessagebox
import requests
from utils.variables import VERSION, APP_NAME, REPO_NAME
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def stop_update(MainWindow: "MainWindowClass", title, message, icon):
    CTkMessagebox(title=title, message=message, icon=icon)
    MainWindow.updating = False


def download_last_release(MainWindow: "MainWindowClass", version: str, asset_name: str):
    msg = CTkMessagebox(title=f"{APP_NAME} (updating)",
                        message=f"Update of {APP_NAME} is started, please wait...",
                        icon="info")
    response = requests.get(f'https://github.com/KiTant/{REPO_NAME}/releases/download/{version}/{asset_name}')
    msg.destroy()
    if response.ok:
        try:
            with open(f"{APP_NAME}{version}.exe", "wb") as file:
                file.write(response.content)
            stop_update(MainWindow, title=f"{APP_NAME} (updating)", icon="check",
                        message="New update successfully installed as new file"
                                " in directory where storages this version."
                                "You can delete this version and open new.")
        except:
            stop_update(MainWindow, title=f"{APP_NAME} (downloading update)", icon="cancel",
                        message="Unexpected error while creating new file with update.")
    else:
        stop_update(MainWindow, title=f"{APP_NAME} (downloading update)", icon="cancel",
                    message="Unexpected error while trying to get last release, please check your internet.")


def check_last_version(MainWindow: "MainWindowClass"):
    for window in MainWindow.all_children:
        if window.title() == f"{APP_NAME} (checking updates)" or MainWindow.updating:
            return
    MainWindow.updating = True
    msg = CTkMessagebox(title=f"{APP_NAME} (checking updates)",
                        message="Trying to check updates please wait...",
                        icon="info")
    response = requests.get(f"https://api.github.com/repos/KiTant/{REPO_NAME}/releases/latest")
    msg.destroy()
    if response.ok:
        latest_release = response.json()
        if VERSION < latest_release['tag_name'][1:]:
            msg = CTkMessagebox(title=f"{APP_NAME} (checking updates)",
                                message="Your version is outdated, do you want to update?",
                                icon="info", options=["Yes", "No"], topmost=False)
            if msg.get() in ["Yes"]:
                found_file = False
                if not latest_release['assets']:
                    MainWindow.updating = False
                    return
                for asset in latest_release['assets']:
                    if asset['name'].strip().startswith(f"{APP_NAME}") and asset['name'].strip().endswith(".exe"):
                        found_file = True
                        download_last_release(MainWindow, latest_release['tag_name'], asset['name'])
                if not found_file:
                    stop_update(MainWindow, title=f"{APP_NAME} (updating)", icon="info",
                                message=f"Not found main file of {APP_NAME}, update stopped.")
        else:
            stop_update(MainWindow, title=f"{APP_NAME} (checking updates)", icon="info",
                        message=f"You have latest release of {APP_NAME}")
    else:
        stop_update(MainWindow, title=f"{APP_NAME} (checking updates)", icon="cancel",
                    message="Unexpected error while trying to get last release, please check your internet.")
