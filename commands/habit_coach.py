import json
import os
import threading
import time
from datetime import datetime

from core.voice_output import speak
from core.registry import register_command
from gui.message_router import show_in_chat

HABIT_FILE = "data/habits.json"
LOG_FILE = "data/habit_log.json"

# Ensure files exist
os.makedirs("data", exist_ok=True)
for file in [HABIT_FILE, LOG_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)

def load_json(file):
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ---------------------------- CORE COMMANDS ----------------------------

@register_command("add habit")
def add_habit(params=None):
    if not params:
        return "❗ Say something like: Add habit drink water at 10AM and 3PM"

    parts = params.split(" at ")
    if len(parts) != 2:
        return "❗ Please use the format: Add habit [habit name] at [times separated by 'and']"

    habit_name = parts[0].strip().lower()
    times = [t.strip().upper() for t in parts[1].split(" and ")]

    habits = load_json(HABIT_FILE)
    habits[habit_name] = times
    save_json(HABIT_FILE, habits)

    show_in_chat(f"✅ Added habit: **{habit_name}** at {', '.join(times)}")
    speak(f"Got it. I’ll remind you to {habit_name} at those times.")
    return "Habit added."

@register_command("list habits")
def list_habits(params=None):
    habits = load_json(HABIT_FILE)
    if not habits:
        return "📭 You don’t have any habits yet."

    response = "📋 Your current habits:\n"
    for habit, times in habits.items():
        response += f"- {habit.title()} at {', '.join(times)}\n"

    show_in_chat(response.strip())
    speak("Here are your current habits.")
    return "Listed habits."

@register_command("mark habit")
def mark_done(params=None):
    if not params:
        return "❗ Say something like: Mark habit drink water done"

    habit_name = params.strip().lower()
    today = datetime.now().strftime("%Y-%m-%d")
    log = load_json(LOG_FILE)
    log.setdefault(today, {})
    log[today][habit_name] = "done"
    save_json(LOG_FILE, log)

    show_in_chat(f"✅ Marked **{habit_name}** as done for today.")
    speak(f"Great job completing {habit_name}!")
    return "Habit marked."

@register_command("review day")
def review_day(params=None):
    today = datetime.now().strftime("%Y-%m-%d")
    habits = load_json(HABIT_FILE)
    log = load_json(LOG_FILE).get(today, {})

    completed = [h for h in habits if log.get(h) == "done"]
    missed = [h for h in habits if h not in completed]

    summary = f"📊 **Daily Habit Review for {today}**\n"
    summary += f"✅ Done: {', '.join(completed) if completed else 'None'}\n"
    summary += f"❌ Missed: {', '.join(missed) if missed else 'None'}"

    show_in_chat(summary)
    speak(f"You completed {len(completed)} out of {len(habits)} habits today.")
    return "Day reviewed."

@register_command("remove habit")
def remove_habit(params=None):
    if not params:
        return "❗ Say something like: Remove habit meditate"

    habit_name = params.strip().lower()
    habits = load_json(HABIT_FILE)
    if habit_name not in habits:
        return f"❌ Habit '{habit_name}' not found."

    del habits[habit_name]
    save_json(HABIT_FILE, habits)

    show_in_chat(f"🗑️ Removed habit: **{habit_name}**")
    speak(f"Okay, removed the habit {habit_name}.")
    return "Habit removed."

# ---------------------------- SCHEDULING REMINDERS ----------------------------

def schedule_reminders():
    def reminder_loop():
        while True:
            now = datetime.now().strftime("%I:%M%p")
            habits = load_json(HABIT_FILE)
            for habit, times in habits.items():
                for t in times:
                    if now == t:
                        speak(f"⏰ Reminder: It's time to {habit}")
                        show_in_chat(f"🔔 Reminder: Time to **{habit}**")
            time.sleep(60)  # check every minute

    thread = threading.Thread(target=reminder_loop, daemon=True)
    thread.start()

# Start the reminder scheduler once when the module is loaded
schedule_reminders()
