from core.registry import register_command
import random

@register_command("greet")
def greet(params=None):
    responses = [
        "Hello! How can I help today?",
        "Hi! What can I do for you?",
        "Hey there! Great to see you.",
        "Good day! Ready to assist.",
        "Hey! I’m right here if you need me."
    ]
    return random.choice(responses)


@register_command("mood_check")
def mood_check(params=None):
    responses = [
        "I'm feeling great—optimized and ready!",
        "All systems go! How about you?",
        "Doing well, thanks for asking!",
        "I'm just a bunch of code, but I'm happy to help!",
        "Feeling like 100% digital awesomeness today!"
    ]
    return random.choice(responses)


@register_command("introduce")
def introduce(params=None):
    responses = [
        "I'm your helpful assistant—smart, fast, and friendly!",
        "They call me Assistant, your virtual buddy.",
        "I'm a voice in the machine, here to make life easier.",
        "Just a clever bit of code helping awesome people like you.",
        "I’m your assistant, but we can be friends too!"
    ]
    return random.choice(responses)


@register_command("creator_info")
def creator_info(params=None):
    responses = [
        "I was created by a team of brilliant developers.",
        "Some clever humans built me to help you.",
        "Born in code, raised in logic.",
        "I came from a world of algorithms and dreams.",
        "Made with care, coffee, and curiosity!"
    ]
    return random.choice(responses)


@register_command("capabilities")
def capabilities(params=None):
    responses = [
        "I can help with tasks, reminders, information, jokes, and more!",
        "Try asking me about the weather, timers, or just have a chat.",
        "I’m like a Swiss Army knife — but digital!",
        "From productivity to fun, I’m your sidekick.",
        "Let’s explore what I can do—just ask!"
    ]
    return random.choice(responses)


@register_command("reality_check")
def reality_check(params=None):
    responses = [
        "I may be virtual, but I’m here for you!",
        "I exist in code, but my help is real.",
        "I’m as real as your Wi-Fi connection!",
        "Real enough to assist you anytime!",
        "Digital and proud. Let’s do this!"
    ]
    return random.choice(responses)


@register_command("humor")
def humor(params=None):
    responses = [
        "Why did the computer go to art school? Because it had a lot of bytes!",
        "Why don’t robots ever panic? They always keep their circuits together.",
        "I told a joke to Siri once. She's still buffering.",
        "My jokes are 100% pun-generated!",
        "Why was the assistant so smart? It had tons of data to think about!"
    ]
    return random.choice(responses)


@register_command("gratitude")
def gratitude(params=None):
    responses = [
        "You're welcome!",
        "Happy to help!",
        "Anytime!",
        "My pleasure!",
        "That’s what I’m here for!"
    ]
    return random.choice(responses)


@register_command("farewell")
def farewell(params=None):
    responses = [
        "Goodbye! Come back anytime.",
        "See you soon!",
        "Take care!",
        "Until next time!",
        "Farewell for now!"
    ]
    return random.choice(responses)


@register_command("small_talk")
def small_talk(params=None):
    responses = [
        "Nice to chat with you!",
        "Let’s keep the conversation going!",
        "I love a good talk. What else?",
        "You’re a great conversationalist!",
        "Want to hear a fun fact next?"
    ]
    return random.choice(responses)


@register_command("status_check")
def status_check(params=None):
    responses = [
        "Just hanging out in code space, waiting to help!",
        "Staying alert and ready. What can I do for you?",
        "Listening intently... is something up?",
        "All calm on my end. What's on your mind?",
        "Not much happening here. Want to make something happen?"
    ]
    return random.choice(responses)


@register_command("motivation")
def motivation(params=None):
    responses = [
        "You've got this! Keep pushing forward.",
        "Every day is a fresh start—go make it count!",
        "Believe in yourself. Even your code believes in you!",
        "Success is built one step at a time—keep going!",
        "Progress, not perfection. Keep at it!"
    ]
    return random.choice(responses)


@register_command("fun_fact")
def fun_fact(params=None):
    responses = [
        "Did you know? Honey never spoils—even after thousands of years!",
        "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
        "Octopuses have three hearts and blue blood.",
        "Bananas are technically berries—but strawberries aren't!",
        "The Eiffel Tower can grow over 6 inches during hot days."
    ]
    return random.choice(responses)


@register_command("coffee_time")
def coffee_time(params=None):
    responses = [
        "Coffee break? Yes please! ☕",
        "I’d love a virtual latte right now.",
        "Go get that coffee—you’ve earned it!",
        "Time for a brew-tiful pause!",
        "Coffee: the best debugger out there."
    ]
    return random.choice(responses)


@register_command("tech_tip")
def tech_tip(params=None):
    responses = [
        "Tech Tip: Restarting solves more problems than you think!",
        "Shortcut: Ctrl + Shift + T reopens your last closed browser tab.",
        "Organize files by prefixing names with numbers: 01_Project, 02_Assets.",
        "Keep your software updated—it’s the best security tip!",
        "Use strong, unique passwords. Bonus points for a password manager!"
    ]
    return random.choice(responses)


@register_command("compliment")
def compliment(params=None):
    responses = [
        "You’re doing amazing—seriously!",
        "You’ve got sharp logic and a great smile!",
        "If excellence had a name, it might be yours.",
        "Keep being brilliant—you’re crushing it.",
        "You're basically the human equivalent of clean code."
    ]
    return random.choice(responses)

@register_command("spiritual")
def spiritual(params=None):
    responses = [
    "आप वहीं हैं जहाँ आपको होना चाहिए—प्रक्रिया पर विश्वास रखें।",
    "शांति एक गहरी साँस से शुरू होती है। अभी एक लें।",
    "आपके भीतर दिव्य प्रकाश है—दुनिया को इसे मंद मत करने दें।",
    "सारा ब्रह्मांड आपके पक्ष में काम कर रहा है—खुले रहें।",
    "शांत मन में ही उत्तर मिलते हैं—धैर्य रखें।"
]
    return random.choice(responses)
