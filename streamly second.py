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

# Add dashboard title and description
st.title("Economic Growth vs Environmental Impact")
st.write("This dashboard compares GDP per capita and CO2 emissions across countries.")

# Add multiple country selection
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    sorted(df["Country"].unique()),
    default=["United States", "United Kingdom", "China", "India"]
)

# Add year range slider
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2000, 2023)
)

# Filter data using countries and year range
filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# Add scatter plot with colour by country
scatter_fig = px.scatter(
    filtered_df,
    x="GDP",
    y="CO2",
    color="Country",
    title="GDP vs CO2"
)
st.plotly_chart(scatter_fig)

# Add GDP and CO2 line charts
gdp_line = px.line(filtered_df, x="Year", y="GDP", color="Country", title="GDP Over Time")
st.plotly_chart(gdp_line)

co2_line = px.line(filtered_df, x="Year", y="CO2", color="Country", title="CO2 Over Time")
st.plotly_chart(co2_line)