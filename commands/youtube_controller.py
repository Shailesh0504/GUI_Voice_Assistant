import pyautogui
import keyboard
from core.registry import register_command

@register_command("control youtube")
def control_youtube_feature(params):
    """
    Controls YouTube video playback via keyboard shortcuts.
    Make sure the YouTube player tab is focused.
    """
    if not params or not params.strip():
        return "🎙️ Please tell me what action to perform on the YouTube video — like pause, mute, or fullscreen."

    action = params.lower().strip()

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
        "skip ad": None  # special case
    }

    # Normalize action for matching
    matched_key = None
    for phrase, key in key_map.items():
        if phrase in action:
            matched_key = key_map[phrase]
            break

    if matched_key:
        try:
            keyboard.press_and_release(matched_key)
            return f"Performed: **{phrase.capitalize()}** on YouTube."
        except Exception as e:
            return f"❌ Failed to perform action: {phrase}.\nError: {e}"

    elif "skip ad" in action:
        try:
            # Move to likely skip button location (adjust if needed)
            pyautogui.moveTo(1100, 500, duration=0.2)
            pyautogui.click()
            return "Tried to click 'Skip Ad' on YouTube."
        except Exception as e:
            return f"⚠️ Could not skip the ad. Error: {e}"

    else:
        return (
            f"Sorry, I didn’t understand '{action}'.\n"
            "Try saying something like 'pause the video', 'mute YouTube', or 'skip ad'."
        )
