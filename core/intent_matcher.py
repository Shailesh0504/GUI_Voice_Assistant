import json
import os
import re
from rapidfuzz import process, fuzz

COMMANDS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "commands.json")

with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
    command_patterns = json.load(f)

flat_phrases = []
phrase_to_command = {}

for command_key, phrases in command_patterns.items():
    for phrase in phrases:
        phrase_lower = phrase.lower()
        flat_phrases.append(phrase_lower)
        phrase_to_command[phrase_lower] = command_key

def extract_app_name(user_input):
    """Extract app name from open/close app command."""
    match = re.search(r"(?:open|close)(?: application)? (.+)", user_input)
    return match.group(1).strip() if match else None


def match_intent(user_input: str, threshold=85):
    user_input = user_input.strip().lower()
    print(f"🔍 Received input: {user_input}")

    # NLP-style routing
    if any(x in user_input for x in [
        "spell", "check spelling", "how do you spell", "spelling of", "correct spelling", "check the spelling"
    ]):
        return "spell check", user_input

    if user_input.startswith("convert") or "to inr" in user_input or "to usd" in user_input:
        return "convert currency", user_input

    if "how many" in user_input and any(curr in user_input for curr in ["dollars", "rupees", "euros", "liters", "meters", "kilometers"]):
        return "convert units", user_input

    if any(x in user_input for x in ["plus", "minus", "multiply", "divide", "+", "-", "*", "/", "calculate", "solve", "percent", "%"]):
        return "perform calculation", user_input

    if any(x in user_input for x in ["battery", "out of power", "battery level"]):
        return "check battery", user_input

    if any(x in user_input for x in ["screenshot", "screen capture", "take snapshot"]):
        return "take screenshot", user_input

    if any(x in user_input for x in ["translate", "क्या बोलते हैं", "how do you say", "meaning of", "मतलब क्या है"]):
        return "translate text", user_input

    if "remind" in user_input or "reminder" in user_input or "याद दिला" in user_input:
        if "add" in user_input:
            return "add reminder", user_input
        elif "read" in user_input or "what's" in user_input:
            return "read reminder", user_input
        elif "change" in user_input or "edit" in user_input:
            return "edit reminder", user_input
        elif "remove" in user_input or "delete" in user_input:
            return "delete reminder", user_input
        return "set reminder", user_input

    if any(x in user_input for x in ["weather", "rain", "बारिश", "forecast"]):
        return "check weather", user_input

    if any(x in user_input for x in ["news", "headlines", "latest news", "खबरें"]):
        return "read news", user_input

    if any(x in user_input for x in ["joke", "चुटकुला", "funny", "joke sunao"]):
        return "tell joke", user_input

    if any(x in user_input for x in ["time", "clock", "समय", "बजा है"]):
        return "tell time", user_input

    if any(x in user_input for x in ["date", "calendar", "day", "तारीख"]):
        return "tell date", user_input

    # 🔧 App open/close logic (enhanced)
    if user_input.startswith("open"):
        app_name = extract_app_name(user_input)
        if app_name:
            return "open app", app_name
    if user_input.startswith("close"):
        app_name = extract_app_name(user_input)
        if app_name:
            return "close app", app_name

    if any(x in user_input for x in ["shutdown", "power off", "turn off", "shut down"]):
        return "shutdown", user_input

    if "restart" in user_input or "reboot" in user_input:
        return "restart", user_input

    if "logout" in user_input or "sign out" in user_input:
        return "logout", user_input

    if any(x in user_input for x in ["lock", "step away", "just coming", "i will be back", "lock my pc", "lock screen"]):
        return "lock", user_input

    if any(x in user_input for x in [
        "youtube download", "download youtube video", "download youtube audio", "download youtube playlist",
        "download youtube video from url", "download youtube audio from url", "download youtube playlist from url",
        "download youtube video from link", "download youtube audio from link", "download youtube playlist from link"
    ]):
        return "youtube download", user_input

    if "search" in user_input and "google" in user_input:
        return "search google", user_input

    if "wikipedia" in user_input or "tell me about" in user_input:
        return "search wikipedia", user_input

    if "todo" in user_input or "to-do" in user_input:
        if "add" in user_input:
            return "add todo", user_input
        elif "read" in user_input or "what's" in user_input:
            return "read todo", user_input
        elif "change" in user_input or "edit" in user_input:
            return "edit todo", user_input
        elif "remove" in user_input or "delete" in user_input:
            return "delete todo", user_input

    if "alarm" in user_input:
        if "stop all" in user_input:
            return "stop all alarms", user_input
        elif "stop" in user_input or "cancel" in user_input:
            return "stop alarm", user_input
        elif "set" in user_input or "wake me" in user_input:
            return "set alarm", user_input

    if "timer" in user_input or "countdown" in user_input:
        return "set timer", user_input

    if "backup" in user_input or "backup folder" in user_input:
        return "backup folder", user_input

    if "clean" in user_input or "clean temp files" in user_input:
        return "clean temp files", user_input

    if "create note" in user_input or "note" in user_input:
        if "read" in user_input:
            return "read note", user_input
        elif "delete" in user_input:
            return "delete note", user_input
        elif "edit" in user_input:
            return "edit note", user_input
        return "create note", user_input

    if any(x in user_input for x in [
        "stock price", "stock", "share price", "market price", 
        "मुझे स्टॉक प्राइस बताओ", "स्टॉक प्राइस", "शेयर का भाव", "शेयर प्राइस", "भाव बताओ"
    ]):
        return "stock price", user_input

    if any(x in user_input for x in [
        "start screen recording", "record screen", "begin screen recording",
        "start recording my screen", "please record screen",
        "i need to record this meeting", "can you record the screen"
    ]):
        return "start screen recording", user_input

    if any(x in user_input for x in [
        "stop screen recording", "end screen recording", "stop recording",
        "that's all i need", "you can stop now", "please stop the recording"
    ]):
        return "stop screen recording", user_input

    if any(x in user_input for x in [
        "help", "what can you do", "what are your features",
        "show me help", "commands list", "how can you assist"
    ]):
        return "help", user_input

    if "youtube" in user_input or "play song" in user_input or "गाना" in user_input:
        return "play youtube", user_input

    if any(x in user_input for x in [
        "clear recycle bin", "empty recycle bin", "delete recycle bin"
    ]):
        return "clear recycle bin", user_input

    if any(x in user_input for x in flat_phrases if "control youtube" in phrase_to_command.get(x, "")) and "youtube" in user_input:
        return "control youtube", user_input
    
    if "close this tab" in user_input or "close current tab" in user_input or "close this then" in user_input:
        return "control chrome", user_input
    if "क्लोज दिस तब" in user_input or "क्रोम टैब बंद करो" in user_input:
        return "control chrome", user_input

    if any(x in user_input for x in flat_phrases if "control chrome" in phrase_to_command.get(x, "")) and "chrome" in user_input:
        return "control chrome", user_input

    # 🧠 Fuzzy fallback
    candidate_phrases = [p for p in flat_phrases if len(p) > 3 or len(user_input) <= 6]
    match, score, _ = process.extractOne(user_input, candidate_phrases, scorer=fuzz.partial_ratio)

    if score >= threshold:
        command_key = phrase_to_command[match]
        params = re.sub(rf"\b{re.escape(match)}\b", "", user_input).strip()
        print(f"Fuzzy Match: '{match}' → Intent: '{command_key}' (Confidence: {score}%)")
        return command_key, params

    elif 50 <= score < threshold:
        command_key = phrase_to_command.get(match)
        if command_key:
            print(f"🤔 Low-confidence match: '{match}' → Intent: '{command_key}' (Confidence: {score}%)")
            return "uncertain", {
                "suggested_command": command_key,
                "suggested_phrase": match,
                "original_input": user_input
            }

    print(f"❌ No intent matched for input: '{user_input}'")
    return None, user_input
