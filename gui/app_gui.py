# gui/app_gui.py

import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Entry, Button
import speech_recognition as sr
import threading
from gtts import gTTS
import os
import tempfile
import pygame
import time
from colorama import Fore, Style as ColorStyle
import speech_recognition as sr
from core.translator import Translator
from core.intent_matcher import match_intent  # make sure this is available
from colorama import Fore, Style as ColorStyle
from PIL import Image, ImageTk
from core.logger import log_function
from core.interaction_manager import InteractionManager
from core.dispatcher import dispatch
from gui.message_router import show_in_chat


root = None

pygame.mixer.init()
voice_enabled = True
listening_active = False



# ----------------- SPEAK ----------------- #
def speak(text):
    global voice_enabled
    if not text or not text.strip():
        return

    if not voice_enabled:
        print(Fore.YELLOW + "[Muted] " + text + ColorStyle.RESET_ALL)
        return

    print(Fore.MAGENTA + f"Jarvis: {text}" + ColorStyle.RESET_ALL)
    temp_path = None
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        # Non-blocking check for mute
        while pygame.mixer.music.get_busy():
            if not voice_enabled:
                pygame.mixer.music.stop()
                print(Fore.YELLOW + "[Speech stopped due to mute]" + ColorStyle.RESET_ALL)
                break
            time.sleep(0.05)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        time.sleep(0.2)

    except Exception as e:
        print(Fore.RED + f"TTS Error: {e}" + ColorStyle.RESET_ALL)

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(Fore.RED + f"Temp cleanup error: {e}" + ColorStyle.RESET_ALL)



# ----------------- LISTEN ----------------- #
def recognize_voice():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print(Fore.CYAN + "🎙️ Listening..." + ColorStyle.RESET_ALL)
            audio = recognizer.listen(source, timeout=5)

            try:
                original_text = recognizer.recognize_google(audio, language='hi-IN')
                print(Fore.BLUE + f"🗣️ Heard: {original_text}" + ColorStyle.RESET_ALL)

                # Step 1: Match intent using raw Hindi input
                from core.intent_matcher import match_intent
                command_key, _ = match_intent(original_text)

                # Step 2: If command doesn't need translation — return raw
                non_translate_intents = ["translate text", "play youtube", "joke", "read news"]
                if command_key in non_translate_intents:
                    print(Fore.YELLOW + f"⚡ Intent: {command_key} → using original input." + ColorStyle.RESET_ALL)
                    return original_text, original_text

                # Step 3: Else translate input to English
                translated_text = Translator(target_lang="en").translate(original_text)
                if translated_text:
                    print(Fore.GREEN + f"🌐 Translated: {translated_text}" + ColorStyle.RESET_ALL)
                    return translated_text, original_text
                else:
                    print(Fore.RED + "❗ Translation failed." + ColorStyle.RESET_ALL)
                    return None, original_text

            except sr.UnknownValueError:
                print(Fore.RED + "❗ Could not understand what you said." + ColorStyle.RESET_ALL)
            except sr.RequestError as e:
                print(Fore.RED + f"❗ API Error: {e}" + ColorStyle.RESET_ALL)
    except sr.WaitTimeoutError:
        print(Fore.YELLOW + "⏱️ Timeout: No speech detected." + ColorStyle.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"❗ Unexpected Error: {e}" + ColorStyle.RESET_ALL)

    return None, None




def clean_exit():
    global listening_active
    listening_active = False
    try:
        pygame.quit()
    except:
        pass
    try:
        root.destroy()
    except:
        pass
    os._exit(0)  # Force exit as fallback


  

# ----------------- GUI ----------------- #
class FuturisticAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("800x570")       
        self.style = Style(theme='darkly')
        self.is_muted = False
        self.manager = InteractionManager()
        self.setup_ui()

    def setup_ui(self):
        try:
            bg_image = Image.open("assets/futuristic_bg.jpg").resize((800, 570))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            tk.Label(self.root, image=self.bg_photo).place(relx=0, rely=0, relwidth=1, relheight=1)
        except:
            pass

        self.chat_box = tk.Text(self.root, bg="#101010", fg="#39FF14", font=("Consolas", 12), wrap="word", insertbackground="#39FF14")
        self.chat_box.pack(padx=10, pady=10, fill="both", expand=True)
        self.chat_box.insert("end", "🤖 Hello! I'm your assistant. How can I help you today?\n\n")
        self.chat_box.config(state="disabled")

        frame = tk.Frame(self.root, bg="#101010")
        frame.pack(pady=10)

        self.entry = Entry(frame, font=("Consolas", 12), width=50, bootstyle="info")
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.bind("<Return>", self.handle_text_input)

        Button(frame, text="📤 Send", bootstyle="success-outline", command=self.handle_text_input).pack(side="left", padx=(0, 5))
        self.listen_btn = Button(frame, text="🎤 Listen", bootstyle="warning-outline", command=self.toggle_listen)
        self.listen_btn.pack(side="left", padx=(0, 5))
        Button(frame, text="🧹 Clear", bootstyle="danger", command=self.clear_chat).pack(side="left", padx=(0, 5))
        self.mute_btn = Button(frame, text="🔇 Mute", bootstyle="secondary", command=self.toggle_mute)
        self.mute_btn.pack(side="left", padx=(0, 5))

        self.status_var = tk.StringVar()
        self.status_var.set("🟢 Ready")
        self.status = tk.Label(self.root, textvariable=self.status_var, anchor="w", font=("Consolas", 10), bg="#222", fg="white")
        self.status.pack(side="bottom", fill="x")

    def update_status(self, message):
        self.status_var.set(f"🔔 {message}")
        self.root.update_idletasks()

    def append_message(self, sender, message):
        tag = "user" if "You" in sender else "assistant"
        self.chat_box.config(state="normal")
        self.chat_box.insert("end", f"{sender}: {message}\n", tag)
        self.chat_box.tag_config("user", foreground="#00FFFF", font=("Consolas", 12, "bold"))
        self.chat_box.tag_config("assistant", foreground="#7CFC00", font=("Consolas", 12, "italic"))
        self.chat_box.config(state="disabled")
        self.chat_box.see("end")

    def clear_chat(self):
        self.chat_box.config(state="normal")
        self.chat_box.delete(1.0, "end")
        self.chat_box.insert("end", "🤖 Hello! I'm your futuristic assistant. How can I help you today?\n\n")
        self.chat_box.config(state="disabled")
        self.update_status("Chat cleared.")

    def toggle_mute(self):
        global voice_enabled
        voice_enabled = not voice_enabled
        self.is_muted = not self.is_muted
        self.mute_btn.config(text="🔊 Unmute" if self.is_muted else "🔇 Mute")
        self.update_status("Voice muted." if self.is_muted else "Voice unmuted.")

    @log_function
    def handle_text_input(self, event=None):
        user_input = self.entry.get().strip()
        if user_input:
            self.entry.delete(0, "end")
            self.append_message("🧑 You", user_input)
            self.respond(user_input)
            self.update_status("Message sent.")

    @log_function
    def respond(self, text):
        if not text.strip():
            return

        if "exit" in text.lower() or "bye" in text.lower() or "goodbye" in text.lower():
            self.append_message("🤖 Assistant", "👋 Exiting assistant. Goodbye!")
            speak("Exiting assistant. Goodbye!")
            clean_exit()
            return

        # Timer follow-up
        if self.manager.pending_confirmation and self.manager.pending_confirmation["action"] == "set_timer":
            duration = text.strip()
            self.manager.pending_confirmation = None
            from commands import timer_manager
            reply = timer_manager.set_timer(duration, on_complete=self.handle_timer_complete)
            self.append_message("🤖 Assistant", reply)
            threading.Thread(target=speak, args=(reply,)).start()

            return

        reply = self.manager.process(text)
        if not reply:
            reply = "⚠️ Sorry, I didn't catch that."

        self.append_message("🤖 Assistant", reply)
        threading.Thread(target=speak, args=(reply,)).start()

        self.update_status("Awaiting next command.")

    def toggle_listen(self):
        global listening_active
        listening_active = not listening_active
        if listening_active:
            self.listen_btn.config(text="🛑 Stop", bootstyle="danger")
            self.update_status("Listening...")
            threading.Thread(target=self._continuous_listen_thread).start()
        else:
            self.listen_btn.config(text="🎤 Listen", bootstyle="warning-outline")
            self.update_status("Listening stopped.")

    def _continuous_listen_thread(self):
        while listening_active:
            self.update_status("Listening... say something")
            translated_text, original_text = recognize_voice()
            final_input = translated_text or original_text

            if final_input and "exit" in final_input.lower():
                self.append_message("🧑 You (Voice)", final_input)
                self.append_message("🤖 Assistant", "👋 Exiting assistant.")
                speak("Exiting assistant. Goodbye!")
                clean_exit()
                return

            if final_input:
                self.append_message("🧑 You (Voice)", final_input)
                self.respond(final_input)
            else:
                if not hasattr(self, "_last_error") or time.time() - self._last_error > 5:
                    self.update_status("❗ Sorry, I didn't catch that.")
                    self._last_error = time.time()
                self.update_status("Listening stopped.")

    def handle_timer_complete(self, msg):
        self.append_message("🤖 Assistant", msg)
        speak("Time's up!")
