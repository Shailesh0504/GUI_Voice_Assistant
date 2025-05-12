# commands/alarm_manager.py

import time
import threading
from datetime import datetime
from core.registry import register_command

alarms = []

@register_command("set alarm")
def set_alarm(params):
    if not params:
        return "Please specify a time like '07:30'."
    alarm_time = params.strip()
    try:
        datetime.strptime(alarm_time, "%H:%M")
        if alarm_time not in alarms:
            alarms.append(alarm_time)
            return f"Alarm set for {alarm_time}."
        else:
            return f"Alarm for {alarm_time} already exists."
    except ValueError:
        return "Invalid format. Use HH:MM (24-hour)."

@register_command("stop alarm")
def stop_alarm(params):
    if not params:
        return "Please provide a time like '07:30' to stop."

    alarm_time = params.strip()
    if alarm_time in alarms:
        alarms.remove(alarm_time)
        return f"Alarm for {alarm_time} stopped."
    else:
        return f"No alarm set for {alarm_time}."

@register_command("stop all alarms")
def stop_all_alarms(params=None):
    alarms.clear()
    return "All alarms have been stopped."

@register_command("list alarms")
def list_alarms(params=None):
    if not alarms:
        return "No alarms are currently set."
    return "Current alarms:\n" + "\n".join(f"• {a}" for a in alarms)

def check_alarms_loop():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in alarms:
            print(f"Alarm ringing for {now}!")
            from gui.app_gui import speak
            speak(f"Alarm ringing! It's {now}")
            time.sleep(60)  # Avoid repeating in the same minute
        time.sleep(30)
