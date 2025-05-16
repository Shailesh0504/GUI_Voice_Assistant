import threading
import time
import os
import re
import json
from datetime import datetime, timedelta
from core.registry import register_command
from core.voice_output import speak
from pygame import mixer
from rapidfuzz import process, fuzz  # ✅ Fuzzy matching added

REMINDER_SOUND_PATH = os.path.join(os.path.dirname(__file__), "../sounds/reminder.mp3")
REMINDER_FILE = os.path.join(os.path.dirname(__file__), "../data/reminders.json")
mixer.init()

def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []

    with open(REMINDER_FILE, "r", encoding="utf-8") as f:
        reminders = json.load(f)

    # Patch missing 'date' field
    today = datetime.today().strftime("%Y-%m-%d")
    for r in reminders:
        if "date" not in r:
            r["date"] = today

    return reminders

def save_reminders(reminders):
    with open(REMINDER_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)

def parse_date(text):
    text = text.lower()
    today = datetime.today()

    if "today" in text:
        return today.strftime("%Y-%m-%d")
    elif "tomorrow" in text:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")

    match = re.search(r'(\d{1,2})\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*', text)
    if match:
        day = match.group(1)
        month_str = match.group(2)
        month_map = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
        }
        month = month_map[month_str]
        year = today.year
        try:
            parsed_date = datetime(year, month, int(day))
            return parsed_date.strftime("%Y-%m-%d")
        except:
            return None
    return today.strftime("%Y-%m-%d")

@register_command("set reminder")
def set_reminder(params):
    if not params:
        return "❗ Please say something like: 'Remind me to submit report on 15 May at 5 pm'."

    text = params.replace(".", "").lower()
    date_str = parse_date(text)

    match = re.search(r'(\d{1,2}(:\d{2})?\s?(am|pm)|\d{1,2}(am|pm))', text)
    if not match:
        return "❗ Could not find time. Try '5 pm' or '12:30 am'."

    time_str = match.group(1).strip()
    cleaned = text.replace(time_str, "")
    cleaned = re.sub(r"\b(remind me to|set reminder|reminder|on|at|for)\b", "", cleaned)
    message = cleaned.strip().capitalize()

    if not message:
        return "❗ Could not find what to remind. Try: 'Remind me to take medicine at 9 am'."

    try:
        parsed_time = datetime.strptime(time_str, "%I:%M %p" if ':' in time_str else "%I %p")
        formatted_time = parsed_time.strftime("%H:%M")
        reminders = load_reminders()
        reminders.append({"message": message, "time": formatted_time, "date": date_str})
        save_reminders(reminders)
        return f"📅 Reminder set for {date_str} at {formatted_time}: ‘{message}’"
    except ValueError:
        return "❗ Invalid time. Use format like '12:00 pm' or '7:30 am'."

@register_command("list reminders")
def list_reminders(params=None):
    reminders = load_reminders()
    if not reminders:
        return "📭 You have no reminders set."

    now = datetime.now()
    filtered = []

    # --- Natural date and time filtering ---
    if params:
        text = params.lower()

        # DATE MATCHING
        if "today" in text:
            date_filter = now.strftime("%Y-%m-%d")
            filtered = [r for r in reminders if r.get("date") == date_filter]

        elif "tomorrow" in text:
            tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
            filtered = [r for r in reminders if r.get("date") == tomorrow]

        # TIME WINDOW MATCHING
        elif "morning" in text:
            filtered = [r for r in reminders if r.get("date") == now.strftime("%Y-%m-%d") and int(r["time"][:2]) < 12]

        elif "afternoon" in text:
            filtered = [r for r in reminders if r.get("date") == now.strftime("%Y-%m-%d") and 12 <= int(r["time"][:2]) < 17]

        elif "evening" in text or "tonight" in text:
            filtered = [r for r in reminders if r.get("date") == now.strftime("%Y-%m-%d") and 17 <= int(r["time"][:2]) < 21]

        elif "night" in text:
            filtered = [r for r in reminders if r.get("date") == now.strftime("%Y-%m-%d") and int(r["time"][:2]) >= 21]

        else:
            # fallback to fuzzy match on message
            from rapidfuzz import process, fuzz
            messages = [r['message'] for r in reminders]
            result = process.extractOne(params, messages, scorer=fuzz.ratio, score_cutoff=70)
            if result:
                _, _, index = result
                r = reminders[index]
                return f"🔍 Closest match:\n• {r['date']} {r['time']} → {r['message']}"
            else:
                return f"❗ No reminder found matching ‘{params}’."

    # If no filter or after filtering
    final_list = filtered if params else reminders

    if not final_list:
        return f"📭 No matching reminders."

    lines = [f"• {r['date']} {r['time']} → {r['message']}" for r in final_list]
    return "Active reminders:\n" + "\n".join(lines)


@register_command("clear reminders")
def clear_reminders(params=None):
    save_reminders([])
    return "🗑️ All reminders have been cleared."

def play_reminder_sound():
    try:
        if os.path.exists(REMINDER_SOUND_PATH):
            mixer.music.load(REMINDER_SOUND_PATH)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.5)
            mixer.music.stop()
    except Exception as e:
        print(f"❗ Reminder sound error: {e}")

def check_due_reminders():
    while True:
        now_time = datetime.now().strftime("%H:%M")
        now_date = datetime.now().strftime("%Y-%m-%d")
        reminders = load_reminders()
        due = [r for r in reminders if r["time"] == now_time and r["date"] == now_date]

        for r in due:
            print(f"🔔 Reminder: {r['message']}")
            try:
                speak(f"Reminder: {r['message']}")
                threading.Thread(target=play_reminder_sound, daemon=True).start()
            except Exception as e:
                print(f"❗ Voice error: {e}")

        remaining = [r for r in reminders if not (r["time"] == now_time and r["date"] == now_date)]
        save_reminders(remaining)
        time.sleep(30)
