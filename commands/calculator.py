# commands/calculator.py

import re
import pyautogui
import unicodedata
from core.registry import register_command
from core.voice_output import speak

@register_command("perform calculation")
def perform_calculation(params=None):
    """
    Safely parses and evaluates voice-based or text-based math input.
    Handles percentages, basic math, smart punctuation, and filler words.
    """

    if not params:
        return "Please tell me what you'd like to calculate. For example: '15% of 3500'."

    # Step 1: Normalize and clean input
    expression = unicodedata.normalize("NFKD", params).encode("ascii", "ignore").decode("ascii")
    expression = expression.lower().replace(",", "")
    expression = expression.replace("×", "*").replace("x", "*").replace("^", "**")

    # Step 2: Remove filler words that break eval
    filler_words = [
        "what is", "what's", "calculate", "solve", "find", "equals", "is",
        "please", "tell me", "how much is", "answer", "of", "?", "="
    ]
    for word in filler_words:
        expression = expression.replace(word, "")

    expression = expression.strip()

    # Step 3: Replace percent phrases like "15% 3500" or "15% of 3500"
    # Detect `15%` followed by a number (with or without "of")
    percent_pattern = re.search(r"(\d+(\.\d+)?)\s*%(?:\s*of)?\s*(\d+(\.\d+)?)", expression)
    if percent_pattern:
        percent = float(percent_pattern.group(1))
        base = float(percent_pattern.group(3))
        expression = f"({percent} / 100) * {base}"
        description = f"{percent}% of {base}"
    else:
        description = expression

    # Step 4: Ask user to confirm
    confirm = pyautogui.confirm(
        title="Perform Calculation",
        text=f"Shall I calculate {description} for you?",
        buttons=["Yes", "No"]
    )

    if confirm != "Yes":
        return "Okay, cancelled the calculation."

    # Step 5: Try to evaluate
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        speak(f"The result is {result}")
        return f"Result: {result}"
    except Exception as e:
        return f"❌ Could not perform the calculation: {e}"
