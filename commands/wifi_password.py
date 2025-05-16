import subprocess
import threading
from core.voice_output import speak
from core.registry import register_command
from gui.message_router import show_in_chat

def fetch_wifi_passwords():
    try:
        # Get list of Wi-Fi profiles
        output = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
        profiles = [line.split(":")[1].strip() for line in output.splitlines() if "All User Profile" in line]

        if not profiles:
            show_in_chat("📡 No Wi-Fi profiles found.")
            speak("No Wi-Fi profiles found.")
            return

        results = ["Saved Wi-Fi Passwords:"]
        for profile in profiles:
            try:
                detail_output = subprocess.check_output(f'netsh wlan show profile "{profile}" key=clear', shell=True, text=True)
                for line in detail_output.splitlines():
                    if "Key Content" in line:
                        password = line.split(":")[1].strip()
                        results.append(f"• {profile}: 🔑 {password}")
                        break
                else:
                    results.append(f"• {profile}: 🔒 Password not found")
            except subprocess.CalledProcessError:
                results.append(f"• {profile}: ⚠️ Error reading password")

        final_output = "\n".join(results)
        show_in_chat(final_output)
        speak("Here are your stored Wi-Fi passwords.")

    except Exception as e:
        error_msg = f"❗ Failed to retrieve Wi-Fi passwords: {str(e)}"
        show_in_chat(error_msg)
        speak("Sorry, I could not fetch Wi-Fi passwords.")

@register_command("show wifi password")
def show_wifi_password(params=None):
    threading.Thread(target=fetch_wifi_passwords, daemon=True).start()
    return "Retrieving saved Wi-Fi passwords..."
