def normalize_chrome_command(action: str) -> str:
    """
    Maps natural language phrases to standardized Chrome control actions.
    Returns one of the known command keys like: 'new tab', 'close tab', etc.
    """
    action = action.lower().strip()

    mapping = {
        "new tab": [
            "open new tab", "new tab", "chrome tab", "browser tab",
            "ओपन न्यू तब", "नया टैब", "नया टैब खोलो"
        ],
        "close tab": [
            "close tab", "close this tab", "close current tab", "close the tab",
            "close this then", "इस टैब को बंद करो", "tab बंद करो"
        ],
        "reopen tab": ["reopen tab", "reopen closed tab", "last closed tab"],
        "new window": ["new window", "open new window", "नया विंडो"],
        "close window": ["close window", "close this window", "exit chrome"],
        "next tab": [
            "next tab", "switch next tab", "switch to next tab", "go to next tab",
            "switch next then", "अगला टैब", "स्विच नेक्स्ट तब"
        ],
        "previous tab": [
            "previous tab", "switch to previous tab", "last tab", "go back tab",
            "पिछला टैब", "स्विच प्रीवियस तब"
        ],
        "refresh": ["refresh", "reload tab", "refresh chrome", "पेज रिफ्रेश करो"],
        "open history": ["open history", "chrome history", "इतिहास दिखाओ"],
        "open downloads": ["open downloads", "download page", "डाउनलोड खोलो"],
        "incognito": ["incognito", "open incognito", "गुप्त मोड", "private tab"],
        "clear history": [
            "clear history", "delete history", "wipe history",
            "क्रोम हिस्ट्री साफ करो", "इतिहास मिटाओ"
        ]
    }

    for command, phrases in mapping.items():
        if any(phrase in action for phrase in phrases):
            return command

    return action  # return original if nothing matched
