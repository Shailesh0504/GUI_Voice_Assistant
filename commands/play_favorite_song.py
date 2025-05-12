import os
import random
import subprocess
from core.registry import register_command

# Globals to track current state
song_index = -1
songs_list = []


@register_command("play favorite song")
def play_favorite_song(params=None):
    """
    Plays a random song from the user's Videos/Favorite directory on Windows.
    Creates the folder if missing and provides helpful guidance.
    """
    global song_index, songs_list

    try:
        fav_folder = get_favorite_folder()

        if not os.path.exists(fav_folder):
            os.makedirs(fav_folder, exist_ok=True)
            open_folder(fav_folder)
            return (
                f"📁 Folder created: {fav_folder}\n"
                "🎵 Please add some .mp3 or video files to enjoy your music."
            )

        songs_list = get_song_files(fav_folder)

        if not songs_list:
            open_folder(fav_folder)
            return (
                f"📂 The folder '{fav_folder}' is empty.\n"
                "➕ Add some .mp3 or .mp4 files to get started."
            )

        # Choose a random song that isn't the same as last one (if possible)
        available_indexes = list(range(len(songs_list)))
        if song_index in available_indexes and len(songs_list) > 1:
            available_indexes.remove(song_index)

        song_index = random.choice(available_indexes) if available_indexes else 0
        return play_selected_song(fav_folder, songs_list[song_index])

    except Exception as e:
        return f"❌ Error while playing favorite song.\nDetails: {e}"


@register_command("next song")
def play_next_favorite_song(params=None):
    """
    Plays the next song in the list. Wraps around to start if at the end.
    """
    global song_index, songs_list

    try:
        if not songs_list:
            return "❗ No songs loaded. Please say 'play favorite song' first."

        fav_folder = get_favorite_folder()

        song_index = (song_index + 1) % len(songs_list)
        return play_selected_song(fav_folder, songs_list[song_index])

    except Exception as e:
        return f"❌ Couldn't play the next song.\nDetails: {e}"


@register_command("repeat song")
def repeat_current_song(params=None):
    """
    Repeats the last played song.
    """
    global song_index, songs_list

    try:
        if not songs_list or song_index == -1:
            return "❗ No song has been played yet. Please say 'play favorite song' first."

        fav_folder = get_favorite_folder()
        return play_selected_song(fav_folder, songs_list[song_index])

    except Exception as e:
        return f"❌ Couldn't repeat the song.\nDetails: {e}"


# -------------------- Helpers -------------------- #

def get_favorite_folder():
    return os.path.join(os.path.expandvars("%USERPROFILE%"), "Videos", "Favorite")

def get_song_files(folder):
    return [
        f for f in os.listdir(folder)
        if f.lower().endswith((".mp3", ".wav", ".mp4", ".m4a", ".avi", ".mkv"))
    ]

def play_selected_song(folder, filename):
    try:
        song_path = os.path.join(folder, filename)
        os.startfile(song_path)  # Windows-only
        return f"🎶 Playing: {filename}"
    except Exception as e:
        return f"❌ Failed to play {filename}.\nDetails: {e}"

def open_folder(path):
    try:
        os.startfile(path)
    except Exception as e:
        print(f"⚠️ Could not open folder: {e}")
