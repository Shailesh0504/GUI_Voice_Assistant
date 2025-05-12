# commands/news_reader.py

import webbrowser
from core.registry import register_command

@register_command("read news")
def read_news(params=None):
    """
    Opens top Indian news headlines directly without asking.
    """
    webbrowser.open("https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en")
    return "Opening today’s top news headlines from India..."
