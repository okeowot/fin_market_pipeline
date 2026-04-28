# 📈 Global Market Terminal
An end-to-end data pipeline that extracts and visualizes real-time performance metrics for the top 25 Stocks and Cryptocurrencies.

## 🚀 Features
- **Dynamic ETL:** Automated extraction from Alpha Vantage API with custom transformation logic.
- **Multi-Asset Schema:** Handles inconsistent data structures between Equities and Digital Assets.
- **Optimized UI:** Built with Streamlit, utilizing Session State for seamless navigation and Caching to respect API rate limits.
- **Financial Analytics:** Real-time calculation of 1D, 1W, 1M, and 1Y percentage changes.

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **Libraries:** Pandas, Requests, Streamlit, Dotenv
- **API:** Alpha Vantage

## 🏁 Getting Started
1. **Clone the repo:** `git clone https://github.com/your-username/fin_market_pipeline.git`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Setup Keys:** Rename `.env.example` to `.env` and add your Alpha Vantage API Key.
4. **Run the App:** `streamlit run dashboard/app.py`

## Dashboard Images
<img width="1891" height="456" alt="regular" src="https://github.com/user-attachments/assets/2ff6614e-1943-457f-9aa5-5d5b7c1aaace" />
<img width="1869" height="719" alt="BTC" src="https://github.com/user-attachments/assets/5223bbf7-4255-44e8-bc40-be792103949f" />
<img width="1909" height="707" alt="AAPL" src="https://github.com/user-attachments/assets/8f680b7e-d2a1-4cdd-b4e5-6143cbee0fb3" />



