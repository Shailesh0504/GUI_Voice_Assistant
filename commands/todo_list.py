# commands/todo_list.py

import json
import os
import pyautogui
from core.registry import register_command

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
        return "What should I add to your to-do list?"
    tasks = load_tasks()
    tasks.append(params.strip())
    save_tasks(tasks)
    return f"Done—‘{params.strip()}’ is on your list."

@register_command("read todo")
def read_todo(params=None):
    tasks = load_tasks()
    if not tasks:
        return "Your to-do list is empty."

    task_lines = [f"{i+1}. {task}" for i, task in enumerate(tasks)]
    summary = "\n".join(task_lines)

    pyautogui.confirm("Would you like me to read them aloud?", title="To-Do Summary", buttons=["Yes", "No"])
    return f"Here are your tasks for today:\n{summary}"

@register_command("edit todo")
def edit_todo(params):
    if not params or " to " not in params:
        return "Please say something like: 'Change task 2 to buy groceries.'"

    try:
        before, after = params.split(" to ", 1)
        index = int([i for i in before.split() if i.isdigit()][0]) - 1
        tasks = load_tasks()

        if 0 <= index < len(tasks):
            confirm = pyautogui.confirm(f"Change task {index+1} to: '{after}'?", title="Confirm Edit", buttons=["Yes", "No"])
            if confirm == "Yes":
                tasks[index] = after.strip()
                save_tasks(tasks)
                return f"Task {index+1} updated to ‘{after.strip()}’."
            else:
                return "Edit cancelled."
        else:
            return f"❌ Task {index+1} doesn’t exist."

    except Exception as e:
        return f"❌ Couldn’t edit task: {e}"

@register_command("delete todo")
def delete_todo(params):
    if not params:
        return "Please tell me which task to remove (e.g., 'Remove buy milk')."

    tasks = load_tasks()
    match = next((i for i, task in enumerate(tasks) if params.lower() in task.lower()), None)

    if match is None:
        return f"I couldn’t find a task matching ‘{params}’."

    confirm = pyautogui.confirm(f"Delete task: ‘{tasks[match]}’?", title="Confirm Delete", buttons=["Yes", "No"])
    if confirm == "Yes":
        removed = tasks.pop(match)
        save_tasks(tasks)
        return f"Removed ‘{removed}’ from your to-do list."
    else:
        return "Deletion cancelled."
