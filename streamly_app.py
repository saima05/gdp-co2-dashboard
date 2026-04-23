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

st.markdown("""
This dashboard explores the relationship between GDP per capita and CO₂ emissions per capita.
Use the filters to compare countries and analyse trends over time.
""")

# Create sidebar filters for user input
st.sidebar.header("Filters")

# Get a list of all countries in the dataset
countries = sorted(df["Country"].unique())

# Allow the user to select countries
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=["United States", "United Kingdom", "China", "India", "Brazil"]
)

# Allow the user to select a range of years
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

# Filter the dataset based on selected countries and years
filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# Show a warning if no data is selected
if filtered_df.empty:
    st.warning("Please select at least one country.")
    st.stop()

# Display key summary metrics
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Countries", filtered_df["Country"].nunique())
col2.metric("Avg GDP", f"{filtered_df['GDP'].mean():,.0f}")
col3.metric("Avg CO2", f"{filtered_df['CO2'].mean():.2f}")

# Create a scatter plot to show the relationship between GDP and CO2
st.subheader("Relationship Between GDP and CO₂ Emissions")

scatter_fig = px.scatter(
    filtered_df,
    x="GDP",
    y="CO2",
    color="Country",
    size="Population",
    hover_name="Country",
    title="GDP per Capita vs CO₂ Emissions per Capita",
    labels={
        "GDP": "GDP per Capita (current US$)",
        "CO2": "CO₂ Emissions per Capita",
        "Population": "Population"
    }
)

st.plotly_chart(scatter_fig, width="stretch")

# Create line charts to show GDP and CO2 trends over time
st.subheader("GDP and CO₂ Trends Over Time")

col4, col5 = st.columns(2)

# Plot GDP trend over time
with col4:
    gdp_line = px.line(
        filtered_df,
        x="Year",
        y="GDP",
        color="Country",
        title="GDP per Capita Over Time",
        labels={
            "GDP": "GDP per Capita (current US$)",
            "Year": "Year"
        }
    )
    st.plotly_chart(gdp_line, width="stretch")

# Plot CO2 trend over time
with col5:
    co2_line = px.line(
        filtered_df,
        x="Year",
        y="CO2",
        color="Country",
        title="CO₂ Emissions per Capita Over Time",
        labels={
            "CO2": "CO₂ Emissions per Capita",
            "Year": "Year"
        }
    )
    st.plotly_chart(co2_line, width="stretch")

# Create a bar chart showing the top 10 countries globally by GDP in the selected year
latest_year = year_range[1]

bar_df = (
    df[df["Year"] == latest_year]
    .sort_values("GDP", ascending=False)
    .head(10)
)

st.subheader(f"Top 10 Countries by GDP per Capita in {latest_year}")

bar_fig = px.bar(
    bar_df,
    x="Country",
    y="GDP",
    color="Country",
    title=f"Top 10 GDP per Capita Countries ({latest_year})",
    labels={
        "GDP": "GDP per Capita (current US$)",
        "Country": "Country"
    }
)

st.plotly_chart(bar_fig, width="stretch")

# Show the filtered dataset in an expandable section
with st.expander("View Data"):
    st.dataframe(filtered_df)