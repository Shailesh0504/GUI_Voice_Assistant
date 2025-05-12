# commands/text_translator.py

from core.registry import register_command
from deep_translator import GoogleTranslator
from core.voice_output import speak
import re
import os
import datetime

def log_failed_translation(text, target_lang):
    os.makedirs("logs", exist_ok=True)
    with open("logs/failed_translations.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Text: '{text}' → Unsupported language: '{target_lang}'\n")

def normalize_input(text):
    text = text.strip().lower()

    # Flexible Hindi pattern: allow cutoff after "में"
    hindi_pattern = re.search(
        r"(.+?) (?:को|की|का|इसको|उसको)? (.+?) में(?: (?:क्या|कैसे)? बोलते हैं)?",
        text
    )
    if hindi_pattern:
        phrase = hindi_pattern.group(1).strip("'\"“”‘’ ")
        lang = hindi_pattern.group(2).strip()
        lang_map = {
            "इंग्लिश": "english", "अंग्रेज़ी": "english", "हिंदी": "hindi",
            "जापानी": "japanese", "फ्रेंच": "french", "स्पेनिश": "spanish",
            "जर्मन": "german", "चाइनीज": "chinese", "रूसी": "russian",
            "बंगाली": "bengali", "मराठी": "marathi", "तमिल": "tamil"
        }
        lang = lang_map.get(lang, lang)
        return f"'{phrase}' in {lang}"

    # English-style fallback
    fuzzy_en = re.search(r"(?:how to|how do you|what(?: do you)?|meaning of)? ?(?:say|speak|write|translate)? ?(.+?) in (\w+)", text)
    if fuzzy_en:
        phrase = fuzzy_en.group(1).strip("'\"“”‘’ ")
        lang = fuzzy_en.group(2).strip()
        return f"'{phrase}' in {lang}"

    # Direct match: 'word' in language
    exact = re.search(r"['\"](.+?)['\"] in (\w+)", text)
    if exact:
        phrase = exact.group(1)
        lang = exact.group(2)
        return f"'{phrase}' in {lang}"

    return text


@register_command("translate text")
def translate_text(params=None):
    """
    Translates a phrase into another language using deep_translator.
    Supports:
    • "‘book’ in Japanese"
    • "how to say खाना in Japanese"
    • "नहाना को इंग्लिश में क्या बोलते हैं"
    """
    if not params:
        return "Please tell me what you'd like to translate and to which language."

    normalized = normalize_input(params)

    match = re.search(r"['\"](.+?)['\"] in (\w+)", normalized)
    if not match:
        return (
            f"🤖 I didn’t catch the phrase or language properly.\n"
            f"(Debug: normalized = {normalized})\n"
            "Try something like:\n"
            "• How do you say 'book' in Spanish?\n"
            "• 'खुश' को इंग्लिश में क्या बोलते हैं?"
        )

    text, target_lang = match.group(1), match.group(2).lower()

    try:
        # validate supported languages
        supported_langs = GoogleTranslator.get_supported_languages(as_dict=True)
        if target_lang not in supported_langs and target_lang not in supported_langs.values():
            log_failed_translation(text, target_lang)
            return (
                f"Sorry, I can’t translate into '{target_lang.title()}' yet.\n"
                "I’ll need to update my memory to support that language."
            )

        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        speak(translated, lang=target_lang)
        return f"‘{text}’ in {target_lang.title()} is:\nTranslated: {translated}"
    
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return (
            f"❌ Could not complete the translation due to an unexpected error.\n"
            f"Assistant will keep learning to improve!"
        )
