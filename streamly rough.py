# Import the required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page layout and title
st.set_page_config(page_title="GDP vs CO2 Dashboard", layout="wide")

# Load the cleaned dataset from the CSV file
df = pd.read_csv("cleaned_co2_gdp_data.csv")

# Display the main title and description of the dashboard
st.title("Economic Growth vs Environmental Impact")

# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("cleaned_co2_gdp_data.csv")

# Add basic dashboard title
st.title("GDP vs CO2 Dashboard")

# Add single country filter
country = st.sidebar.selectbox("Select Country", df["Country"].unique())

# Filter data by selected country
filtered_df = df[df["Country"] == country]

# Add basic scatter plot
scatter_fig = px.scatter(filtered_df, x="GDP", y="CO2")
st.plotly_chart(scatter_fig)

# Add basic GDP trend line chart
gdp_line = px.line(filtered_df, x="Year", y="GDP")
st.plotly_chart(gdp_line)