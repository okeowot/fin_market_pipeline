import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def get_raw_data(symbol, asset_type="stock"):
    """Fetch raw JSON/DataFrame from the API."""
    function = "TIME_SERIES_DAILY" if asset_type == "stock" else "DIGITAL_CURRENCY_DAILY"
    params = {"function": function, "symbol": symbol, "apikey": API_KEY}
    
    if asset_type == "crypto":
        params["market"] = "USD"

    response = requests.get(BASE_URL, params=params)
    data = response.json()
    print(data)
    # Identify the correct JSON key based on asset type
    key = "Time Series (Daily)" if asset_type == "stock" else "Time Series (Digital Currency Daily)"
    
    if key not in data:
        raise ValueError(f"Error fetching data for {symbol}: {data.get('Note', 'Check API limits')}")
        
    return pd.DataFrame(data[key]).T