import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd

# Function to get latitude and longitude of a city using Geopy
def get_lat_long(city):
    geolocator = Nominatim(user_agent="my_geocoder")  # Set a valid user agent
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Function to get latitude and longitude of a Brazilian city
def get_lat_long_brazil(city):
    # Check if the city is in Brazil to obtain the latitude and longitude
    lat, long = get_lat_long(city + ", Brazil")
    if lat and long:
        return lat, long
    else:
        return None, None
    

# Sample data
states = ['São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Rio Grande do Sul', 'Paraná']
cities = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Porto Alegre', 'Curitiba']

products = ['Product A', 'Product B', 'Product C']

num_rows = 100

np.random.seed(42)
years = np.random.randint(2010, 2025, num_rows)
months = np.random.choice(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], num_rows)
states_random = np.random.choice(states, num_rows)
cities_random = np.random.choice(cities, num_rows)
products_random = np.random.choice(products, num_rows)
value = np.random.randint(1, 150, num_rows)

data = pd.DataFrame({
    'Year': years,
    'Month': months,
    'State': states_random,
    'City': cities_random,
    'Product': products_random,
    'Value': value
})

# Add latitude and longitude columns to the DataFrame
data['Latitude'], data['Longitude'] = zip(*data['City'].apply(get_lat_long))

# Save DataFrame to Excel file
data.to_excel("test_data.xlsx", index=False)

