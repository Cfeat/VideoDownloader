from yt_dlp import YoutubeDL
import os
from tkinter import filedialog
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading

def choose():
    folder = filedialog.askdirectory(title="请选择下载保存的目录")
    if not folder:
        folder = os.getcwd()
    return folder

def download(url: str, dir: str, tmplt: str = "%(title)s.%(ext)s", progress_callback=None):
    output = os.path.join(dir, tmplt)

    def hook(d):
        if d['status'] == 'downloading' and progress_callback:
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes:
                percent = int(downloaded_bytes / total_bytes * 100)
                progress_callback(percent)

    opt = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output,
        'noplaylist': True,
        'progress_hooks': [hook]
    }
    with YoutubeDL(opt) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', None)
        print(f"Downloaded: {title}")

def run():
    def select():
        folder = choose()
        download_path.set(folder)

    def update_progress(val):
        progress["value"] = val
        progress_label.config(text=f"{val}%")

    def start():
        video_url = url.get().strip()
        folder = download_path.get()
        status.config(text="正在下载...", bootstyle="info")
        progress["value"] = 0
        progress_label.config(text="0%")

        if not video_url:
            status.config(text="请输入视频链接", bootstyle="danger")
            return
        if not folder:
            status.config(text="请选择下载目录", bootstyle="danger")
            return

        def thread_task(video_url, folder_path):
            try:
                download(video_url, folder_path, progress_callback=update_progress)
                status.config(text="下载完成", bootstyle="success")
            except Exception as e:
                status.config(text=f"下载失败: {e}", bootstyle="danger")

        threading.Thread(target=thread_task, args=(video_url, folder)).start()
        
    app = ttk.Window(themename="flatly")
    app.title("视频下载器")
    app.geometry("900x600")
    app.resizable(False, False)

    try:
        app.iconbitmap("icon.ico")
    except Exception:
        print("未找到 icon.ico，跳过设置图标。")

    global url, download_path
    url = tk.StringVar()
    download_path = tk.StringVar()

    ttk.Label(app, text="🎬 视频链接:", font=("微软雅黑", 15)).pack(pady=(60, 5))
    ttk.Entry(app, textvariable=url, width=80).pack()

    ttk.Label(app, text="📁 下载目录:", font=("微软雅黑", 15)).pack(pady=(50, 5))
    frame = ttk.Frame(app)
    frame.pack()
    ttk.Entry(frame, textvariable=download_path, width=60).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(frame, text="浏览", command=select, bootstyle='secondary').pack(side=tk.LEFT)

    ttk.Button(app, text="开始下载", command=start, bootstyle='primary').pack(pady=70)

    progress = ttk.Progressbar(app, orient="horizontal", length=400, mode="determinate")
    progress.pack(pady=(10, 0))
    progress_label = ttk.Label(app, text="0%", font=("微软雅黑", 10))
    progress_label.pack()

    global status
    status = ttk.Label(app, text="", font=("微软雅黑", 10))
    status.pack(pady=10)

    app.mainloop()

if __name__ == '__main__':
    run()
