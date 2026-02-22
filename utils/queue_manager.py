import queue
import threading
import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def add_to_queue(MainWindow: "MainWindowClass", given_url: str = None):
    from utils.notify_manager import notification

    url = given_url if given_url else MainWindow.url_var.get()
    if url:
        MainWindow.download_queue.put(url)
        with MainWindow.display_lock:
            MainWindow.queue_for_display.append(url)
        update_queue_display(MainWindow)
        if not given_url:
            if MainWindow.settings["link_auto_remove"] == "Enabled":
                MainWindow.url_var.set("")
            notification(MainWindow, {"status": "BaseT", "text": "URL added to the queue",
                                           "color": "green"})
        else:
            notification(MainWindow, {"status": "BaseT", "text": "Loaded queue from previous session",
                                           "color": "green"})
    else:
        notification(MainWindow, {"status": "Base", "text": "Error: Please enter a video URL.",
                                       "color": "red", "icon": "cancel"})


def clear_queue(MainWindow: "MainWindowClass"):
    from utils.notify_manager import notification

    if not MainWindow.is_processing_queue:
        with MainWindow.download_queue.mutex:
            MainWindow.download_queue.queue.clear()
        with MainWindow.display_lock:
            MainWindow.queue_for_display.clear()
        update_queue_display(MainWindow)
        notification(MainWindow, {"status": "BaseT", "text": "Queue cleared", "icon": "check",
                                       "color": "green"})


def update_queue_display(MainWindow: "MainWindowClass"):
    MainWindow.queue_window.textbox.configure(state="normal")
    MainWindow.queue_window.textbox.delete("0.0", "end")
    with MainWindow.display_lock:
        if MainWindow.queue_for_display:
            urls = "\n".join(MainWindow.queue_for_display)
            MainWindow.queue_window.textbox.insert("0.0", urls)
    MainWindow.queue_window.textbox.configure(state="disabled")


def start_queue_processing(MainWindow: "MainWindowClass"):
    from utils.notify_manager import notification

    if MainWindow.is_processing_queue:
        notification(MainWindow, {"status": "Base", "text": "Error: Queue download in process.",
                                       "color": "red", "icon": "cancel"})
        return
    if MainWindow.download_queue.empty():
        notification(MainWindow, {"status": "Base", "text": "Error: Queue is empty.",
                                       "color": "red", "icon": "cancel"})
        return

    MainWindow.stop_download_flag = False
    MainWindow.is_processing_queue = True
    MainWindow.rpc.rpc_update(state=f"Downloading queue... ( {MainWindow.download_queue.qsize()} video(s) )")
    MainWindow.download_thread = threading.Thread(target=lambda: process_queue(MainWindow), daemon=True)
    MainWindow.download_thread.start()

    MainWindow.download_button.configure(state="disabled")
    MainWindow.add_to_queue_button.configure(state="disabled")
    MainWindow.clear_queue_button.configure(state="disabled")
    MainWindow.stop_button.configure(state="normal")


def process_queue(MainWindow: "MainWindowClass"):
    from utils.notify_manager import notification
    from utils.download_manager import download_video

    while not MainWindow.stop_download_flag:
        try:
            url = MainWindow.download_queue.get(block=False)
        except queue.Empty:
            break

        with MainWindow.display_lock:
            if MainWindow.queue_for_display:
                MainWindow.queue_for_display.pop(0)
        MainWindow.after(0, lambda: update_queue_display(MainWindow))

        download_video(MainWindow, url=url, queue_enabled=True)

        if MainWindow.stop_download_flag:
            temp_q = queue.Queue()
            temp_q.put(url)
            while not MainWindow.download_queue.empty():
                temp_q.put(MainWindow.download_queue.get())
            MainWindow.download_queue = temp_q
            with MainWindow.display_lock:
                MainWindow.queue_for_display.insert(0, url)
            MainWindow.after(0, lambda: update_queue_display(MainWindow))
            break

        if not MainWindow.download_queue.empty() and not MainWindow.stop_download_flag:
            MainWindow.after(0, lambda: notification(MainWindow, {"status": "DownloadingUpdate",
                                                          "text": "Pause for 5 seconds...", "color": "blue"}))
            time.sleep(5)

    MainWindow.after(0, lambda: queue_finished(MainWindow))


def queue_finished(MainWindow: "MainWindowClass"):
    from utils.notify_manager import notification

    MainWindow.is_processing_queue = False
    MainWindow.download_button.configure(state="normal")
    MainWindow.add_to_queue_button.configure(state="normal")
    MainWindow.clear_queue_button.configure(state="normal")
    MainWindow.stop_button.configure(state="disabled")

    if MainWindow.stop_download_flag:
        notification(MainWindow, {"status": "DownloadingUpdate",
                                       "text": "Download stopped (unavailable-fragments)",
                                       "color": "red"})
        MainWindow.rpc.rpc_update(state=f"Just chillin (🔴)")
    else:
        notification(MainWindow, {"status": "DownloadingUpdate",
                                       "text": "Queue download completed successfully!",
                                       "color": "green", "value": 100, "icon": "check"})
        MainWindow.progress_bar.set(0)
        MainWindow.rpc.rpc_update(state=f"Just chillin (🟢)")

__all__ = ["add_to_queue", "clear_queue", "start_queue_processing"]
