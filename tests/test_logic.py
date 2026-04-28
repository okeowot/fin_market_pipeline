import time
from scripts.extract import get_raw_data
from scripts.transform import clean_and_calculate

try:
    print("Testing Stock Extraction (AAPL)...")
    raw_stock = get_raw_data("AAPL", "stock")
    df_stock, stats_stock = clean_and_calculate(raw_stock, "stock")
    print(f"✅ Success! Current Price: ${stats_stock['price']}")
    print(f"Daily Change: {stats_stock['1d']:.2f}%")

    print("\nWaiting 15 seconds to avoid API rate limits...")
    time.sleep(15)


    print("\nTesting Crypto Extraction (BTC)...")
    raw_crypto = get_raw_data("BTC", "crypto")
    df_crypto, stats_crypto = clean_and_calculate(raw_crypto, "crypto")
    print(f"✅ Success! Current BTC Price: ${stats_crypto['price']}")
    
except Exception as e:
    print(f"❌ Test Failed: {e}")
