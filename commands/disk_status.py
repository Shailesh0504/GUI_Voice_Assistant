import shutil
import psutil
from core.registry import register_command
from core.voice_output import speak
from gui.message_router import show_in_chat

@register_command("check system")
def check_system_status(params=None):
    """
    Reports both disk and RAM usage status.
    """
    try:
        # Disk status (C:/)
        total, used, free = shutil.disk_usage("C:/")
        total_gb = total // (2**30)
        used_gb = used // (2**30)
        free_gb = free // (2**30)
        percent_free = round((free / total) * 100)

        disk_msg = (
            f"💽 Disk Usage for Drive C:\n"
            f"• Total: {total_gb} GB\n"
            f"• Used: {used_gb} GB\n"
            f"• Free: {free_gb} GB ({percent_free}% free)"
        )

        # RAM status
        ram = psutil.virtual_memory()
        total_ram = ram.total // (2**30)
        used_ram = ram.used // (2**30)
        free_ram = ram.available // (2**30)
        ram_percent = ram.percent

        ram_msg = (
            f"🧠 RAM Usage:\n"
            f"• Total: {total_ram} GB\n"
            f"• Used: {used_ram} GB\n"
            f"• Free: {free_ram} GB ({100 - ram_percent}% free)"
        )

        # Output to chat and voice
        speak(f"You have about {free_gb} gigabytes free disk space and {free_ram} gigabytes free RAM.")
        show_in_chat(disk_msg)
        show_in_chat(ram_msg)

        return "[system status shown]"

    except Exception as e:
        error_msg = f"❌ Unable to retrieve system info: {e}"
        speak("Sorry, I couldn't fetch your system information.")
        show_in_chat(error_msg)
        return "[system error]"
