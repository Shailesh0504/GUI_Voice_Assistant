import time
import threading
from datetime import datetime
import os
import re
from core.registry import register_command
from pygame import mixer

alarms = []
alarm_ringing_time = None  # Currently ringing alarm time
ALARM_SOUND_PATH = os.path.join(os.path.dirname(__file__), "../sounds/alarm.mp3")

# Initialize mixer once
mixer.init()

@register_command("set alarm")
def set_alarm(params):
    if not params:
        return "Please say something like: 'Set alarm for 6:30 AM' or 'Wake me up at 07:00'."

    params = (
        params.lower()
        .replace(".", "")
        .replace("at", "")
        .replace("set", "")
        .replace("alarm", "")
        .replace("ka", "")
        .replace("baje", "")
        .replace("subah", "")
        .replace("lagao", "")
        .strip()
    )

    match = re.search(r'(\d{1,2})(:\d{2})?\s*(am|pm)?', params)
    if not match:
        return "⚠️ Sorry, I couldn't understand the time. Try '6:30 AM' or '07:00'."

    hour = int(match.group(1))
    minutes = int(match.group(2)[1:]) if match.group(2) else 0
    meridiem = match.group(3)

    if meridiem == "pm" and hour != 12:
        hour += 12
    elif meridiem == "am" and hour == 12:
        hour = 0

    alarm_time = f"{hour:02d}:{minutes:02d}"

    try:
        datetime.strptime(alarm_time, "%H:%M")
        if alarm_time not in alarms:
            alarms.append(alarm_time)
            return f"⏰ Alarm set for {alarm_time}."
        else:
            return f"🔁 Alarm for {alarm_time} already exists."
    except ValueError:
        return "⚠️ Invalid format. Try saying: 'set alarm for 6:30 AM'."


@register_command("stop alarm")
def stop_alarm(params=None):
    global alarm_ringing_time
    if alarm_ringing_time:
        mixer.music.stop()
        stopped_time = alarm_ringing_time
        alarm_ringing_time = None
        return f"🛑 Alarm for {stopped_time} stopped."

    # Optional: allow stopping future alarm too
    if params:
        alarm_time = params.strip()
        if alarm_time in alarms:
            alarms.remove(alarm_time)
            return f"🛑 Alarm for {alarm_time} removed."
        else:
            return f"⚠️ No alarm set for {alarm_time}."
    return "⚠️ No alarm is currently ringing."


@register_command("stop all alarms")
def stop_all_alarms(params=None):
    global alarm_ringing_time
    alarm_ringing_time = None
    mixer.music.stop()
    alarms.clear()
    return "🛑 All alarms have been stopped."


@register_command("list alarms")
def list_alarms(params=None):
    if not alarms:
        return "📭 No alarms are currently set."
    return "⏰ Current alarms:\n" + "\n".join(f"• {a}" for a in alarms)


def check_alarms_loop():
    global alarm_ringing_time

    while True:
        now = datetime.now().strftime("%H:%M")

        if now in alarms and alarm_ringing_time is None:
            print(f"🔔 Alarm ringing for {now}!")
            try:
                from gui.app_gui import speak, show_in_chat
                show_in_chat(f"⏰ Alarm ringing for {now}!")
                speak(f"Wake up! It's {now}.")

                # Play alarm sound
                if os.path.exists(ALARM_SOUND_PATH):
                    mixer.music.load(ALARM_SOUND_PATH)
                    mixer.music.play(-1)  # loop until stopped

                alarm_ringing_time = now
            except Exception as e:
                print(f"❗ Alarm error: {e}")

        time.sleep(30)
