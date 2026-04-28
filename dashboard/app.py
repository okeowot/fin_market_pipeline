import streamlit as st
import sys
import os
import time

# Path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.extract import get_raw_data
from scripts.transform import clean_and_calculate

st.set_page_config(page_title="Market Pulse", layout="wide")

# --- CACHING LOGIC ---
# This saves your API credits! It remembers the data for 24 hours.
@st.cache_data(ttl=86400) 
def get_cached_data(symbol, asset_type):
    raw_df = get_raw_data(symbol, asset_type)
    return clean_and_calculate(raw_df, asset_type)

st.title("📈 Global Market Terminal")

# --- SIDEBAR SELECTION ---
st.sidebar.header("Navigation")

# Add a 'key' to the radio button so we can track changes
category = st.sidebar.radio(
    "Select Asset Class", 
    ["Stocks", "Cryptocurrency"],
    key="class_selector"
)

# NEW: If the category changes, clear the previous results
if "last_category" not in st.session_state:
    st.session_state.last_category = category

if st.session_state.last_category != category:
    st.session_state.market_data = None
    st.session_state.market_stats = None
    st.session_state.last_category = category

# Top 25 Lists
stocks_25 = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B", "V", "UNH", 
             "JNJ", "WMT", "JPM", "MA", "PG", "AVGO", "ORCL", "HD", "CVX", "COST", 
             "ABBV", "MRK", "KO", "PEP", "BAC"]

crypto_25 = ["BTC", "ETH", "USDT", "BNB", "SOL", "XRP", "USDC", "ADA", "AVAX", "DOGE", 
             "DOT", "TRX", "LINK", "MATIC", "WBTC", "SHIB", "DAI", "BCH", "LTC", "ATOM", 
             "UNI", "LEO", "ETC", "XLM", "OKB"]

if category == "Stocks":
    symbol = st.sidebar.selectbox("Select Top 25 Stocks", stocks_25)
    asset_type = "stock"
else:
    symbol = st.sidebar.selectbox("Select Top 25 Crypto", crypto_25)
    asset_type = "crypto"

# --- TRACKING CHANGES ---
# Initialize tracking variables if they don't exist
if "last_category" not in st.session_state:
    st.session_state.last_category = category
if "last_symbol" not in st.session_state:
    st.session_state.last_symbol = symbol

# RESET LOGIC: If the user picks a different category or a different ticker,
# clear the old data so we don't show Apple prices for Bitcoin.
if st.session_state.last_category != category or st.session_state.last_symbol != symbol:
    st.session_state.market_data = None
    st.session_state.market_stats = None
    # Update the trackers to the current selection
    st.session_state.last_category = category
    st.session_state.last_symbol = symbol

# --- MAIN DASHBOARD ---
# 1. Initialize session state for the data if it doesn't exist
if 'market_data' not in st.session_state:
    st.session_state.market_data = None
if 'market_stats' not in st.session_state:
    st.session_state.market_stats = None

if st.sidebar.button(f"Analyze {symbol}"):
    try:
        with st.spinner(f"Pulling {symbol} data..."):
            # Save the results into session state
            df, stats = get_cached_data(symbol, asset_type)
            st.session_state.market_data = df
            st.session_state.market_stats = stats
    except Exception as e:
        st.error(f"Error: {e}")

# 2. Only display if we actually have data in session state
# --- THE DISPLAY LAYER ---
if st.session_state.market_data is not None:
    df = st.session_state.market_data
    stats = st.session_state.market_stats

    # 1. Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", f"${stats['price']:,.2f}")
    col2.metric("24h Change", f"{stats['1d']:.2f}%", delta=f"{stats['1d']:.2f}%")
    col3.metric("7d Change", f"{stats['1w']:.2f}%", delta=f"{stats['1w']:.2f}%")
    col4.metric("30d Change", f"{stats['1m']:.2f}%", delta=f"{stats['1m']:.2f}%")

    # 2. The Chart
    st.subheader(f"Price Action: {symbol} (Last 100 Days)")
    st.line_chart(df['close'])
    
    # 3. Raw Data Toggle
    if st.checkbox("Show Raw Data Table"):
        st.dataframe(df)
else:
    # This shows when the screen is "reset"
    st.info(f"💡 The terminal is ready. Click 'Analyze {symbol}' to load the data.")