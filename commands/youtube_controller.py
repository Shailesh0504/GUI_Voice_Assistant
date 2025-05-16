import re
import pyautogui
import keyboard
import pygetwindow as gw
from core.registry import register_command
from rapidfuzz import process, fuzz

@register_command("control youtube")
def control_youtube_feature(params):
    """
    Controls YouTube video playback via keyboard shortcuts.
    Checks if a YouTube tab is focused before triggering actions.
    """
    if not params or not params.strip():
        return "🎙️ Please tell me what action to perform on the YouTube video — like pause, mute, or fullscreen."

    action = params.lower().strip()
    action = re.sub(r'[-_]', ' ', action)

    key_map = {
        "play": "space",
        "pause": "space",
        "mute": "m",
        "unmute": "m",
        "fullscreen": "f",
        "exit fullscreen": "f",
        "captions": "c",
        "subtitles": "c",
        "theater": "t",
        "increase volume": "up",
        "decrease volume": "down",
        "volume up": "up",
        "volume down": "down",
        "forward": "right",
        "seek forward": "right",
        "backward": "left",
        "seek backward": "left",
        "skip ad": None
    }

    matched_phrase, score, _ = process.extractOne(
        action, key_map.keys(), scorer=fuzz.partial_ratio
    )

    if score >= 80:
        if not is_youtube_focused():
            return "⚠️ YouTube is not currently in focus.\n👉 Please select the YouTube tab and try again."

        if matched_phrase == "skip ad":
            try:
                screen_width, screen_height = pyautogui.size()
                pyautogui.moveTo(screen_width - 200, screen_height // 2, duration=0.2)
                pyautogui.click()
                return "🪄 Tried to click 'Skip Ad' on YouTube."
            except Exception as e:
                return f"⚠️ Could not skip the ad. Error: {e}"

        matched_key = key_map[matched_phrase]
        if matched_key:
            try:
                keyboard.press_and_release(matched_key)
                return f"✅ Performed: **{matched_phrase.capitalize()}** on YouTube."
            except Exception as e:
                return f"❌ Failed to perform action: {matched_phrase}.\nError: {e}"

    return (
        f"Sorry, I didn’t understand '{action}'.\n"
        "Try saying something like 'pause the video', 'mute YouTube', or 'skip ad'."
    )

def is_youtube_focused():
    """Returns True if a window with YouTube in the title is currently focused."""
    try:
        window = gw.getActiveWindow()
        return window and "youtube" in window.title.lower()
    except Exception:
        return False
