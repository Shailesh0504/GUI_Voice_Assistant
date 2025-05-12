# commands/wikipedia_search.py

try:
    import wikipedia
    from wikipedia.exceptions import DisambiguationError, PageError
except ImportError:
    wikipedia = None
    DisambiguationError = PageError = Exception  # fallback to avoid NameError

from core.registry import register_command

@register_command("search wikipedia")
def search_wikipedia(params):
    """
    Search Wikipedia and return the first summary paragraph.
    Example:
      "Search Ramayana on Wikipedia"
      "Tell me about Artificial Intelligence"
    """
    if wikipedia is None:
        return "❌ Wikipedia search feature is unavailable. Please install the 'wikipedia' module."

    if not params or not str(params).strip():
        return "Please tell me what to search on Wikipedia."

    try:
        # Detect Hindi characters (basic Unicode check)
        lang = "hi" if any(c in str(params) for c in "अआइईउऊएऐओऔकखगघचछजझ") else "en"
        wikipedia.set_lang(lang)
        summary = wikipedia.summary(params.strip(), sentences=2)
        return f"According to Wikipedia:\n{summary}"
    

    except DisambiguationError as e:
        return f"That topic is too broad. Did you mean: {', '.join(e.options[:3])}?"
    except PageError:
        return "❌ No page found on Wikipedia for that topic."
    except Exception as e:
        return f"⚠️ Error searching Wikipedia: {str(e)}"
