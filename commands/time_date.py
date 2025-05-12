# commands/time_date.py

from datetime import datetime
from core.registry import register_command

@register_command("tell time")
def tell_time(params=None):
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    full_date = now.strftime("%A, %d %B %Y")

    return f"Right now is {current_time}.\nToday is {full_date}."

@register_command("tell date")
def tell_date(params=None):
    now = datetime.now()
    full_date = now.strftime("%A, %d %B %Y")
    return f"Today is {full_date}."
