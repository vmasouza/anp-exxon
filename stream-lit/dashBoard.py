import pandas as pd
import numpy as np 
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
import plotly.express as px

data = pd.read_excel("test_data.xlsx")

# App title and description
st.title("ANP and ExxonMobil Dashboard")
st.markdown("""
    This dashboard provides insights into ANP and ExxonMobil data.
    Explore different filters and visualize the data dynamically.
""")

# Sidebar filters
with st.sidebar:
    st.title("Filters")
    dynamic_filters = DynamicFilters(df=data, filters=['Year', 'Month', 'State', 'City', 'Product'])
    dynamic_filters.display_filters(location="sidebar")

# Main content area
st.header("Data Overview")

# Display filtered DataFrame
dynamic_filters.display_df()

# Plot
st.header("Value by Year and State")
fig = px.bar(dynamic_filters.filter_df(), x='Year', y='Value', color='State', barmode='group', title='Value by Month and State')
st.plotly_chart(fig, use_container_width=True)

# Map
st.header("Map")
st.map(dynamic_filters.filter_df()[['LAT', 'LON']])