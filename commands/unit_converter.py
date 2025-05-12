# commands/unit_converter.py

import re
from core.registry import register_command
from core.voice_output import speak

try:
    from pint import UnitRegistry
except ImportError:
    UnitRegistry = None

ureg = UnitRegistry() if UnitRegistry else None
if ureg:
    ureg.default_format = "~P"  # Pretty print units

@register_command("convert units")
def convert_units(params=None):
    """
    Converts between measurement units using natural phrasing.
    Example: "How many liters are in 2 gallons?"
    """
    if UnitRegistry is None or ureg is None:
        return "❌ Unit conversion feature is unavailable. Please install the 'pint' module."

    if not params:
        return "🔁 Please tell me what you'd like to convert. For example: 2 gallons to liters."

    pattern = re.search(r"(\d+(\.\d+)?)\s*(\w+)\s+(?:to|in|into|equals|=)\s+(\w+)", params.lower())
    if not pattern:
        return (
            "🤖 I couldn't understand the units or format.\n"
            "Try something like: '2 gallons to liters' or 'How many km in 5 miles?'"
        )

    quantity = float(pattern.group(1))
    from_unit = pattern.group(3)
    to_unit = pattern.group(4)

    try:
        result = ureg(quantity, from_unit).to(to_unit)
        result_str = f"{quantity} {from_unit} = {result:.2f}"
        speak(f"{quantity} {from_unit} is approximately {result:.2f}")
        return f"✅ {result_str}"

    except Exception as e:
        return f"❌ Could not convert units: {e}"
