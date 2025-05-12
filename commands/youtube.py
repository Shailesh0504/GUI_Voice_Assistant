import webbrowser
import re
import urllib.parse
from core.registry import register_command

# Common filler and trigger words to strip from the query
TRIGGER_KEYWORDS = [
    "play song", "song", "video", "on youtube", "from youtube", "youtube par", "search",
    "गाना", "सॉन्ग", "वीडियो", "बजाओ", "चलाओ", "सुनाओ", "यूट्यूब", "यूट्यूब पर"
]

@register_command("play youtube")
def play_youtube(params):
    """
    Cleans up the spoken input and opens a YouTube search for the query.
    Supports English and Hindi mix commands.
    """
    if not params or not params.strip():
        return "Please tell me what song or video you'd like to play on YouTube."

    # Step 1: Normalize and strip filler/trigger words
    query = params.lower()

    for keyword in TRIGGER_KEYWORDS:
        query = re.sub(rf"\b{re.escape(keyword.lower())}\b", "", query, flags=re.IGNORECASE)

    query = re.sub(r"\s+", " ", query).strip()

    if not query:
        return "I need a song or video name to play. Please try again."

    # Step 2: Construct YouTube search URL
    search_query = f"{query} song"
    encoded_query = urllib.parse.quote_plus(search_query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    # Step 3: Open in browser
    webbrowser.open(url)
    return f"Searching YouTube for: *{query}*"
