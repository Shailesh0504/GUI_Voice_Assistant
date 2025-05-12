import importlib
import pkgutil
import os
from core.registry import command_registry
from core.intent_matcher import match_intent

def load_all_modules():
    """
    Dynamically imports all Python modules from the 'commands' folder.
    Ensures that all decorated command functions are registered at runtime.
    """
    commands_dir = os.path.join(os.path.dirname(__file__), "..", "commands")
    for finder, name, ispkg in pkgutil.iter_modules([commands_dir]):
        if not name.startswith("_"):
            importlib.import_module(f"commands.{name}")

def dispatch(user_input: str) -> str:
    """
    Matches user input to a command using intent matcher, and routes it to the corresponding function.
    """
    command_key, params = match_intent(user_input)

    # ✅ Friendly handling for social/polite acknowledgements
    if command_key == "acknowledge":
        return params  # contains preformatted friendly response

    # ✅ Route to matched command
    if command_key in command_registry:
        try:
            return command_registry[command_key](params)
        except Exception as e:
            return f"⚠️ Error while executing command: {e}"

    return "🤖 Sorry, I didn't understand that command."

# Load all feature modules at import time
load_all_modules()
