import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="CAPM Beta Comparison", layout="wide")
st.title(" CAPM Beta Comparison Tool")

st.markdown("""
Compare the *Beta* values of multiple stocks to understand how volatile they are relative to the market.
-  Beta > 1 = More volatile  
-  Beta < 1 = Less volatile  
-  Beta ≈ 1 = Moves with market  
""")

tickers_input = st.text_input("Enter stock tickers separated by comma (e.g., AAPL, MSFT, TSLA)", "TSLA")
tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]


if st.button("Compare Beta Values"):
    beta_data = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            beta = stock.info.get('beta', None)

            if beta is not None:
                beta_data.append({'Ticker': ticker, 'Beta': beta})
            else:
                beta_data.append({'Ticker': ticker, 'Beta': 'N/A'})
        except Exception as e:
            beta_data.append({'Ticker': ticker, 'Beta': 'Error'})

   
    df = pd.DataFrame(beta_data)

    
    st.subheader("Beta Table")
    st.dataframe(df)

    
    df_plot = df[df['Beta'].apply(lambda x: isinstance(x, (int, float)))]

    
    if not df_plot.empty:
        st.subheader("Beta Comparison Chart")
        fig = px.bar(
            df_plot,
            x="Ticker",
            y="Beta",
            color="Beta",
            color_continuous_scale="bluered",
            title="Stock Beta Values",
            labels={"Beta": "CAPM Beta"}
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No valid numeric beta values to plot.")
