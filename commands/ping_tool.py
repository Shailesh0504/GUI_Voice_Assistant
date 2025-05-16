import platform
import subprocess
import threading
import re
from core.voice_output import speak
from core.registry import register_command
from gui.message_router import show_in_chat

def ping_target(hostname):
    os_name = platform.system().lower()
    count_flag = "-n" if os_name == "windows" else "-c"
    command = ["ping", count_flag, "4", hostname]

    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        latency = extract_latency(result, os_name)
        loss = extract_packet_loss(result, os_name)

        summary = f"📡 Ping Results for {hostname}:\n" \
                  f"🕒 Average latency: {latency} ms\n" \
                  f"📉 Packet loss: {loss}"

        show_in_chat(summary)
        speak(f"Ping complete. Latency {latency} milliseconds, packet loss {loss}.")
    except subprocess.CalledProcessError as e:
        show_in_chat(f"❌ Failed to ping {hostname}: {e.output}")
        speak(f"Ping to {hostname} failed.")
    except Exception as e:
        show_in_chat(f"❗ Error: {str(e)}")
        speak("An error occurred while pinging.")

def extract_latency(output, os_name):
    if os_name == "windows":
        match = re.search(r"Average = (\d+)", output)
    else:
        match = re.search(r"avg(?:/|=)(\d+\.\d+)", output)
    return match.group(1) if match else "N/A"

def extract_packet_loss(output, os_name):
    match = re.search(r"(\d+)%\s*loss", output) if os_name == "windows" else re.search(r"(\d+)% packet loss", output)
    return f"{match.group(1)}%" if match else "N/A"

@register_command("ping")
def ping_command(params):
    if not params:
        return "❗ Please provide a domain or IP to ping."

    hostname = params.strip().replace("ping", "").strip()
    if not hostname:
        return "❗ Please specify a valid hostname or IP."

    threading.Thread(target=ping_target, args=(hostname,), daemon=True).start()
    return f"📡 Pinging {hostname}..."
