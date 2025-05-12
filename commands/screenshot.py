# commands/screenshot.py

import os
from datetime import datetime
import pyautogui
from core.registry import register_command
from core.voice_output import speak

@register_command("take screenshot")
def take_screenshot(params=None):
    """
    Captures and saves a screenshot with a timestamped filename.
    Asks the user for confirmation before proceeding.
    """

    try:
        user_choice = pyautogui.confirm(
            title="Screenshot",
            text="🖼️ Got it—should I take a screenshot and save it?",
            buttons=["Yes", "No"]
        )

        if user_choice != "Yes":
            return "❎ Screenshot cancelled."

        # Prepare save directory
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        # Create timestamped filename
        filename = datetime.now().strftime("screenshot_%Y-%m-%d_%H-%M-%S.png")
        filepath = os.path.join(screenshot_dir, filename)

        # Capture and save screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)

        speak("Screenshot saved successfully.")
        return f"📸 Screenshot saved as:\n{filepath}"

    except Exception as e:
        return f"❌ Failed to capture screenshot: {e}"
