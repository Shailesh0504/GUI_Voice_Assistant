# commands/cleaner.py

import os
import shutil
import threading
import platform
from core.registry import register_command
from core.voice_output import speak
import pyautogui

def confirm_action(action_name):
    return pyautogui.confirm(
        text=f"Are you sure you want to {action_name}?",
        title=f"Confirm {action_name.title()}",
        buttons=["Yes", "No"]
    ) == "Yes"

@register_command("clean temp files")
def clean_temp_files(params=None):
    """
    Cleans system/user temporary files after user confirmation.
    Runs in a separate thread to avoid blocking the main UI.
    """

    def cleanup():
        system = platform.system()
        temp_dirs = []

        if system == "Windows":
            temp_dirs = [
                os.getenv("TEMP"),
                os.getenv("TMP"),
                r"C:\Windows\Temp"
            ]
        else:
            temp_dirs = ["/tmp"]

        cleaned_files = 0
        failed = []

        try:
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    for root, dirs, files in os.walk(temp_dir):
                        for f in files:
                            file_path = os.path.join(root, f)
                            try:
                                os.remove(file_path)
                                cleaned_files += 1
                            except Exception:
                                failed.append(file_path)

                        for d in dirs:
                            dir_path = os.path.join(root, d)
                            try:
                                shutil.rmtree(dir_path, ignore_errors=True)
                            except Exception:
                                failed.append(dir_path)

            speak(f"Cleanup completed. Removed {cleaned_files} files.")
            return (f"Temporary files cleaned. {cleaned_files} files removed.")
        except Exception as e:
            speak("Cleanup failed.")
            print(f"Cleanup failed due to error: {e}")

    # Confirm before starting cleanup
    action_desc = "clear temporary files to free up space"
    speak(f"Got it — shall I {action_desc}?")
    if not confirm_action(action_desc):
        speak("Okay, cleanup cancelled.")
        return "Cleanup cancelled."

    # Start cleanup in a separate thread
    threading.Thread(target=cleanup, daemon=True).start()
    return "Starting cleanup in the background..."
