# commands/help.py

from core.registry import register_command
from core.voice_output import speak
import threading
import tkinter as tk
from tkinter import scrolledtext

# Replace this with an import if COMMAND_MAP is stored elsewhere
COMMAND_MAP = {
    "greet": ["hello", "hi", "hey", "good morning", "hey assistant"],
    "mood_check": ["how are you", "how's it going", "how do you feel"],
    "introduce": ["what is your name", "what's your name", "who are you", "introduce yourself"],
    "creator_info": ["who created you", "who made you", "where are you from"],
    "capabilities": ["what can you do", "what do you do", "how do you work", "how do you function"],
    "reality_check": ["are you real", "are you human", "do you remember me", "do you know me", "do you understand me"],
    "gratitude": ["thank you", "thanks", "thanks a lot"],
    "farewell": ["bye", "goodbye", "see you later", "talk to you later", "farewell"],
    "small_talk": ["nice to meet you", "pleasure meeting you", "let's chat", "let's talk"],
    "status_check": [ "what is happening", "what are you working on", "kya ho raha hai", "how's it going" ],
    "motivation": ["motivate me","i need motivation","give me a boost","say something inspiring","encourage me"],
    "fun_fact": [ "tell me a fact", "give me a fun fact", "say something interesting", "random fact please", "what’s a cool fact" ],
    "coffee_time": ["coffee time","i need coffee","let's take a break","time for coffee","coffee suggestion"],
    "tech_tip": [ "tech tip please", "give me a tech tip", "how to be better with tech", "helpful tech advice", "computer tip" ],
    "compliment": [ "give me a compliment", "say something nice", "compliment me", "cheer me up", "make me smile" ],
    "set alarm": ["set alarm", "wake me up at", "alarm for"],
    "set timer": ["set timer", "start timer", "start my workout"],
    "stop alarm": ["stop alarm", "cancel alarm"],
    "set reminder": ["remind me to", "set reminder", "remind"],
    "play youtube": ["play on youtube", "play song", "गाना बजाओ"],
    "open app": ["open", "launch", "start"],
    "close app": ["close", "exit"],
    "tell joke": ["tell me a joke", "joke sunao"],
    "search google": ["search", "google", "look up"],
    "search wikipedia": ["search wikipedia", "on wikipedia", "wikipedia"],
    "shutdown": ["shutdown", "power off"],
    "restart": ["restart", "reboot"],
    "logout": ["logout", "sign out"],
    "lock": ["lock my system", "lock screen"],
    "add todo": ["add task", "write in my to-do", "add to list"],
    "read todo": ["read my tasks", "show to-do"],
    "edit todo": ["edit to-do", "update task"],
    "delete todo": ["delete task", "remove"],
    "tell time": ["what time is it", "current time", "टाइम बताओ"],
    "tell date": ["what's the date", "आज कौन सा दिन है"],
    "check weather": ["will it rain", "weather forecast", "मौसम कैसा है"],
    "read news": ["read news", "top news", "headlines"],
    "translate text": ["translate this", "say in", "translate"],
    "take screenshot": ["screenshot", "capture screen"],
    "check battery": ["battery level", "check battery"],
    "convert units": ["convert units", "how many liters", "unit conversion"],
    "perform calculation": ["calculate", "15% of", "solve"],
    "convert currency": ["convert currency", "usd to inr"],
    "spell check": ["spell check", "how to spell"],
    "backup folder": ["backup folder", "backup my data"],
    "clean temp files": ["clean temp files", "clear temp"],
    "create note": ["create a note", "note", "नोट बनाओ"],
    "stock price": ["stock price", "check share price"],
    "start screen recording": ["start screen recording", "record screen"],
    "stop screen recording": ["stop screen recording"],
    "youtube download": ["download youtube video", "download youtube audio", "download youtube playlist"],
    "play favorite song": ["play favorite song", "play my favorite song", "play something I like", "play from favorite list", "play from my saved songs", "play a song from favorites", "play from favorite folder", "play local favorite song", "start my favorite track", "play a random favorite"],
    "control youtube": [ "pause youtube", "play youtube video", "mute youtube", "unmute youtube", "fullscreen youtube", "exit fullscreen youtube", "turn on captions", "skip ad on youtube", "increase volume on youtube", "decrease volume on youtube", "forward youtube video", "rewind youtube video" ],
    "help": ["help", "what can you do", "commands list"]
    
}

@register_command("help")
def show_help(params=None):
    threading.Thread(
        target=speak,
        args=("Here's the full command reference. I've highlighted your exact matches.",),
        daemon=True
    ).start()
    threading.Thread(target=show_help_gui, daemon=True).start()
    return "Help window opened."


def show_help_gui():
    import tkinter as tk
    from tkinter import scrolledtext

    def populate(text_widget, query=""):
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)

        query = query.lower().strip()
        matched_any = False

        for cmd, triggers in COMMAND_MAP.items():
            cmd_lower = cmd.lower()
            triggers_lower = [t.lower() for t in triggers]

            show = False
            if query == cmd_lower:
                show = True
            elif query in triggers_lower:
                show = True
            elif query in cmd_lower or any(query in trig for trig in triggers_lower):
                show = True
            elif not query:
                show = True

            if show:
                matched_any = True
                text_widget.insert(tk.END, f"{cmd.title()}\n")
                for trig in triggers:
                    text_widget.insert(tk.END, f"  - {trig}\n")
                text_widget.insert(tk.END, "\n")

        if not matched_any:
            text_widget.insert(tk.END, "No matching commands found.\n")

        text_widget.config(state='disabled')

    root = tk.Tk()
    root.title("Smart Assistant Help")
    root.geometry("800x600")
    root.configure(bg="white")
    root.resizable(False, False)

    title = tk.Label(
        root, text="Smart Assistant – Help & Commands",
        font=("Segoe UI", 16),
        bg="white", fg="black"
    )
    title.pack(pady=10)

    search_frame = tk.Frame(root, bg="white")
    search_frame.pack(pady=5)

    search_var = tk.StringVar()

    def on_search(event=None):
        term = search_var.get()
        populate(help_area, term)

    search_entry = tk.Entry(
        search_frame, textvariable=search_var,
        font=("Segoe UI", 12), width=50,
        bg="white", fg="black", insertbackground="black",
        relief=tk.GROOVE, bd=1
    )
    search_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=4)
    search_entry.focus_set()
    search_entry.bind('<Return>', on_search)

    search_button = tk.Button(
        search_frame, text="Search",
        font=("Segoe UI", 10),
        bg="#dddddd", fg="black", activebackground="#cccccc",
        padx=10, pady=2,
        command=on_search
    )
    search_button.pack(side=tk.LEFT)

    help_area = scrolledtext.ScrolledText(
        root, wrap=tk.WORD,
        font=("Segoe UI", 11), height=25,
        bg="white", fg="black", insertbackground="black",
        relief=tk.GROOVE, borderwidth=1
    )
    help_area.pack(padx=12, pady=12, fill=tk.BOTH, expand=True)

    close_btn = tk.Button(
        root, text="Close", font=("Segoe UI", 10),
        bg="#dddddd", fg="black", command=root.destroy,
        padx=10, pady=4
    )
    close_btn.pack(pady=10)

    populate(help_area)
    root.mainloop()
