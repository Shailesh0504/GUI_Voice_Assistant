# commands/system_control.py

import os
import platform
import pyautogui
from core.registry import register_command
from core.voice_output import speak

def confirm_action(action_name):
    confirm = pyautogui.confirm(
        speak(f"Are you sure you want to {action_name} the system?"),
        text=f"Are you sure you want to {action_name} the system?",
        title=f"Confirm {action_name.title()}",
        buttons=["Yes", "No"]
    )
    return confirm == "Yes"

@register_command("shutdown")
def shutdown_system(params=None):
    if not confirm_action("shutdown"):
        return "❎ Shutdown cancelled."

    if platform.system() == "Windows":
        os.system("shutdown /s /t 1")
    else:
        os.system("shutdown now")
    return "🛑 Shutting down the system..."

@register_command("restart")
def restart_system(params=None):
    if not confirm_action("restart"):
        return "❎ Restart cancelled."

    if platform.system() == "Windows":
        os.system("shutdown /r /t 1")
    else:
        os.system("reboot")
    return "🔄 Restarting the system..."

@register_command("logout")
def logout_user(params=None):
    if not confirm_action("logout"):
        return "❎ Logout cancelled."

    if platform.system() == "Windows":
        os.system("shutdown /l")
    else:
        os.system("pkill -KILL -u $USER")
    return "🚪 Logging out..."

@register_command("lock")
def lock_system(params=None):
    if platform.system() == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")
    else:
        os.system("gnome-screensaver-command -l")
    return "Ok sir, for the safety of your system, it is now locked."
