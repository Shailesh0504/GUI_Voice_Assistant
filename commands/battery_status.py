import psutil
import pyautogui
import threading
import time
from core.voice_output import speak
from core.registry import register_command
from gui.message_router import show_in_chat

@register_command("check battery")
def check_battery(params=None):
    """
    Checks and announces the current battery status of the device.
    Also starts a background thread to monitor battery levels.
    """
    confirm = pyautogui.confirm(
        title="Battery Status",
        text="Would you like me to tell you the current battery level?",
        buttons=["Yes", "No"]
    )

    if confirm != "Yes":
        return "Okay, battery check skipped."

    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return "Battery information is not available on this device."

        percent = battery.percent
        plugged = battery.power_plugged

        status = f"{percent}% {'(charging)' if plugged else '(not charging)'}"
        speak(f"Your battery is at {percent} percent. {'It is charging.' if plugged else 'It is not charging.'}")

        # Friendly proactive tips
        if plugged and percent == 100:
            speak("Battery fully charged. You may unplug the charger to preserve battery health.")
        elif not plugged and percent <= 20:
            speak("Battery is low. Please plug in your charger soon to avoid shutdown.")

        # Start background monitoring thread
        threading.Thread(target=monitor_battery_status, daemon=True).start()

        return f"Battery Status: {status}"

    except Exception as e:
        return f"Unable to retrieve battery status: {e}"


def monitor_battery_status():
    notified_full = False
    notified_low = False

    while True:
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = battery.power_plugged

                if plugged and percent >= 100 and not notified_full:
                    message = "Heads up! Battery is now full. Please unplug the charger."
                    speak("Heads up! Battery is now full. Please unplug the charger.")
                    show_in_chat("🔋 " + message)  # ✅ show in chat
                    notified_full = True
                    notified_low = False

                elif not plugged and percent <= 20 and not notified_low:
                    message = "Warning: Battery is below 20 percent. Please plug in the charger."
                    speak("Warning: Battery is below 20 percent. Please plug in the charger.")
                    show_in_chat("🔋 " + message)  # ✅ show in chat
                    notified_low = True
                    notified_full = False

                # Reset notification flags if battery moves out of critical state
                if percent < 100 and plugged:
                    notified_full = False
                if percent > 20 and not plugged:
                    notified_low = False

        except Exception:
            pass

        time.sleep(60)

