import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="GDP and CO2 Dashboard", layout="wide")

# Load data
df = pd.read_csv("cleaned_co2_gdp_data.csv")

# Title
st.title("Economic Growth and Environmental Impact Dashboard")
st.markdown(
    "This dashboard explores the relationship between GDP per capita and CO₂ emissions "
    "per capita across countries over time."
)

# Sidebar filters
st.sidebar.header("Filters")

countries = sorted(df["Country"].unique())
selected_countries = st.sidebar.multiselect(
    "Select country/countries",
    countries,
    default=["United Kingdom", "United States", "China"] if all(c in countries for c in ["United Kingdom", "United States", "China"]) else countries[:3]
)

year_range = st.sidebar.slider(
    "Select year range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

# Filter data
filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Countries Selected", filtered_df["Country"].nunique())
col2.metric("Average GDP per Capita", f"{filtered_df['GDP'].mean():,.2f}")
col3.metric("Average CO₂ per Capita", f"{filtered_df['CO2'].mean():.2f}")

st.markdown("---")

# Scatter plot
st.subheader("GDP per Capita vs CO₂ Emissions per Capita")
scatter_fig = px.scatter(
    filtered_df,
    x="GDP",
    y="CO2",
    color="Country",
    size="Population",
    hover_name="Country",
    animation_frame="Year",
    title="Relationship Between GDP and CO₂ Emissions"
)
st.plotly_chart(scatter_fig, use_container_width=True)

# Line charts
col4, col5 = st.columns(2)

with col4:
    st.subheader("GDP per Capita Over Time")
    gdp_line = px.line(
        filtered_df,
        x="Year",
        y="GDP",
        color="Country",
        title="GDP per Capita Trends"
    )
    st.plotly_chart(gdp_line, use_container_width=True)

with col5:
    st.subheader("CO₂ Emissions per Capita Over Time")
    co2_line = px.line(
        filtered_df,
        x="Year",
        y="CO2",
        color="Country",
        title="CO₂ Emissions Trends"
    )
    st.plotly_chart(co2_line, use_container_width=True)

# Bar chart for latest selected year
latest_year = year_range[1]
bar_df = filtered_df[filtered_df["Year"] == latest_year].sort_values("GDP", ascending=False).head(10)

st.subheader(f"Top 10 Countries by GDP per Capita in {latest_year}")
bar_fig = px.bar(
    bar_df,
    x="Country",
    y="GDP",
    color="Country",
    title=f"Top 10 GDP per Capita Countries in {latest_year}"
)
st.plotly_chart(bar_fig, use_container_width=True)

# Data preview
with st.expander("View filtered data"):
    st.dataframe(filtered_df)