# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page layout
st.set_page_config(page_title="GDP vs CO2 Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("cleaned_co2_gdp_data.csv")

# Add dashboard title and description
st.title("Economic Growth vs Environmental Impact")
st.write("This dashboard explores GDP per capita and CO2 emissions per capita over time.")

# Add sidebar filters
st.sidebar.header("Filters")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    sorted(df["Country"].unique()),
    default=["United States", "United Kingdom", "China", "India"]
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2000, 2023)
)

# Filter dataset based on user selections
filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# Display key metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Countries", filtered_df["Country"].nunique())
col2.metric("Avg GDP", f"{filtered_df['GDP'].mean():,.0f}")
col3.metric("Avg CO2", f"{filtered_df['CO2'].mean():.2f}")

# Display scatter plot
st.subheader("Relationship Between GDP and CO2")
scatter_fig = px.scatter(
    filtered_df,
    x="GDP",
    y="CO2",
    color="Country",
    size="Population",
    hover_name="Country",
    title="GDP per Capita vs CO2 Emissions per Capita"
)
st.plotly_chart(scatter_fig, width="stretch")

# Display line charts side by side
st.subheader("GDP and CO2 Trends Over Time")
col4, col5 = st.columns(2)

with col4:
    gdp_line = px.line(filtered_df, x="Year", y="GDP", color="Country", title="GDP per Capita Over Time")
    st.plotly_chart(gdp_line, width="stretch")

with col5:
    co2_line = px.line(filtered_df, x="Year", y="CO2", color="Country", title="CO2 Emissions per Capita Over Time")
    st.plotly_chart(co2_line, width="stretch")

# Fix bar chart by using full dataset instead of filtered data
latest_year = year_range[1]

bar_df = (
    df[df["Year"] == latest_year]
    .sort_values("GDP", ascending=False)
    .head(10)
)

st.subheader(f"Top 10 Countries by GDP per Capita in {latest_year}")
bar_fig = px.bar(bar_df, x="Country", y="GDP", color="Country")
st.plotly_chart(bar_fig, width="stretch")