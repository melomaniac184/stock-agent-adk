import requests

ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
BASE_URL = "https://www.alphavantage.co/query"

def get_current_price(ticker):
    """
    Fetches the current stock price for the given ticker using Alpha Vantage API.
    """
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            price = data["Global Quote"]["05. price"]
            return {
                "ticker": ticker.upper(),
                "price": float(price),
                "currency": "USD"
            }
        else:
            return {"error": "Price data not found. Check the ticker or try again later."}

    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}
