import keyboard
import subprocess
import time
import psutil
import pygetwindow as gw
from core.registry import register_command
from utils.chrome_normalizer import normalize_chrome_command

@register_command("control chrome")
def control_chrome_browser(params):
    """
    Enhanced Chrome controller:
    - Normalizes natural phrases using shared utility
    - Checks if Chrome is running and focused
    - Triggers key-based automation for browser control
    """
    if not params or not params.strip():
        return "Please specify what to do in Chrome — like 'new tab', 'incognito mode', or 'clear history'."

    action = normalize_chrome_command(params)

    if not is_chrome_running():
        return "❌ Chrome doesn't seem to be open. Please start Chrome and try again."

    if not is_chrome_focused():
        return "⚠️ Chrome is open, but not in focus.\n👉 Please bring the Chrome window to the front and try again."

    command_map = {
        "new tab": lambda: keyboard.press_and_release("ctrl+t"),
        "close tab": lambda: keyboard.press_and_release("ctrl+w"),
        "reopen tab": lambda: keyboard.press_and_release("ctrl+shift+t"),
        "new window": lambda: keyboard.press_and_release("ctrl+n"),
        "close window": lambda: keyboard.press_and_release("alt+f4"),
        "next tab": lambda: keyboard.press_and_release("ctrl+tab"),
        "previous tab": lambda: keyboard.press_and_release("ctrl+shift+tab"),
        "refresh": lambda: keyboard.press_and_release("ctrl+r"),
        "open history": lambda: keyboard.press_and_release("ctrl+h"),
        "open downloads": lambda: keyboard.press_and_release("ctrl+j"),
    }

    if action in command_map:
        try:
            command_map[action]()
            return f"✅ Chrome action performed: **{action.capitalize()}**"
        except Exception as e:
            return f"❌ Failed to perform Chrome action '{action}'.\nError: {e}"

    elif action == "incognito":
        try:
            subprocess.Popen(["chrome", "--incognito"])
            return "🕵️ Incognito window launched in Chrome."
        except Exception as e:
            return f"❌ Failed to open Chrome incognito mode.\nError: {e}"

    elif action == "clear history":
        try:
            subprocess.Popen(["chrome", "chrome://settings/clearBrowserData"])
            time.sleep(2)
            keyboard.press_and_release("tab tab tab tab tab tab tab tab tab tab enter")
            return "🧹 Opened Chrome's clear history page and triggered clearing."
        except Exception as e:
            return f"❌ Failed to clear history.\nError: {e}"

    return (
        f"🤔 I couldn't understand the Chrome action: '{params}'.\n"
        "Try saying 'new tab', 'open incognito', or 'clear history'."
    )

# ------------------ Utilities ------------------ #

def is_chrome_running():
    """Check if Chrome is running in background."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and "chrome" in proc.info['name'].lower():
            return True
    return False

def is_chrome_focused():
    """Check if Chrome is the currently focused window."""
    try:
        win = gw.getActiveWindow()
        return win and "chrome" in win.title.lower()
    except:
        return False
