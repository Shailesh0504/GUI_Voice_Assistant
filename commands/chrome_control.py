import keyboard
import subprocess
import time
import psutil
import pygetwindow as gw
from core.registry import register_command
from utils.chrome_normalizer import normalize_chrome_command
from rapidfuzz import process, fuzz

@register_command("control chrome")
def control_chrome_browser(params):
    """
    Enhanced Chrome controller with fuzzy matching:
    - Normalizes user input
    - Uses rapidfuzz to handle natural phrasing
    - Supports incognito, history, and browser key commands
    """
    if not params or not params.strip():
        return "Please specify what to do in Chrome — like 'new tab', 'incognito mode', or 'clear history'."

    raw_action = normalize_chrome_command(params)

    if not is_chrome_running():
        try:
            subprocess.Popen(["chrome"])
            time.sleep(3)  # Give Chrome time to launch
        except Exception as e:
            return f"Failed to launch Chrome.Error: {e}"
        
    

    if not focus_chrome_window():
        return "⚠️ Couldn't focus Chrome window. Please ensure it's not minimized and try again."

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

    # 🎯 Fuzzy match with rapidfuzz
    best_match, score, _ = process.extractOne(
        raw_action, list(command_map.keys()), scorer=fuzz.partial_ratio
    )

    if score >= 80:
        try:
            command_map[best_match]()
            return f"✅ Chrome action performed: **{best_match.capitalize()}**"
        except Exception as e:
            return f"❌ Failed to perform Chrome action '{best_match}'.\nError: {e}"

    elif "incognito" in raw_action:
        try:
            subprocess.Popen(["chrome", "--incognito"])
            return "🕵️ Incognito window launched in Chrome."
        except Exception as e:
            return f"❌ Failed to open Chrome incognito mode.\nError: {e}"

    elif "clear history" in raw_action or "delete history" in raw_action:
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

def focus_chrome_window():
    """Bring Chrome to front if it's running."""
    try:
        windows = gw.getWindowsWithTitle("Chrome")
        for win in windows:
            if "chrome" in win.title.lower():
                win.restore()
                time.sleep(0.5)
                win.activate()
                return True
    except:
        pass
    return False
