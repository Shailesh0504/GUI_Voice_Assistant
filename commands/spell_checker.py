# commands/spell_checker.py

import re
from core.registry import register_command
from core.voice_output import speak

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None

@register_command("spell check")
def spell_check(params=None):
    """
    Spell-checks a word or phrase and suggests correction.
    Supports inputs like:
    - 'Check spelling of definitely'
    - 'How do you spell recieve'
    - 'Spell accomodate'
    """
    if TextBlob is None:
        return "❌ Spell checker is unavailable because the 'textblob' module is not installed."

    if not params or not params.strip():
        return "🔤 Please say the word or sentence you want to spell-check."

    match = re.search(r"(?:spell(?:ing)?(?: of)?\s)?([a-zA-Z\s'-]+)", params, re.IGNORECASE)
    phrase = match.group(1).strip() if match else params.strip()

    if not phrase or len(phrase.split()) > 5:
        return "⚠️ Please provide a short word or phrase to check."

    blob = TextBlob(phrase)
    corrected = str(blob.correct())

    if corrected.lower() == phrase.lower():
        return f"✅ The spelling of '{phrase}' looks correct."

    response = f"📝 The corrected spelling is: '{corrected}'"
    speak(response)
    return response
