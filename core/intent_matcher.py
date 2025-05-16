import json
import os
import re
from rapidfuzz import process, fuzz

COMMANDS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "commands.json")
KNOWN_WEBSITES = ["google", "youtube", "linkedin", "github", "gmail", "chatgpt", "glpi", "facebook", "instagram", "twitter"]


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
    
    if any(user_input.startswith(p) for p in ["add task", "add this to my list", "remind me to", "note to"]):
        for prefix in ["add task", "add this to my list", "remind me to", "note to"]:
            if user_input.startswith(prefix):
                return "add todo", user_input[len(prefix):].strip()


    # Standard todo/to-do logic
    if "todo" in user_input or "to-do" in user_input:
        if any(x in user_input for x in ["add", "write", "create"]):
            return "add todo", user_input
        elif any(x in user_input for x in ["read", "show", "what's", "list", "display"]):
            return "read todo", user_input
        elif any(x in user_input for x in ["edit", "change", "update", "modify"]):
            return "edit todo", user_input
        elif any(x in user_input for x in ["remove", "delete", "clear"]):
            return "delete todo", user_input
        else:
            return "read todo", user_input  # Fallback: assume read if unsure
            
    # 🧠 Memory Log Intents
    if any(x in user_input for x in flat_phrases if "add memory" in phrase_to_command.get(x, "")):
        return "add memory", user_input

    # 🧠 Smart memory lookup detection
    if any(x in user_input for x in flat_phrases if "read memory" in phrase_to_command.get(x, "")):
        return "read memory", user_input

    # Catch common phrasing like: "what is my X", "do you remember my Y"
    if re.search(r"\bwhat( is|'s)? my\b", user_input) or "check in your memory" in user_input or "do you remember" in user_input:
        return "read memory", user_input

    # Bonus fallback: catch private info queries
    if "delete my" in user_input or "forget my" in user_input:
        return "delete memory", user_input

    if "show memory" in user_input or "show memories" in user_input:
        return "list memories", user_input

    if any(x in user_input for x in flat_phrases if "update memory" in phrase_to_command.get(x, "")):
        return "update memory", user_input



    if any(x in user_input for x in ["+", "-", "*", "/", "percent", "%", "calculate", "multiply", "divide", "add", "subtract"]):
        return "perform calculation", user_input

    if re.search(r"\bwhat is\b", user_input) and re.search(r"\d", user_input):
        return "perform calculation", user_input

    if any(x in user_input for x in ["battery", "out of power", "battery level"]):
        return "check battery", user_input

    if any(x in user_input for x in ["screenshot", "screen capture", "take snapshot"]):
        return "take screenshot", user_input

    if any(x in user_input for x in ["translate", "क्या बोलते हैं", "how do you say", "meaning of", "मतलब क्या है"]):
        return "translate text", user_input

    if "remind" in user_input or "reminder" in user_input or "याद दिला" in user_input:        
        if any(word in user_input for word in ["list", "show", "what's", "read", "check"]):
            return "list reminders", None
        elif any(word in user_input for word in ["clear", "remove", "delete"]):
            return "clear reminders", None
        elif any(word in user_input for word in ["change", "edit", "update", "modify"]):
            return "edit reminder", user_input
        elif re.search(r'\d{1,2}(:\d{2})?\s?(am|pm)', user_input) or \
            any(word in user_input for word in ["tomorrow", "today"]) or \
            re.search(r'(\d{1,2})\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', user_input):
            return "set reminder", user_input
        return "list reminders", None

    if any(x in user_input for x in ["weather", "rain", "बारिश", "forecast"]):
        return "check weather", user_input

    if any(x in user_input for x in ["news", "headlines", "latest news", "खबरें"]):
        return "read news", user_input

    if any(x in user_input for x in ["joke", "चुटकुला", "funny", "joke sunao"]):
        return "tell joke", user_input
    
    # 🧭 Known website detection
    if user_input.startswith("open") or user_input.startswith("visit") or "launch" in user_input:
        for site in KNOWN_WEBSITES:
            if site in user_input:
                return "open website", user_input
            
    if user_input.startswith("add") and ("http://" in user_input or "https://" in user_input):
        return "add website", user_input
    
    if any(x in user_input for x in ["list", "show", "display", "reveal"]):
        if any(y in user_input for y in ["website", "websites", "site", "sites", "tools", "category", "ai", "dev", "games", "movies", "social", "education"]):
            return "list websites", user_input

    
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

    

    if any(x in user_input for x in ["alarm", "wake me", "set alarm", "alarm at"]):
        if "stop all" in user_input or "cancel all" in user_input:
            return "stop all alarms", user_input
        elif any(x in user_input for x in ["stop", "cancel", "remove", "delete"]) and "alarm" in user_input:
            return "stop alarm", user_input
        elif any(x in user_input for x in ["set", "wake me", "add", "create", "alarm at", "alarm for"]):
            return "set alarm", user_input


    # 🎯 Handle natural timer phrases early
    if any(re.search(rf"\b{kw}\b", user_input) for kw in [
    "set timer", "start timer", "timer for", "countdown for"
    ]) or re.search(r'\b\d+\s*(min|minute|minutes|sec|second|seconds)\b', user_input):
        return "set timer", user_input


    if "backup" in user_input or "backup folder" in user_input:
        return "backup folder", user_input    
    
    if any(x in user_input for x in ["time", "clock", "समय", "बजा है"]):
        return "tell time", user_input

    if any(x in user_input for x in ["date", "calendar", "day", "तारीख"]):
        return "tell date", user_input

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

    if any(x in user_input for x in [
        "clear recycle bin", "empty recycle bin", "delete recycle bin"
    ]):
        return "clear recycle bin", user_input

    if any(
        phrase in user_input
        for phrase in flat_phrases
        if phrase_to_command.get(phrase) == "control youtube"
    ):
        return "control youtube", user_input

    
    # 🌐 Control Chrome intent detection
    if any(
        phrase in user_input
        for phrase in flat_phrases
        if phrase_to_command.get(phrase) == "control chrome"
    ):
        return "control chrome", user_input

    # Additional specific phrases (not in flat_phrases or not reliably mapped)
    if any(x in user_input for x in [
        "close this tab", "close current tab", "close this then",
        "क्लोज दिस तब", "क्रोम टैब बंद करो"
    ]):
        return "control chrome", user_input

    
    if any(x in user_input for x in flat_phrases if "disk usage" in phrase_to_command.get(x,"")) and "ram status" in user_input:
        return "check disk", user_input    
       
    if any(x in user_input for x in flat_phrases if "navigate to" in phrase_to_command.get(x,"")) and ("navigate" in user_input or "where is" in user_input):
        return "navigate to", user_input
    
    if any(
        phrase in user_input
        for phrase in flat_phrases
        if phrase_to_command.get(phrase) == "play favorite song"
    ):
        return "play favorite song", user_input
    
    if "play favorite song" in user_input:
        return "play favorite song", user_input
    
    if any(
        phrase in user_input
        for phrase in flat_phrases
        if phrase_to_command.get(phrase) == "play youtube"
    ):
        return "play youtube", user_input

    # Bonus fallback
    if "youtube" in user_input or "play" in user_input:
        return "play youtube", user_input
    
    if any(x in user_input for x in flat_phrases if "check internet speed" in phrase_to_command.get(x,"")) and (
        "इंटरनेट" in user_input and "स्पीड" in user_input
    ):
        return "check internet speed", user_input
    
    if any(x in user_input for x in flat_phrases if "show wifi password" in phrase_to_command.get(x,"")) and "wifi" in user_input:
        return "show wifi password", user_input
    
    
    
    if any(x in user_input for x in flat_phrases if "ping" in phrase_to_command.get(x,"")) and "ping" in user_input:
        return "ping", user_input
    
    # 🔁 Habit Coach Commands (JSON + keyword enhanced)
    if any(phrase in user_input for phrase in flat_phrases):
        for phrase in flat_phrases:
            if phrase in user_input:
                command_key = phrase_to_command.get(phrase)

                # Refine for habit logic
                if command_key == "add habit" and any(x in user_input for x in ["add", "track", "create", "start"]):
                    return "add habit", user_input
                if command_key == "read habit" and any(x in user_input for x in ["read", "show", "list", "what", "view"]):
                    return "read habit", user_input
                if command_key == "delete habit" and any(x in user_input for x in ["delete", "remove", "clear", "cancel", "stop"]):
                    return "delete habit", user_input   

                
             

    # 💸 Expense Tracker Intents
    if any(x in user_input for x in flat_phrases if "add expense" in phrase_to_command.get(x, "")):
        return "add expense", user_input

    if any(x in user_input for x in flat_phrases if "read expenses" in phrase_to_command.get(x, "")):
        return "read expenses", user_input

    if any(x in user_input for x in flat_phrases if "delete expense" in phrase_to_command.get(x, "")):
        return "delete expense", user_input

    if any(x in user_input for x in flat_phrases if "summarize expenses" in phrase_to_command.get(x, "")):
        if "week" in user_input:
            return "summarize expenses", "this week"
        elif "month" in user_input:
            return "summarize expenses", "this month"
        return "summarize expenses", ""




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
