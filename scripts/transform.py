import pandas as pd

def clean_and_calculate(raw_df, asset_type="stock"):
    """Cleans raw API data and handles inconsistent column names."""
    
    # 1. FIX: Check for the multiple possible names Alpha Vantage uses for 'Close'
    possible_close_cols = ["4. close", "4b. close (USD)", "4a. close (USD)"]
    
    # Find which column actually exists in our data
    found_col = None
    for col in possible_close_cols:
        if col in raw_df.columns:
            found_col = col
            break
            
    if not found_col:
        raise KeyError(f"Could not find a 'close' column. Found columns: {list(raw_df.columns)}")

    # 2. Proceed with renaming and cleaning
    df = raw_df[[found_col]].rename(columns={found_col: "close"}).astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=False)

    current_price = df.iloc[0]['close']

    def get_pct(days_ago):
        try:
            hist_price = df.iloc[days_ago]['close']
            return ((current_price - hist_price) / hist_price) * 100
        except IndexError:
            return 0.0

    metrics = {
        "price": current_price,
        "1d": get_pct(1),
        "1w": get_pct(7),
        "1m": get_pct(30),
        "1y": get_pct(365)
    }
    
    return df, metrics