import os.path
import yt_dlp
import threading
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def progress_hook(MainWindow: "MainWindowClass", d):
    from utils.notify_manager import notification

    if MainWindow.stop_download_flag:
        raise yt_dlp.utils.DownloadError("Download stopped")

    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        if total_bytes:
            downloaded_bytes = d.get('downloaded_bytes')
            progress = downloaded_bytes / total_bytes
            MainWindow.after(0, lambda: MainWindow.progress_bar.set(progress))
            MainWindow.after(0, lambda: notification(MainWindow,
                                                          {"status": "DownloadingUpdate",
                                                           "text": f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']}"
                                                           f" at {d['_speed_str']}",
                                                           "notify_text": f"Downloading at {d['_speed_str']}",
                                                           "color": "blue", "value": d['_percent_str'].strip()[:-1]}))

    elif d['status'] == 'finished':
        MainWindow.after(0, lambda: MainWindow.progress_bar.set(1))
        MainWindow.after(0, lambda: notification(MainWindow,
                                                      {"status": "DownloadingUpdate", "text": "Processing...",
                                                       "color": "blue"}))


def start_download_thread(MainWindow: "MainWindowClass"):
    from utils.notify_manager import notification

    url = MainWindow.url_var.get()
    save_path = MainWindow.save_path_var.get()
    if not url:
        notification(MainWindow, {"status": "Base", "text": "Error: Please enter a video URL.",
                                       "color": "red", "icon": "cancel"})
        return
    if not save_path or not os.path.exists(save_path):
        notification(MainWindow, {"status": "Base", "text": "Error: Please select a save folder.",
                                       "color": "red", "icon": "cancel"})
        return

    MainWindow.stop_download_flag = False
    MainWindow.download_thread = threading.Thread(target=lambda: download_video(MainWindow), daemon=True)
    MainWindow.download_thread.start()


def download_video(MainWindow: "MainWindowClass", url: str = None, queue_enabled: bool = False):
    from utils.notify_manager import notification

    url = url if url else MainWindow.url_var.get()
    save_path = MainWindow.save_path_var.get()
    download_type = MainWindow.download_type_var.get()
    quality = MainWindow.quality_var.get()
    use_cookies = MainWindow.use_cookies_var.get()
    cookies_file_path = MainWindow.cookies_file_path_var.get()

    if not queue_enabled:
        MainWindow.rpc.rpc_update(state=f"Downloading video...")

    MainWindow.after(0, lambda: MainWindow.download_button.configure(state="disabled"))
    MainWindow.after(0, lambda: MainWindow.stop_button.configure(state="normal"))
    MainWindow.after(0, lambda: notification(MainWindow, {
                         "link": url, "status": "Downloading", "text": "Starting download...", "color": "blue"}))
    MainWindow.after(0, lambda: MainWindow.progress_bar.set(0))

    try:
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'progress_hooks': [lambda d: progress_hook(MainWindow, d)],
            'noplaylist': True,
            'merge_output_format': 'mp4',
            'abort-on-unavailable-fragments': True,
            'skip_unavailable_fragments': False
        }
        if use_cookies and os.path.exists(cookies_file_path):
            ydl_opts['cookiefile'] = cookies_file_path
        if download_type == "Audio Only (MP3)":
            ydl_opts['format'] = 'bestaudio/best' if quality.startswith("Best") else 'worstaudio/worst'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif download_type == "Video Only":
            if quality.endswith("Best (video)") or quality == "Best (both)":
                ydl_opts['format'] = 'bestvideo[acodec=none]/bestvideo'
            elif quality.endswith("Worst (video)") or quality == "Worst (both)":
                ydl_opts['format'] = 'worstvideo[acodec=none]/worstvideo'
            else:
                resolution = quality[:-1]
                ydl_opts['format'] = f'bestvideo[height<={resolution}][acodec=none]/bestvideo[height<={resolution}]'
        elif download_type == "Custom Format":
            custom_format = MainWindow.settings['custom_format']
            if custom_format.strip():
                ydl_opts['format'] = MainWindow.settings['custom_format']
            else:
                notification(MainWindow, {"status": "Base", "text": "Error: Your custom format is empty.",
                                               "color": "red", "icon": "cancel"})
                return
        else:
            if quality == "Best (both)":
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
            elif quality == "Worst (both)":
                ydl_opts['format'] = 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worstvideo+worstaudio/worst'
            elif quality == "Best (audio); Worst (video)":
                ydl_opts['format'] = 'worstvideo[ext=mp4]+bestaudio[ext=m4a]/worstvideo+bestaudio'
            elif quality == "Worst (audio); Best (video)":
                ydl_opts['format'] = 'bestvideo[ext=mp4]+worstaudio[ext=m4a]/bestvideo+worstaudio'
            else:
                resolution = quality[:-1]
                ydl_opts['format'] = f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]' \
                                     f'/bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not MainWindow.stop_download_flag:
            MainWindow.after(0, lambda: notification(MainWindow, {"status": "DownloadingUpdate",
                                           "text": "Video download completed successfully!",
                                           "color": "green", "value": 100, "icon": "check"}))
            MainWindow.rpc.rpc_update(state=f"Just chillin (🟢)")

    except yt_dlp.utils.DownloadError as e:
        if not MainWindow.stop_download_flag:
            error_message = str(e)
            if "Download stopped" in error_message:
                MainWindow.after(0, lambda: notification(MainWindow, {"status": "DownloadingUpdate",
                                               "text": "Download stopped (unavailable-fragments)", "color": "red"}))
            else:
                if "invalid start byte" in error_message.lower():
                    error_message = "Error when using a cookies file, \n" \
                                    "please check that the file you are using contains cookies"
                elif "search youtube" in error_message.lower():
                    error_message = "It looks like you entered an incorrect link."
                elif "private" in error_message.lower():
                    error_message = "This video is private, maybe with using cookies it can be downloaded"
                MainWindow.after(0, lambda: notification(MainWindow, {"status": "Base",
                                               "text": f"Error: {error_message}",
                                               "color": "red", "icon": "cancel"}))
            MainWindow.rpc.rpc_update(state=f"Just chillin (🔴)")

    except Exception as err:
        if not MainWindow.stop_download_flag:
            MainWindow.after(0, lambda: notification(MainWindow, {"status": "Base",
                                                                       "text": f"An unexpected error occurred: {err}",
                                                                       "color": "red", "icon": "cancel"}))
            MainWindow.rpc.rpc_update(state=f"Just chillin (🔴)")

    finally:
        if MainWindow.stop_download_flag:
            MainWindow.after(0, lambda: notification(MainWindow, {"status": "DownloadingUpdate",
                                                               "text": "Download stopped (unavailable-fragments)",
                                                               "color": "red"}))
            MainWindow.rpc.rpc_update(state=f"Just chillin (🔴)")
        if not queue_enabled:
            MainWindow.after(0, lambda: MainWindow.download_button.configure(state="normal"))
            MainWindow.after(0, lambda: MainWindow.stop_button.configure(state="disabled"))


def stop_download(MainWindow: "MainWindowClass"):
    from utils.notify_manager import notification

    if MainWindow.download_thread and MainWindow.download_thread.is_alive():
        MainWindow.stop_download_flag = True
        notification(MainWindow, {"status": "DownloadingUpdate",
                                       "text": "Stopping download...",
                                       "color": "orange"})
        MainWindow.stop_button.configure(state="disabled")

__all__ = ["progress_hook", "start_download_thread", "download_video", "stop_download"]
