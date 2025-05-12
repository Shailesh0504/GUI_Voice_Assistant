import tkinter as tk
from tkinter import messagebox, filedialog
from pytubefix import YouTube, Playlist
import threading
import os
from core.registry import register_command
from gui.message_router import show_in_chat

# ------------ Helper: Fix short URLs ------------
def normalize_youtube_url(url):
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

# ------------ Download Logic ------------
def download_video(url, path, status_label, progress_bar, params=None):
    try:
        url = normalize_youtube_url(url)
        yt = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: update_progress_bar(yt, progress_bar, bytes_remaining))
        stream = yt.streams.get_highest_resolution()
        status_label.config(text=f"⬇️ Downloading: {yt.title[:40]}...", fg="blue")
        stream.download(output_path=path)
        progress_bar['value'] = 100
        status_label.config(text=f"✅ Download complete! File saved in:\n📁 {path}", fg="green")
        show_in_chat(f"✅ Download complete! File saved in:\n📁 {path}")
    except Exception as e:
        status_label.config(text=f"❌ Error: {e}", fg="red")


def download_audio(url, path, status_label, progress_bar, params=None):
    try:
        url = normalize_youtube_url(url)
        yt = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: update_progress_bar(yt, progress_bar, bytes_remaining))
        stream = yt.streams.filter(only_audio=True).first()
        status_label.config(text=f"🎧 Downloading Audio: {yt.title[:40]}...", fg="blue")
        out_file = stream.download(output_path=path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        progress_bar['value'] = 100
        status_label.config(text=f"✅ MP3 Saved successfully in:\n📁 {path}", fg="green")
    except Exception as e:
        status_label.config(text=f"❌ Error: {e}", fg="red")


def download_playlist(url, path, status_label, progress_bar, params=None):
    try:
        url = normalize_youtube_url(url)
        pl = Playlist(url)
        status_label.config(text=f"🎞 Downloading Playlist: {pl.title}", fg="blue")
        for video in pl.videos:
            video.streams.get_highest_resolution().download(output_path=path)
        progress_bar['value'] = 100
        status_label.config(text=f"✅ Playlist downloaded successfully in:\n📁 {path}", fg="green")
    except Exception as e:
        status_label.config(text=f"❌ Error: {e}", fg="red")


def update_progress_bar(yt, progress_bar, bytes_remaining):
    total_size = yt.streams.get_highest_resolution().filesize
    downloaded = total_size - bytes_remaining
    percent = int((downloaded / total_size) * 100)
    progress_bar['value'] = percent


def start_download(url_entry, status_label, progress_bar, mode):
    url = url_entry.get()
    if not url:
        show_in_chat("Please enter a YouTube video or playlist URL.")
        messagebox.showwarning("Missing URL", "Please enter a YouTube video or playlist URL.")
        return

    path = filedialog.askdirectory()
    if not path:
        return

    if mode == 'video':
        target_func = download_video
    elif mode == 'audio':
        target_func = download_audio
    else:
        target_func = download_playlist

    thread = threading.Thread(
        target=target_func,
        args=(url, path, status_label, progress_bar, None),
        daemon=True
    )
    thread.start()


# ------------ GUI ------------
@register_command("youtube download")
def launch_gui(params=None):
    root = tk.Tk()
    root.title("🎬 YouTube Downloader")
    root.geometry("500x360")
    root.config(bg="#f2f2f2")

    tk.Label(root, text="📺 YouTube URL:", bg="#f2f2f2", font=("Segoe UI", 11)).pack(pady=(20, 5))
    url_entry = tk.Entry(root, width=50, font=("Segoe UI", 10))
    url_entry.pack(pady=(0, 10))

    status_label = tk.Label(root, text="Enter a video or playlist URL above.", bg="#f2f2f2", font=("Segoe UI", 10), fg="gray")
    status_label.pack(pady=5)

    progress_bar = tk.ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=5)

    btn_frame = tk.Frame(root, bg="#f2f2f2")
    btn_frame.pack(pady=10)

    video_btn = tk.Button(
        btn_frame, text="⬇️ Download Video", command=lambda: start_download(url_entry, status_label, progress_bar, mode='video'),
        bg="#007acc", fg="white", font=("Segoe UI", 10), padx=10, pady=5
    )
    video_btn.grid(row=0, column=0, padx=5)

    audio_btn = tk.Button(
        btn_frame, text="🎧 Download MP3", command=lambda: start_download(url_entry, status_label, progress_bar, mode='audio'),
        bg="#6f42c1", fg="white", font=("Segoe UI", 10), padx=10, pady=5
    )
    audio_btn.grid(row=0, column=1, padx=5)

    playlist_btn = tk.Button(
        btn_frame, text="📁 Download Playlist", command=lambda: start_download(url_entry, status_label, progress_bar, mode='playlist'),
        bg="#28a745", fg="white", font=("Segoe UI", 10), padx=10, pady=5
    )
    playlist_btn.grid(row=0, column=2, padx=5)

    # Fix for Progressbar styling
    style = tk.ttk.Style()
    style.theme_use('clam')
    style.configure("TProgressbar", thickness=15, troughcolor='#ddd', background='#4CAF50')

    root.mainloop()