import json
import os
import pyautogui
from rapidfuzz import process, fuzz

from core.registry import register_command
from core.voice_output import speak
from gui.message_router import show_in_chat

TODO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "todo.json")

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@register_command("add todo")
def add_to_todo(params):
    if not params:
        message = "What should I add to your to-do list?"
        speak(message)
        return message

    tasks = load_tasks()
    tasks.append(params.strip())
    save_tasks(tasks)

    message = f"Done—‘{params.strip()}’ is on your list."
    speak(message)
    show_in_chat(message)
    return message

@register_command("read todo")
def read_todo(params=None):
    tasks = load_tasks()
    if not tasks:
        message = "Your to-do list is empty."
        speak(message)
        return message

    if params:
        match, score, index = process.extractOne(params, tasks, scorer=fuzz.ratio, score_cutoff=70, return_index=True)
        if match:
            message = f"📌 Closest task match: {index + 1}. {match}"
            speak(message)
            show_in_chat(message)
            return message
        else:
            message = f"❌ Couldn't find any task similar to ‘{params}’."
            speak(message)
            return message

    task_lines = [f"{i+1}. {task}" for i, task in enumerate(tasks)]
    summary = "\n".join(task_lines)
    speak(f"You have {len(tasks)} tasks.")
    pyautogui.confirm("Would you like me to read them aloud?", title="To-Do Summary", buttons=["Yes", "No"])
    show_in_chat(summary)
    return f"Here are your tasks for today:\n{summary}"

@register_command("edit todo")
def edit_todo(params):
    if not params or " to " not in params:
        message = "Please say something like: 'Change task 2 to buy groceries.'"
        speak(message)
        return message

    try:
        before, after = params.split(" to ", 1)
        tasks = load_tasks()

        # Try index-based edit
        digits = [int(i) for i in before.split() if i.isdigit()]
        if digits:
            index = digits[0] - 1
            if 0 <= index < len(tasks):
                confirm = pyautogui.confirm(f"Change task {index+1} to: '{after}'?", title="Confirm Edit", buttons=["Yes", "No"])
                if confirm == "Yes":
                    tasks[index] = after.strip()
                    save_tasks(tasks)
                    message = f"Task {index+1} updated to ‘{after.strip()}’."
                    speak(message)
                    show_in_chat(message)
                    return message
                else:
                    return "Edit cancelled."
            else:
                return f"❌ Task {index+1} doesn’t exist."

        # Fuzzy match edit
        match, score, index = process.extractOne(before.strip(), tasks, scorer=fuzz.ratio, score_cutoff=70, return_index=True)
        if match:
            confirm = pyautogui.confirm(f"Change task '{match}' to: '{after}'?", title="Confirm Edit", buttons=["Yes", "No"])
            if confirm == "Yes":
                tasks[index] = after.strip()
                save_tasks(tasks)
                message = f"Updated task to ‘{after.strip()}’."
                speak(message)
                show_in_chat(message)
                return message
            else:
                return "Edit cancelled."
        else:
            return f"❌ Couldn't find a matching task to edit."

    except Exception as e:
        return f"❌ Couldn’t edit task: {e}"

@register_command("delete todo")
def delete_todo(params):
    if not params:
        message = "Please tell me which task to remove (e.g., 'Remove buy milk')."
        speak(message)
        return message

    tasks = load_tasks()
    if not tasks:
        message = "Your to-do list is empty."
        speak(message)
        return message

    match, score, index = process.extractOne(params, tasks, scorer=fuzz.ratio, score_cutoff=70, return_index=True)
    if match is None:
        message = f"I couldn’t find a task similar to ‘{params}’."
        speak(message)
        return message

    confirm = pyautogui.confirm(f"Delete task: ‘{match}’?", title="Confirm Delete", buttons=["Yes", "No"])
    if confirm == "Yes":
        removed = tasks.pop(index)
        save_tasks(tasks)
        message = f"Removed ‘{removed}’ from your to-do list."
        speak(message)
        show_in_chat(message)
        return message
    else:
        return "Deletion cancelled."
