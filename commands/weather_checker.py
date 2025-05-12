# commands/weather_checker.py

import webbrowser
import json
import os
import pyautogui
from core.registry import register_command

FAV_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "favorite_cities.json")

def load_favorites():
    if not os.path.exists(FAV_FILE):
        return []
    with open(FAV_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_favorites(fav_list):
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(fav_list, f, ensure_ascii=False, indent=2)

@register_command("check weather")
def check_weather(params=None):
    favorites = load_favorites()

    # Ask for city name
    city = pyautogui.prompt(
        text="Which city shall I check the weather for?",
        title="Check Weather"
    )

    if not city:
        return "⚠️ You didn’t provide a city name."

    city = city.strip().title()

    # Ask if it should be saved
    if city not in favorites:
        if len(favorites) < 2:
            add = pyautogui.confirm(
                text=f"Would you like me to save '{city}' as one of your 2 favorite cities?",
                title="Save City?",
                buttons=["Yes", "No"]
            )
            if add == "Yes":
                favorites.append(city)
                save_favorites(favorites)
        else:
            pyautogui.alert(
                text=f"You already have 2 favorite cities: {', '.join(favorites)}.\nRemove one manually to add a new one.",
                title="Limit Reached"
            )

    # Open weather info
    webbrowser.open(f"https://www.google.com/search?q=weather+in+{city.replace(' ', '+')}")
    return f"🌦️ Fetching today's weather forecast for {city}..."
