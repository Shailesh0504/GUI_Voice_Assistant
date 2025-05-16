import os
import json
from datetime import datetime, timedelta

from core.voice_output import speak
from core.registry import register_command
from gui.message_router import show_in_chat

EXPENSE_FILE = "data/expenses.json"

# Ensure folder and file exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(EXPENSE_FILE):
    with open(EXPENSE_FILE, "w") as f:
        json.dump([], f)

def load_expenses():
    with open(EXPENSE_FILE, "r") as f:
        content = f.read().strip()
        try:
            data = json.loads(content) if content else []
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            print("⚠️ Corrupted expense file. Reinitializing...")
            return []


def save_expenses(data):
    with open(EXPENSE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -------------------- COMMANDS --------------------

@register_command("add expense")
def add_expense(params=None):
    if not params:
        return "❗ Please say something like: 'I spent 200₹ on groceries'"

    words = params.lower().split()
    amount = None
    for word in words:
        try:
            amount = float(word)
            break
        except:
            continue

    if amount is None:
        return "❗ Couldn't detect a valid amount. Try: 'Add expense 150 for lunch'"

    # Basic category detection
    categories = ["groceries", "food", "lunch", "dinner", "transport", "movie", "bills", "shopping", "snacks"]
    category = next((x for x in categories if x in words), "miscellaneous")

    note = params
    entry = {
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    expenses = load_expenses()
    expenses.append(entry)
    save_expenses(expenses)

    show_in_chat(f"💸 Added expense: ₹{amount} for **{category}**")
    speak(f"Expense of {amount} rupees for {category} added.")
    return "Expense recorded."

@register_command("read expenses")
def read_expenses(params=None):
    expenses = load_expenses()
    today = datetime.now().strftime("%Y-%m-%d")
    today_expenses = [e for e in expenses if e['date'] == today]

    if not today_expenses:
        return "📭 No expenses recorded for today."

    response = f"📒 Expenses for {today}:\n"
    for e in today_expenses:
        response += f"- ₹{e['amount']} ({e['category']}) – {e['note']}\n"

    total = sum(e['amount'] for e in today_expenses)
    response += f"\n**Total Today:** ₹{total}"
    show_in_chat(response)
    speak(f"Today's total spending is ₹{total}")
    return "Expenses listed."

@register_command("delete expense")
def delete_expense(params=None):
    expenses = load_expenses()
    if not expenses:
        return "⚠️ No expenses to delete."

    last = expenses.pop()
    save_expenses(expenses)

    show_in_chat(f"🗑️ Deleted last expense: ₹{last['amount']} ({last['category']}) – {last['note']}")
    speak("Last expense deleted.")
    return "Last expense removed."

@register_command("summarize expenses")
def summarize_expenses(params=None):
    expenses = load_expenses()
    if not expenses:
        return "📭 No expenses recorded."

    today = datetime.now().date()

    # Default filter: all time
    filtered_expenses = expenses
    title = "📊 Expense Summary (All Time):"

    if params:
        params = params.lower()
        if "week" in params:
            week_ago = today - timedelta(days=7)
            filtered_expenses = [e for e in expenses if datetime.strptime(e['date'], "%Y-%m-%d").date() >= week_ago]
            title = "📊 Expense Summary (Last 7 Days):"
        elif "month" in params:
            month_ago = today.replace(day=1)
            filtered_expenses = [e for e in expenses if datetime.strptime(e['date'], "%Y-%m-%d").date() >= month_ago]
            title = "📊 Expense Summary (This Month):"

    if not filtered_expenses:
        return "📭 No expenses found for that period."

    summary = {}
    for e in filtered_expenses:
        cat = e['category']
        summary[cat] = summary.get(cat, 0) + e['amount']

    response = title + "\n"
    for cat, amt in summary.items():
        response += f"- {cat.title()}: ₹{amt:.2f}\n"

    total = sum(summary.values())
    response += f"\n**Total:** ₹{total:.2f}"
    show_in_chat(response)
    speak(f"Total spending {('this week' if 'week' in params else 'this month' if 'month' in params else 'overall')} is ₹{int(total)}.")
    return "Filtered summary shown."

