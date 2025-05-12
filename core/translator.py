# core/translator.py
from deep_translator import GoogleTranslator
from langdetect import detect

class Translator:
    def __init__(self, source_lang="auto", target_lang="en"):
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate(self, text):
        try:
            detected_lang = detect(text)
            if detected_lang == self.target_lang:
                return text
            return GoogleTranslator(source=detected_lang, target=self.target_lang).translate(text)
        except Exception as e:
            print(f"[Translator Error] {e}")
            return text  # Fallback to original
