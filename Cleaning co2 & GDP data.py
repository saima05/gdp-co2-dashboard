import pandas as pd

# Load the raw dataset
df = pd.read_csv("C:\\Users\\lavan\\Downloads\\CO2 & GDP data.csv")

# Remove unnecessary columns if they exist
columns_to_drop = ["Series Code", "Country Code"]
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Convert the dataset from wide format to long format
df_melted = df.melt(
    id_vars=["Country Name", "Series Name"],
    var_name="Year",
    value_name="Value"
)

# Clean the Year column so it only keeps the year number
df_melted["Year"] = df_melted["Year"].astype(str).str.extract(r"(\d{4})")

# Convert Value column to numeric
df_melted["Value"] = pd.to_numeric(df_melted["Value"], errors="coerce")

# Pivot the dataset so each row is one country-year combination
df_pivot = df_melted.pivot_table(
    index=["Country Name", "Year"],
    columns="Series Name",
    values="Value"
).reset_index()

# Remove the grouped column label
df_pivot.columns.name = None

# Rename columns to shorter names
df_pivot = df_pivot.rename(columns={
    "Country Name": "Country",
    "GDP per capita (current US$)": "GDP",
    "Carbon dioxide (CO2) emissions excluding LULUCF per capita (t CO2e/capita)": "CO2",
    "Population, total": "Population"
})

# Convert columns to correct types
df_pivot["Year"] = pd.to_numeric(df_pivot["Year"], errors="coerce")
df_pivot["GDP"] = pd.to_numeric(df_pivot["GDP"], errors="coerce")
df_pivot["CO2"] = pd.to_numeric(df_pivot["CO2"], errors="coerce")

if "Population" in df_pivot.columns:
    df_pivot["Population"] = pd.to_numeric(df_pivot["Population"], errors="coerce")

# Drop rows where GDP or CO2 is missing
required_columns = ["GDP", "CO2"]
df_cleaned = df_pivot.dropna(subset=required_columns)

# Drop rows where Year is missing
df_cleaned = df_cleaned.dropna(subset=["Year"])

# Sort values for easier use later
df_cleaned = df_cleaned.sort_values(by=["Country", "Year"])

# Reset index
df_cleaned = df_cleaned.reset_index(drop=True)

# Save cleaned dataset
df_cleaned.to_csv("cleaned_co2_gdp_data.csv", index=False)

# Preview cleaned data
print(df_cleaned.head())
print(df_cleaned.info())
print(df_cleaned.shape)