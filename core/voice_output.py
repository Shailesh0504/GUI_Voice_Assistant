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
    print(Fore.MAGENTA + f"Jarvis: {text}" + Style.RESET_ALL)
    temp_path = None
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        time.sleep(0.2)

    except Exception as e:
        logger.error(f"TTS Error: {e}")
        print(Fore.RED + f"TTS Error: {e}" + Style.RESET_ALL)

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                logger.warning(f"Could not delete temp file: {e}")
