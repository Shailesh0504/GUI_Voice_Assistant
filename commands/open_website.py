import os
import json
import webbrowser
from core.registry import register_command
from core.voice_output import speak
from gui.message_router import show_in_chat

KNOWN_SITES_FILE = os.path.join(os.path.dirname(__file__), "../data/known_sites.json")

def load_known_sites():
    try:
        with open(KNOWN_SITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_known_sites(data):
    with open(KNOWN_SITES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@register_command("open website")
def open_website(params=None):
    if not params:
        speak("Please tell me which website you'd like to open.")
        return "No input provided."

    query = params.strip().lower()
    sites = load_known_sites()

    for category, links in sites.items():
        for name, url in links.items():
            if name in query:
                webbrowser.open(url)
                speak(f"Opening {name} from {category} category.")
                show_in_chat(f"🌐 Opening: {url}")
                return f"Opened: {url}"

    # fallback
    if "." in query:
        url = f"https://{query}"
        webbrowser.open(url)
        speak(f"Opening {url}")
        show_in_chat(f"🌐 Opening: {url}")
        return f"Opened: {url}"

    return "❌ Site not recognized."
