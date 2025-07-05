import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


st.set_page_config(page_title="CAPM Return", layout="wide")
st.title(" CAPM Expected Return Calculator")

st.markdown("""
The Capital Asset Pricing Model (CAPM) estimates the *expected return* of a stock based on its risk compared to the market.
""")


st.subheader(" Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input("Stock Ticker (e.g., AAPL)", "TSLA")

with col2:
    risk_free_rate = st.number_input("Risk-Free Rate (%)", value=4.0)

with col3:
    market_return = st.number_input("Market Return (%)", value=10.0)


if st.button("Calculate CAPM Return"):
    stock = yf.Ticker(ticker)

    try:
        beta = stock.info.get('beta', None)

        if beta is None:
            st.error(" Beta information not available for this stock.")
        else:
            capm_return = risk_free_rate + beta * (market_return - risk_free_rate)

            
            st.success(f" Beta of *{ticker.upper()}*: {beta:.2f}")
            st.success(f" *Expected CAPM Return*: {capm_return:.2f}%")

            
            st.markdown("---")
            st.markdown("###  Interpretation")
            st.write(f"- If the market returns *{market_return}%*, then **{ticker.upper()}** is expected to return *{capm_return:.2f}%* based on its risk level.")
            st.write(f"- A beta of {beta:.2f} means the stock is {'more' if beta > 1 else 'less'} volatile than the market.")

            
            fig = go.Figure(data=[
                go.Bar(name='Market Return', x=['Return'], y=[market_return], marker_color='blue'),
                go.Bar(name=f'{ticker.upper()} CAPM Return', x=['Return'], y=[capm_return], marker_color='green')
            ])

            fig.update_layout(
                title="CAPM Return vs Market Return",
                yaxis_title="Return (%)",
                barmode='group',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f" Error fetching data for {ticker.upper()}. Please check the ticker symbol or your internet connection.")
