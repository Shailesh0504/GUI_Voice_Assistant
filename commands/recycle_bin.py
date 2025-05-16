import ctypes
import pyautogui
import threading
import platform
from core.voice_output import speak
from core.registry import register_command


def confirm_recycle_bin_clear():
    return pyautogui.confirm(
        text="Are you sure you want to permanently clear the Recycle Bin?",
        title="Confirm Recycle Bin Cleanup",
        buttons=["Yes", "No"]
    ) == "Yes"


def clear_recycle_bin_windows():
    SHERB_NOCONFIRMATION = 0x00000001
    SHERB_NOPROGRESSUI = 0x00000002
    SHERB_NOSOUND = 0x00000004

    try:
        result = ctypes.windll.shell32.SHEmptyRecycleBinW(
            None, None, SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND
        )
        if result == 0:
            speak("Recycle Bin cleared successfully.")
        else:
            speak("Could not clear the Recycle Bin.")
    except Exception as e:
        speak("An error occurred while clearing the Recycle Bin.")
        print(f"Error clearing Recycle Bin: {e}")


def cleanup_thread():
    if not confirm_recycle_bin_clear():
        speak("Recycle Bin cleanup cancelled.")
        return

    clear_recycle_bin_windows()


@register_command("clear recycle bin")
def handle_recycle_bin_cleanup(params=None):
    if platform.system() != "Windows":
        speak("Recycle Bin cleanup is only supported on Windows.")
        return "This feature is only available on Windows."

    speak("Shall I go ahead and empty your Recycle Bin?")
    threading.Thread(target=cleanup_thread, daemon=True).start()
    return "🗑️ Recycle Bin cleanup initiated."
