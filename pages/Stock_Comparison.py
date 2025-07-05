import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="Stock Comparison", layout="wide")
st.title("Stock Comparison Tool")

st.markdown("Compare two stocks side-by-side based on key financial metrics and recent price trends.")


col1, col2 = st.columns(2)

with col1:
    ticker1 = st.text_input("Enter First Ticker (e.g. AAPL)", "AAPL").strip().upper()
with col2:
    ticker2 = st.text_input("Enter Second Ticker (e.g. TSLA)", "TSLA").strip().upper()


def fetch_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "Company Name": info.get("longName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Market Cap": info.get("marketCap", "N/A"),
        "Current Price": info.get("currentPrice", "N/A"),
        "PE Ratio": info.get("trailingPE", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A"),
        "Beta": info.get("beta", "N/A"),
    }


def fetch_price_data(ticker):
    try:
        df = yf.download(ticker, period="30d")
        if df.empty:
            return None
        return df.reset_index()
    except Exception:
        return None

if st.button("Compare Stocks"):
    try:
        
        data1 = fetch_info(ticker1)
        data2 = fetch_info(ticker2)

        
        st.subheader("📋 Side-by-Side Comparison")
        comparison_df = pd.DataFrame({
            f"{ticker1}": data1,
            f"{ticker2}": data2
        })

        st.dataframe(comparison_df)

        
        try:
            metrics = ["Market Cap", "Current Price", "PE Ratio", "Dividend Yield", "Beta"]
            values1 = [data1.get(metric, 0) if isinstance(data1.get(metric), (int, float)) else 0 for metric in metrics]
            values2 = [data2.get(metric, 0) if isinstance(data2.get(metric), (int, float)) else 0 for metric in metrics]

            fig = go.Figure(data=[
                go.Bar(name=ticker1, x=metrics, y=values1),
                go.Bar(name=ticker2, x=metrics, y=values2)
            ])

            fig.update_layout(
                title="Metric Comparison Bar Chart",
                barmode='group',
                xaxis_title="Metrics",
                yaxis_title="Value (Log Scale)",
                yaxis_type="log",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not generate bar chart: {e}")

    except Exception as e:
        st.error(f"Unexpected error occurred: {e}")