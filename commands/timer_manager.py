# commands/timer_manager.py

import time
import threading
from core.registry import register_command
from playsound import playsound
import os
import re

def parse_duration(text):
    text = text.lower().strip()

    if "minute" in text or "मिनट" in text or "min" in text:
        num = ''.join(filter(str.isdigit, text))
        return int(num) * 60 if num else None
    if "second" in text or "सेकंड" in text or "sec" in text:
        num = ''.join(filter(str.isdigit, text))
        return int(num) if num else None
    if text.isdigit():
        return int(text) * 60
    return None

def start_timer(duration_secs, label="timer"):
    def run_timer():
        time.sleep(duration_secs)
        try:
            playsound(os.path.join(os.path.dirname(__file__), "../data/timer_done.mp3"))
        except:
            pass
        from gui.app_gui import speak
        speak(f"Time's up for your {label}!")
    threading.Thread(target=run_timer, daemon=True).start()

@register_command("set timer")
def handle_timer_command(params):
    if not params or not any(unit in params.lower() for unit in ["minute", "second", "मिनट", "सेकंड", "min", "sec", "मिन", "सेक"]):
        from core.interaction_manager import interaction_manager_instance  # 🔁 Moved inside
        interaction_manager_instance.pending_confirmation = {"action": "set_timer"}
        return "Alright—how long should I set the timer for?"

    match = re.search(r'(\d+)\s*(minute|minutes|min|second|seconds|sec|मिनट|सेकंड)', params.lower())

    if not match:
        from core.interaction_manager import interaction_manager_instance
        interaction_manager_instance.pending_confirmation = {"action": "set_timer"}
        return "Okay—how long should I set the timer for?"

    duration_secs = parse_duration(params)
    if duration_secs:
        start_timer(duration_secs)
        return f"Timer started for {params.strip()}."
    else:
        return "⚠️ I couldn’t understand the duration. Try '2 minutes' or '30 seconds'."

def set_timer(duration_text, on_complete=None):
    duration_secs = parse_duration(duration_text)
    if duration_secs:
        start_timer(duration_secs)
        if on_complete:
            on_complete("Timer started.")
        return f"Timer started for {duration_text.strip()}."
    else:
        return "⚠️ Sorry, I couldn't understand that time."
