import psutil
import pyautogui
import threading
import time
from core.voice_output import speak
from core.registry import register_command
from gui.message_router import show_in_chat

@register_command("check battery")
def check_battery(params=None):
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

        speak(f"Your battery is at {percent} percent. {'It is currently charging.' if plugged else 'It is not charging.'}")

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
    last_plugged_state = None  # to track plug/unplug events

    while True:
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = battery.power_plugged

                # Detect plug/unplug events
                if last_plugged_state is not None and plugged != last_plugged_state:
                    if plugged:
                        msg = "🔌 Charger connected. Device is now charging."
                        speak("Charger connected. Charging has started.")
                        show_in_chat(msg)
                    else:
                        msg = "🔌 Charger disconnected. Device is now running on battery."
                        speak("Charger disconnected. Running on battery.")
                        show_in_chat(msg)
                last_plugged_state = plugged

                # Full battery notification
                if plugged and percent >= 100 and not notified_full:
                    msg = "🔋 Battery is now fully charged. You can unplug the charger."
                    speak("Battery is now fully charged. You can unplug the charger.")
                    show_in_chat(msg)
                    notified_full = True
                    notified_low = False

                # Low battery notification
                elif not plugged and percent <= 20 and not notified_low:
                    msg = "🔋 Warning: Battery is below 20 percent. Please connect the charger."
                    speak("Battery is below 20 percent. Please connect the charger.")
                    show_in_chat(msg)
                    notified_low = True
                    notified_full = False

                # Reset flags
                if percent < 100 and plugged:
                    notified_full = False
                if percent > 20 and not plugged:
                    notified_low = False

        except Exception:
            pass

        time.sleep(60)  # Check every 1 minute
