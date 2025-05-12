# commands/stock_price.py

try:
    import yfinance as yf
except ImportError:
    yf = None

from core.registry import register_command

# speak will be called from the GUI after return
@register_command("stock price")
def check_stock_price(params=None):
    """
    Fetches current stock price and returns result to GUI.
    GUI will handle speaking after showing the response.
    """
    if yf is None:
        return "❌ Stock price feature is unavailable. Please install the 'yfinance' module."

    if not params:
        return "📈 Please tell me which stock you want to check."

    query = params.strip().lower()

    stock_map = {
        "tcs": "TCS.NS",
        "reliance": "RELIANCE.NS",
        "infosys": "INFY.NS",
        "hdfc": "HDFCBANK.NS",
        "wipro": "WIPRO.NS",
        "tata steel": "TATAMSTEEL.NS",
        "ongc": "ONGC.NS",
        "bharat petroleum": "BPCL.NS"
    }

    hindi_to_eng = {
        "रिलायंस": "reliance",
        "टीसीएस": "tcs",
        "विप्रो": "wipro",
        "इंफोसिस": "infosys",
        "एचडीएफसी": "hdfc",
        "ओएनजीसी": "ongc",
        "टाटा स्टील": "tata steel"
    }

    for hindi, eng in hindi_to_eng.items():
        if hindi in query:
            query = eng

    ticker = None
    for name, tk in stock_map.items():
        if name in query:
            ticker = tk
            query = name
            break

    if not ticker:
        return f"❓ Sorry, I don't recognize the stock: '{query}'. Try TCS, Reliance, etc."

    try:
        stock = yf.Ticker(ticker)
        price = stock.info['regularMarketPrice']
        currency = stock.info.get("currency", "INR")
        response = f"📈 The current price of {query.upper()} is {price} {currency}."
        return response
    except Exception as e:
        return f"❌ Error fetching price for {query.upper()}: {e}"
