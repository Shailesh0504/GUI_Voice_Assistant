import os
import subprocess
import psutil
import pygetwindow as gw
from core.registry import register_command
from threading import Thread
from tkinter import messagebox

# Applications map
APPLICATIONS = {
    "calculator": "C:\\Windows\\System32\\calc.exe",
    "notepad": "C:\\Windows\\System32\\notepad.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
    "outlook": "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE",
    "vs code": "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "paint": "C:\\Windows\\System32\\mspaint.exe",
    "command prompt": "C:\\Windows\\System32\\cmd.exe",
    "task manager": "C:\\Windows\\System32\\Taskmgr.exe",
    "explorer": "C:\\Windows\\explorer.exe",
    "control panel": "C:\\Windows\\System32\\control.exe",
    "snipping tool": "C:\\Windows\\System32\\SnippingTool.exe",
    "device manager": "C:\\Windows\\System32\\devmgmt.msc",
    "vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
    "discord": "C:\\Users\\%USERNAME%\\AppData\\Local\\Discord\\app-1.11.1\\Discord.exe",
    "teams": "C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart \"Teams.exe\"",
    "cisco vpn": "C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\vpnui.exe",
    "brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
    "obs studio": "C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe"
}

editable_apps = ["notepad", "word", "excel", "powerpoint", "paint"]

UWP_APP_TITLES = {
    "calculator": "Calculator",
    "photos": "Photos",
    "clock": "Clock",
    "settings": "Settings"
}

def expand_path(path):
    return os.path.expandvars(path)

def is_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
            return True
    return False

def bring_to_front(app_key):
    windows = gw.getWindowsWithTitle(app_key.title())
    if windows:
        window = windows[0]
        if window.isMinimized:
            window.restore()
        window.activate()
        return True
    return False

@register_command("open app")
def open_application(params):
    if not params:
        return "❗ Please specify which application to open."

    app_key = params.lower().strip()
    app_path = APPLICATIONS.get(app_key)

    if not app_path:
        return f"❌ Sorry, I don't recognize the application '{app_key}'."

    expanded_path = expand_path(app_path)
    exe_name = os.path.basename(expanded_path)

    if is_running(exe_name):
        bring_to_front(app_key)
        return f"📌 {app_key.title()} is already open. I've brought it to the front."

    try:
        Thread(target=subprocess.Popen, args=(expanded_path,), daemon=True).start()
        return f"Opening {app_key.title()}..."
    except Exception as e:
        return f"❌ Failed to open {app_key.title()}: {e}"

@register_command("close app")
def close_application(app_name):
    app_name = app_name.lower().strip()
    exe_name = f"{app_name}.exe"

    # Special handling for UWP apps
    if app_name in UWP_APP_TITLES:
        title = UWP_APP_TITLES[app_name]
        windows = gw.getWindowsWithTitle(title)
        if windows:
            if app_name in editable_apps:
                messagebox.showwarning(
                    title=f"Closing {app_name.capitalize()}",
                    message=f"{app_name.capitalize()} may have unsaved work.\nPlease save before continuing."
                )
            os.system("taskkill /f /im ApplicationFrameHost.exe >nul 2>&1")
            return f"{app_name.capitalize()} has been closed."
        else:
            return f"{app_name.capitalize()} is not currently running."

    # Regular .exe apps
    if not is_running(exe_name):
        return f"🔍 {app_name.capitalize()} is not currently running."

    if app_name in editable_apps:
        messagebox.showwarning(
            title=f"Closing {app_name.capitalize()}",
            message=f"{app_name.capitalize()} may have unsaved work.\nPlease save it before continuing."
        )

    result = os.system(f"taskkill /f /im {exe_name} >nul 2>&1")
    if result == 0:
        return f"{app_name.capitalize()} has been closed."
    else:
        return f"Failed to close {app_name.capitalize()}. It may require admin rights."
