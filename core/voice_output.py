# core/voice_output.py

from gtts import gTTS
import pygame
import tempfile
import os
import time
from colorama import Fore, Style
import logging

logger = logging.getLogger(__name__)

def speak(text, lang='en'):
    # 🛡 Input validation
    if isinstance(text, (list, tuple)):
        text = " ".join(map(str, text))
    elif not isinstance(text, str):
        text = str(text)

    if not text.strip():
        print(Fore.YELLOW + "[speak] Warning: Empty or invalid text passed. Skipping TTS." + Style.RESET_ALL)
        return

    # 🎙 Print to console
    print(Fore.MAGENTA + f"Jarvis: {text}" + Style.RESET_ALL)

    temp_path = None
    try:
        # 🔊 Text-to-speech conversion
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)

        # 🎧 Playback
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        time.sleep(0.2)

    except Exception as e:
        logger.error(f"TTS Error: {e}")
        print(Fore.RED + f"[speak] Error during TTS playback: {e}" + Style.RESET_ALL)

    finally:
        # 🧹 Cleanup temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                logger.warning(f"[speak] Could not delete temp file: {e}")
