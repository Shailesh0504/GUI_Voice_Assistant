# 🤖 Smart Voice + GUI Assistant

An intelligent, multilingual, and modular AI assistant with a modern GUI interface.  
Supports voice & text input, contextual interaction, alarms, reminders, timers, media control, and real-time system monitoring like battery status alerts — all in a futuristic and user-friendly design.

---

## 🚀 Features

🚀 Features
🎤 Voice & Text Input
Understands both Hindi and English commands naturally via speech or keyboard.

🧠 Context-Aware Intent Detection
Recognizes commands like:
“set alarm at 7 AM”
“गाना बजाओ”

“shutdown the system”
“how do you say water in Hindi”
thanks to a vast, multilingual trigger map.

🕒 Smart Time Management
Set alarms, timers, and reminders
View and clear reminders
Continuous background checks

🔋 Battery Monitoring Assistant
Alerts when battery is full and plugged in
Warns if below 20% and unplugged
Guidance appears in chat and voice

🌦️ Weather & News
Ask “क्या बारिश होगी?” or “Will it rain today?”
Read latest headlines with “read news”

🌐 Web & Wikipedia Search
Search Google and Wikipedia with multilingual prompts
Example: “गूगल पर सर्च करो”, “tell me about Einstein”

🎶 YouTube Playback & Downloading
Play music/videos using voice
Pause, skip, volume, captions, fullscreen
Download YouTube audio/video

📂 PC & App Management

Open/close apps like Notepad, Word, Chrome

Lock system, shutdown, restart, logout

Clean temp files, empty recycle bin

📊 Unit, Currency, and Math Conversions
“2 gallons to liters”
“convert euros to rupees”
“15% of 240” or “solve 12 x 9”

📄 To-Do & Note Manager
Add, read, edit, delete tasks
Create simple voice notes

🔁 Chrome Control (Experimental)
Open/close tabs and windows

Incognito mode, refresh, history, downloads

“पिछला टैब खोलो” or “new tab in chrome”

🧠 Smart Translation & Language Support

Understands and translates between Hindi and English

Prompts like “translate dog to Hindi” or “पानी को इंग्लिश में क्या कहते हैं”

💬 Interactive GUI Chat Interface

Built with Tkinter + ttkbootstrap

Voice responses appear in chat too

Custom styles with futuristic feel

🧩 Modular Command System

Add new commands via @register_command() decorator

Fully extensible with simple Python files

---

## 🖥️ Demo

![screenshot](assets/demo_screenshot.png)  
> Shows assistant in action responding to voice & battery alerts!

---
Project Structure
voice_assistant/
├── main.py                           ✅ You already have this, slightly refactored
├── gui/
│   └── app_gui.py                    ✅ Your GUI moved here
├── core/
│   ├── dispatcher.py                 🔄 (To be created)
│   ├── voice_input.py                🔄
│   ├── voice_output.py               🔄
│   ├── intent_matcher.py             🔄
│   ├── registry.py                   🔄
│   ├── translator.py                 ✅ From your code
│   ├── logger.py                     ✅ Decorator already used
│   └── interaction_manager.py        ✅ Already in use
├── commands/
│   ├── __init__.py
│   ├── reminder_scheduler.py         ✅ Used in your threading logic
│   ├── alarm_manager.py              ✅ Used
│   └── timer_manager.py              🔄 Will create soon
├── data/
│   ├── commands.json                 🔄 Intent phrases
│   └── config.yaml                   🔄 User config
├── assets/
│   └── futuristic_bg.jpg             ✅ Background image
├── utils/
│   └── helper.py                     🔄 Utility functions
├── logs.txt                          ✅ Your voice assistant logs here
├── requirements.txt                  ✅ Will be generated
└── README.md                         🔄 Documentation


## 📦 Requirements

- Python 3.10–3.13
- [gTTS](https://pypi.org/project/gTTS/)
- [pygame](https://pypi.org/project/pygame/)
- [psutil](https://pypi.org/project/psutil/)
- [pyautogui](https://pypi.org/project/pyautogui/)
- [ttkbootstrap](https://pypi.org/project/ttkbootstrap/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Pillow](https://pypi.org/project/Pillow/)
- [colorama](https://pypi.org/project/colorama/)

Install all dependencies with:

```bash
pip install -r requirements.txt

Running the Assistant
python main.py

Tips
You can easily add multi-step follow-ups (e.g., setting a timer).
All speak(...) responses also appear in the GUI chat.
Modify app_gui.py for look, colors, or layout.


📜 License
MIT License – free to use, customize, and extend.
🙌 Credits
Built with ❤️ using Python, Tkinter, pygame, and gTTS.
Inspired by Jarvis and futuristic voice assistants.


---

Would you like a version of this README with **badges**, a **GIF demo**, or deployment instructions for `.exe`?



