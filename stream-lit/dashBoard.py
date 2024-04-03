import pandas as pd
import numpy as np 
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
import plotly.express as px

# Sample data

# Define the random values
states = ['São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Rio Grande do Sul', 'Paraná']
cities = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Porto Alegre', 'Curitiba']
products = ['Product A', 'Product B', 'Product C']

# Define the number of rows
num_rows = 100

# Generate random data
np.random.seed(42)
years = np.random.randint(2010, 2025, num_rows)
months = np.random.choice(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], num_rows)
states_random = np.random.choice(states, num_rows)
cities_random = np.random.choice(cities, num_rows)
products_random = np.random.choice(products, num_rows)
value = np.random.randint(1, 150)

# Create the DataFrame
data = pd.DataFrame({
    'Year': years,
    'Month': months,
    'State': states_random,
    'City': cities_random,
    'Product': products_random,
    'Value': value
})

# Panel title
st.title("DashBoard ANP e ExxonMobil")

# Layout dos filtros
dynamic_filters = DynamicFilters(df=data, filters=['Year', 'Month', 'State', 'City', 'Product'])


with st.sidebar:
    st.write("Filters")
    
dynamic_filters.display_filters(location="sidebar")

dynamic_filters.display_df()

# Gráfico
fig = px.bar(dynamic_filters.df, x='Year', y='Value', color='State', barmode='group', title='Valor por Month e State')
st.plotly_chart(fig, use_container_width=True)