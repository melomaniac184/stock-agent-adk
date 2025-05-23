# agents/ticker_price_change.py

import requests
from datetime import datetime, timedelta

ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY"  # Replace with your Alpha Vantage key
BASE_URL = "https://www.alphavantage.co/query"

def get_price_change(ticker, days=7):
    """
    Calculates the stock price change over the past N days.
    
    :param ticker: Stock ticker symbol (e.g., "TSLA")
    :param days: Number of days ago to compare with today
    :return: Dictionary with percent change and price details
    """
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "Time Series (Daily)" not in data:
            return {"error": "Historical data not found for ticker."}

        time_series = data["Time Series (Daily)"]

        # Get today's and N-days-ago dates
        sorted_dates = sorted(time_series.keys(), reverse=True)
        today = sorted_dates[0]

        # Try to find a valid date N days ago (market might be closed on exact date)
        target_date = None
        count = 0
        for d in sorted_dates[1:]:
            count += 1
            if count == days:
                target_date = d
                break

        if not target_date:
            return {"error": f"Not enough data to look {days} days back."}

        current_price = float(time_series[today]["4. close"])
        old_price = float(time_series[target_date]["4. close"])
        change = current_price - old_price
        percent_change = (change / old_price) * 100

        return {
            "ticker": ticker.upper(),
            "current_price": current_price,
            "price_n_days_ago": old_price,
            "days": days,
            "change": round(change, 2),
            "percent_change": round(percent_change, 2)
        }

    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}
