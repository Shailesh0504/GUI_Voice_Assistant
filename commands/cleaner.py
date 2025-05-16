import os
import shutil
import threading
import platform
import pyautogui
from core.registry import register_command
from core.voice_output import speak
from gui.message_router import show_in_chat

def confirm_action(action_name):
    return pyautogui.confirm(
        text=f"Are you sure you want to {action_name}?",
        title=f"Confirm {action_name.title()}",
        buttons=["Yes", "No"]
    ) == "Yes"

@register_command("clean temp files")
def clean_temp_files(params=None):
    """
    Cleans temporary system/user files after confirmation.
    Runs in a background thread to avoid freezing the UI.
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
        failed_items = []

        try:
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    for root, dirs, files in os.walk(temp_dir):
                        for f in files:
                            try:
                                os.remove(os.path.join(root, f))
                                cleaned_files += 1
                            except Exception:
                                failed_items.append(f)

                        for d in dirs:
                            try:
                                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                            except Exception:
                                failed_items.append(d)

            message = f"🧹 Cleanup complete. Removed {cleaned_files} temporary files."
            speak(f"Cleanup finished. I removed {cleaned_files} unnecessary files.")
            show_in_chat(message)

        except Exception as e:
            speak("Sorry, something went wrong while cleaning.")
            show_in_chat(f"❌ Cleanup failed due to: {e}")

    # Voice introduction
    speak("You asked me to clean up temporary files to free up space.")
    action_desc = "clean temporary files"

    if not confirm_action(action_desc):
        speak("Understood. I won't delete anything.")
        return "🛑 Cleanup cancelled by user."

    # Start background cleanup
    threading.Thread(target=cleanup, daemon=True).start()
    speak("Cleaning started in the background. I'll let you know when it's done.")
    return "🧹 Starting cleanup in the background..."
