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

# country filter
country = st.sidebar.selectbox("Select Country", df["Country"].unique())

filtered_df = df[df["Country"] == country]

# year filter
year = st.sidebar.selectbox("Select Year", df["Year"].unique())

filtered_df = filtered_df[filtered_df["Year"] == year]

# scatter plot
scatter_fig = px.scatter(
    filtered_df,
    x="GDP",
    y="CO2"
)

st.plotly_chart(scatter_fig)

# GDP line chart
gdp_line = px.line(
    filtered_df,
    x="Year",
    y="GDP"
)

st.plotly_chart(gdp_line)

# CO2 line chart
co2_line = px.line(
    filtered_df,
    x="Year",
    y="CO2"
)

st.plotly_chart(co2_line)

# bar chart using filtered data
bar_df = filtered_df.sort_values("GDP", ascending=False).head(10)

bar_fig = px.bar(
    bar_df,
    x="Country",
    y="GDP"
)

st.plotly_chart(bar_fig)

# summary metrics
st.write("Average GDP:", filtered_df["GDP"].mean())
st.write("Average CO2:", filtered_df["CO2"].mean())
