import requests
import threading
from core.voice_output import speak
from core.registry import register_command
from gui.message_router import show_in_chat

def check_connectivity():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def background_speedtest():
    if not check_connectivity():
        message = "❌ You are not connected to the internet."
        show_in_chat(message)
        speak(message)
        return

    show_in_chat("🕒 Checking your internet speed...")
    speak("Checking your internet speed. Please wait...")

    try:
        import speedtest  # ✅ Lazy import to prevent PyInstaller issues

        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000
        ping_result = st.results.ping

        result = (
            f"📡 Internet Speed Test Result:\n"
            f"⬇️ Download: {download_speed:.2f} Mbps\n"
            f"⬆️ Upload: {upload_speed:.2f} Mbps\n"
            f"📶 Ping: {ping_result:.2f} ms"
        )

        show_in_chat(result)
        speak("Here are your internet speed results.")
        speak(result.replace("\n", ". "))

    except ImportError:
        msg = "❗ Speedtest module is not installed. Please install it using 'pip install speedtest-cli'."
        show_in_chat(msg)
        speak("Speedtest module is missing.")
    except Exception as e:
        error_msg = f"❗ Failed to check internet speed: {str(e)}"
        show_in_chat(error_msg)
        speak("Sorry, I couldn't check the internet speed.")

@register_command("check internet speed")
def check_internet_speed(params=None):
    threading.Thread(target=background_speedtest, daemon=True).start()
    return "✅ Command received."
