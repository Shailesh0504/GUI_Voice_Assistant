import re
from core.voice_output import speak
from core.registry import register_command

currency_map = {
    "rupees": "INR", "indian rupees": "INR",
    "usd": "USD", "dollars": "USD",
    "euros": "EUR", "euro": "EUR", "€": "EUR",
    "pounds": "GBP", "gbp": "GBP", "£": "GBP",
    "yen": "JPY", "jpy": "JPY", "¥": "JPY",
    "aed": "AED", "dirhams": "AED",
}

@register_command("convert currency")
def convert_currency(params=None):
    if not params:
        return "Please say something like: Convert 100 dollars to rupees."

    match = re.search(r"([€$₹£¥]?\s?\d+(\.\d+)?)(?:\s*(\w+))?\s+(?:to|in)\s+(\w+)", params.lower())
    if not match:
        return "I couldn’t understand the format. Try: Convert 100 USD to INR"

    raw_amount = match.group(1).replace("€", "").replace("$", "").replace("₹", "").replace("£", "").replace("¥", "").strip()
    amount = float(raw_amount)
    source_unit = match.group(3) or "EUR"
    target_unit = match.group(4)

    source_currency = currency_map.get(source_unit.lower(), source_unit.upper())
    target_currency = currency_map.get(target_unit.lower(), target_unit.upper())

    try:
        from forex_python.converter import CurrencyRates, CurrencyCodes
    except ImportError:
        return "❌ Currency conversion feature is unavailable because the required module 'forex-python' is not installed."

    try:
        c = CurrencyRates()
        result = c.convert(source_currency, target_currency, amount)
        symbol = CurrencyCodes().get_symbol(target_currency)
        speak(f"{amount} {source_currency} is approximately {result:.2f} {target_currency}")
        return f"{amount} {source_currency} = {symbol or target_currency} {result:.2f}"
    except Exception as e:
        return f"❌ Currency conversion failed: {e}"
