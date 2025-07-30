from win11toast import notify, update_progress
from CTkMessagebox import CTkMessagebox
from utils.variables import APP_NAME, ICON_PATH
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def notification(MainWindow: "MainWindowClass", notifyParams: dict):
    MainWindow.update_status(notifyParams["text"], text_color=notifyParams["color"])

    if MainWindow.settings["notifications"].endswith("MessageBox") and notifyParams.get("icon"):
        CTkMessagebox(title=APP_NAME, message=notifyParams["text"], icon=notifyParams["icon"],
                      topmost=False)

    elif MainWindow.settings["notifications"].endswith("WindowsNotification"):
        from utils.helpers import resource_path

        if notifyParams["status"] == "Base":
            notify(title=f"{APP_NAME} notification", body=notifyParams["text"],
                   icon={'src': resource_path(ICON_PATH),
                         'placement': 'appLogoOverride'})

        elif notifyParams["status"] == "Downloading":
            notify(title=f"{APP_NAME} notification",
                   icon={'src': resource_path(ICON_PATH),
                         'placement': 'appLogoOverride'},
                   progress={
                       'title': notifyParams["link"],
                       'status': notifyParams["text"],
                       'value': 0,
                       'valueStringOverride': '0 / 100 %'
                   })

        elif notifyParams["status"] == "DownloadingUpdate":
            if notifyParams.get("value"):
                update_progress(progress={'value': float(notifyParams["value"])/100,
                                          'status': notifyParams.get("notify_text") or notifyParams["text"],
                                          'valueStringOverride': f'{notifyParams["value"]} / 100 %'})
            else:
                update_progress(progress={'status': notifyParams.get("notify_text") or notifyParams["text"]})

__all__ = ["notification"]
