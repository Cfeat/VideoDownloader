from yt_dlp import YoutubeDL
import os
from tkinter import filedialog

def choose():
    folder = filedialog.askdirectory(title="请选择下载保存的目录")
    if not folder:
        folder = os.getcwd()
    return folder

def download(url: str, dir: str, tmplt: str = "%(title)s.%(ext)s"):
    output = os.path.join(dir, tmplt)
    opt = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output,
        'noplaylist': True
    }
    with YoutubeDL(opt) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', None)
        print(f"Downloaded: {title}")

if __name__ == '__main__':
    url = input("请输入要下载的视频链接: ").strip()
    download_dir = choose()
    download(url, download_dir)
