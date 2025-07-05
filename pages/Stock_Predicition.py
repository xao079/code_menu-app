import streamlit as st
from pages.utils.model_train import get_data, stationary_check, get_rolling_mean, get_differencing_order, fit_model, scaling, evaluate_model, get_forecast, inverse_scaling
import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

st.set_page_config(
    page_title = "Stock Prediction",
    page_icon = "chart_with_downwards_trend",
    layout = "wide",
)

st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input('Stock Ticker', 'TSLA')

rmse = 0

st.subheader('Predicting Next 30 days Close Price for:' + ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.write("**Model RMSE Score:**", rmse)

forecast = get_forecast(scaled_data, differencing_order)


forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

rolling_price = pd.DataFrame(rolling_price)
rolling_price.columns = ['Close']
rolling_price['Type'] = 'Historical'

forecast = pd.DataFrame(forecast)
forecast.columns = ['Close']
forecast['Type'] = 'Forecast'

st.write('##### Forecast Data (Next 30 days)')

import plotly.express as px
fig = px.line(forecast.reset_index(),
              x = 'index', y = 'Close', color = 'Type',
              labels = {'index': 'Date',
                        'Close' : 'Price'},
                        title = 'Close Price : Historical vs Forecast')
fig.update_layout(height = 400, legend_title_text = 'Price Type')
st.plotly_chart(fig, use_container_width = True)

forecast = pd.concat([rolling_price, forecast], axis = 0)


st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width = True)


forecast_only = forecast[forecast['Type'] == 'Forecast'].copy()
from plotly.graph_objs import Figure, Table

fig_table = Figure(data=[Table(
    header=dict(
        values=list(forecast_only.reset_index().columns),
        fill_color='#2C3E50',  
        font=dict(color='white', size=14),
        align='center'
    ),
    cells=dict(
        values=[forecast_only.reset_index()[col] for col in forecast_only.reset_index().columns],
        fill_color=[['#F2F3F4', '#ECF0F1'] * (len(forecast_only) // 2 + 1)],
        align='center',
        font=dict(color='black', size=13)
    )
)])

fig_table.update_layout(height=500, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig_table, use_container_width=True)




