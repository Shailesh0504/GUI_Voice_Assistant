import webbrowser
import re
import urllib.parse
from core.registry import register_command
from rapidfuzz import fuzz

TRIGGER_KEYWORDS = [
    "play", "search", "open", "watch", "show",
    "song", "video", "channel", "news",
    "on youtube", "from youtube", "youtube par", "youtube pe", "you tube", "youtub", "you tub", "yt",
    "on", "the", "my", 
    "गाना", "सॉन्ग", "वीडियो", "बजाओ", "चलाओ", "सुनाओ", "चैनल", "न्यूज़", "यूट्यूब", "यूट्यूब पर"
]

@register_command("play youtube")
def play_youtube(params):
    if not params or not params.strip():
        return "Please tell me what song or video you'd like to play on YouTube."

    query = params.lower().strip()

    # Fuzzy keyword stripping
    words = query.split()
    clean_words = []
    for word in words:
        if not any(fuzz.partial_ratio(word, kw) > 85 for kw in TRIGGER_KEYWORDS):
            clean_words.append(word)

    # Reassemble cleaned query
    cleaned_query = " ".join(clean_words).strip()
    if not cleaned_query:
        return "I need a song or video name to play. Please try again."

    display_query = cleaned_query.title()
    encoded_query = urllib.parse.quote_plus(cleaned_query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    webbrowser.open(url)
    return f"Searching YouTube for: *{display_query}*"
