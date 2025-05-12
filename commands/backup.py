# commands/backup.py

import os
import shutil
from datetime import datetime
from core.registry import register_command
from core.voice_output import speak
import pyautogui

def confirm_action(action_name):
    confirm = pyautogui.confirm(
        text=f"Are you sure you want to {action_name} the system?",
        title=f"Confirm {action_name.title()}",
        buttons=["Yes", "No"]
    )
    return confirm == "Yes"  # using the GUI confirmation

@register_command("backup folder")
def backup_folder(params=None):
    """
    Backs up a user-specified folder like Documents or Pictures.
    Example: "Backup my Documents folder"
    """

    folder_map = {
        "documents": os.path.expanduser("~/Documents"),
        "downloads": os.path.expanduser("~/Downloads"),
        "pictures": os.path.expanduser("~/Pictures"),
        "desktop": os.path.expanduser("~/Desktop")
    }

    folder_key = None
    if params:
        for key in folder_map:
            if key in params.lower():
                folder_key = key
                break

    if not folder_key:
        return "❓ I didn't catch which folder to back up. Please specify Documents, Downloads, etc."

    source_path = folder_map[folder_key]
    date_str = datetime.now().strftime("%Y-%m-%d")
    backup_dir = os.path.expanduser(f"~/Backups/{folder_key.capitalize()}_{date_str}/")

    # GUI confirmation
    confirmation_text = f"start backing up your {folder_key.capitalize()} folder"
    speak(f"🗂️ {confirmation_text}?")
    if not confirm_action(confirmation_text):
        return "❌ Backup cancelled."

    try:
        if not os.path.exists(source_path):
            return f"⚠️ The folder '{folder_key}' does not exist."

        os.makedirs(backup_dir, exist_ok=True)
        shutil.copytree(source_path, backup_dir, dirs_exist_ok=True)
        speak(f"✅ Backup of your {folder_key} folder completed.")
        return f"✅ Backup of your {folder_key} folder completed successfully."

    except Exception as e:
        speak("❌ Backup failed due to an error.")
        return f"❌ Backup failed: {e}"
