# navigation.py

import webbrowser
import urllib.parse
from core.registry import register_command

@register_command("navigate to")
def navigate_to(location):
    try:
        if not location or not isinstance(location, str):
            raise ValueError("Invalid location provided.")

        # Sanitize input phrase
        cleaned_location = location.lower().strip()
        for prefix in ["navigate to", "where is", "where's", "go to"]:
            if cleaned_location.startswith(prefix):
                cleaned_location = cleaned_location[len(prefix):].strip()
                break

        if not cleaned_location:
            raise ValueError("No location provided after cleaning.")

        # URL encode and generate map URL
        query = urllib.parse.quote_plus(cleaned_location)
        url = f"https://www.google.com/maps/search/?api=1&query={query}"
        webbrowser.open(url)

        # Return feedback message only
        return f"Here is the map for {cleaned_location.title()}"

    except Exception as e:
        return handle_error(f"Error navigating to '{location}': {str(e)}")


def handle_error(error_message):
    print(f"[navigation.py] {error_message}")
    return "Sorry, I couldn't find the location. Please try again."
