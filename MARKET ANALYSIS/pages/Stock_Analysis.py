import streamlit as st
import pandas as pd
import yfinance as yf # type: ignore
import plotly.graph_objects as go # type: ignore
import datetime as dt
import ta
from pages.utils.plotly_figure import plotly_table

# Page configuration
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Stock Analysis Dashboard")

# Define layout columns
col1, col2, col3 = st.columns(3)

today = dt.date.today()

# Input fields
with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")

with col2:
    start_date = st.date_input("Choose Start Date", dt.date(today.year - 1, today.month, today.day))

with col3:
    end_date = st.date_input("Choose End Date", today)

# Fetch stock data
stock = yf.Ticker(ticker)

# Display company information
st.subheader(f"📌 {ticker.upper()} - Company Overview")
try:
    st.write(stock.info['longBusinessSummary'])
    st.write("**Sector:**", stock.info['sector'])
    st.write("**Full-Time Employees:**", stock.info['fullTimeEmployees'])
    st.write("**Website:**", stock.info['website'])
except KeyError:
    st.warning("Some stock information is not available.")

# Display financial highlights
st.subheader("💹 Financial Highlights")
col1, col2 = st.columns(2)

with col1:
    try:
        df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
        df['Value'] = [
            stock.info.get('marketCap', 'N/A'),
            stock.info.get('beta', 'N/A'),
            stock.info.get('trailingEps', 'N/A'),
            stock.info.get('trailingPE', 'N/A')
        ]
        st.table(df)
    except Exception as e:
        st.error(f"Error displaying financial data
