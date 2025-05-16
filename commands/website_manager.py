# commands/website_manager.py

import os
import json
import webbrowser
from rapidfuzz import process
from core.voice_output import speak
from core.registry import register_command
from gui.message_router import show_in_chat

KNOWN_SITES_FILE = os.path.join(os.path.dirname(__file__), "../data/known_sites.json")

def load_sites():
    try:
        with open(KNOWN_SITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}
    
# 🌐 Generic command to list websites using fuzzy category match
@register_command("list websites")
def list_websites(params=None):
    sites = load_sites()

    if not params:
        speak("Please tell me which category you're interested in.")
        return "ℹ️ Available categories: " + ', '.join(sites.keys())

    categories = list(sites.keys())
    query = params.lower().strip()

    # 🎯 Use RapidFuzz to find best category match (with score threshold)
    matched_category, score, _ = process.extractOne(query, categories, score_cutoff=60)

    if not matched_category:
        all_categories = ', '.join(categories)
        speak("Sorry, I couldn't find that category. Available ones are: " + all_categories)
        return f"❌ Unknown category. Available categories: {all_categories}"

    # ✅ Show websites in the matched category
    entries = sites.get(matched_category, {})
    if not entries:
        return f"📭 No websites found in the '{matched_category}' category."

    result_lines = [f"📂 {matched_category.title()} Websites:"]
    for name, url in entries.items():
        result_lines.append(f"• {name} → {url}")

    result = "\n".join(result_lines)
    show_in_chat(result)
    speak(f"I found {len(entries)} website{'s' if len(entries) > 1 else ''} in {matched_category}.")
    return "✅ Website list shown."
