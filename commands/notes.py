# commands/notes.py

import os
import json
import threading
from datetime import datetime
from core.registry import register_command
from core.voice_output import speak
import pyautogui

def confirm_action(action_name):
    confirm = pyautogui.confirm(
        text=f"Are you sure you want to {action_name} the system?",
        title=f"Confirm {action_name.title()}",
        buttons=["Yes", "No"]
    )
    return confirm == "Yes"  # using the GUI confirmation

NOTES_FILE = os.path.expanduser("data/assistant_notes.json")

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

@register_command("create note")
def create_note(params=None):
    if not params:
        return "📝 What would you like me to note down?"

    note_text = params.replace("note", "", 1).replace(":", "").strip()
    if not note_text:
        return "📝 Please provide some content for the note."

    speak(f"📝 Got it—shall I add: ‘{note_text}’ to your notes?")
    if not confirm_action(f"add this note:\n\n‘{note_text}’"):
        return "🛑 Note creation cancelled."

    def _add():
        notes = load_notes()
        new_note = {
            "id": (notes[-1]["id"] + 1) if notes else 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "content": note_text
        }
        notes.append(new_note)
        save_notes(notes)
        speak("✅ Your note has been saved.")
        print(f"📝 Saved: {new_note['content']}")

    threading.Thread(target=_add, daemon=True).start()
    return "📝 Saving your note in the background..."

@register_command("read notes")
def read_notes(params=None):
    notes = load_notes()
    if not notes:
        return "📭 No notes found."

    speak(f"📖 You have {len(notes)} notes.")
    output = "\n".join([f"{note['id']}. {note['content']} ({note['timestamp']})" for note in notes])
    print(output)
    return output

@register_command("edit note")
def edit_note(params=None):
    if not params:
        return "📝 Please say which note number to edit and the new text."

    parts = params.lower().replace("edit note", "").strip().split(" ", 1)
    if len(parts) < 2:
        return "✏️ Please provide both the note number and the new content."

    try:
        note_id = int(parts[0])
    except ValueError:
        return "❌ Invalid note number."

    new_content = parts[1].strip()
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            old = note["content"]
            note["content"] = new_content
            note["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_notes(notes)
            speak("✅ Note updated.")
            return f"✏️ Note {note_id} updated from:\n‘{old}’\nto:\n‘{new_content}’"

    return f"❌ Note with ID {note_id} not found."

@register_command("delete note")
def delete_note(params=None):
    if not params:
        return "🗑️ Please say the note number you want to delete."

    try:
        note_id = int(params.lower().replace("delete note", "").strip())
    except ValueError:
        return "❌ Invalid note number."

    notes = load_notes()
    note_to_delete = next((n for n in notes if n["id"] == note_id), None)
    if not note_to_delete:
        return f"❌ Note with ID {note_id} not found."

    speak(f"🗑️ Are you sure you want to delete note {note_id}: ‘{note_to_delete['content']}’?")
    if not confirm_action(f"delete note:\n\n‘{note_to_delete['content']}’"):
        return "🛑 Deletion cancelled."

    notes = [n for n in notes if n["id"] != note_id]
    save_notes(notes)
    speak("✅ Note deleted.")
    return f"🗑️ Note {note_id} deleted successfully."
