# commands/google_search.py

import webbrowser
from core.registry import register_command

@register_command("search google")
def search_on_google(params):
    """
    Opens the given query on Google.
    Examples:
        - "search for python tutorial"
        - "google cricket score"
    """
    if not params:
        return "Please tell me what to search on Google."

    query = params.strip().replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

    return f"Searching on Google for: {params}"
