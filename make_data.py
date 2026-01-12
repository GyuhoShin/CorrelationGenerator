#%%
import requests
import pandas as pd
import os

year = "2023"
dataset = "acs/acs1/profile"
base_url = f"https://api.census.gov/data/{year}/{dataset}"

# 2. Define the Variables we want to fetch
# Format: "API_CODE": "Human Readable Name"
# You can find more codes at: https://api.census.gov/data/2022/acs/acs1/profile/variables.html
variables = {
    "NAME": "State",
    "DP03_0062E": "Median Income",       # Median Household Income
    "DP02_0068PE": "Bachelor Degree Pct", # % Bachelor's Degree or Higher
    "DP03_0061PE": "Income Over 200k Pct",  # % Households with Income over $200,000
    "DP03_0009PE": "Unemployment Rate",  # % Unemployment Rate
    "DP03_0128PE": "Poverty Rate",       # % People below poverty level
    "DP05_0001E": "Total Population",    # Total Population
    "DP02_0066PE": "High School Grad Pct", # % High School Graduate or Higher
    "DP04_0001E": "Total Housing Units",  # Total Housing Units
    "DP05_0019PE": "Population Under 18 Pct",        # % Population under 18 years
    "DP05_0024PE": "Population Over 65 Pct",          # % Population 65 years and over
    "DP03_0074PE": "Food Stamps Pct",
    "DP03_0099PE": "Uninsured Pct",
    "DP02_0093PE": "Foreign Born Pct",
    "DP02_0114PE": "Non English Home Pct",
    "DP03_0024PE": "Work From Home Pct",
    "DP03_0025E": "Mean Commute Time",
    "DP03_0021PE": "Public Transit Pct",
    "DP02_0002PE": "Married Couple Household Pct",  # % Married Couple Households
    #"DP02_0027PE": "Married Male (15 and over)",   # % Males 15+ never married
    #"DP02_0033PE": "Married Female (15 and over)", # % Females 15+ married
    "DP02_0022PE": "Non Family House Pct",  # % People living alone/with roommates (Urbanization proxy)
}


# Construct the query parameters
cols = ",".join(variables.keys())
params = {
    "get": cols,
    "for": "state:*", 
}

print("Fetching data from Census Bureau...")
response = requests.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.rename(columns=variables)
    numeric_cols = list(variables.values())
    numeric_cols.remove("State") 
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])
    df = df[df["State"] != "Puerto Rico"]

    # Reorder columns by category
    column_order = [
        "State",
        # Demographics
        "Total Population", "Population Under 18 Pct", "Population Over 65 Pct", 
        "Foreign Born Pct", "Non English Home Pct", 
        "Married Couple Household Pct",
        # Economy & Wealth
        "Median Income", "Poverty Rate", "Unemployment Rate", 
        "Food Stamps Pct", "Uninsured Pct", "Income Over 200k Pct",
        # Education
        "Bachelor Degree Pct", "High School Grad Pct",
        # Housing & Lifestyle
        "Total Housing Units", "Work From Home Pct", "Mean Commute Time", 
        "Public Transit Pct", "Non Family House Pct"
    ]
    df = df[column_order]

    # 4. Save to CSV
    output_filename = os.path.join(os.path.dirname(__file__), "dataset.csv")

    df.to_csv(output_filename, index=False)
    print(f"Success! Saved {len(df)} rows to {output_filename}")
    print(df.head())

else:
    print(f"Error: {response.status_code}")
    print(response.text)
#%%
