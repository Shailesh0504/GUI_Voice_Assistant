import os
import json
from datetime import datetime

from core.voice_output import speak
from core.registry import register_command
from gui.message_router import show_in_chat

MEMORY_FILE = "data/memories.json"

# Ensure file exists
os.makedirs("data", exist_ok=True)
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

def load_memories():
    with open(MEMORY_FILE, "r") as f:
        content = f.read().strip()
        try:
            data = json.loads(content) if content else []
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def save_memories(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -------------------- CORE FUNCTIONS --------------------

@register_command("add memory")
def add_memory(params=None):
    if not params:
        return "❗ Please say what you'd like me to remember."

    text = params.strip()
    tags = [word.lower() for word in text.split() if len(word) > 3 and word.isalnum()]

    entry = {
        "text": text,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": tags
    }

    memories = load_memories()
    memories.append(entry)
    save_memories(memories)

    show_in_chat(f"🧠 Got it! I’ll remember this:\n→ {entry['text']}")
    speak("Okay, I've stored that in memory.")
    return "Memory stored."


@register_command("read memory")
def read_memory(params=None):
    if not params:
        return "❗ Please specify what you're looking for."

    query = params.strip().lower()
    query_words = query.split()
    memories = load_memories()

    matches = [
        m for m in memories
        if any(word in m['text'].lower() for word in query_words)
        or any(word in tag.lower() for word in query_words for tag in m.get('tags', []))
    ]

    if not matches:
        keywords = ", ".join([w for w in query_words if len(w) > 2])
        response = f"🤔 I checked my memory, but I couldn’t find anything related to '{keywords}'."
        show_in_chat(response)
        speak("I don’t have anything about that in memory yet.")
        return response

    response = f"🔍 Found {len(matches)} matching memory item(s):\n"
    for m in matches:
        response += f"- {m['text']} (🗓️ {m['date']})\n"

    show_in_chat(response.strip())
    speak(f"I found {len(matches)} memory item{'s' if len(matches) > 1 else ''} related to your query.")
    return "Memory retrieved."




@register_command("delete memory")
def delete_memory(params=None):
    if not params:
        return "❗ Please tell me what memory you want me to forget."

    query = params.strip().lower()
    query_words = query.split()

    memories = load_memories()
    matches = [
        m for m in memories
        if any(word in m['text'].lower() for word in query_words)
        or any(word in tag.lower() for word in query_words for tag in m.get('tags', []))
    ]

    if not matches:
        return f"⚠️ No memory found matching '{query}'."

    # Remove matched memories
    remaining = [m for m in memories if m not in matches]
    save_memories(remaining)

    show_in_chat(f"🗑️ Deleted {len(matches)} memory item(s) matching '{query}'.")
    speak(f"Deleted {len(matches)} memory item{'s' if len(matches) > 1 else ''}.")
    return "Memory deleted."



@register_command("list memories")
def list_memories(params=None):
    memories = load_memories()

    if not memories:
        return "📭 I don’t have any memories saved yet."

    response = "📚 All Stored Memories:\n"
    for m in memories:
        response += f"- {m['text']} (🗓️ {m['date']})\n"

    show_in_chat(response.strip())
    speak(f"You have {len(memories)} memory item{'s' if len(memories) > 1 else ''} stored.")
    return "Memories listed."


@register_command("update memory")
def update_memory(params=None):
    if not params:
        return "❗ Please tell me which memory you'd like to update."

    query = params.strip().lower()
    query_words = query.split()
    memories = load_memories()

    # Match memories by text or tags
    matches = [
        m for m in memories
        if any(word in m['text'].lower() for word in query_words)
        or any(word in tag.lower() for word in query_words for tag in m.get('tags', []))
    ]

    if not matches:
        return f"⚠️ No memory found matching '{query}'."

    if len(matches) > 1:
        show_in_chat(f"⚠️ Found {len(matches)} matches. Please be more specific.")
        speak("I found multiple matching memories. Can you be more specific?")
        return "Too many matches."

    old_memory = matches[0]
    show_in_chat(f"📝 Old memory: {old_memory['text']}")
    speak("What should I update it to?")

    # 🔄 Smart voice or text input
    try:
        from core.voice_input import listen
        new_text = listen().strip()
    except Exception:
        speak("Voice input not available. Please type the updated memory.")
        new_text = input("✏️ Type the new memory: ").strip()

    if not new_text:
        return "❗ I didn’t catch the new memory."

    # 🧠 Extract new tags or fallback to old ones
    new_tags = [word for word in new_text.lower().split() if len(word) > 3 and word.isalnum()]
    if not new_tags:
        new_tags = old_memory.get("tags", [])
        speak("The updated memory is vague, so I'm keeping the original keywords for better search.")

    updated = {
        "text": new_text,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": new_tags
    }

    # Replace only the matched memory
    updated_memories = [updated if m == old_memory else m for m in memories]
    save_memories(updated_memories)

    show_in_chat(f"✅ Memory updated to:\n→ {updated['text']}")
    speak("Got it. I've updated that memory.")
    return "Memory updated."
