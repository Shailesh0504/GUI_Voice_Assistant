# commands/reminder_manager.py

import threading
import time
from datetime import datetime
from core.registry import register_command

reminders = []

@register_command("set reminder")
def set_reminder(params):
    """
    Smart reminder parser for messy input like:
    - "Remind me 12:00 p.m. Drink water on"
    - "Drink water on 7 PM"
    """

    import re

    if not params:
        return "❗ Please say something like: 'Remind me to drink water at 7 pm'."

    # Normalize punctuation and lowercase
    text = params.replace('.', '').lower()

    # Extract time using regex
    match = re.search(r'(\d{1,2}(:\d{2})?\s?(am|pm))', text)
    if not match:
        return "❗ Could not find time. Try '7 pm' or '12:30 am'."

    time_str = match.group(1).strip()
    message = text.replace(time_str, "").replace("on", "").replace("at", "").strip().capitalize()

    if not message:
        return "❗ Could not find what to remind. Try: 'Remind me to drink water at 7 pm'."

    try:
        parsed_time = datetime.strptime(time_str, "%I:%M %p" if ':' in time_str else "%I %p")
        formatted_time = parsed_time.strftime("%H:%M")
        reminders.append({"message": message, "time": formatted_time})
        return f"Reminder set for {formatted_time}: {message}"
    except ValueError:
        return "Invalid time. Use format like '12:00 pm' or '7:30 am'."


@register_command("list reminders")
def list_reminders(params=None):
    if not reminders:
        return "📭 You have no reminders set."
    lines = [f"• {r['time']} → {r['message']}" for r in reminders]
    return "Active reminders:\n" + "\n".join(lines)

@register_command("clear reminders")
def clear_reminders(params=None):
    reminders.clear()
    return "All reminders have been cleared."

def check_due_reminders():
    """
    Background function to check reminders every 30 seconds
    """
    while True:
        now = datetime.now().strftime("%H:%M")
        due = [r for r in reminders if r["time"] == now]

        for r in due:
            print(f"🔔 Reminder: {r['message']}")
            try:
                from gui.app_gui import speak
                speak(f"Reminder: {r['message']}")
                return(f"Reminder: {r['message']}")
            except:
                pass

        # Remove triggered
        reminders[:] = [r for r in reminders if r["time"] != now]
        time.sleep(30)
