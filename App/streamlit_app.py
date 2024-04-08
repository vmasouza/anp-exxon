import pandas as pd
import numpy as np 
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.express as px
from statsmodels.tsa.statespace.sarimax import SARIMAX

data = pd.read_csv("Database//UF-072001-022024.csv", sep=",")

months = {
    1: 'JANEIRO',
    2: 'FEVEREIRO',
    3: 'MARÇO',
    4: 'ABRIL',
    5: 'MAIO',
    6: 'JUNHO',
    7: 'JULHO',
    8: 'AGOSTO',
    9: 'SETEMBRO',
    10: 'OUTUBRO',
    11: 'NOVEMBRO',
    12: 'DEZEMBRO'
}

# Applying the mappings
data.loc[:, 'MES'] = data['MES'].map(months)

# App title and description
st.title("ANP and ExxonMobil Dashboard")
st.markdown("""
    This dashboard provides insights into ANP and ExxonMobil data.
    Explore different filters and visualize the data dynamically.
""")

# Sidebar filters
with st.sidebar:
    st.title("Filters")
    dynamic_filters = DynamicFilters(df=data, filters=['ANO', 'MES', 'REGIAO', 'ESTADO', 'PRODUTO'])
    dynamic_filters.display_filters(location="sidebar", gap="large")
    
    st.button("Reset All filters")
      

# Main content area
st.header("Data Overview")

# Display filtered DataFrame
dynamic_filters.display_df()

# Plot
st.header("Title")
fig = px.bar(dynamic_filters.filter_df(), x='ESTADO', y='QUANTIDADE0M3', color='REGIAO', barmode='group', title='Title')
st.plotly_chart(fig, use_container_width=True)


# Time Series Decomposition
st.title('Time Series Decomposition')
st.markdown("""
    "To generate the decomposition of a time series, select only 1 state and one specific product."
""")

# Decompose the time series to understand its components
example_data = dynamic_filters.filter_df()
example_data = example_data[['DATA', 'ESTADO', 'PRODUTO', 'QUANTIDADE0M3']]

# Create interactive filters for state and product
selected_state = st.selectbox('Select a state:', example_data['ESTADO'].unique())
selected_product = st.selectbox('Select a product:', example_data['PRODUTO'].unique())

# Button to generate the plots
if st.button('Generate'):
    
    # Filter the data according to selections
    filtered_data = example_data[(example_data['ESTADO'] == selected_state) & (example_data['PRODUTO'] == selected_product)]
    
    # Plot the original time series
    fig_original = px.line(filtered_data, x=filtered_data.index, y='QUANTIDADE0M3', title='Original Time Series')
    st.plotly_chart(fig_original)
    
    # Prepare data for time series analysis
    example_ts = filtered_data.set_index('DATA')['QUANTIDADE0M3']
    
    # Decompose the time series
    decomposition = seasonal_decompose(example_ts, model='additive', period=12)
    
    # Plot the decomposition components
    fig_trend = px.line(x=decomposition.trend.index, y=decomposition.trend)
    fig_seasonal = px.line(x=decomposition.seasonal.index, y=decomposition.seasonal)
    fig_residual = px.scatter(x=decomposition.resid.index, y=decomposition.resid)
    
    # defining plot style
    fig_trend.update_layout(title=f'Trend Component of product {selected_product} in state {selected_state}',
                    xaxis_title='Date',
                    yaxis_title='Quantity (cubic meters)')
    fig_seasonal.update_layout(title=f'Seasonal Component of product {selected_product} in state {selected_state}',
                    xaxis_title='Date',
                    yaxis_title='Quantity (cubic meters)')
    fig_residual.update_layout(title=f'Residual Component {selected_product} in state {selected_state}',
                    xaxis_title='Date',
                    yaxis_title='Quantity (cubic meters)')
    
    # Display the component graphs
    st.subheader('Decomposed Time Series Components')
    st.plotly_chart(fig_trend)
    st.plotly_chart(fig_seasonal)
    st.plotly_chart(fig_residual)
    
    # ======= SAMIRA =======

    # The seasonal_decompose already suggested a yearly seasonality (period=12 months), 
    # so let's use that as a starting point for the SARIMA model.
    # We'll start with the same (1,1,1) configuration for ARIMA parameters and add a simple seasonal component.

    # Define SARIMA model configuration
    sarima_order = (1, 1, 1)
    seasonal_order = (1, 1, 1, 12)

    # Fit the SARIMA model
    sarima_model = SARIMAX(example_ts, order=sarima_order, seasonal_order=seasonal_order)
    sarima_model_fit = sarima_model.fit(disp=False)

    # Forecast the next 12 months with the SARIMA model
    sarima_forecast = sarima_model_fit.forecast(steps=12)

    # To ensure the forecast aligns correctly on the timeline, we create a new date range starting from the last date
    # of the historical data
    forecast_dates = pd.date_range(start=example_ts.index[-1], periods=len(sarima_forecast) + 1, freq='M')[1:]

    # Plotting the corrected visualization using Plotly Express
    fig = px.line()
    fig.add_scatter(x=example_ts.index, y=example_ts, mode='lines+markers', name='Original')
    fig.add_scatter(x=forecast_dates, y=sarima_forecast, mode='lines+markers', name='SARIMA Forecast', line=dict(color='red'))
    fig.update_layout(title=f'Corrected Forecast for {selected_product} in {selected_state} using SARIMA Model',
                    xaxis_title='Date',
                    yaxis_title='Quantity (cubic meters)'
                    )

    st.plotly_chart(fig)