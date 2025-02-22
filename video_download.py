import os
import re
import tkinter as tk
from tkinter import messagebox
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# 清理標題中的特殊字符
def sanitize_title(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)  # 移除文件名中不合法的字符

# 下載函數
def download_with_retry(url, retries=3):
    attempt = 0
    # 提前提取影片信息獲得標題並清理
    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = sanitize_title(info.get('title', 'unknown_title'))  # 清理標題

    # 設定資料夾名稱
    folder_name = video_title
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # 修改下載選項
    ydl_opts_download = {
        'writethumbnail': True,
        'outtmpl': os.path.join(folder_name, '%(title)s.%(ext)s'),  # 存儲到新資料夾中
        'download_archive': 'downloaded_videos2.ext'
    }

    ydl_opts_thumbnail_only = {
        'writethumbnail': True,
        'skip_download': True,
        'outtmpl': os.path.join(folder_name, '%(title)s.%(ext)s')  # 存儲到新資料夾中
    }

    while attempt < retries:
        try:
            with YoutubeDL(ydl_opts_download) as ydl:
                ydl.download([url])
                print(f"影片已下載到資料夾: {folder_name}")

                # 嘗試只下載封面圖
                with YoutubeDL(ydl_opts_thumbnail_only) as ydl_thumb:
                    ydl_thumb.download([url])
            break
        except DownloadError as e:
            print(f"下載錯誤：{e}; 在重試...")
            attempt += 1
            if attempt == retries:
                print("重試次數達上限，停止嘗試。")
                messagebox.showerror("下載失敗", "下載嘗試次數達到上限，請稍後重試。")

# 創建GUI
def start_download():
    url = url_entry.get()
    if url:
        download_with_retry(url)
        messagebox.showinfo("下載完成", "影片及封面下載完成！")
    else:
        messagebox.showwarning("錯誤", "請輸入影片網址。")

# 設定Tkinter主窗口
root = tk.Tk()
root.title("影片下載器")

# 標籤和輸入框
tk.Label(root, text="請輸入影片網址:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=10)

# 下載按鈕
download_button = tk.Button(root, text="開始下載", command=start_download)
download_button.pack(pady=20)

# 運行GUI應用程式
root.mainloop()
